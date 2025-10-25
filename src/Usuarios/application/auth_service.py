"""
Servicio de autenticación JWT centralizado
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from src.core.config import settings
from src.Usuarios.domain.schemas import UserTokenData


class AuthService:
    """Servicio centralizado para manejo de JWT"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = settings.secret_key
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        """Crear token JWT con datos del usuario"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def verify_token(self, token: str) -> UserTokenData:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])

            user_id_str: str = payload.get("sub")
            email: str = payload.get("email")

            if user_id_str is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )

            # Convertir user_id de string a int
            user_id = int(user_id_str)

            return UserTokenData(user_id=user_id, email=email)
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado"
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: user_id no es un número"
            )

    def hash_password(self, password: str) -> str:
        """Hashear una contraseña"""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar una contraseña contra su hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
