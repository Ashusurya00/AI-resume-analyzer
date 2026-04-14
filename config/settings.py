"""
Enterprise Configuration — Resume Analyzer
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    model_name: str = Field(default="gpt-4o-mini", env="MODEL_NAME")
    temperature: float = Field(default=0.3, env="TEMPERATURE")
    app_version: str = "2.0.0"
    output_dir: str = Field(default="outputs", env="OUTPUT_DIR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
os.makedirs(settings.output_dir, exist_ok=True)
