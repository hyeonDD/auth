from register_app.db.mysql.base_class import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP, func


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    create_at = Column(TIMESTAMP, default=func.now(), nullable=False)