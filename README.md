# LCL Secure Lab (LSL) 🛡️🧪

## 🏢 Overview
**LCL Secure Lab** is an open-source security research project by **LINDA Cyber Legion (LCL) Corp.** 
It provides a dedicated, high-isolation environment for analyzing AI-related vulnerabilities, specifically targeting LLM exploit crafting and malicious model payload (e.g., GGUF, ONNX) execution.

## ⚖️ Disclaimer
This project is intended for **authorized security research and educational purposes only**. 
LINDA Cyber Legion (LCL) Corp. and the project contributors are not responsible for any misuse, damage, or illegal activities performed using the tools and configurations provided in this repository. 
Unauthorized testing or attacking of individuals, organizations, or systems without explicit prior permission is strictly prohibited and may result in legal consequences.
Use this laboratory responsibly within a controlled and legal environment.

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
- `/examples`: Proof-of-Concept and testing scripts.
    - `poc_ssti_gguf.py`: Generates a GGUF file with a simulated SSTI payload.
    - `test_isolation.py`: Verifies sandbox restrictions (network, filesystem).
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

# 5. Verify the sandbox with an isolation test
python3 examples/test_isolation.py
```

## 🛠️ Community Contributions
We encourage researchers to contribute:
- **New PoC Scripts:** Add examples of novel LLM attack vectors to `/examples`.
- **Hardened Configs:** Improve `configs/hardened_nsjail.cfg` for better security/performance.
- **Audit Rules:** Add detection patterns to `scripts/gguf_audit.py`.

Please ensure all "Internal" or "Live Experiment" data is kept in the `workspace/` directory, which is excluded from version control.

---
*Maintained by the LCL Corp. Engineering Team.*
