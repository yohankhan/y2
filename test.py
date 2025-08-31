import requests
import json

# Extract audio
url = "https://y2-6dw1.onrender.com/extract-audio"
payload = {
    "url": "https://youtu.be/IcGN5jyC2yM?si=8KBkiqIcF_d49Fxi",
    "format": "wav",
    "sample_rate": 16000
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    result = response.json()
    print("Success:", result)
    
    # Download the audio file
    file_id = result['audio_path']
    download_url = f"https://y2-6dw1.onrender.com/download-audio/{file_id}"
    
    audio_response = requests.get(download_url)
    with open("audio.wav", "wb") as f:
        f.write(audio_response.content)
    
    print("Audio downloaded as audio.wav")
else:
    print("Error:", response.json())