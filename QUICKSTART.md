# Quick Start Guide - Bank Islami AI Bot

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd c:\Users\noufal.ehaab\Desktop\Tasks\final-code
pip install -r requirements.txt
```

### 2. Verify `.env` File
The `.env` file is pre-configured with all credentials. No changes needed!

### 3. Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Output should show:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Test the Application

### Open Web UI
Navigate to: http://localhost:8000

### Test Text Message
```bash
curl -X POST "http://localhost:8000/message?text=Tell me about Islamic savings account"
```

**Response:**
```json
{
  "text": "Islamic Savings Account offers Sharia-compliant banking...",
  "audio": {
    "format": "audio/mpeg",
    "size_bytes": 12345
  }
}
```

### Test Voice Message
```bash
# First create a test audio file or use an existing one
curl -X POST "http://localhost:8000/message" \
  -F "file=@test_audio.mp3"
```

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "ok": true,
  "version": "2.0",
  "rag": "Azure AI Search"
}
```

## Integration Points

### WhatsApp Webhook
When someone sends a message on WhatsApp:
1. Message received at `/webhook`
2. Auto-transcribed if voice message
3. Processed through Azure AI Search + GPT-4o
4. Reply sent automatically (text + voice)

### Azure Communication Services (ACS)
When someone sends a message via ACS:
1. Event received at `/acs/events`
2. Processed same as WhatsApp
3. Reply sent via ACS advanced messaging

## Key Features Now Active

✅ **Azure AI Search** - Real-time FAQ retrieval  
✅ **GPT-4o** - Multimodal text + voice understanding  
✅ **Unified Endpoint** - Single `/message` for text & audio  
✅ **WhatsApp Integration** - Automatic voice transcription & reply  
✅ **ACS Integration** - Azure Communication Services support  
✅ **Automatic TTS** - Responses returned as audio  

## Common Queries to Test

```bash
# Product inquiry
curl -X POST "http://localhost:8000/message?text=What are the features of your Islamic account?"

# Account opening
curl -X POST "http://localhost:8000/message?text=How do I open an account?"

# Eligibility
curl -X POST "http://localhost:8000/message?text=Who can open an account?"

# Documents needed
curl -X POST "http://localhost:8000/message?text=What documents do I need?"
```

## Troubleshooting

**Error: "Missing required env var"**
- Check all `.env` variables are set

**Error: "Azure Search unauthorized"**
- Verify search credentials in `.env`

**Error: "GPT-4o API error"**
- Check Azure OpenAI endpoint and key

**Audio not working**
- Verify `AZURE_TTS_DEPLOYMENT` is set to `gpt-4o`

## Architecture

```
User Input (Text/Voice)
    ↓
/message endpoint
    ├─ Text? → Skip transcription
    └─ Audio? → STT Transcription
    ↓
Query Processing
    ├─ Search Azure AI Search
    ├─ Get relevant FAQs
    └─ Build context
    ↓
GPT-4o Generation
    └─ Generate intelligent response
    ↓
Response
    ├─ Text reply
    └─ Audio synthesis (TTS)
```

## Next: Deploy to Azure

When ready to deploy:
1. Push to GitHub
2. Connect to Azure App Service
3. Set environment variables in Azure
4. Deploy via GitHub Actions or Azure DevOps

## Documentation

For detailed information, see `AZURE_IMPLEMENTATION.md` in the project root.

---

**Status:** ✅ Ready for production  
**Version:** 2.0 (Azure-native)  
**Last Updated:** January 2026
