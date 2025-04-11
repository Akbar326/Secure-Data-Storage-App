# 🛡️ Secure Data Encryption System using Streamlit

This project is a **Streamlit-based secure data encryption and decryption system**, built entirely using **Python**. It allows users to **store sensitive information with a passkey**, and **retrieve it by decrypting with the same passkey**. It demonstrates basic principles of cryptography, data handling, and user interface design in Streamlit.

---

## 🚀 Features

- 🔐 Encrypts text using **Fernet symmetric encryption**.
- 🗝️ Stores data with **hashed passkey (SHA-256)**.
- ❌ Allows **3 decryption attempts only**, then redirects to a **Login Page**.
- 💾 Works **entirely in memory**, with no external database.
- 🧠 Tracks **failed attempts** per session.
- 🧹 Option to **delete stored encrypted data**.
- 🖥️ **User-friendly UI** with improved sidebar, icons, layout, and footer.

---

## 🧪 How it Works

1. Navigate to `Store Data` and enter text + passkey.
2. Your data is encrypted and stored securely.
3. Navigate to `Retrieve Data` to decrypt it using the same passkey.
4. After **3 wrong attempts**, access is blocked until reauthorization via `Login Page`.

---

## 📂 Technologies Used

- Python
- Streamlit
- Cryptography (Fernet)
- hashlib (SHA-256)
- In-memory dictionary

---

## 👨‍💻 Developed by

**Akbar Ali**  

---
