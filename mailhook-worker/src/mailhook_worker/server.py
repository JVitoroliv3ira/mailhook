import asyncio
from pathlib import Path
from mailhook_worker.config.config import Settings
from mailhook_worker.database.db import init_db

async def main() -> None:
    settings = Settings()

    Path(settings.DATA_DIR).mkdir(parents=True, exist_ok=True)

    await init_db(settings.DATABASE_URL)

    print(f'[mailhook-worker] SMTP rodando em {settings.SMTP_HOST}:{settings.SMTP_PORT}')

    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('[mailhook-worker] Encerrando...')
