# envguard

**Fail-fast, human-friendly environment configuration for Python projects**

---

## Why envsafe?

Managing environment variables across multiple environments (dev, staging, prod) is a pain:

- Missing variables cause runtime errors.
- Typos break apps silently.
- Developers often rely on fragile `.env` files.
- Secrets can accidentally leak in logs.

**envguard solves all this with:**

- Schema-based configuration in Python.
- Fail-fast validation with clear error messages. 
- Automatic `.env.example` generation.  
- Environment diff tool to compare `.env` files.  
- Secure by default (no secrets printed).  

---

## 📦 Installation


