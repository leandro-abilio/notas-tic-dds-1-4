import streamlit as st

# Configuração da página do navegador
st.set_page_config(page_title="Portal de Notas", page_icon="🎓", layout="centered")

# Estilização leve para centralizar e deixar o visual limpo
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

# Base de dados completa (Hardcoded)
alunos = {
    339418: {"nome": "ANA JÚLIA MORAES VASCONCELOS", "nota": 82.9},
    338363: {"nome": "ANA PAULA MEDEIROS POLACK", "nota": 82.3},
    330047: {"nome": "ANDRÉ LUIS DO NASCIMENTO DE PAULA", "nota": 88.1},
    218553: {"nome": "ARTHUR KIRMSE ROCHA", "nota": 79.6},
    333496: {"nome": "ARTHUR NASCIMENTO CASTELLAR", "nota": 88.1},
    336221: {"nome": "BERNARDO SIMÕES SOUSA MOREIRA", "nota": 93.5},
    337757: {"nome": "BRAYAN LUCAS SIQUEIRA DOS SANTOS", "nota": 78.0},
    87311: {"nome": "BRENO RODRIGUES STOCO", "nota": 77.9},
    335248: {"nome": "DANIEL MARTINS DE ABREU", "nota": 87.9},
    328262: {"nome": "ENTHONY BIRCHLER MACHADO", "nota": 77.2},
    81803: {"nome": "FELLIPE BASTOS DE SOUSA", "nota": 94.0},
    335204: {"nome": "GABRIEL ARPINI DOS SANTOS", "nota": 90.9},
    330010: {"nome": "GUILHERME ABREU RIBEIRO", "nota": 87.9},
    327067: {"nome": "GUILHERME DE OLIVEIRA BARROS", "nota": 73.3},
    336222: {"nome": "HEITOR SCARPAT DE SÁ", "nota": 70.0},
    333451: {"nome": "JOÃO BERNARDO DE LEMOS BELCAVELLO", "nota": 79.5},
    331258: {"nome": "JOÃO PEDRO RIBEIRO COSTA", "nota": 83.9},
    336675: {"nome": "KAMILLY VITORIA DIAS DENIZ", "nota": 86.8},
    310439: {"nome": "LARA PEDROTI DE SALLES", "nota": 83.3},
    19828: {"nome": "LARA SANTOS PEREIRA", "nota": 83.2},
    336597: {"nome": "LEONARDO TAVARES RODRIGUES", "nota": 89.7},
    298641: {"nome": "LEVI BRANCAGLION TEODORO", "nota": 91.0},
    333490: {"nome": "LUCAS FRANK PEREIRA", "nota": 79.1},
    330427: {"nome": "LUCCA XAVIER GIURIZATO", "nota": 88.2},
    329587: {"nome": "LUIZ EDUARDO MONTEIRO AMORIM", "nota": 94.4},
    336606: {"nome": "LUIZ HENRIQUE LORENZONI BASTOS", "nota": 92.6},
    335169: {"nome": "MAITÊ MARTINS BRAGA", "nota": 83.1},
    21747: {"nome": "MANUELA FREGONASSI DE MATOS", "nota": 94.0},
    335053: {"nome": "MARIA EDUARDA SIMÕES LAIBER", "nota": 81.1},
    330240: {"nome": "MIGUEL BITTENCOURT PINHEIRO", "nota": 94.5},
    336028: {"nome": "PEDRO HENRIQUE ALVES DA COSTA", "nota": 91.8},
    257891: {"nome": "PEDRO LUCAS BENTO GAZIRE", "nota": 83.5},
    330653: {"nome": "RAFAEL PISSINATTI DOS SANTOS SOUSA", "nota": 90.8},
    330078: {"nome": "RAFFAEL BONADIMAN LOVATTI", "nota": 88.0},
    185064: {"nome": "RENAN BARBOSA DE SOUZA", "nota": 88.5}
}

st.title("🎓 Consulta de Notas")
st.subheader("Insira seu Registro Acadêmico (RA) para acessar o painel.")

# Campo tipo 'password' esconde os números digitados por privacidade
ra_input = st.text_input("Registro Acadêmico:", type="password", help="Digite apenas os números do seu RA")

if st.button("Consultar Nota"):
    if ra_input.strip():
        try:
            ra_digitado = int(ra_input)
            
            if ra_digitado in alunos:
                aluno = alunos[ra_digitado]
                st.success("✨ Acesso Autorizado!")
                
                # Exibe o resultado de forma elegante
                st.balloons() # Efeito visual de comemoração
                st.markdown(f"### 👤 **Aluno(a):** {aluno['nome']}")
                st.metric(label="Nota Final", value=f"{aluno['nota']} pts")
            else:
                st.error("❌ RA não encontrado. Verifique os dados e tente novamente.")
        except ValueError:
            st.warning("⚠️ Formato inválido. O Registro Acadêmico deve conter apenas números.")
    else:
        st.warning("⚠️ Por favor, preencha o campo do Registro Acadêmico.")