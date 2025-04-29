import json
from ollama import chat, ChatResponse
from pydantic import BaseModel
from typing import List
from pydantic import BaseModel
from typing import List, Dict
from ollama import chat

class RCAItem(BaseModel):
    cause: str
    correction: str
    prevention: str

class RCAGroup(BaseModel):
    man: List[RCAItem]
    machine: List[RCAItem]
    material: List[RCAItem]
    method: List[RCAItem]
    measurement: List[RCAItem]
    mother_nature: List[RCAItem]





def get_correction_prevention(rca_dict: dict) -> dict:
    prompt = """
    You are given a categorized list of root causes under the 6M framework (man, machine, material, method, measurement, mother_nature). For each 'reason', provide:
    1. A correction – an immediate fix.
    2. A prevention – a long-term measure.

    Output the result using the following JSON schema:
    {
    "man": [
        {
        "cause": "...",
        "correction": "...",
        "prevention": "..."
        }
    ],
    ...
    }
    """

    full_prompt = prompt + "\nHere is the RCA:\n" + json.dumps(rca_dict, indent=2)

    response = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': full_prompt}],
        format=RCAGroup.model_json_schema()
    )

    # Parse the response into a Pydantic object
    rca_structured = RCAGroup.model_validate_json(response.message.content)
    return rca_structured.model_dump()