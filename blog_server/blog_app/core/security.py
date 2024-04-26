# from passlib.context import CryptContext


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def get_password_hash(password: str) -> str:
#     """
#     패스워드 해시화
#     """
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """
#     패스워드 해시 확인용
#     """
#     return pwd_context.verify(plain_password, hashed_password)
