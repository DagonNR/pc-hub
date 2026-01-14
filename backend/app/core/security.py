import os, base64, json, hmac, hashlib
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _get_secret_key() -> str:
    key = os.getenv("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY no está configurada en variables de entorno")
    return key

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def _sign(data: bytes) -> str:
    secret = _get_secret_key().encode()
    return _b64url_encode(hmac.new(secret, data, hashlib.sha256).digest())

def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    expire_minutes = expires_minutes or int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    header = {"alg": "HS256", "typ": "JWT"}

    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload.update({"exp": int(expire.timestamp())})

    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())

    signing_input = f"{header_b64}.{payload_b64}".encode()
    signature = _sign(signing_input)

    return f"{header_b64}.{payload_b64}.{signature}"

def decode_access_token(token: str) -> Optional[dict]:
    try:
        header_b64, payload_b64, signature = token.split(".")

        signing_input = f"{header_b64}.{payload_b64}".encode()
        expected_signature = _sign(signing_input)

        if not hmac.compare_digest(signature, expected_signature):
            return None

        payload = json.loads(_b64url_decode(payload_b64).decode())

        if "exp" in payload and datetime.utcnow().timestamp() > payload["exp"]:
            return None

        return payload
    except Exception:
        return None
