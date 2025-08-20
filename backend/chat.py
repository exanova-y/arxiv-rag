from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .server_sent_events import SSEStreamResponse, get_text
from .run_agent import run_agent, q_template

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(request: Request) -> StreamingResponse:
    print("received POST request to /api/chat/")
    data = await request.json()
    messages = data.get("messages", [])
    last_message = messages[-1] if messages else {}
    content = get_text(last_message)
    
    query_text = f'User query: "{content}".\n'
    
    # run agent (remember, it's async) and get response
    response = await run_agent(content, q_template, stream=True)
    
    return SSEStreamResponse(parts=[str(response)], query=query_text)