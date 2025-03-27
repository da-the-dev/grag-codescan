__all__ = ["settings"]

from pydantic_settings import BaseSettings, SettingsConfigDict

# Example settings class
class SidebarSettings(BaseSettings):
    REPO: str
    OWNER: str
    BRANCH: str
    TOKEN: str

    model_config = SettingsConfigDict(
        env_prefix="SIDEBAR_DEFAULT_",
        env_file=".env",
        extra="ignore",
    )
    
class QdrantSettings(BaseSettings):
    HOST: str

    model_config = SettingsConfigDict(
        env_prefix="QDRANT_",
        env_file=".env",
        extra="ignore",
    )

# Initialize all of the settings classes from above over here
class Settings(BaseSettings):
    sidebar: SidebarSettings = SidebarSettings()
    qdrant: QdrantSettings = QdrantSettings()

# For an example of accessing settings check src/modules/sidebar.py
settings = Settings()
