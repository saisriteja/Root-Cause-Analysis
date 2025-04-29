from utils.rca_ollama_inference import get_structured_ollama_response
from utils.capa_analysis import get_correction_prevention

class RCA_CAPA:
    def __init__(self, situation_prompt):
        self.situation_prompt = situation_prompt

    def rca_analysis(self):

        prompt_intro = """I am giving you a situation and I expect a fish bone (Ishikawa) analysis using the 6M's:
                            1. Man (People)
                            2. Machine (Equipment/Tools)
                            3. Material
                            4. Method (Process/Procedure)
                            5. Measurement
                            6. Mother Nature (Environment)

                            Each category should include a title and a brief description.

                            """
        final_prompt = prompt_intro + f"Situation: '{self.situation_prompt}'"

        # Run
        result = get_structured_ollama_response(final_prompt)
        # print(result.model_dump_json(indent=2))
        return result

    def capa_analysis(self, rca_dict):
        # Get the CAPA analysis
        capa_result = get_correction_prevention(rca_dict)
        return capa_result



if __name__ == '__main__':
    

    # Situation and prompt definition
    situation = (
        "A hammer accidentally fell from height and hit a worker on the head "
        "when he is doing welding work, causing injury."
    )


    rca_capa = RCA_CAPA(situation)
    rca_result = rca_capa.rca_analysis()
    capa_result = rca_capa.capa_analysis(rca_result.model_dump())

    print(rca_result.model_dump_json(indent=2))
    print('-----------------------------------------')
    print(capa_result)

