import base64
import hashlib
import pyotp
import time

SUFFIX = "HENNGECHALLENGE004"

def make_base32_secret(userid: str) -> str:
    """
    Build the shared secret required by the challenge:
      secret = userid + "HENNGECHALLENGE004"
    Then encode it in Base32 for pyotp.
    """
    raw = (userid + SUFFIX).encode("ascii")        # raw bytes per spec
    b32 = base64.b32encode(raw).decode("ascii")    # Base32 string for pyotp
    return b32

def totp_now(userid: str, digits: int = 10) -> str:
    """
    Generate the current TOTP using:
      - SHA-512 digest
      - 30-second time step
      - T0 = 0 (default)
    """
    secret_b32 = make_base32_secret(userid)
    t = pyotp.TOTP(secret_b32, digits=digits, interval=30, digest=hashlib.sha512)
    return t.now()

def totp_at(userid: str, for_unix_time: int, digits: int = 6) -> str:
    """
    Generate a TOTP at a specific Unix timestamp (useful for testing).
    """
    secret_b32 = make_base32_secret(userid)
    t = pyotp.TOTP(secret_b32, digits=digits, interval=30, digest=hashlib.sha512)
    return t.at(for_unix_time)

def verify_code(userid: str, code: str, leeway_steps: int = 1) -> bool:
    """
    Verify a code allowing small clock drift (±leeway_steps time windows).
    """
    secret_b32 = make_base32_secret(userid)
    t = pyotp.TOTP(secret_b32, digits=6, interval=30, digest=hashlib.sha512)
    # valid_window counts steps before/after the current one
    return t.verify(code, valid_window=leeway_steps)

if __name__ == "__main__":
    uid = "evotianusx@gmail.com"  # <-- replace with your userid
    code = totp_now(uid)
    print("Base32 secret:", make_base32_secret(uid))
    print("Current TOTP :", code)
    # Example verification against "now"
    print("Verify now   :", verify_code(uid, code))



# curl --request POST \
#   --url https://api.challenge.hennge.com/challenges/backend-recursion/004 \
#   --header 'Authorization: Basic ZXZvdGlhbnVzeEBnbWFpbC5jb206MjEwNzY4NzYzNg==' \
#   --header 'Content-Type: application/json' \
#   --header 'User-Agent: insomnia/11.5.0' \
#   --data '{
# 	"github_url": "https://gist.github.com/evotianusx/f30971c89e2b83aba8809951c5346c31",
# 	"contact_email": "evotianusx@gmail.com",
# 	"solution_language": "python"
# }'