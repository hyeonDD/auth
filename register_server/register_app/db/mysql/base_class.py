from sqlalchemy.ext.declarative import as_declarative, declared_attr


# python class를 사용하여 sqlalchemy의 orm을 수행할 수 있도록 wrapping
@as_declarative()
class Base:
    id: int
    __name__: str

    # class 이름을 소문자로 __tablename__ 속성 만들기
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
