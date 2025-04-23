import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📁 File Converter & Cleaner", layout="wide")

st.markdown("""
    <style>
    /* General App Styles */
    .stApp {
        background: linear-gradient(to right, #f0f8ff, #e0f7fa);
        color: #1e3a8a;
        font-family: 'Arial', sans-serif;
    }
    
    /* Header Styles */
    h1, h2, h3 {
        color: #0288d1;
        font-weight: bold;
        text-align: center;
    }
    
    /* Paragraph and Label Styling */
    p, label, span {
        color: #0277bd;
        font-size: 1rem;
    }

    /* File Uploader Section */
    .stFileUploader {
        padding: 15px;
        border: 2px solid #0288d1;
        border-radius: 12px;
        background-color: #e1f5fe;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Button Styles */
    div.stButton > button {
        background-color: #0288d1;
        color: white;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: bold;
        text-transform: uppercase;
        transition: background-color 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #039be5;
    }

    /* Download Button Styles */
    .stDownloadButton {
        background-color: #26c6da !important;
        color: white !important;
        border-radius: 12px;
        font-weight: bold;
        padding: 12px 25px;
        transition: background-color 0.3s ease;
    }
    
    .stDownloadButton:hover {
        background-color: #00acc1 !important;
    }

    /* Checkboxes and Radio Buttons */
    .stCheckbox > label, .stRadio > label {
        color: #0288d1;
        font-size: 1rem;
        font-weight: bold;
    }
    
    /* Sidebar Styles */
    section[data-testid="stSidebar"] {
        background-color: #e3f2fd;
        border-right: 2px solid #0288d1;
        padding: 20px;
    }

    /* Dataframe Table Styling */
    .stDataFrame {
        border: 1px solid #0288d1;
        border-radius: 8px;
        padding: 10px;
    }

    /* Chart Styles */
    .stBarChart {
        border-radius: 8px;
        background-color: #fafafa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)


# ✅ Now continue with the rest of your app
st.title("📁 File Converter & Cleaner")
st.write("Upload your CSV and Excel files to clean the data and convert formats effortlessly 🚀")

# File uploader
files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()

        # Try reading file safely
        try:
            df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        except Exception as e:
            st.error(f"❌ Error reading {file.name}: {e}")
            continue

        st.subheader(f"🔍 Preview: {file.name}")
        st.dataframe(df.head())

        # Fill missing values
        if st.checkbox(f"🧹 Fill missing values – {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled successfully!")
            st.dataframe(df.head())

        # Column selector
        selected_columns = st.multiselect(
            f"🧩 Choose columns to keep – {file.name}",
            df.columns.tolist(),
            default=df.columns.tolist()
        )
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart for numeric data
        if st.checkbox(f"📈 Show chart – {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Format selection
        format_choice = st.radio(f"💾 Export format for {file.name}:", ["CSV", "Excel"], key=f"radio_{file.name}")

        # Download button
        if st.button(f"⬇️ Download {file.name} as {format_choice}", key=f"btn_{file.name}"):
            output = BytesIO()
            if format_choice == "CSV":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.rsplit(".", 1)[0] + ".csv"
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.rsplit(".", 1)[0] + ".xlsx"
            output.seek(0)

            st.download_button("⬇️ Download File", data=output, file_name=new_name, mime=mime)
            st.success("🎉 File processed and ready!")
