import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from mcp_demo.server import THREADS, list_threads, mcp


def test_list_threads_function_returns_three_threads():
    threads = list_threads()

    assert len(threads) == 3
    for thread in threads:
        assert set(thread.keys()) == {"id", "title"}


@pytest.mark.anyio
async def test_list_threads_tool_call_returns_three_threads():
    async with create_connected_server_and_client_session(mcp._mcp_server) as client:
        result = await client.call_tool("list_threads", {})

        assert not result.isError
        payload = result.structuredContent["result"]
        assert len(payload) == 3
        assert payload == THREADS


@pytest.fixture
def anyio_backend():
    return "asyncio"
