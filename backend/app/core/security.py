import base64
import json
import hmac
import hashlib
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    return hmac.compare_digest(hashlib.sha256(password.encode()).hexdigest(), hashed_password)

def _sign(data: bytes) -> str:
    return base64.urlsafe_b64encode(
        hmac.new(SECRET_KEY.encode(), data, hashlib.sha256).digest()
    ).decode().rstrip("=")

def create_access_token(data: dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    payload.update({"exp": int(expire.timestamp())})

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    signature = _sign(f"{header_b64}.{payload_b64}".encode())
    return f"{header_b64}.{payload_b64}.{signature}"

def decode_access_token(token: str) -> dict | None:
    try:
        header_b64, payload_b64, signature = token.split(".")
        expected_signature = _sign(f"{header_b64}.{payload_b64}".encode())
        if not hmac.compare_digest(signature, expected_signature):
            return None

        payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode())
        if "exp" in payload and datetime.utcnow().timestamp() > payload["exp"]:
            return None
        return payload
    except Exception:
        return None