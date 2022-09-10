from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date, func

from .base import Base


class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    discord_id = Column(Integer, unique=True)
    created_at = Column(DateTime, default=func.now())


class AdminModel(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, server_default=func.now())
