#Create our streamlit app
#Give a title - Code reviewer app
#Ask user to enter a code/program
#Click a button for getting code review
#Use open ai API to review the code and comment on how to improve 
#the code

'''
I have main.py and call_openai.py
give me code separate for each file
put streamlit code in main.py
and api call code in call_openai.py
'''

import hmac
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()


from services.call_openai import get_code_review
#services folder - call_openai.py file and get_code_review()

# Streamlit app title
st.title("Code Reviewer App")

# Prompt user to enter code
code_input = st.text_area("Enter your code/program here:")

# Button to get code review
if st.button("Get Code Review"):
    if code_input.strip() == "":
        st.warning("Please enter some code before requesting a review.")
    else:
        with st.spinner('Reviewing your code...'):
            review = get_code_review(code_input)
            st.subheader("Code Review:")
            st.text_area("Review", review, height=300)
