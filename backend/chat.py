from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

# absolute
from backend.server_sent_events import SSEStreamResponse, get_text
from backend.run_agent import run_agent, q_template

import time

router = APIRouter(prefix="/chat")

@router.post("/")
async def chat(request: Request) -> StreamingResponse:
    print("received POST request to /api/chat/")
    
    data = await request.json()
    messages = data.get("messages", [])
    last_message = messages[-1] if messages else {}
    content = get_text(last_message)
    
    query_text = f'User query: "{content}".\n'
    agent_start = time.time()

    # using try/except as the error status won't be sent to the endpoint.
    try:
        # run agent (remember, it's async) and get response
        response = await run_agent(content, q_template, stream=True)
        agent_end = time.time()
        total_time = agent_end - agent_start
        print("Time taken:", total_time)
        return SSEStreamResponse(parts=[str(response)], query=query_text)
    
    except Exception as e:    
        if "429" in str(e):
            fallback_response = "⚠️ The server is busy. Please try again in a few seconds."
        else:
            fallback_response = "❌ Something went wrong. Please try again."
        return SSEStreamResponse(parts=[fallback_response], query=query_text)