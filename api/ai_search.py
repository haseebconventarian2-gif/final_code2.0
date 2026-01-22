"""
Azure AI Search RAG Pipeline Module

This module provides RAG (Retrieval-Augmented Generation) functionality
using Azure AI Search as the knowledge base.
"""

import os
from typing import Optional

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential


def require_env(name: str) -> str:
    """Get required environment variable."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


def get_search_client() -> SearchClient:
    """Initialize and return Azure Search client."""
    endpoint = require_env("AZURE_SEARCH_ENDPOINT")
    key = require_env("AZURE_SEARCH_KEY")
    index_name = require_env("AZURE_SEARCH_INDEX")
    
    credential = AzureKeyCredential(key)
    return SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)


async def search_knowledge_base(query: str, top_k: int = 5) -> list[dict]:
    """
    Search Azure AI Search index for relevant documents.
    
    Args:
        query: Search query string
        top_k: Number of top results to return
        
    Returns:
        List of search results with document content and scores
    """
    try:
        client = get_search_client()
        
        # Perform hybrid search (BM25 + vector search recommended)
        # For now, using simple text search
        results = client.search(
            search_text=query,
            top=top_k,
            include_total_count=True,
        )
        
        documents = []
        for result in results:
            doc = {
                "content": result.get("content") or result.get("text") or str(result),
                "score": result.get("@search.score", 0),
                "source": result.get("source") or result.get("title") or "Unknown",
            }
            documents.append(doc)
        
        return documents
    except Exception as e:
        print(f"Azure Search error: {e}")
        return []


async def build_rag_context(query: str) -> str:
    """
    Build RAG context from search results.
    
    Args:
        query: User query to search for
        
    Returns:
        Formatted context string for the LLM
    """
    if not query or not query.strip():
        return ""
    
    documents = await search_knowledge_base(query, top_k=5)
    
    if not documents:
        return ""
    
    context_parts = []
    for doc in documents:
        context_parts.append(
            f"Source: {doc['source']} (Relevance: {doc['score']:.2f})\n"
            f"Content: {doc['content']}"
        )
    
    return "\n\n".join(context_parts)


async def search_tool(query: str) -> dict:
    """
    Tool function for GPT-4o function calling to search knowledge base.
    
    Args:
        query: Search query
        
    Returns:
        Dictionary with search results
    """
    documents = await search_knowledge_base(query, top_k=3)
    
    if not documents:
        return {
            "status": "no_results",
            "message": "No relevant information found in knowledge base"
        }
    
    results = []
    for doc in documents:
        results.append({
            "source": doc["source"],
            "content": doc["content"],
            "confidence": doc["score"]
        })
    
    return {
        "status": "success",
        "results": results
    }
