import streamlit as st
import pandas as pd
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

            Each category should include a title and a list of possible root causes (as 'reasons').
        """
        final_prompt = prompt_intro + f"Situation: '{self.situation_prompt}'"
        return get_structured_ollama_response(final_prompt)

    def capa_analysis(self, rca_dict):
        return get_correction_prevention(rca_dict)


# Streamlit App
st.set_page_config(page_title="RCA-CAPA Analyzer", layout="wide")
st.title("🔍 RCA-CAPA Analysis Tool")

situation = st.text_area("📌 Enter the Situation", 
    placeholder="E.g. A hammer accidentally fell from height and hit a worker on the head during welding work.")

if st.button("Run RCA-CAPA Analysis"):
    if situation.strip():
        with st.spinner("Running analysis..."):
            analyzer = RCA_CAPA(situation)
            rca_result = analyzer.rca_analysis()
            capa_result = analyzer.capa_analysis(rca_result.model_dump())

        # RCA Output in 3x2 Grid Layout
        st.subheader("🎯 Root Cause Analysis (6M Grid)")

        # Create a 3x2 Grid for RCA categories
        cols = st.columns(2)
        
        categories = list(rca_result.model_dump().keys())
        for idx, category_key in enumerate(categories):
            category_data = rca_result.model_dump()[category_key]
            col_idx = idx % 2  # 0 for first column, 1 for second column
            with cols[col_idx]:
                st.markdown(f"### {category_data['title']}")
                st.write("**Root Causes:**")
                for reason in category_data.get("reasons", []):
                    st.markdown(f"- {reason}")

        # CAPA Output as a Table
        st.subheader("🛠️ Corrective and Preventive Actions (CAPA)")

        capa_entries = []
        for category_key, entries in capa_result.items():
            title = rca_result.model_dump().get(category_key, {}).get("title", category_key.capitalize())
            for entry in entries:
                capa_entries.append({
                    'Category': title,
                    'Cause': entry['cause'],
                    'Correction': entry['correction'],
                    'Prevention': entry['prevention']
                })

        # Display CAPA as a DataFrame (table)
        if capa_entries:
            df_capa = pd.DataFrame(capa_entries)
            st.table(df_capa)
    else:
        st.warning("⚠️ Please enter a valid situation description.")
