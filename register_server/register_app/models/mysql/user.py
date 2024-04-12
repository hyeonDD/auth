from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, func

from register_app.db.mysql.base_class import Base


class User(Base):
    id = Column(String(36), default=lambda: uuid4(),
                primary_key=True)
    nickname = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    permission = Column(String(10), default='user', nullable=False)
    create_at = Column(TIMESTAMP, default=func.now(), nullable=False)
