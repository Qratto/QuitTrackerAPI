from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_user: str
    database_password: str
    database_host: str
    database_port: str
    database_name: str

    @property
    def database_url(self):
        return (f"postgresql+asyncpg://{self.database_user}:{self.database_password}"
                f"@{self.database_host}:{self.database_port}/{self.database_name}")

    class Config:
        env_file = ".env"

settings = Settings()