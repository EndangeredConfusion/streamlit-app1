import streamlit as st
import pandas as pd

if "info_added" not in st.session_state:
    st.session_state.info_added = False

if "info" not in st.session_state:
    st.session_state.info = None


def upload_info():
    st.header("Upload Credit Card Info")
    uploaded_file = st.file_uploader("Upload CSV Here", ["csv"])

    if st.button("Confirm"):
        if uploaded_file is not None:
            st.session_state.info_added = True
            st.session_state.info = pd.read_csv(uploaded_file)
        st.rerun()


def main():
    upload_page = st.Page("main.py", title="Upload", icon=":material/upload_file:")

    analysis_page = st.Page("pages/analysis.py", title="Analysis", icon=":material/monitoring:")

    if st.session_state.info_added:
        st.switch_page("pages/analysis.py")
    else:
        upload_info()


if __name__ == "__main__":
    main()
