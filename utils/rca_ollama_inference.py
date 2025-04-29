from ollama import chat, ChatResponse
from pydantic import BaseModel
from typing import List


# Define the model to support multiple reasons per 6M category
class FishboneCategory(BaseModel):
    title: str
    reasons: List[str]

class FishboneAnalysis(BaseModel):
    man: FishboneCategory
    machine: FishboneCategory
    material: FishboneCategory
    method: FishboneCategory
    measurement: FishboneCategory
    mother_nature: FishboneCategory


# Ollama call with structured response
def get_structured_ollama_response(prompt: str) -> FishboneAnalysis:
    response: ChatResponse = chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}],
        format=FishboneAnalysis.model_json_schema(),
    )
    return FishboneAnalysis.model_validate_json(response.message.content)