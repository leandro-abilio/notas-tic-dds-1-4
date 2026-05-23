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

@st.cache_data
def carregar_todos_alunos():
    todos = {}
    for turma, dados in st.secrets.items():
        df = pd.read_csv(io.StringIO(dados["dados"]), dtype={"RA": int})
        df.columns = df.columns.str.strip()

        # Tudo que não for RA ou Nome é matéria — automático!
        colunas_materias = [c for c in df.columns if c not in ("RA", "Nome")]

        for _, row in df.iterrows():
            try:
                ra = int(row["RA"])
            except (ValueError, KeyError):
                continue

            notas = {
                col: row[col]
                for col in colunas_materias
                if pd.notna(row.get(col))
            }

            todos[ra] = {
                "nome": row["Nome"],
                "turma": turma.upper(),
                "notas": notas
            }
    return todos

st.title("🎓 Portal de Notas")
st.subheader("Digite seu Registro Acadêmico (RA) para consultar seu boletim.")

ra_input = st.text_input("Registro Acadêmico:", type="password", help="Digite apenas os números do seu RA")

if st.button("Consultar Notas"):
    if ra_input.strip():
        try:
            ra_digitado = int(ra_input)

            with st.spinner("Carregando..."):
                try:
                    alunos = carregar_todos_alunos()
                except Exception:
                    st.error("❌ Não foi possível carregar os dados. Tente novamente.")
                    st.stop()

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
                    for col, (materia, nota) in zip(cols, aluno["notas"].items()):
                        col.metric(label=materia, value=f"{nota} pts")
                else:
                    st.info("Nenhuma nota lançada ainda.")
            else:
                st.error("❌ RA não encontrado. Verifique os dados e tente novamente.")
        except ValueError:
            st.warning("⚠️ Formato inválido. O RA deve conter apenas números.")
    else:
        st.warning("⚠️ Por favor, preencha o campo do RA.")
