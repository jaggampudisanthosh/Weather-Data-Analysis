"""User authentication (SQLite) with email OTP. Passwords and OTPs are salted + hashed."""
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).parent / "users.db"
OTP_TTL = 300        # seconds
MAX_ATTEMPTS = 5


def _conn():
    return sqlite3.connect(DB_PATH)


def _hash(text: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", text.encode(), salt, 120_000).hex()


def _admin_password() -> str:
    """Admin password: [admin] password in secrets.toml, or ADMIN_PASSWORD env, else default."""
    try:
        import streamlit as st
        if "admin" in st.secrets and st.secrets["admin"].get("password"):
            return str(st.secrets["admin"]["password"])
    except Exception:
        pass
    return os.getenv("ADMIN_PASSWORD") or "weather@123"


def init_db():
    with _conn() as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT,
                pw_hash TEXT NOT NULL,
                pw_salt BLOB NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        c.execute(
            """CREATE TABLE IF NOT EXISTS otps (
                email TEXT, purpose TEXT, otp_hash TEXT, salt BLOB,
                expires REAL, attempts INTEGER DEFAULT 0,
                PRIMARY KEY (email, purpose)
            )"""
        )
    admin_pw = _admin_password()
    if not username_exists("admin"):
        _insert("admin", "admin@example.com", admin_pw)
    elif not verify("admin", admin_pw):       # keep admin password in sync with secrets
        salt = os.urandom(16)
        with _conn() as c:
            c.execute("UPDATE users SET pw_hash=?, pw_salt=? WHERE username='admin'",
                      (_hash(admin_pw, salt), salt))


def username_exists(username: str) -> bool:
    with _conn() as c:
        return c.execute("SELECT 1 FROM users WHERE username=?",
                         (username.strip().lower(),)).fetchone() is not None


def email_exists(email: str) -> bool:
    with _conn() as c:
        return c.execute("SELECT 1 FROM users WHERE email=?",
                         (email.strip().lower(),)).fetchone() is not None


def _insert(username, email, password):
    salt = os.urandom(16)
    with _conn() as c:
        c.execute("INSERT INTO users (username,email,pw_hash,pw_salt) VALUES (?,?,?,?)",
                  (username.strip().lower(), email.strip().lower(), _hash(password, salt), salt))


def validate_signup(username, email, password, confirm):
    """Returns (ok, message)."""
    if not re.fullmatch(r"[A-Za-z0-9_]{3,20}", username.strip()):
        return False, "Username must be 3-20 characters (letters, numbers, underscore)."
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
        return False, "Enter a valid email address."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    if password != confirm:
        return False, "Passwords do not match."
    if username_exists(username):
        return False, "Username already taken."
    if email_exists(email):
        return False, "An account with this email already exists."
    return True, ""


def register(username, email, password):
    _insert(username, email, password)
    return True, "Account created successfully."


def verify(username, password) -> bool:
    with _conn() as c:
        row = c.execute("SELECT pw_hash, pw_salt FROM users WHERE username=?",
                        (username.strip().lower(),)).fetchone()
    return bool(row) and hmac.compare_digest(row[0], _hash(password, row[1]))


# ---------------- OTP ----------------
def issue_otp(email: str, purpose: str) -> str:
    otp = f"{secrets.randbelow(10**6):06d}"
    salt = os.urandom(16)
    with _conn() as c:
        c.execute("INSERT OR REPLACE INTO otps VALUES (?,?,?,?,?,0)",
                  (email.strip().lower(), purpose, _hash(otp, salt), salt, time.time() + OTP_TTL))
    return otp


def check_otp(email: str, purpose: str, otp: str):
    """Returns (ok, message). OTP is single-use."""
    email = email.strip().lower()
    with _conn() as c:
        row = c.execute("SELECT otp_hash, salt, expires, attempts FROM otps "
                        "WHERE email=? AND purpose=?", (email, purpose)).fetchone()
        if not row:
            return False, "No OTP requested for this email. Click 'Send OTP' first."
        otp_hash, salt, expires, attempts = row
        if time.time() > expires:
            c.execute("DELETE FROM otps WHERE email=? AND purpose=?", (email, purpose))
            return False, "OTP expired. Please request a new one."
        if attempts >= MAX_ATTEMPTS:
            return False, "Too many wrong attempts. Please request a new OTP."
        if not hmac.compare_digest(otp_hash, _hash(otp.strip(), salt)):
            c.execute("UPDATE otps SET attempts=attempts+1 WHERE email=? AND purpose=?",
                      (email, purpose))
            return False, "Incorrect OTP."
        c.execute("DELETE FROM otps WHERE email=? AND purpose=?", (email, purpose))
    return True, "OTP verified."


def reset_password(email: str, otp: str, new_password: str, confirm: str):
    """Verifies the OTP and sets a new password. Returns (ok, message)."""
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters."
    if new_password != confirm:
        return False, "Passwords do not match."
    ok, msg = check_otp(email, "reset", otp)
    if not ok:
        return False, msg
    salt = os.urandom(16)
    with _conn() as c:
        c.execute("UPDATE users SET pw_hash=?, pw_salt=? WHERE email=?",
                  (_hash(new_password, salt), salt, email.strip().lower()))
    return True, "Password reset successfully. You can log in now."
