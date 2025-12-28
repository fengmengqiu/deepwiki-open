"""LiteLLM ModelClient integration.

This client connects to internal company LiteLLM deployments,
which provide a unified interface to multiple LLM providers.
"""

import os
from typing import Optional, Callable, Any, Literal

import logging
from openai.types import Completion

from api.openai_client import OpenAIClient

log = logging.getLogger(__name__)


class LiteLLMClient(OpenAIClient):
    """LiteLLM client that extends OpenAIClient for company internal LLM proxy.

    LiteLLM is compatible with OpenAI API format, so we inherit from OpenAIClient
    and customize the initialization for internal deployment.

    Args:
        api_key (Optional[str], optional): LiteLLM API key. Defaults to None.
        chat_completion_parser (Callable[[Completion], Any], optional): Parser function. Defaults to None.
        input_type (Literal["text", "messages"], optional): Input type. Defaults to "text".
        base_url (Optional[str], optional): LiteLLM API base URL. Defaults to None.
        env_base_url_name (str): Environment variable for base URL. Defaults to "LITELLM_BASE_URL".
        env_api_key_name (str): Environment variable for API key. Defaults to "LITELLM_API_KEY".

    Example:
        ```python
        # Using environment variables
        os.environ["LITELLM_API_KEY"] = "sk-xxx"
        os.environ["LITELLM_BASE_URL"] = "https://litellm-internal.123u.com/"

        client = LiteLLMClient()
        ```
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        chat_completion_parser: Callable[[Completion], Any] = None,
        input_type: Literal["text", "messages"] = "text",
        base_url: Optional[str] = None,
        env_base_url_name: str = "LITELLM_BASE_URL",
        env_api_key_name: str = "LITELLM_API_KEY",
    ):
        """Initialize LiteLLM client with custom environment variable names.

        The base_url will be read from LITELLM_BASE_URL environment variable if not provided.
        The api_key will be read from LITELLM_API_KEY environment variable if not provided.
        """
        # Default base URL for company internal LiteLLM deployment
        default_base_url = "https://litellm-internal.123u.com/"

        # Initialize parent OpenAIClient with LiteLLM-specific configuration
        super().__init__(
            api_key=api_key,
            chat_completion_parser=chat_completion_parser,
            input_type=input_type,
            base_url=base_url or os.getenv(env_base_url_name, default_base_url),
            env_base_url_name=env_base_url_name,
            env_api_key_name=env_api_key_name,
        )

        log.info(f"Initialized LiteLLM client with base_url: {self.base_url}")
