import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

#dados
duckdb_con = duckdb.connect('dw.duckdb', read_only=True)
conta_clientes_df = duckdb_con.execute("SELECT * FROM conta_clientes").fetchdf()
duckdb_con.close()

st.title("Análise de Contagem de Clientes por País")

st.sidebar.header('Configurações do Filtro')
paises_selecionados = st.sidebar.multiselect(
    'Selecione os Países',
    options=conta_clientes_df['Country'].unique(),
    default=conta_clientes_df['Country'].unique()
)

st.sidebar.info("Use os filtros acima para ajustar os dados e a visualização.")

dados_filtrados = conta_clientes_df[conta_clientes_df['Country'].isin(paises_selecionados)]
dados_filtrados = dados_filtrados.sort_values('CustomerCount', ascending=False)

tab1, tab2 = st.tabs(["Dados", "Gráfico"])

with tab1:
    st.write(dados_filtrados)

if not dados_filtrados.empty:
    with tab2:
        fig = px.bar(
            dados_filtrados,
            x='CustomerCount',
            y='Country',
            orientation='h',
            title='Contagem de Clientes por País',
            labels={'CustomerCount': 'Número de Clientes', 'Country': 'País'}
        )
        st.plotly_chart(fig)
else:
    with tab2:
        st.write("Nenhum dado disponível para os países selecionados.")


