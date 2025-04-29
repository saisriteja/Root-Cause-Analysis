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

if __name__ == '__main__':
    path = 'sample_images/welding_at_height.jpg'
    image_analyzer = ImageAnalyzer(path)
    analysis_result = image_analyzer.analyze_image()
    checklist = image_analyzer.get_checklist(analysis_result)
    print("analysis_result")
    print(analysis_result)
    print("checklist")
    print(checklist)