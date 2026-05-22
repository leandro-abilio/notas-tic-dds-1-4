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

# Nomes legíveis das matérias
MATERIAS = {
    "intro_tic": "Introdução a TIC",
    "intro_qep": "Introdução a QeP"
}

@st.cache_data
def carregar_todos_alunos():
    """Lê todas as turmas dos Secrets e junta num dicionário único por RA."""
    todos = {}
    for turma, dados in st.secrets.items():
        df = pd.read_csv(io.StringIO(dados["dados"]), dtype={"ra": int})
        for _, row in df.iterrows():
            todos[row["ra"]] = {
                "nome": row["nome"],
                "turma": turma.upper(),
                "notas": {
                    col: row[col]
                    for col in MATERIAS
                    if col in df.columns and pd.notna(row[col])
                }
            }
    return todos

alunos = carregar_todos_alunos()

st.title("🎓 Portal de Notas")
st.subheader("Digite seu Registro Acadêmico (RA) para consultar seu boletim.")

ra_input = st.text_input("Registro Acadêmico:", type="password", help="Digite apenas os números do seu RA")

if st.button("Consultar Notas"):
    if ra_input.strip():
        try:
            ra_digitado = int(ra_input)

            if ra_digitado in alunos:
                aluno = alunos[ra_digitado]
                st.success("✨ Acesso Autorizado!")
                st.balloons()

                st.markdown(f"### 👤 {aluno['nome']}")
                st.markdown(f"**Turma:** {aluno['turma']}")
                st.divider()

                if aluno["notas"]:
                    st.markdown("#### 📋 Boletim")
                    cols = st.columns(len(aluno["notas"]))
                    for col, (materia_key, nota) in zip(cols, aluno["notas"].items()):
                        col.metric(label=MATERIAS[materia_key], value=f"{nota} pts")
                else:
                    st.info("Nenhuma nota lançada ainda.")

            else:
                st.error("❌ RA não encontrado. Verifique os dados e tente novamente.")
        except ValueError:
            st.warning("⚠️ Formato inválido. O RA deve conter apenas números.")
    else:
        st.warning("⚠️ Por favor, preencha o campo do RA.")
