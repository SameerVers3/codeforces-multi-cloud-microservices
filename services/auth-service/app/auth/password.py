import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    if not plain_password or not hashed_password:
        return False
    try:
        # Truncate password to 72 bytes (bcrypt limit)
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Hash a password."""
    if not password:
        raise ValueError("Password cannot be empty")
    # Truncate password to 72 bytes (bcrypt limit)
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

