"""Sends OTP emails over SMTP. Config comes from .streamlit/secrets.toml ([smtp]) or SMTP_* env vars."""
import os
import smtplib
from email.message import EmailMessage


def _config():
    cfg = {}
    try:
        import streamlit as st
        if "smtp" in st.secrets:
            cfg = dict(st.secrets["smtp"])
    except Exception:
        pass
    if not cfg:
        cfg = {
            "host": os.getenv("SMTP_HOST"),
            "port": os.getenv("SMTP_PORT", "587"),
            "user": os.getenv("SMTP_USER"),
            "password": os.getenv("SMTP_PASSWORD"),
            "sender": os.getenv("SMTP_SENDER"),
            "starttls": os.getenv("SMTP_STARTTLS", "true"),
        }
    if not (cfg.get("host") and cfg.get("user") and cfg.get("password")):
        return None
    cfg.setdefault("sender", cfg["user"])
    cfg["port"] = int(cfg.get("port") or 587)
    cfg["starttls"] = str(cfg.get("starttls", "true")).lower() != "false"
    return cfg


def is_configured() -> bool:
    return _config() is not None


def demo_allowed() -> bool:
    """Demo mode (OTP shown on screen) is allowed ONLY when running on localhost."""
    if os.getenv("DEMO_OTP") == "1":
        return True
    try:
        import streamlit as st
        host = (st.context.headers.get("Host") or "").lower()
        return host.startswith(("localhost", "127.0.0.1", "[::1]"))
    except Exception:
        return False


def send_otp(to_email: str, otp: str, purpose: str):
    """Returns (ok, message)."""
    cfg = _config()
    if cfg is None:
        return False, "SMTP not configured"
    action = "verify your email" if purpose == "signup" else "reset your password"
    msg = EmailMessage()
    msg["Subject"] = "Weather Data Analysis System - Your OTP"
    msg["From"] = cfg["sender"]
    msg["To"] = to_email
    msg.set_content(
        f"Your OTP to {action} is: {otp}\n\n"
        "It is valid for 5 minutes. If you did not request this, ignore this email."
    )
    try:
        if cfg["port"] == 465:
            server = smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=15)
        else:
            server = smtplib.SMTP(cfg["host"], cfg["port"], timeout=15)
            if cfg["starttls"]:
                server.starttls()
        with server:
            server.login(cfg["user"], cfg["password"])
            server.send_message(msg)
        return True, "OTP sent"
    except smtplib.SMTPAuthenticationError:
        return False, ("Email login failed. Use a Gmail App Password "
                       "(not your normal password) and check the email address.")
    except Exception as exc:
        return False, f"Could not send email: {exc}"
