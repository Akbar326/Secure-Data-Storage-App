import streamlit as st
import hashlib
import json
import os
import time
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from hashlib import pbkdf2_hmac

# Constants
DATA_FILE = 'secure_data.json'
SALT = b'secure_salt_Value'
LOCKOUT_DURATION = 60

# Streamlit config
st.set_page_config(page_title="🔐 Secure Data App", page_icon="🔐", layout="centered")

# Sidebar design
with st.sidebar:
    st.markdown("## 🔐 Secure Storage")
    menu = ['🏠 Home', '📝 Register', '🔓 Login', '💾 Store Data', '📂 Retrieve Data']
    choice = st.radio("Navigation", menu)

# Session states
if 'authenticated_user' not in st.session_state:
    st.session_state.authenticated_user = None
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'lockout_time' not in st.session_state:
    st.session_state.lockout_time = 0

# Load and save
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def generate_key(passkey):
    key = pbkdf2_hmac('sha256', passkey.encode(), SALT, 100000)
    return urlsafe_b64encode(key)

def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000).hex()

def encrypt_text(text, key):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    try:
        cipher = Fernet(generate_key(key))
        return cipher.decrypt(encrypted_text.encode()).decode()
    except:
        return None

stored_data = load_data()

# Pages
if choice == '🏠 Home':
    st.title("🏠 Home")
    st.subheader("🔐 Welcome to Secure Data Storage")
    st.markdown("""
    This application helps you securely store and retrieve **sensitive data**.
    
    ### How It Works:
    1. 📝 Register with a username and password.
    2. 🔓 Login using your credentials.
    3. 💾 Store sensitive data (encrypted).
    4. 📂 Retrieve or delete your data when needed.

    Everything stays local, safe, and secure!
    """)

elif choice == '📝 Register':
    st.title("📝 Register")
    username = st.text_input('👤 Username')
    password = st.text_input('🔑 Password', type='password')
    confirm_password = st.text_input('🔁 Confirm Password', type='password')

    if st.button('✅ Register'):
        if not username or not password:
            st.error('🚫 Both fields are required')
        elif password != confirm_password:
            st.error('🚫 Passwords do not match')
        elif username in stored_data:
            st.error('🚫 Username already exists')
        else:
            stored_data[username] = {'password': hash_password(password), 'data': []}
            save_data(stored_data)
            st.success('✅ Registration successful!')

    st.markdown("🔒 Already registered? Go to **Login** section.")

elif choice == '🔓 Login':
    st.title("🔓 Login")

    if time.time() < st.session_state.lockout_time:
        remaining_time = int(st.session_state.lockout_time - time.time())
        st.error(f'⏱ Too many attempts. Try again in {remaining_time} seconds.')
        st.stop()

    username = st.text_input('👤 Username')
    password = st.text_input('🔑 Password', type='password')

    if st.button('🔐 Login'):
        if username in stored_data and stored_data[username]['password'] == hash_password(password):
            st.session_state.authenticated_user = username
            st.session_state.failed_attempts = 0
            st.success('✅ Login successful!')
        else:
            st.session_state.failed_attempts += 1
            remaining = 3 - st.session_state.failed_attempts
            st.error(f'❌ Invalid credentials. {remaining} attempts remaining.')

            if st.session_state.failed_attempts >= 3:
                st.session_state.lockout_time = time.time() + LOCKOUT_DURATION
                st.error('🚫 Too many failed attempts. Locked for 60 seconds.')

elif choice == '💾 Store Data':
    st.title("💾 Store Encrypted Data")

    if not st.session_state.authenticated_user:
        st.warning('⚠ Please login first.')
    else:
        data = st.text_area('📥 Enter data to store')
        passkey = st.text_input('🔑 Enter passkey', type='password')

        if st.button('💾 Encrypt & Save'):
            if data and passkey:
                encrypted = encrypt_text(data, generate_key(passkey))
                stored_data[st.session_state.authenticated_user]['data'].append(encrypted)
                save_data(stored_data)
                st.success('✅ Data encrypted and stored.')
            else:
                st.error('🚫 All fields are required.')

elif choice == '📂 Retrieve Data':
    st.title("📂 Retrieve Encrypted Data")

    if not st.session_state.authenticated_user:
        st.warning('⚠ Please login first.')
    else:
        user_data = stored_data.get(st.session_state.authenticated_user, {}).get('data', [])
        if not user_data:
            st.info('📭 No data found.')
        else:
            st.markdown("### 🗂 Your Encrypted Data:")
            for i, item in enumerate(user_data):
                st.code(item, language='text')
                passkey = st.text_input(f'🔑 Passkey for item {i+1}', key=f'pass_{i}', type='password')

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f'🧪 Decrypt {i+1}', key=f'decrypt_{i}'):
                        if passkey:
                            result = decrypt_text(item, passkey)
                            if result:
                                st.success(f'🔓 Decrypted: {result}')
                            else:
                                st.error('🚫 Decryption failed.')
                        else:
                            st.warning('⚠️ Please enter a passkey.')

                with col2:
                    if st.button(f'🗑 Delete {i+1}', key=f'delete_{i}'):
                        stored_data[st.session_state.authenticated_user]['data'].pop(i)
                        save_data(stored_data)
                        st.success('🗑 Data deleted successfully')
                        st.rerun()

# Footer
st.markdown("---")
st.markdown("<center>Build with love by <strong>Akbar Ali</strong></center>", unsafe_allow_html=True)
