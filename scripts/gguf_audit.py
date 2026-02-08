#!/usr/bin/env python3
import sys
import argparse
from gguf import GGUFReader

def scan_gguf(file_path):
    print(f"[*] Analyzing GGUF file: {file_path}")
    try:
        reader = GGUFReader(file_path)
        
        print(f"[+] Found {len(reader.tensors)} tensors and {len(reader.fields)} metadata fields.")
        
        # Check for Chat Templates (Common SSTI vector)
        template_key = "tokenizer.chat_template"
        if template_key in reader.fields:
            template_val = reader.fields[template_key].parts[0].tobytes().decode("utf-8", "ignore")
            print(f"[!] WARNING: Found Chat Template metadata.")
            print(f"--- TEMPLATE START ---\n{template_val}\n--- TEMPLATE END ---")
            
            # Basic suspicious pattern check
            suspicious_patterns = ["import", "popen", "system", "eval", "globals", "config"]
            for pattern in suspicious_patterns:
                if pattern in template_val.lower():
                    print(f"[CRITICAL] Suspicious Jinja2 pattern detected: '{pattern}'")
        else:
            print("[+] No explicit chat template found in metadata.")
            
    except Exception as e:
        print(f"[-] Error reading GGUF file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LCL GGUF Semantic Audit Tool")
    parser.add_argument("file", help="Path to the .gguf file")
    args = parser.parse_args()
    scan_gguf(args.file)
