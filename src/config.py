from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = '7659379669:AAFTStumVn5YQF49FSBnwztwBjidXB_OlKY'

    APP_HOST: str = '0.0.0.0.0'
    APP_PORT: int = 5783
    APP_WORKERS: int = 1


settings = Settings()
