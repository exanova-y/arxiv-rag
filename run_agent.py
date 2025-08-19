import asyncio
from build_agent import agent   

# create a user-side prompt template to chat with an agent
q_template = (
    "I am interested in {topic}. \n"
    "Find papers in your knowledge database related to this topic; use the following template to query research_paper_query_engine_tool tool: 'Provide title, summary, authors and link to download for papers related to {topic}'. If there are not, could you fetch the recent one from arXiv? \n"
)


async def run_agent(topic: str):  
    handler = agent.run(q_template.format(topic=topic))
    # stream mode allows you to see thought processes and tool calls

    # async for ev in handler.stream_events():
    #     if isinstance(ev, ToolCallResult):
    #         print(f"\nCall {ev.tool_name} with {ev.tool_kwargs}\nReturned: {ev.tool_output}")
    #     if isinstance(ev, AgentStream):
    #         print(f"{ev.delta}", end="", flush=True)
    response = await handler
    return response

async def main():
    response = await run_agent("cybersecurity") # use await when there are multiple async calls
    response2 = await run_agent("african elephants") # something irrelevant to test refinement functions
    print(str(response))
    print(str(response2))


asyncio.run(main()) # asyncio can only be used once I think