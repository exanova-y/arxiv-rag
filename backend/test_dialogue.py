# separately from main, you can run this to test assistant
import requests
import time

assistant_message = "this is an automated message."

for i in range(10):
    print(f"assistant: {assistant_message}")
    response = requests.post(
        "http://127.0.0.1:8000/api/chat/",
        json={"messages": [{"parts": [{"type": "text", "text": assistant_message}]}]},
        stream=True
    )
    
    print("user:\n", end="")
    # some formatting will be needed here
    
    time.sleep(2)
