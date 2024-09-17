#Link para acesso do dataset: https://www.data.rio/documents/41e3de8e032d43019d6b00b7a0618b68/about

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import xlrd
import time

#Criando as funções
def botao(conteudo: str, acao):
    "Cria botao simples"
    if st.button(conteudo):
        acao

def big_numbers(value:float, metric:str) -> None:
    """
    Criar big numbers (métricas) no dashboard
    Args:
    value(float) = valor que será plotado
    metric(str) = descrição da métrica
    """
    st.metric(label = metric, value = value)

def radio_box(conteudo:str, opcoes):
    'Cria uma lista de opções para serem marcadas'
    st.radio(conteudo,opcoes)

def dashboard():
    st.title('Análise da evolução de ocupação dos hotéis no Rio de Janeiro')
    
    background_color = st.selectbox("Escolha uma cor de fundo", ["Light", "Blue"])
    
    colormap = {
        "Light": "#fafafa",
        "Blue": "#d6e3e9"
    }
    
    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colormap[background_color]};
    }}
    </style>
    """, unsafe_allow_html=True)

    xls_file = st.file_uploader("Upload a .xls file", type=["xls"])

    if xls_file is not None:

        df = pd.read_excel(xls_file, engine='xlrd', header = 6).dropna().drop(columns = ['Unnamed: 1'])

        st.write(df)

        df = df.rename(
            columns={
                'Unnamed: 0':'Ano'
            }
            )

        df = pd.melt(df, id_vars=["Ano"], var_name="Mes", value_name="ocupacao")

        mes_map = {
            'Janeiro': '01', 'Fevereiro': '02', 'Março': '03', 'Abril': '04',
            'Maio': '05', 'Junho': '06', 'Julho': '07', 'Agosto': '08',
            'Setembro': '09', 'Outubro': '10', 'Novembro': '11', 'Dezembro': '12'
        }

        df['Mes_Num'] = df['Mes'].map(mes_map)

        df['Data'] = df['Ano'].astype(str) + '-' + df['Mes_Num'] + '-01'

        df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d')

        df = df[df['Ano'] >= 2016].reset_index()

        df.drop(columns=['index'],inplace=True)

        anos = pd.Series(df['Ano'].unique())
        selected_boxes = st.multiselect("Selecione colunas do dataset para exibir uma tabela com essas colunas", df.columns)
        st.write(df[selected_boxes])

        ano_selecionado = st.radio(
                'Selecione um dos anos abaixo para filtrar esse dataset',
                anos.unique()
                )

        df_filtered = df[df['Ano'] == ano_selecionado]

        if st.checkbox('Mostrar Dataframe'):
            st.write(df_filtered)

        if st.checkbox('Deseja efetuar o download desses dados?'):
            progress_bar = st.progress(0)
            for counter in range (1,101):
                time.sleep(0.015)
                progress_bar.progress(counter)
            with st.spinner('Carregando arquivo...'):
                time.sleep(3)

        st.download_button(label = 'Clique aqui para baixar o arquivo filtrado ▶',
                        data = df_filtered.to_csv(index=False),
                        file_name= f'dados_{ano_selecionado}.csv')

        if st.button('Mostrar Dashboard com os dados filtrados ▶'):

            st.metric('Máximo de ocupacao',value=df_filtered['ocupacao'].max())
            st.metric('Média de ocupacao',value=df_filtered['ocupacao'].mean())
            st.metric('Mínimo de ocupacao',value=df_filtered['ocupacao'].min())

            st.bar_chart(df_filtered,x='Data',y='ocupacao')

            st.scatter_chart(df_filtered,x = 'Mes_Num',y = 'ocupacao')

if __name__ == "__main__":
    dashboard()