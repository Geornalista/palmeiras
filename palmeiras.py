import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.header(
    """
    **BUSCA ESCALAÇÃO DO PALMEIRAS NA HISTÓRIA**

    """
)

file = 'palmeiras1.csv'
df_jogos = pd.read_csv(file,sep=';',skipinitialspace=True)

df1 = df_jogos[['Data','Campeonato','Estadio','Mandante','Visitante','GOLS_H','GOLS_A','LINK']]
df1.index = df1.index.set_names(['Partida'])
df1.reset_index(inplace=True)

lista_datas = df1.set_index('Partida').T.to_dict('list')

# Criando o Dicionário com a Lista de Jogos
df2 = df_jogos.iloc[: , [7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]].copy()
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

def result(i):
  if lista_datas[i][5] > lista_datas[i][6]:
    res = 'casa'
    if lista_datas[i][3] == 'Palmeiras' or lista_datas[i][3] == 'Palestra Italia':
      palm = 'V'
    else:
      palm = 'D'
  elif lista_datas[i][6] > lista_datas[i][5]:
    res = 'fora'
    if lista_datas[i][4] == 'Palmeiras' or lista_datas[i][4] == 'Palestra Italia':
      palm = 'V'
    else:
      palm = 'D'
  else:
    res = 'empate'
    palm = 'E'
  if lista_datas[i][3] == 'Palmeiras' or lista_datas[i][3] == 'Palestra Italia':
    GM = lista_datas[i][5]
    GS = lista_datas[i][6]
  else:
    GM = lista_datas[i][6]
    GS = lista_datas[i][5]

  return res,palm,GM,GS

def busca_escalacao(jogadores):
  flag = 0
  jogos=[]
  camp=[]
  estad=[]
  res=[]
  palm=[]
  GM0 = 0
  GS0 = 0

  for i in range(njogos):
    if set(jogadores).issubset(lista_jogos[i]):
      flag=1
      res1,palm1,GM1,GS1 = result(i)
      res.append(res1)
      palm.append(palm1)
      camp.append(lista_datas[i][1])
      estad.append(lista_datas[i][2])
      jogos.append(i)

      GM0 = GM0 + GM1
      GS0 = GS0 + GS1

  if flag == 0:
    st.write('Nenhum jogo encontrado corresponde aos jogadores pesquisados')

  for item in jogos:
    jogo = [s.title() for s in list(lista_jogos[item]) if str(s) != 'nan']
    jogo = [x.replace('-', ' ') for x in jogo]
    st.subheader(f'Partida {item+1}: {lista_datas[item][0]} {lista_datas[item][3].title()} {lista_datas[item][5]} X {lista_datas[item][6]} {lista_datas[item][4].title()} ({lista_datas[item][1].title()} - Estádio: {lista_datas[item][2].title()}) ')

    for jogador in jogo:
      if jogador == jogo[0]:
        texto = jogador+' '
      else:
        texto = texto+', '+jogador
    st.write(texto)

  st.sidebar.write(f'Total de Partidas: {len(jogos)}')
  return(camp,estad,res,palm,GM0,GS0)

if st.sidebar.button('Procurar'):
  camp,estad,res,palm,GM,GS = busca_escalacao(escalacao)
  st.sidebar.write(f'Gols Marcados: {GM}')
  st.sidebar.write(f'Gols Sofridos: {GS}')
  st.sidebar.write(f'Palmeiras')
  st.sidebar.write(f"Vitórias: {palm.count('V')}")
  st.sidebar.write(f"Empates: {palm.count('E')}")
  st.sidebar.write(f"Derrotas: {palm.count('D')}")