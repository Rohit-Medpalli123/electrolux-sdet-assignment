"""
Pytest fixtures and configuration.

Provides shared fixtures for API client, base URL, logger, and schema.
"""

import json
import pytest
from pathlib import Path
from src.api_client import APIClient
from src.response_handler import ResponseHandler
from utils.logger import get_logger


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--base-url",
        action="store",
        default="https://jsonplaceholder.typicode.com",
        help="Base URL for API tests"
    )


@pytest.fixture(scope="session")
def base_url(request):
    """
    Provide base URL for API tests.

    Can be overridden via command line:
    pytest --base-url="https://custom-url.com"
    """
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def logger():
    """Provide logger instance for tests."""
    return get_logger("APITests")


@pytest.fixture(scope="function")
def api_client(base_url, logger):
    """
    Provide API client instance.

    Yields client and ensures proper cleanup after test.
    """
    client = APIClient(base_url=base_url, timeout=10, max_retries=3)
    logger.info(f"API client created for test with base_url: {base_url}")
    yield client
    client.close()
    logger.info("API client closed")


@pytest.fixture(scope="session")
def response_handler():
    """Provide response handler instance."""
    return ResponseHandler()


@pytest.fixture(scope="session")
def post_schema():
    """
    Provide post schema for validation.

    Loads schema from schemas/post_schema.json
    """
    schema_path = Path(__file__).parent.parent / "schemas" / "post_schema.json"
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    return schema


@pytest.fixture(autouse=True)
def log_separator_after_test():
    """
    Add a visual separator after each test to make logs more readable.
    
    This fixture is automatically applied to all tests due to autouse=True.
    It yields control during test execution and then adds a separator
    to the log once the test has completed.
    """
    # This code runs before each test
    yield
    # This code runs after each test completes
    
    # Add a separator line to visually distinguish between tests
    logger = get_logger("TestSeparator")
    logger.info(f"\n" + "=" * 80 + f"\n✅ TEST COMPLETED\n" + "=" * 80 + "\n")

