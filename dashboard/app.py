import streamlit as st
import pandas as pd
import requests

API_URL = st.secrets.get("api_url", "http://localhost:8000")

st.title("Mini‑TMR Molecule Registry")

tab1, tab2 = st.tabs(["Upload", "Browse"])

with tab1:
    st.header("Bulk Upload CSV")
    csv_file = st.file_uploader("Upload scored_molecules.csv", type=["csv"])
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        if st.button("Upload to Registry"):
            payload = df.to_dict(orient="records")
            res = requests.post(f"{API_URL}/molecules/bulk", json=payload)
            st.write(res.json())

with tab2:
    st.header("Browse Registry")
    limit = st.slider("Number of records", 10, 500, 100)
    res = requests.get(f"{API_URL}/molecules/?limit={limit}")
    if res.status_code == 200:
        df = pd.DataFrame(res.json())
        st.dataframe(df)