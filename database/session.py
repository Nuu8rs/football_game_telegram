from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import DatabaseConfig, DatabaseType
from logging_config import logger
from typing import Generator

connection_string = DatabaseConfig.get_connection_string(DatabaseType.USER)
engine = create_async_engine(connection_string, pool_size=10, max_overflow=0)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> Generator[AsyncSession,None,None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        else:
            await session.commit()
        finally:
            logger.debug("Session closed")
            await session.close()
