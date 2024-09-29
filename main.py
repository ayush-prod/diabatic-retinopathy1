import streamlit as st
import pandas as pd
from PIL import Image
from gpt_analysis import analyze_diabetic_retinopathy, details
from image_processing import preprocess_image
from utils import get_dr_scale_definition

st.set_page_config(page_title="Diabetic Retinopathy Diagnostic App",
                   layout="wide")


def main():
    st.title("Diabetic Retinopathy Diagnostic App")

    # Patient Information Input
    st.header("Patient Information")
    patient_name = st.text_input("Patient Name")
    doctor_name = st.text_input("Doctor Name")
    hospital_name = st.text_input("Hospital Name")
    visit_date = st.date_input("Date of Visit")

    # Image Upload
    uploaded_file = st.file_uploader("Choose a retinal scan image",
                                     type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Retinal Scan", use_column_width=True)

        # Button to analyze the image
        if st.button("Analyze Retinal Scan"):
            with st.spinner("Analyzing image..."):
                preprocessed_image = preprocess_image(image)
                analysis_result = analyze_diabetic_retinopathy(
                    preprocessed_image)
                report = "No report available."
                if str(analysis_result).isdigit():
                    report = details(
                        preprocessed_image,
                        get_dr_scale_definition(int(analysis_result)))
            # Display analysis results
            st.header("Diabetic Retinopathy Analysis")
            if not str(analysis_result).isdigit():
                st.error(f"An error occurred: {analysis_result}")
                st.write(f"Error details: {analysis_result}")
            else:
                st.subheader("DR Scale")
                st.write(f"DR Scale: {analysis_result}")
                st.subheader("Detailed Analysis")
                st.write(report)

                # Create a DataFrame for patient information and analysis results
                data = {
                    "Patient Name": [patient_name],
                    "Doctor Name": [doctor_name],
                    "Hospital Name": [hospital_name],
                    "Visit Date": [visit_date],
                    "DR Scale": [analysis_result],
                    "Analysis": [report]
                }
                df = pd.DataFrame(data)

                # Option to download the report as CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download Report as CSV",
                    data=csv,
                    file_name="diabetic_retinopathy_analysis.csv",
                    mime="text/csv",
                )


if __name__ == "__main__":
    main()
