import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client



"""
Make sure:
1. the server is running before this script
2. the server is configured to use SSE transport
3. the server is listening on port xxxx

to run the server:
uv run server.py
"""

async def main():
    async with sse_client("http://127.0.0.1:8000/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f" - {tool.name}: {tool.description}")

            result = await session.call_tool("get_alerts", arguments={"state": "CA"})
            print(result.content[0].text)



if __name__ == "__main__":
    asyncio.run(main())