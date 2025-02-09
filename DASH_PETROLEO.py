import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def gerar_df():
    url = "https://raw.githubusercontent.com/flavioalmeeida/FIAP-TechChallange-FASE4/3a488bc28d967d9c97cc47244fb39f63d38944ae/DADOS_PETROLEO.xlsx"
    df = pd.read_excel(
        io=url, 
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:Q",
        nrows=11345
    )
    return df

df = gerar_df()

# Título do Dashboard
st.title("Projeção do Valor do Barril de Petróleo")

# Seleção de intervalo de datas
data_selecionada = st.date_input(
    "Escolha o intervalo de datas para visualizar:",
    value=[df["data"].min(), df["data"].max()],
    min_value=df["data"].min(),
    max_value=df["data"].max()
)

# Garantir que o usuário selecionou as duas datas corretamente
if len(data_selecionada) == 2:
    data_inicial, data_final = pd.to_datetime(data_selecionada[0]), pd.to_datetime(data_selecionada[1])
    df_filtrado = df[(df["data"] >= data_inicial) & (df["data"] <= data_final)]
    
    # Mostrar um resumo do intervalo selecionado
    st.write(f"Exibindo dados de **{data_inicial.strftime('%d/%m/%Y')}** até **{data_final.strftime('%d/%m/%Y')}**.")
    
    # Gráfico de linha mostrando y e y_pred para o intervalo selecionado
    fig = px.line(df_filtrado, x="data", y=["y", "y_pred"], labels={"value": "Valor (US$)", "data": "Data"},
                  title="Projeção vs Valor Real do Barril de Petróleo (Acumulado no Intervalo)")
    st.plotly_chart(fig)
    
    # Mostrar valor projetado mais recente dentro do intervalo
    if not df_filtrado.empty:
        valor_pred_mais_recente = df_filtrado["y_pred"].iloc[-1]
        st.metric(label=f"Última projeção no intervalo selecionado ({data_final.strftime('%d/%m/%Y')})", 
                  value=f"{valor_pred_mais_recente:.2f} US$")
else:
    # Gráfico padrão com todos os dados antes de selecionar o intervalo completo
    st.write("Selecione um intervalo completo para visualizar os dados filtrados.")
    fig = px.line(df, x="data", y=["y", "y_pred"], labels={"value": "Valor (US$)", "data": "Data"},
                  title="Projeção Completa do Valor do Barril de Petróleo")
    st.plotly_chart(fig)
