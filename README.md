# LCL Secure Lab (LSL) 🛡️🧪

## 🏢 Overview
**LCL Secure Lab** is an open-source security research project by **LINDA Cyber Legion (LCL) Corp.** 
It provides a dedicated, high-isolation environment for analyzing AI-related vulnerabilities, specifically targeting LLM exploit crafting and malicious model payload (e.g., GGUF, ONNX) execution.

## 🛡️ Security Features
- **OS-Level Isolation:** Utilizing Linux namespaces (NSJail/Bubblewrap) to create a "Digital Hazmat Suit".
- **Zero-Network Policy:** Strictly air-gapped execution by default.
- **Resource Constrainment:** Fine-grained control over Memory and CPU to prevent DoS.
- **Forensic Logging:** Comprehensive syscall and behavior monitoring.

## 📁 Repository Structure
- `/configs`: Hardened sandbox profiles (e.g., `hardened_nsjail.cfg`).
- `/scripts`: Automated setup and execution wrappers.
    - `setup_lab.sh`: Automated dependency installer.
    - `run_isolated.sh`: NSJail execution wrapper.
    - `gguf_audit.py`: Semantic metadata scanner for GGUF model files.
- `/audit`: (Local only) Results and forensic reports.

## 🚀 Getting Started
```bash
# 1. Clone the repo
git clone https://github.com/linda-agi/lcl-secure-lab.git
cd lcl-secure-lab

# 2. Setup the environment
bash scripts/setup_lab.sh

# 3. Perform a safe audit on a model
python3 scripts/gguf_audit.py /path/to/your/model.gguf

# 4. Run an untrusted script in isolation
bash scripts/run_isolated.sh python3 malicious_poc.py
```

## 🤝 Community & Contribution
This project is part of the **Linda Firewall** ecosystem. We welcome contributions from security researchers and AI developers.

---
*Maintained by the LCL Corp. Engineering Team.*
