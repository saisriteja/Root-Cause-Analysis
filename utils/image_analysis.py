from ollama import chat
from pydantic import BaseModel
from typing import List, Optional
from typing_extensions import Literal

class Object(BaseModel):
    name: str
    confidence: float
    attributes: str 

class ImageDescription(BaseModel):
    summary: str
    objects: List[Object]
    scene: str
    colors: List[str]
    time_of_day: Literal['Morning', 'Afternoon', 'Evening', 'Night']
    setting: Literal['Indoor', 'Outdoor', 'Unknown']
    text_content: Optional[str] = None
    # New fields for RCA and CAPA analysis
    person_actions: Optional[str] = None  # What the person is doing
    task_description: Optional[str] = None  # What tasks are being performed
    potential_issues: Optional[str] = None  # Potential risks or issues in the context

def get_image_analysis(path):

    response = chat(
        model='llama3.2-vision',
        format=ImageDescription.model_json_schema(),  # Pass in the schema for the response
        messages=[
            {
                'role': 'user',
                'content': 'Analyze this image and describe what you see, including any objects, the scene, colors, text, and any activities or tasks the person is performing. Also, assess potential issues or risks that could arise from the context.',
                'images': [path],
            },
        ],
        options={'temperature': 0},  # Set temperature to 0 for more deterministic output
    )

    # Assuming the response contains the required context for RCA and CAPA analysis
    image_description = ImageDescription.model_validate_json(response.message.content)

    # Extract the RCA and CAPA information
    person_actions = image_description.person_actions
    task_description = image_description.task_description
    potential_issues = image_description.potential_issues

    # # Output the analysis
    # print(f"Person Actions: {person_actions}")
    # print(f"Task Description: {task_description}")
    # print(f"Potential Issues: {potential_issues}")
    return [person_actions, task_description, potential_issues]


from ollama import chat
from typing import List
from ollama import chat
from pydantic import BaseModel
from typing import List

# Define the structured output class
class JobChecklist(BaseModel):
    checklist_items: List[str]

# Define the class to send to the model for structured output
class JobAnalysisDescription:
    def __init__(self, person_actions: str, task_description: str, potential_issues: str):
        self.person_actions = person_actions
        self.task_description = task_description
        self.potential_issues = potential_issues

    def to_message_format(self):
        prompt = {
            'role': 'user',
            'content': f"Given the following analysis:\nPerson's Actions: {self.person_actions}\nTask Description: {self.task_description}\nPotential Issues: {self.potential_issues}\nGenerate a checklist of 10 structured items (in bullet points) to do or consider before performing the job, based on the person's actions, the task description, and any potential issues or risks. Format the output as a list of 10 numbered points."
        }

        # Make the API call to Ollama to generate the checklist
        response = chat(
            model='llama3.2-vision',
            messages=[prompt],
            options={'temperature': 0},  # Set temperature to 0 for more deterministic output
            format=JobChecklist.model_json_schema(),  # Specify the schema for structured output
        )

        # Parse the response using the defined JobChecklist Pydantic model
        job_checklist = JobChecklist.model_validate_json(response.message.content)

        return job_checklist.checklist_items