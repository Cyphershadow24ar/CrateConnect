"""
Food Rescue Backend — Application Configuration.

Loads settings from environment variables / .env file.
"""

from urllib.parse import quote_plus

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_ENV: str = "development"

    # Database — individual components (preferred, handles special chars in passwords)
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "changeme"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "food_rescue"

    # Database — fallback monolithic URL (ignored when DB components are set)
    DATABASE_URL: str = ""

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173"

    # Inventory
    EXPIRY_ALERT_DAYS: int = 3

    # Demo tenant — deterministic UUID for Milestone 1
    DEMO_BUSINESS_ID: str = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }

    @property
    def database_url(self) -> str:
        """
        Build the SQLAlchemy database URL.

        Uses individual DB_* components to properly URL-encode the password.
        Falls back to DATABASE_URL if it is explicitly set and DB_PASSWORD is default.
        """
        encoded_password = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+psycopg://{self.DB_USER}:{encoded_password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
