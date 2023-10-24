import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import calendar

# Carregue a base de dados
data = pd.read_csv('dados/Arquivo_NetFlix.csv')

# Calcule a contagem de filmes e programas de TV
total_filmes = data[data['type'] == 'Movie'].shape[0]
total_tv_shows = data[data['type'] == 'TV Show'].shape[0]

# Crie uma lista de dados
dados = [total_filmes, total_tv_shows]
rotulos = ['Filmes', 'Programas de TV']

# Adicione o total de filmes e programas de TV ao lado dos rótulos
rotulos_formatados = [f'{rotulo} ({dados[i]})' for i, rotulo in enumerate(rotulos)]

# Crie um gráfico de pizza com estilo personalizado
fig, ax = plt.subplots()
ax.pie(
    dados,
    labels=rotulos_formatados,
    autopct='%1.1f%%',
    startangle=90,
    colors=['#FF9999', '#66B3FF'],
    wedgeprops={'edgecolor': 'black', 'linewidth': 1.2}
)
ax.axis('equal')  # Garanta que o gráfico seja uma pizza perfeita

# Configure o estilo do título
st.markdown("<h1 style='text-align: center; color: #333;'>Proporção de Filmes e Programas de TV na Netflix</h1>", unsafe_allow_html=True)

# Adicione o gráfico ao Streamlit
st.pyplot(fig)

# Encontrar os 10 principais países que mais produzem conteúdo
top_countries = data['country'].value_counts().head(10)

# Crie um gráfico de barras
fig, ax = plt.subplots()
ax.barh(top_countries.index, top_countries.values, color='skyblue')
ax.set_xlabel('Número de Títulos')
ax.set_ylabel('Países')
ax.set_title('Top 10 Países que Mais Produzem Conteúdo na Netflix')

# Mostrar os números no gráfico
for i, value in enumerate(top_countries.values):
    ax.text(value, i, str(value), va='center', fontsize=10)

# Adicione um espaço
st.write(" ")

# Configure o estilo do título
st.markdown("<h2 style='text-align: center; color: #333;'>Top 10 Países que Mais Produzem Conteúdo na Netflix</h2>", unsafe_allow_html=True)

# Adicione o gráfico ao Streamlit
st.pyplot(fig)
