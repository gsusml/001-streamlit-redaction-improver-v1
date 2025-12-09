import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq


template = """
You are an expert multi-language code converter.
Your goals are:
- Read and fully understand the provided source code.
- Rewrite the code in a *different target programming language* specified by the user.
- Preserve the original logic, structure, and behavior.
- Improve clarity when needed, but DO NOT change functionality.
- If the input language or target language is ambiguous, ask for clarification.
- Add comments in the target language only if the user requests them.

Below is the source code and the target language:

SOURCE_LANGUAGE: {source_language}
TARGET_LANGUAGE: {target_language}

SOURCE_CODE:
\"\"\"
{source_code}
\"\"\"

YOUR OUTPUT ({target_language}) with comments in SPANISH:
"""

prompt = PromptTemplate(
    input_variables=["source_language", "target_language", "source_code"],
    template=template,
)


def load_LLM(api_key):
    return ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
        temperature=0
    )


st.set_page_config(page_title="Code converter")
st.header("Convierte un código entre lenguajes de programación.")


col1, col2 = st.columns(2)
with col1:
    st.markdown("Convierte código de un lenguaje de programación en otro.")
with col2:
    st.write("Contact with [AI Accelera](https://aiaccelera.com)")


st.markdown("## Introduce tu API KEY de GROQ")
api_key = st.text_input("Groq API Key", type="password")


st.markdown("## Introduce el código que debe ser recodificado")
source_code_input = st.text_area("Code", height=300)


if len(source_code_input) > 15000:
    st.error("El tamaño máximo de caracteres del código es de 15000")
    st.stop()


col1, col2 = st.columns(2)
with col1:
    source_language = st.selectbox(
        "Lenguaje Fuente",
        ("Python", "JavaScript", "R", "C#", "Go", "PHP", "Ruby", "C++", "Rust", "Swift")
    )
with col2:
    target_language = st.selectbox(
        "Lenguaje Objetivo",
        ("Python", "JavaScript", "R", "C#", "Go", "PHP", "Ruby", "C++", "Rust", "Swift")
    )


language_map = {
    "Python": "python",
    "JavaScript": "javascript",
    "R": "r",
    "C#": "csharp",
    "C++": "cpp",
    "Go": "go",
    "PHP": "php",
    "Ruby": "ruby",
    "Rust": "rust",
    "Swift": "swift",
}

pygments_lang = language_map[target_language]


st.markdown("### Código convertido:")

if source_code_input:
    if not api_key:
        st.warning("Por favor, introduzca su Groq API KEY.", icon="⚠️")
        st.stop()

    if source_language == target_language:
        st.info("El lenguaje fuente y objetivo son iguales. No se requiere conversión.")
        st.stop()

    llm = load_LLM(api_key)

    prompt_filled = prompt.format(
        source_language=source_language,
        target_language=target_language,
        source_code=source_code_input
    )

    response = llm.invoke(prompt_filled)
    converted_code = response.content

    st.code(converted_code, language=pygments_lang)
