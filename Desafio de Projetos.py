#!/usr/bin/env python
# coding: utf-8

# # Projeto Covid-19
# ## Digital Innovation One 
# 
# 

# In[2]:


# importando as bibliotecas 
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# In[3]:


# importar os dados do projeto 
url = 'https://raw.githubusercontent.com/neylsoncrepalde/projeto_eda_covid/master/covid_19_data.csv'


# In[8]:


# o arquivo vai ser lido como datas e não como textos
df = pd.read_csv(url, parse_dates = ['ObservationDate', 'Last Update'])
df


# In[9]:


#Conferir os tipos de cada coluna 
df.dtypes


# Nomes de colunas não devem ter letras maiúsculas e nem caracteres especiais. Vamos implementar uma função para fazer a limpeza dos nomes das colunas 

# In[10]:


#importar a biblioteca re e fazer a função para corrigir 
import re
def corrige_colunas(col_name):
    return re.sub(r"[/| ]", "", col_name).lower() 


# In[11]:


#vamos corrigir todas as colunas do df
df.columns = [corrige_colunas(col) for col in df.columns]


# In[12]:


df


# # Brasil 
#  vamos selecionar apenas os dados do Brasil para investigar

# In[13]:


# .loc para identificar apenas daados específicos
df.countryregion.unique()


# In[14]:


df.loc[df.countryregion == "Brazil"]


# In[15]:


brasil = df.loc[
    (df.countryregion == "Brazil") & (df.confirmed > 0)
]


# In[42]:


brasil


# # Casos Confirmados 

# In[16]:


#Gráfico da evolução de casos confirmados 
px.line(brasil, "observationdate", "confirmed", title = "casos confirmados no Brasil")


# # Novos casos por dia 

# In[17]:


#Técnica de programação funcional
brasil["novos_casos"] = list(map(
    lambda x: 0 if (x==0) else brasil["confirmed"].iloc[x] - brasil["confirmed"].iloc[x-1], np.arange(brasil.shape[0]) 
))


# In[47]:


brasil


# In[19]:


#visualizando 
px.line(brasil, x = "observationdate", y = "novos_casos", title = "Novos Csos por dia")


# # Mortes

# In[20]:


fig = go.Figure()
fig.add_trace(
    go.Scatter(x = brasil.observationdate, y=brasil.deaths, name = "Mortes", mode = "lines+markers",
              line = {'color': 'red'})
)
#Layout
fig.update_layout(title='MORTES POR COVID 19')
fig.show()


# # Taxa de Crescimento
# taxa_crescimento =(presente/passado)**(1/n) - 1

# In[27]:


def taxa_crescimento(data, variable, data_inicio =None, data_fim=None):
    #se data inicio for None, define como a primeira dataq disponivel 
    if data_inicio == None:
        data_inicio = data.observationdate.loc[data[variable] > 0].min()
    else:
        data_inicio = pd.to_datetime(data_inicio)
    if data_fim == None:
        data_fim = data.observationdate.iloc[-1]
    else:
        data_fim = pd.to_datetime(data_fim)
    
    #define os valores do presente e passado 
    passado = data.loc[data.observationdate == data_inicio, variable].values[0]
    presente = data.loc[data.observationdate == data_fim, variable].values[0]
    
    #Define o numero de pontos no tempo que vamos avaliar
    n = (data_fim - data_inicio).days
    
    # Calcular a taxa
    taxa = (presente/passado)**(1/n) - 1
    return taxa*100


# In[28]:


# Taxa de crescimento médio do COVID no Brasil em tdo período
taxa_crescimento(brasil, "confirmed")


# In[32]:


def taxa_crescimento_diaria(data, variable, data_inicio=None):
    if data_inicio == None:
        data_inicio = data.observationdate.loc[data[variable] > 0].min()
    else:
        data_inicio = pd.to_datetime(data_inicio)
    data_fim = data.observationdate.max()
    # Define onúmero de pontos no tempo que vamos avaliar 
    n = (data_fim -data_inicio).days
    
    # Taxa calaculada de um dia para outro 
    taxas = list(map(
        lambda x: (data[variable].iloc[x] - data[variable].iloc[x-1]) / data[variable].iloc[x-1], 
        range (1,n+1)
    ))
    return np.array(taxas) *100


# In[34]:


tx_dia = taxa_crescimento_diaria(brasil, "confirmed")


# In[35]:


tx_dia


# In[37]:


primeiro_dia = brasil.observationdate.loc[brasil.confirmed > 0].min()
px.line(x=pd.date_range(primeiro_dia, brasil.observationdate.max())[1:],
       y=tx_dia, title="taxa de crescimento de casos confirmados no Brasil")


# # Predições 

# In[38]:


#importa bibliotecas 

from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt 


# In[40]:


#fazer com casos confirmados
confirmados = brasil.confirmed
confirmados.index = brasil.observationdate
confirmados 


# In[41]:


#decompor para saber a sazionalidade 
res = seasonal_decompose(confirmados)


# In[42]:


#plotar os gráficos 
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10,8))

ax1.plot(res.observed)
ax2.plot(res.trend)
ax3.plot(res.seasonal)
ax4.plot(confirmados.index, res.resid)
ax4.axhline(0, linestyle="dashed", c="black")
plt.show


# # Modelar os dados
# ## modelo ARIMA

# In[43]:


get_ipython().system('pip install pmdarima')


# In[44]:


from pmdarima.arima import auto_arima
modelo = auto_arima(confirmados)


# In[46]:


fig = go.Figure(go.Scatter(
    x = confirmados.index, y=confirmados, name="Observados"
))

fig.add_trace(go.Scatter(
    x=confirmados.index, y=modelo.predict_in_sample(), name="Preditos"
))

fig.add_trace(go.Scatter(
    x=pd.date_range("2020-05-20", "2020-06-20"), y=modelo.predict(31), name="Forecast"
))

fig.update_layout(title="Previsão de casos confirmados no Brasil nos próximos dias")
fig.show()


# # Modelo de Crescimento
# vamos usar a biblioteca fbprophet

# In[ ]:


get_ipython().system('conda install -c conda-forge fbprophet -y ')


# In[ ]:


from fbprophet import Prophet


# In[ ]:


# Preprocessamentos 
train = confirmados.reset_index()[:-5]
test = confirmados.reste_index()[-5:]

#Renomeando Colunas 
train.rename(columns={"observationdate":"ds", "confirmed": "y"}, inplace=True)
test.rename(columns={"observationdate":"ds", "confirmed": "y"}, inplace=True)

#Definir o modelo de crescimento 
profeta = Prophet(growth="logistic", changepoints=["2020-03-21", "2020-03-30", "2020-04-25",
                                                  "2020-05-03", "2020-05-10"])
pop = 211463256
train["cap"] = pop

#treina o modelo
profeta.fit(train)

#Construir previsões 

future_dates = profeta.make_future_dataframe(periods=200)
future_dates["cap"] = pop
forescast = profeta.predict(future_dates)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




