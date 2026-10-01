import os
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, DateTime, ForeignKey, func, select, delete, Integer
# Используем корректный драйвер aiosqlite для работы с SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram ID
    username: Mapped[str | None] = mapped_column(String(255))
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    # Связи
    surveys: Mapped[list["Survey"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    messages: Mapped[list["Message"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Survey(Base):
    __tablename__ = "surveys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255))
    age: Mapped[int] = mapped_column(Integer)
    city: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="surveys")

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    text: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    user: Mapped["User"] = relationship(back_populates="messages")


class Database:
    @staticmethod
    async def get_stats() -> dict:
        """Возвращает общую статистику по пользователям и опросам (SQLAlchemy)."""
        async with async_session() as session:
            # Поочередно или через отдельные скалярные подзапросы считаем метрики
            total_users_stmt = select(func.count(User.id))
            total_surveys_stmt = select(func.count(Survey.id))
            avg_age_stmt = select(func.avg(Survey.age)).where(Survey.age.is_not(None))

            total_users = (await session.execute(total_users_stmt)).scalar() or 0
            total_surveys = (await session.execute(total_surveys_stmt)).scalar() or 0
            avg_age_raw = (await session.execute(avg_age_stmt)).scalar()

            avg_age = round(float(avg_age_raw), 1) if avg_age_raw is not None else 0

            return {
                "total_users": total_users,
                "total_surveys": total_surveys,
                "avg_age": avg_age
            }

    @staticmethod
    async def get_user_surveys(user_id: int) -> list:
        """Возвращает историю всех опросов для конкретного пользователя."""
        async with async_session() as session:
            stmt = (
                select(Survey.name, Survey.age, Survey.city, Survey.language, Survey.created_at)
                .where(Survey.user_id == user_id)
                .order_by(Survey.created_at.desc())
            )
            result = await session.execute(stmt)
            # .all() вернет список строк-кортежей, сохраняя старое поведение (как fetchall)
            return result.all()

    @staticmethod
    async def clear_user_history(user_id: int) -> None:
        """Удаляет все записи опросов для конкретного пользователя."""
        async with async_session() as session:
            # ПРАВИЛЬНО: делит принимает модель, а .where() применяется к результату функции delete()
            stmt = delete(Survey).where(Survey.user_id == user_id)
            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def add_survey(user_id: int, name: str, age: int, city: str, language: str) -> None:
        """Сохраняет результаты нового опроса в базу данных."""
        async with async_session() as session:
            new_survey = Survey(
                user_id=user_id,
                name=name,
                age=age,
                city=city,
                language=language
            )
            session.add(new_survey)
            await session.commit()

async def get_top_users(limit: int = 10):
    """Возвращает топ пользователей по количеству опросов."""
    async with async_session() as session:
        stmt = (
            select(User.id, User.username, func.count(Survey.id).label("survey_count"))
            .join(Survey, User.id == Survey.user_id)
            .group_by(User.id, User.username)
            .order_by(func.count(Survey.id).desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.all()
