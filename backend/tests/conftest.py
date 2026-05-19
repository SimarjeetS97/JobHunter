import os
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session")
def app_module():
    """Lazily import FastAPI app so tests fail with clear guidance if path differs."""
    module_path = os.getenv("TEST_APP_MODULE", "app.main")
    return pytest.importorskip(module_path, reason=f"Set TEST_APP_MODULE if app isn't at {module_path}")


@pytest.fixture(scope="session")
def app(app_module):
    app = getattr(app_module, "app", None)
    if app is None:
        pytest.fail("FastAPI app instance named `app` not found in TEST_APP_MODULE")
    return app


@pytest_asyncio.fixture
async def async_client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
