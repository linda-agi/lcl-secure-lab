import os
import requests
import json
import logging
from eth_account import Account
from eth_account.messages import encode_defunct

# --- Configuration ---
API_BASE_URL = "https://leviathannews.xyz/api/v1"
QWEN_MACH_URL = "http://localhost:8081/v1/chat/completions"
# Replace with a real private key provided by Bro later
# For now, generate a random one for structure test
TEST_PRIVATE_KEY = os.getenv("LCL_YAPPER_KEY", "0x" + "1" * 64) 
ACCOUNT = Account.from_key(TEST_PRIVATE_KEY)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("Mach-Yapper")

class LeviathanClient:
    def __init__(self, private_key):
        self.account = Account.from_key(private_key)
        self.session = requests.Session()
        self.token = None

    def authenticate(self):
        logger.info(f"Authenticating as {self.account.address}...")
        # 1. Get Nonce
        res = self.session.get(f"{API_BASE_URL}/wallet/nonce/{self.account.address}/")
        res.raise_for_status()
        data = res.json()
        nonce = data["nonce"]
        message_text = data["message"]

        # 2. Sign Message
        message = encode_defunct(text=message_text)
        signed_message = Account.sign_message(message, private_key=self.account.key)
        signature = signed_message.signature.hex()

        # 3. Verify
        verify_payload = {
            "address": self.account.address,
            "nonce": nonce,
            "signature": signature
        }
        res = self.session.post(f"{API_BASE_URL}/wallet/verify/", json=verify_payload)
        res.raise_for_status()
        
        # Extract JWT (usually from cookies or body)
        self.token = res.cookies.get("access_token") or res.json().get("access_token")
        if not self.token:
            raise Exception("Authentication failed: No token received.")
        
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})
        logger.info("Successfully authenticated.")

    def get_news(self):
        res = self.session.get(f"{API_BASE_URL}/news/?status=approved&sort_type=new&per_page=5")
        res.raise_for_status()
        return res.json().get("results", [])

    def post_yap(self, news_id, text):
        payload = {"text": text, "tags": ["insight", "mach"]}
        res = self.session.post(f"{API_BASE_URL}/news/{news_id}/post_yap", json=payload)
        return res.json()

def generate_insight(article):
    logger.info(f"Generating insight for: {article['title']}")
    prompt = f"""[SYSTEM] You are an LCL Corp Senior Financial Security Analyst. 
Analyze the following crypto news and provide a sharp, high-quality professional comment (a 'yap').
Priority: Insights over summaries. Tone: Decisive, professional, 'Cool & Sharp'.
Article Title: {article['title']}
Description: {article.get('description', 'N/A')}
Insight:"""
    
    payload = {
        "model": "qwen-mach",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    try:
        res = requests.post(QWEN_MACH_URL, json=payload, timeout=120)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Failed to generate insight: {e}")
        return None

def run_mission():
    client = LeviathanClient(TEST_PRIVATE_KEY)
    try:
        # client.authenticate() # Commented out until we have a real key/active connection
        news = client.get_news()
        for item in news:
            insight = generate_insight(item)
            if insight:
                logger.info(f"Generated Insight: {insight}")
                # logger.info(f"Posting to ID {item['id']}...")
                # client.post_yap(item['id'], insight)
    except Exception as e:
        logger.error(f"Mission failed: {e}")

if __name__ == "__main__":
    run_mission()
