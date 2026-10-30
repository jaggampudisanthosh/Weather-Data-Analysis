"""Quick check that OTP emails really work.

Usage:   python send_test_email.py your-email@gmail.com
Run it from the weather-app folder (needs .streamlit/secrets.toml).
"""
import sys

import mailer

if len(sys.argv) != 2:
    sys.exit("Usage: python send_test_email.py your-email@gmail.com")

if not mailer.is_configured():
    sys.exit("SMTP not configured. Create .streamlit/secrets.toml (see secrets.toml.example).")

ok, msg = mailer.send_otp(sys.argv[1], "123456", "reset")
print("SUCCESS - check your inbox (and Spam) for the test OTP 123456." if ok else f"FAILED - {msg}")
