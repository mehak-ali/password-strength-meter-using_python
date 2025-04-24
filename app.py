
import streamlit as st
import re
import random
import string

# -------------------------------
# Password Evaluation Function
# -------------------------------
def evaluate_password(password: str):
    score = 0
    feedback = []

    # Rule 1: Length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("🔴 Must be at least 8 characters long.")

    # Rule 2: Uppercase and Lowercase
    if any(c.islower() for c in password) and any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("🔴 Include both uppercase and lowercase letters.")

    # Rule 3: Digit
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("🔴 Add at least one digit (0-9).")

    # Rule 4: Special Character
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔴 Add at least one special character (!@#$%^&*).")

    # Determine strength and color
    if score == 4:
        strength = "🔒 Strong"
        color = "green"
    elif score >= 2:
        strength = "🟠 Moderate"
        color = "orange"
    else:
        strength = "🔓 Weak"
        color = "red"

    return strength, feedback, color, score

# -------------------------------
# Random Password Generator
# -------------------------------
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

# -------------------------------
# Streamlit UI Setup
# -------------------------------
st.set_page_config(page_title="🔐 Password Strength Meter", page_icon="🔑", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🔐 Password Strength Meter</h1>
    <p style='text-align: center; font-size:18px;'>Check the security of your password and get improvement tips!</p>
    """, unsafe_allow_html=True)

# Optional: Password Generator
with st.expander("⚙️ Need a strong password? Click to generate"):
    if st.button("Generate Random Password"):
        st.session_state.generated_password = generate_password()
    generated_pw = st.session_state.get("generated_password", "")
    if generated_pw:
        st.code(generated_pw)

# Password Input
password = st.text_input("🔑 Enter your password:", type="password")

# Evaluate password
if password:
    strength, feedback, color, score = evaluate_password(password)
    
    # Strength Result
    st.markdown(f"<h3 style='color:{color}'>Strength: {strength}</h3>", unsafe_allow_html=True)
    
    # Progress Bar
    st.progress(score / 4)

    # Feedback List
    if feedback:
        st.markdown("💡 <b>Suggestions to Improve:</b>", unsafe_allow_html=True)
        for item in feedback:
            st.write(f"- {item}")
    else:
        st.success("✅ Your password meets all strength criteria!")

# Tips Section
st.markdown("---")
with st.expander("🔐 Password Tips"):
    st.info("""
- Use a mix of uppercase, lowercase, numbers, and symbols.
- Avoid using names, birthdays, or common words.
- Use a passphrase or a password manager for strong unique passwords.
""")

