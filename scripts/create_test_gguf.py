from gguf import GGUFWriter

def create_test_gguf(path):
    print(f"[*] Creating test GGUF: {path}")
    writer = GGUFWriter(path, "llama")
    
    # Add suspicious Chat Template
    malicious_template = "{% for x in ().__class__.__base__.__subclasses__() %}{% if x.__name__ == 'CatchBase' %}{{ x }}{% endif %}{% endfor %}"
    writer.add_string("tokenizer.chat_template", malicious_template)
    
    # Add a dummy tensor
    import numpy as np
    writer.add_tensor("dummy", np.zeros((1, 1), dtype=np.float32))
    
    writer.write_header_to_file()
    writer.write_kv_data_to_file()
    writer.write_tensors_to_file()
    writer.close()
    print("[+] Test GGUF created.")

if __name__ == "__main__":
    create_test_gguf("lcl-secure-lab/audit/test_malicious.gguf")
