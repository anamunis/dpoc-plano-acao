import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="DPOC – Plano de Ação", layout="centered")

st.title("DPOC — Autoavaliação & Plano de Ação")
st.write("Preencha seu nome, marque seus sintomas e gere um plano de ação em PDF.")


# --- NOME DO USUÁRIO ---
name = st.text_input("Nome completo")


# --- CHECKLIST DE SINTOMAS ---
st.header("Auto-check: sinais de piora")
st.write("Marque o que está sentindo:")

symp = {
    "Aumento da falta de ar": st.checkbox("Aumento da falta de ar"),
    "Mais tosse": st.checkbox("Mais tosse"),
    "Alteração do escarro": st.checkbox("Alteração do escarro (cor ou quantidade)"),
    "Febre": st.checkbox("Febre"),
    "Confusão": st.checkbox("Confusão / sonolência incomum")
}

score_symp = sum(symp.values())

if score_symp == 0:
    status = "estável"
elif score_symp <= 2:
    status = "leve"
else:
    status = "grave"


# --- GERADOR DO PLANO ---
def gerar_plano(status):
    if status == "estável":
        return """
Plano para Situacao Estavel
- Mantenha suas medicacoes usuais.
- Continue exercicios respiratorios e caminhada leve.
- Beba agua ao longo do dia.
- Evite exposicao a fumaca, poeira e clima frio.
- Faca o CAT semanalmente para monitorar.
"""

    if status == "leve":
        return """
Exacerbacao Leve - O que fazer agora
- Use seu broncodilatador de resgate conforme prescricao.
- Aumente hidratacao.
- Descanse e evite esforco.
- Avalie melhora em 24-48h.

Quando procurar atendimento
- Se os sintomas nao melhorarem apos 48h.
- Se a falta de ar aumentar mesmo usando a medicacao de resgate.

Cuidados importantes
- Evite locais com muita poeira ou fumaca.
- Mantenha o uso regular das medicacoes de manutencao.
"""

    if status == "grave":
        return """
ATENCAO: SINAIS DE ALERTA - Procure ajuda IMEDIATA
- Falta de ar intensa.
- Confusao, sonolencia excessiva ou febre.
- Aumento acentuado da tosse e do escarro com mudanca de cor.

O que fazer ate chegar ao atendimento:
- Use seu broncodilatador de resgate.
- Sente-se em posicao confortavel, inclinando o tronco para frente.
- Tente respirar com labios semicerrados.
- Evite caminhar ou falar muito.
- Peca ajuda de alguem proximo.

Contatos importantes:
- Unidade de saude mais proxima.
- SAMU: 192.
"""


# --- GERADOR DE PDF (CORRIGIDO) ---
def gerar_pdf(nome, plano_texto):
    pdf = FPDF()
    pdf.add_page()

    largura = pdf.w - 2 * pdf.l_margin

    pdf.set_font("helvetica", size=14)
    pdf.multi_cell(largura, 10, "Plano de Acao - DPOC\n")

    pdf.set_font("helvetica", size=12)
    pdf.multi_cell(largura, 8, f"Nome: {nome}")
    pdf.multi_cell(largura, 8, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")

    pdf.set_font("helvetica", size=11)
    pdf.multi_cell(largura, 6, plano_texto)

    # O FPDF retorna string → convertendo para bytes com encoding latin-1
    pdf_str = pdf.output(dest="S")
    return pdf_str.encode("latin-1")


# --- ESTILO DO BOTÃO ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #d00000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 50px;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)


# --- BOTÃO PARA GERAR PDF ---
gerar = st.button("Gerar Plano de Ação")

if gerar:
    if not name:
        st.error("Por favor, preencha o nome antes de gerar o PDF.")
    else:
        plano_texto = gerar_plano(status)
        pdf_bytes = gerar_pdf(name, plano_texto)  # já é bytes!

        st.success("Plano de ação gerado!")

        st.download_button(
            label="📄 Baixar PDF",
            data=pdf_bytes,
            file_name=f"plano_dpoc_{name}.pdf",
            mime="application/pdf"
        )


# --- TEXTO FIXO ---
st.markdown("""
Para mais informações sobre exacerbação na DPOC, acesse:  
[https://www.instagram.com/estagiariosunicep?igsh=MmwwOXd6OXFpMXA3](https://www.instagram.com/estagiariosunicep?igsh=MmwwOXd6OXFpMXA3)
""")


# --- Rodapé ---
st.markdown("---")
st.caption("Protótipo comunitário baseado em recomendações GOLD 2024.")
