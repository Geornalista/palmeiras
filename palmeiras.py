import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.header(
    """
    **BUSCA ESCALAÇÃO DO PALMEIRAS NA HISTÓRIA**

    """
)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://sep-bucket-prod.s3.amazonaws.com/wp-content/uploads/2019/08/9219-wallpaper-historico_op11-2-768x432.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

file = 'palmeiras.csv'
df_jogos = pd.read_csv(file,sep=';',skipinitialspace=True)

df1 = df_jogos[['Data','Mandante','Visitante','Campeonato','LINK']]
df1.index = df1.index.set_names(['Partida'])
df1.reset_index(inplace=True)

lista_datas = df1.set_index('Partida').T.to_dict('list')

# Criando o Dicionário com a Lista de Jogos
df2 = df_jogos.iloc[: , [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]].copy()
df2.index = df2.index.set_names(['Partida'])
df2.reset_index(inplace=True)

lista_jogos = df2.set_index('Partida').T.to_dict('list')

njogos = len(lista_jogos)

jogadores=[]
for i in range(len(lista_jogos)):
  for jogador in lista_jogos[i]:
    jogadores.append(jogador)
df = pd.DataFrame (jogadores, columns = ['JOGADORES'])
df = df[df['JOGADORES'].notna()]
lista_jogadores = df['JOGADORES'].drop_duplicates().sort_values().tolist()

st.sidebar.header('Escolha os jogadores')
escalacao = st.sidebar.multiselect('Escolha os jogadores que deseja pesquisar',lista_jogadores)

def busca_escalacao(jogadores):
  flag = 0
  jogos=[]
  for i in range(njogos):
    if set(jogadores).issubset(lista_jogos[i]):
      flag=1
      jogos.append(i)
  if flag == 0:
    st.write('Nenhum jogo encontrado corresponde aos jogadores pesquisados')

  for item in jogos:
    jogo = [s.title() for s in list(lista_jogos[item]) if str(s) != 'nan']
    jogo = [x.replace('-', ' ') for x in jogo]
    st.subheader(f'[Partida {item+1}: {lista_datas[item][0]} {lista_datas[item][1].title()} X {lista_datas[item][2].title()} ({lista_datas[item][3].title()})]({lista_datas[item][-1]}) ')
    #st.caption(f'{lista_datas[item][-1]}')
    
    for jogador in jogo:
      if jogador == jogo[0]:
        texto = jogador+' '
      else:
        texto = texto+', '+jogador
    st.write(texto)

  st.sidebar.write(f'Total de Partidas: {len(jogos)}')

if st.sidebar.button('Procurar'):
  busca_escalacao(escalacao)
