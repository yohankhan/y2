# import requests

# url = "https://y2-6dw1.onrender.com/extract-audio"
# payload = {
#     "url": "https://youtu.be/Fzk4KVxt99U?si=AvppB9tHAdWCg-6Y",
#     "format": "wav",
#     "sample_rate": 16000,
#     "use_cookies": True  # This will use your cookies.txt
# }

# response = requests.post(url, json=payload)
# print(response.json())

# diagnose.py
# import requests

# url = "https://y2-6dw1.onrender.com/extract-audio"
# payload = {
#     "url": "https://youtu.be/Fzk4KVxt99U?si=AvppB9tHAdWCg-6Y",  # short test video
#     "format": "wav",
#     "sample_rate": 16000,
#     "use_cookies": True
# }

# try:
#     print("Testing API endpoint...")
#     response = requests.post(url, json=payload, timeout=30)
    
#     print(f"Status Code: {response.status_code}")
#     print(f"Content Type: {response.headers.get('content-type')}")
#     print(f"Response Length: {len(response.text)} characters")
    
#     # Show first 500 characters of response
#     print("\nResponse Preview:")
#     print(response.text[:500])
    
#     # Try to parse as JSON
#     try:
#         json_data = response.json()
#         print("\nJSON Response:")
#         print(json_data)
#     except Exception as json_error:
#         print(f"\nJSON Parse Error: {json_error}")
        
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")
# except Exception as e:
#     print(f"Unexpected error: {e}")


# test_different_videos.py
import requests

url = "https://y2-6dw1.onrender.com/extract-audio"

# Test with various YouTube videos
test_videos = [
    "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo (very first YouTube video)
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
    "https://www.youtube.com/watch?v=YQHsXMglC9A",  # Adele - Hello
    "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - GANGNAM STYLE
]

for video_url in test_videos:
    print(f"\nTesting: {video_url}")
    
    payload = {
        "url": video_url,
        "format": "wav",
        "sample_rate": 16000,
        "use_cookies": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")