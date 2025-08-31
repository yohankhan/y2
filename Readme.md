# YouTube to Whisper API

A FastAPI service that extracts audio from YouTube videos and prepares it for faster-whisper transcription.

## API Endpoints

- `POST /extract-audio` - Extract audio from YouTube video
- `GET /download-audio/{file_id}` - Download processed audio file
- `DELETE /cleanup/{file_id}` - Clean up audio file
- `GET /health` - Health check
- `GET /` - Root endpoint

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --host 0.0.0.0 --port 8000 --reload