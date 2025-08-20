from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .server_sent_events import SSEStreamResponse, get_text

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(request: Request) -> StreamingResponse:
    print("received POST request to /api/chat/")
    data = await request.json()
    messages = data.get("messages", [])
    last_message = messages[-1] if messages else {}
    content = get_text(last_message)
    
    query_text = f'User query: "{content}".\n'
    
    # Simple automated response
    sample_parts = [
        "this is an automated message"
    ]

    return SSEStreamResponse(parts=sample_parts, query=query_text)