import sys
from unittest.mock import MagicMock
import requests
import json

# Force mock the LeviathanClient and generate_insight calls
sys.path.append("lcl-secure-lab/scripts")
import mach_yapper

def test_generation():
    print("[*] Testing Mach-Yapper Generation Logic...")
    
    # Mock article
    mock_article = {
        "id": 1234,
        "title": "Solana reaches new ATH as ETF rumors swirl",
        "description": "Solana (SOL) price has surged 15% in the last 24 hours, hitting a new all-time high. Investors are optimistic about a potential spot ETF approval in the US."
    }
    
    # Call Qwen-Mach
    print(f"[*] Sending to Qwen-Mach (8081)...")
    insight = mach_yapper.generate_insight(mock_article)
    
    if insight:
        print(f"\n[SUCCESS] Qwen-Mach Insight:\n{insight}\n")
    else:
        print("[FAILURE] Qwen-Mach failed to respond.")

if __name__ == "__main__":
    test_generation()
