import ssl

import httpx
import truststore
from openai import OpenAI


def create_openai_client(api_key: str, timeout_seconds: float) -> OpenAI:
    """Create a verified client that also trusts certificates managed by Windows."""
    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    return OpenAI(
        api_key=api_key,
        base_url="https://api.openai.com/v1",
        timeout=timeout_seconds,
        http_client=httpx.Client(
            verify=context,
            timeout=timeout_seconds,
        ),
    )
