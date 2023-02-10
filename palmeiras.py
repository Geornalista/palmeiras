import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode,ColumnsAutoSizeMode

st.set_page_config(
  page_title='ESCALAÇÕES DO PALMEIRAS',
  page_icon='⚽',
  layout="wide")

st.sidebar.header(
    """
    **BUSCA ESCALAÇÃO DO PALMEIRAS NA HISTÓRIA**

    """
)
tab1,tab2,tab3,tab4,tab5 = st.tabs([
                  "📊 Dados Gerais",
                  "🥊 Adversários",
                  "🏟 Estádios",
                  "🥅 Campeonatos",
                  "⚽️ Escalações"])

file = 'palmeiras.csv'
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
    adv = lista_datas[i][4]
  else:
    GM = lista_datas[i][6]
    GS = lista_datas[i][5]
    adv = lista_datas[i][3]

  return res,adv,palm,GM,GS

def busca_escalacao(jogadores):
  flag = 0
  jogos=[]
  camp=[]
  estad=[]
  res=[]
  adv=[]
  palm=[]
  GM0 = 0
  GS0 = 0

  for i in range(njogos):
    if set(jogadores).issubset(lista_jogos[i]):
      flag=1
      res1,adv1,palm1,GM1,GS1 = result(i)
      res.append(res1)
      adv.append(adv1)
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
    with tab5:
      st.subheader(f'[Partida {item+1}: {lista_datas[item][0]} {lista_datas[item][3].title()} {lista_datas[item][5]} X {lista_datas[item][6]} {lista_datas[item][4].title()} ({lista_datas[item][1].title()} - Estádio: {lista_datas[item][2].title()})]({lista_datas[item][-1]}) ')

    for jogador in jogo:
      if jogador == jogo[0]:
        texto = jogador+' '
      else:
        texto = texto+', '+jogador
    with tab5:
      st.write(texto)

  return(camp,estad,res,adv,palm,GM0,GS0)

if st.sidebar.button('Procurar'):
  camp,estad,res,adv,palm,GM,GS = busca_escalacao(escalacao)
  with tab1:
    st.subheader(f'🇳🇬 Palmeiras')

    d = {'COL1': ['Total de Partidas','Vitórias','Empates','Derrotas', 'Total de Gols Marcados','Total de Gols Sofridos' ],
          'COL2': [len(camp),palm.count('V'),palm.count('E'),palm.count('D'),GM,GS ]}
    df = pd.DataFrame(data=d)

    builder = GridOptionsBuilder.from_dataframe(df)
    builder.configure_default_column(min_column_width=5,filterable=False,editable=False,sortable=False,resizable=False,suppressMenu=True)
    builder.configure_column("COL1", header_name="DADOS GERAIS", editable=False)
    builder.configure_column("COL2", header_name="", editable=False)

    go = builder.build()

    grid_response = AgGrid(df,gridOptions = go,
    fit_columns_on_grid_load=True,
    theme="alpine",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True)

  with tab2:
    #st.subheader(f'🥊 Adversários')
    advs = [[x,adv.count(x)] for x in set(adv)]
    t1 = []
    t2 = []
    for i in range(len(advs)):
      t1.append(advs[i][0])
      t2.append(advs[i][1])

    d0 = {'COL1': t1,
          'COL2': t2}
    df0 = pd.DataFrame(data=d0)
    df0 = df0.sort_values(df0.columns[1],ascending=False)

    builder = GridOptionsBuilder.from_dataframe(df0)
    builder.configure_default_column(min_column_width=5,filterable=False,editable=False,sortable=False,resizable=False,suppressMenu=True)
    builder.configure_column("COL1", header_name="DADOS GERAIS", editable=False)
    builder.configure_column("COL2", header_name="", editable=False)

    go0 = builder.build()

    grid_response = AgGrid(df0,gridOptions = go0,
    fit_columns_on_grid_load=True,
    theme="alpine",
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
    allow_unsafe_jscode=True)

    with tab3:
      #st.subheader(f'🏟 Estádios')
      campos = [[x,estad.count(x)] for x in set(estad)]
      tt1=[]
      tt2=[]
      for i in range(len(campos)):
        tt1.append(campos[i][0])
        tt2.append(campos[i][1])

      dd = {'COL1': tt1,
           'COL2': tt2}
      
      df1 = pd.DataFrame(data=dd)
      df1 = df1.sort_values(df1.columns[1],ascending=False)      

      builder = GridOptionsBuilder.from_dataframe(df1)
      builder.configure_default_column(min_column_width=5,filterable=False,editable=False,sortable=False,resizable=False,suppressMenu=True)
      builder.configure_column("COL1", header_name="DADOS GERAIS", editable=False)
      builder.configure_column("COL2", header_name="", editable=False)

      go1 = builder.build()

      grid_response = AgGrid(df1,gridOptions = go1,
      fit_columns_on_grid_load=True,
      theme="alpine",
      columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
      allow_unsafe_jscode=True)

    with tab4:
      #st.subheader(f'🥅 Campeonatos')
      champs = [[x,camp.count(x)] for x in set(camp)]

      tc1=[]
      tc2=[]
      for i in range(len(champs)):
        tc1.append(champs[i][0])
        tc2.append(champs[i][1])

      dc = {'COL1': tc1,
           'COL2': tc2}
      
      df2 = pd.DataFrame(data=dc)
      df2 = df2.sort_values(df2.columns[1],ascending=False)

      builder = GridOptionsBuilder.from_dataframe(df2)
      builder.configure_default_column(min_column_width=5,filterable=False,editable=False,sortable=False,resizable=False,suppressMenu=True)
      builder.configure_column("COL1", header_name="DADOS GERAIS", editable=False)
      builder.configure_column("COL2", header_name="", editable=False)

      go2 = builder.build()

      grid_response = AgGrid(df2,gridOptions = go2,
      fit_columns_on_grid_load=True,
      theme="alpine",
      columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
      allow_unsafe_jscode=True)
    
