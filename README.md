# 🛡️ SafeCheck — Personal Data Leak Detector

A privacy-first web app that checks whether your password has been exposed in a known data breach — without ever sending your actual password over the network.

Built with **Python**, **Streamlit**, and the **Have I Been Pwned (HIBP) k-anonymity API**.

---

## 🚀 Features

- ✅ **Breach Detection** — checks your password against a database of billions of leaked credentials
- ✅ **Password Strength Analyzer** — scores your password on length, character variety, and gives improvement tips
- ✅ **100% Privacy-Preserving** — uses k-anonymity, so your real password never leaves your device (only a partial hash is sent)
- ✅ **Clean, modern UI** — built with Streamlit and custom styling

---

## 🧠 How It Works

1. Your password is hashed locally using **SHA-1**.
2. Only the **first 5 characters** of that hash are sent to the HIBP API.
3. The API returns all known breached hash suffixes matching that prefix.
4. The app checks **locally** if your full hash is in that list — your password itself is never transmitted or stored.

This technique is called **k-anonymity**, and it's the same method used by HIBP's own official password-checking tools.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/safecheck-leak-detector.git
cd safecheck-leak-detector

# Install dependencies
pip install -r requirements.txt
```

## ▶️ Usage

```bash
streamlit run app.py
```

Then open the local URL shown in your terminal (usually `http://localhost:8501`).

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.x |
| Web Framework | Streamlit |
| Breach Database | HaveIBeenPwned Pwned Passwords API |
| Hashing | SHA-1 (via Python `hashlib`) |
| HTTP Client | `requests` |

---

## 📁 Project Structure

```
safecheck-leak-detector/
├── app.py                   # Streamlit UI
├── leak_detector_core.py    # Core breach-checking & strength logic
├── requirements.txt         # Dependencies
└── README.md                # This file
```

---

## 🔮 Future Scope

- Email breach checking (requires a paid HIBP API key)
- Browser extension version
- Password manager integration
- Dark web monitoring alerts

---

## ⚠️ Disclaimer

This tool is built for educational purposes as part of an academic project. It uses HIBP's public Pwned Passwords API responsibly and does not store or log any user passwords.

---

## 👤 Author

**Mayur Shelke**
Computer Science Engineering Student, Sanjivani College of Engineering, Kopargaon
