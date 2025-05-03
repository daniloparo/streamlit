import streamlit as st
import yfinance as yf
from datetime import date
import pandas as pd

from plotly import  graph_objects as go


v_data_inicio = '2025-01-01'
v_data_fim =  date.today().strftime('%Y-%m-%d')


st.title('Análise de Ações')

#criando a sidebar
st.sidebar.header ('Escolha a ação')

n_dias = st.slider ('quantidade de dias de previsão',30, 365)

def get_dados_acoes():
    path = r'C:\Users\danil\OneDrive\Área de Trabalho\streamlit\streamlit\acoes.csv'
    return pd.read_csv(path, delimiter=';')

df = get_dados_acoes()

acao = df['snome']
nome_acao_escolhida = st.sidebar.selectbox('Escolha uma ação:',acao)

def_acao = df[df['snome'] == nome_acao_escolhida]
acao_escolhida = def_acao.iloc[0]['sigla_acao'] 
acao_escolhida = acao_escolhida + '.SA'

@st.cache_data

def get_valores_olines(sigla_acao):
    df = yf.download(sigla_acao, v_data_inicio, v_data_fim)
    df.reset_index(inplace=True)
    return df

df_valores = get_valores_olines(acao_escolhida)
#Criar tabela com os dados
st.subheader(f'Tabela de valores - ' + nome_acao_escolhida)
st.dataframe(df_valores.tail(10))


#Criar gráfico com os dados
st.subheader(f'Gráfico de preços - ' + nome_acao_escolhida)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Close'], name='Fechamento', line_color='yellow'))
fig.add_trace(go.Scatter(x=df_valores['Date'], y=df_valores['Open'], name='Abertura', line_color='blue'))
st.plotly_chart(fig)