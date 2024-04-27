from uuid import uuid4
from sqlalchemy import Column, String, TIMESTAMP, func, CheckConstraint

from blog_app.db.mysql.base_class import Base


class Post(Base):
    id = Column(String(36), default=lambda: uuid4(),
                primary_key=True)
    email = Column(String(255), index=True, nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(500), nullable=False)

    create_at = Column(TIMESTAMP, default=func.now(), nullable=False)
    update_at = Column(TIMESTAMP, default=func.now())

    __table_args__ = (
        # 제목길이 최소 8글자 이상
        CheckConstraint("LENGTH(title) >= 8", name='check_title_min_length'),
        # 내용길이 최소 10글자 이상
        CheckConstraint("LENGTH(description) >= 10",
                        name='check_description_min_length'),
    )
