import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Portal de Notas", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .main { text-align: center; }
    div.stButton > button:first-child {
        background-color: #4CAF50;
        color: white;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Carrega os dados do CSV — só isso substitui todo o dicionário hardcoded!
@st.cache_data
def carregar_alunos():
    csv_texto = st.secrets["alunos"]["dados"]
    df = pd.read_csv(io.StringIO(csv_texto), dtype={"ra": int})
    return df.set_index("ra").to_dict(orient="index")

alunos = carregar_alunos()

st.title("🎓 Consulta de Notas")
st.subheader("Insira seu Registro Acadêmico (RA) para acessar o painel.")

ra_input = st.text_input("Registro Acadêmico:", type="password", help="Digite apenas os números do seu RA")

if st.button("Consultar Nota"):
    if ra_input.strip():
        try:
            ra_digitado = int(ra_input)

            if ra_digitado in alunos:
                aluno = alunos[ra_digitado]
                st.success("✨ Acesso Autorizado!")
                st.balloons()
                st.markdown(f"### 👤 **Aluno(a):** {aluno['nome']}")
                st.metric(label="Nota Final", value=f"{aluno['nota']} pts")
            else:
                st.error("❌ RA não encontrado. Verifique os dados e tente novamente.")
        except ValueError:
            st.warning("⚠️ Formato inválido. O Registro Acadêmico deve conter apenas números.")
    else:
        st.warning("⚠️ Por favor, preencha o campo do Registro Acadêmico.")