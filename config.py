# """
# Configuration module for the story generation service.
# Uses Pydantic's Settings for environment variable parsing and validation.
# """
# import os
# from functools import lru_cache
# from pydantic_settings import BaseSettings
# from pydantic import Field


# class Settings(BaseSettings):
#     # API Keys
#     openai_api_key: str
    
#     # Application settings
#     debug: bool = False
#     model_name: str = "gpt-4o"
#     default_temperature: float = 0.7
    
#     # Optional vector store connection details
#     vector_store_enabled: bool = False
#     vector_store_url: str = ""
#     vector_store_api_key: str = ""
    
#     class Config:
#         """Pydantic configuration."""
#         env_file = ".env"
#         env_file_encoding = "utf-8"
#         case_sensitive = False  # Allow case-insensitive env vars


# @lru_cache()
# def get_settings() -> Settings:
#     return Settings()

"""
Configuration module for the story generation service.
Uses Pydantic's Settings for environment variable parsing and validation.
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # API Keys
    openai_api_key: str
    
    # Application settings
    debug: bool = False
    model_name: str = "gpt-4o"
    default_temperature: float = 0.7
    
    # Optional vector store connection details
    vector_store_enabled: bool = False
    vector_store_url: str = ""
    vector_store_api_key: str = ""
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # Allow case-insensitive env vars
        protected_namespaces = ('settings_',)  # Fixes the model_name warning


@lru_cache()
def get_settings() -> Settings:
    return Settings()