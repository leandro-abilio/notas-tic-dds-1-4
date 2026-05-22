import streamlit as st
import pandas as pd
import io
import requests

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

FILE_ID = "1QbcgF1NekGWxwuXXitzhRIVSnyftk_w1"
DOWNLOAD_URL = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

@st.cache_data(ttl=10)  # Atualiza a cada 5 minutos
@st.cache_data(ttl=10)
def carregar_todos_alunos():
    response = requests.get(DOWNLOAD_URL)
    response.raise_for_status()
    
    xls = pd.ExcelFile(io.BytesIO(response.content))
    todos = {}
    
    for turma in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=turma, dtype={"RA": int})
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
                "turma": turma,
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
                    st.error("❌ Não foi possível carregar os dados. Tente novamente em instantes.")
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
