from pydantic import BaseModel
from pathlib import Path

class Settings(BaseModel):
    SMTP_HOST: str = '0.0.0.0'
    SMTP_PORT: int = 1025 

    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data" 
    DATABASE_URL: str = f'sqlite+aiosqlite:///{DATA_DIR}/mailhook.db'

    class Config:
        env_file = '.env'

