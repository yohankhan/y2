import os
import tempfile
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import aiofiles
import asyncio
from pydantic import BaseModel, HttpUrl
import uuid
from contextlib import asynccontextmanager
import subprocess
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeURL(BaseModel):
    url: HttpUrl
    format: Optional[str] = "wav"
    sample_rate: Optional[int] = 16000
    use_cookies: Optional[bool] = True

class AudioResponse(BaseModel):
    success: bool
    audio_path: Optional[str] = None
    error: Optional[str] = None
    duration: Optional[float] = None
    file_size: Optional[int] = None

# Global variables
cached_audio_files = {}
temp_dir = None
COOKIES_FILE = "cookies.txt"
cookies_available = os.path.exists(COOKIES_FILE)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global temp_dir
    temp_dir = tempfile.mkdtemp()
    logger.info(f"Created temporary directory: {temp_dir}")
    
    if cookies_available:
        logger.info(f"Cookies file found: {COOKIES_FILE}")
    else:
        logger.warning("No cookies.txt file found. Some videos may require authentication.")
    
    yield
    
    # Shutdown: Cleanup
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
        logger.info("Cleaned up temporary directory")
    except:
        pass

app = FastAPI(
    title="YouTube to Whisper API",
    description="API to extract audio from YouTube videos for faster-whisper processing",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_ydl_opts(format: str, output_template: str, use_cookies: bool = True):
    """Get yt-dlp options with cookie support"""
    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': format,
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'no_check_certificate': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        },
        'socket_timeout': 30,
        'retries': 3,
    }
    
    # Add cookies support if available and requested
    if use_cookies and cookies_available:
        opts['cookiefile'] = COOKIES_FILE
        logger.info("Using cookies from cookies.txt file")
    elif use_cookies and not cookies_available:
        logger.warning("Cookies requested but cookies.txt not found")
    
    return opts

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

async def convert_to_whisper_format(input_path: str, output_path: str, sample_rate: int = 16000):
    """Convert audio to format compatible with faster-whisper"""
    try:
        # Use subprocess instead of ffmpeg-python for better compatibility
        cmd = [
            'ffmpeg', '-i', input_path,
            '-acodec', 'pcm_s16le',
            '-ac', '1',
            '-ar', str(sample_rate),
            '-y',  # Overwrite output file
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            logger.error(f"FFmpeg failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        logger.error(f"Audio conversion error: {e}")
        return False

@app.get("/")
async def root():
    return {
        "message": "YouTube to Whisper API", 
        "status": "healthy", 
        "cookies_available": cookies_available
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "youtube-whisper-api",
        "cookies_available": cookies_available
    }

@app.post("/extract-audio", response_model=AudioResponse)
async def extract_audio(youtube_url: YouTubeURL):
<<<<<<< HEAD
=======
    """
    Extract audio from YouTube video with cookie support
    
    Args:
        url: YouTube video URL
        format: Output audio format (wav, mp3, flac)
        sample_rate: Target sample rate (default: 16000 for whisper)
        use_cookies: Whether to use browser cookies (default: True)
        cookies_browser: Browser to extract cookies from (chrome, firefox, edge, etc.)
        cookies_file: Path to cookies.txt file (alternative to browser cookies)
    """
>>>>>>> d70262ce1762ae101c9bf699b2bed50e8c9e4abd
    try:
        video_url = str(youtube_url.url)
        file_id = str(uuid.uuid4())
        temp_output = os.path.join(temp_dir, f"original_{file_id}")
        final_output = os.path.join(temp_dir, f"whisper_ready_{file_id}.wav")
        
        # Download audio using yt-dlp with cookies
        ydl_opts = get_ydl_opts(
            format=youtube_url.format,
            output_template=temp_output,
<<<<<<< HEAD
            use_cookies=youtube_url.use_cookies
        )
        
        logger.info(f"Downloading audio from: {video_url}")
        if youtube_url.use_cookies and cookies_available:
            logger.info("Using cookies for authentication")
=======
            use_cookies=getattr(youtube_url, 'use_cookies', True),
            cookies_browser=getattr(youtube_url, 'cookies_browser', 'chrome'),
            cookies_file=getattr(youtube_url, 'cookies_file', None)
        )
        
        logger.info(f"Downloading audio from: {video_url} with cookies")
>>>>>>> d70262ce1762ae101c9bf699b2bed50e8c9e4abd
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            
            if not info:
                raise HTTPException(status_code=400, detail="Failed to extract video info")
            
            # Find the downloaded file
            downloaded_files = [f for f in os.listdir(temp_dir) if f.startswith(f"original_{file_id}")]
            if not downloaded_files:
                raise HTTPException(status_code=500, detail="Audio file not found after download")
            
            original_file = os.path.join(temp_dir, downloaded_files[0])
            
            # Convert to whisper-compatible format
            logger.info("Converting audio to whisper format...")
            success = await convert_to_whisper_format(
                original_file, 
                final_output, 
                youtube_url.sample_rate
            )
            
            if not success:
                raise HTTPException(status_code=500, detail="Audio conversion failed")
            
            # Get file info
            file_size = os.path.getsize(final_output)
            duration = info.get('duration', 0)
            
            # Clean up original file
            try:
                os.remove(original_file)
            except:
                pass
            
            # Cache the file path
            cached_audio_files[file_id] = {
                'path': final_output,
                'created_at': asyncio.get_event_loop().time()
            }
            
            return AudioResponse(
                success=True,
                audio_path=file_id,
                duration=duration,
                file_size=file_size
            )
            
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
        

# ... (keep the download-audio and cleanup endpoints the same)


@app.get("/download-audio/{file_id}")
async def download_audio(file_id: str):
    """Download the processed audio file"""
    if file_id not in cached_audio_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = cached_audio_files[file_id]['path']
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File no longer exists")
    
    return FileResponse(
        file_path,
        media_type="audio/wav",
        filename=f"audio_{file_id}.wav"
    )

@app.delete("/cleanup/{file_id}")
async def cleanup_audio(file_id: str):
    """Clean up audio file after processing"""
    if file_id in cached_audio_files:
        file_path = cached_audio_files[file_id]['path']
        try:
            os.remove(file_path)
            del cached_audio_files[file_id]
            return {"success": True, "message": "File cleaned up"}
        except:
            return {"success": False, "message": "Cleanup failed"}
    return {"success": False, "message": "File not found"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
