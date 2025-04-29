import os
import shutil
import streamlit as st
from utils.image_analysis import get_image_analysis, JobAnalysisDescription


class ImageAnalyzer:
    def __init__(self, image_path):
        self.image_path = image_path

    def analyze_image(self):
        # Get the analysis from the image
        analysis_result = get_image_analysis(self.image_path)
        return analysis_result

    def get_checklist(self, analysis_result):
        # Create a JobAnalysisDescription object
        job_analysis = JobAnalysisDescription(
            person_actions=analysis_result[0],
            task_description=analysis_result[1],
            potential_issues=analysis_result[2]
        )
        # Get the checklist from the analysis
        message_format = job_analysis.to_message_format()
        return message_format


# Streamlit App
def main():
    st.title("Image Analysis for Job Safety")

    # Upload image file
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Create a path to save the file
        temp_image_path = os.path.join(temp_dir, uploaded_file.name)

        # Save the uploaded file
        with open(temp_image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        st.image(temp_image_path, caption="Uploaded Image", use_column_width=True)

        # Process the image for analysis
        image_analyzer = ImageAnalyzer(temp_image_path)
        analysis_result = image_analyzer.analyze_image()
        checklist = image_analyzer.get_checklist(analysis_result)

        # Display the analysis result
        st.subheader("Analysis Result")
        st.write("Person Actions: ", analysis_result[0])
        st.write("Task Description: ", analysis_result[1] if analysis_result[1] else "No specific task description provided.")
        st.write("Potential Issues: ", analysis_result[2])

        # Display the checklist
        st.subheader("Safety Checklist")
        for i, item in enumerate(checklist, 1):
            st.write(f"{item}")

if __name__ == "__main__":
    main()
