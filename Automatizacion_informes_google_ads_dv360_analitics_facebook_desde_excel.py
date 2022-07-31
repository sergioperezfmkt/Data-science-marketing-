# -*- coding: utf-8 -*-
"""Automatizacion_informes_google_ads_dv360_analitics_facebook_desde_excel

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Oa0l-i7d5QDOHJ-Hf7-KCOhujYX8_fuq

Este notebook te valdra como referencia de como automatizar un informe para  que aune los datos de Google analitics ,Google dv360 ,Google ads , Facebook ads y imprimierloS en un excel.

#Instrucciones
"""

#360 en excel el resto csv
#mismos idiomas siempre 
#nombre archivos facebook.csv  dv360 , ads_dis, ads_sem , g_analytics

"""#Instalaciones """

from pandas import DataFrame
import numpy as np
import seaborn as sns
import pandas as pd
import re
from numpy.ma.core import shape
from sklearn.preprocessing import StandardScaler ,scale
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt 
import matplotlib.pyplot as plt
import numpy as np
import openpyxl 
from openpyxl.chart import BarChart,Reference 
from openpyxl import load_workbook

pd.options.display.max_columns = 40
pd.options.display.max_rows = 40

"""#Google analitics """

df_google_analitics = pd.read_csv("/content/g_analytics.csv",encoding='utf-8', sep='delimiter', header=None)

df_google_analitics = df_google_analitics.drop(labels=[0,1,2,3,4,5,6], axis=0)

df_google_analitics=df_google_analitics.rename(columns={0:"p"})
#dividimos columnas
split_data_analitics = df_google_analitics["p"].str.split(",")
data_analitics = split_data_analitics.to_list()
names_analitics = ["Fecha","Canales","Campanha","Fuente","Medio","Sesiones_google_anali_m"]
df_google_analitics = pd.DataFrame(data_analitics, columns=names_analitics)

df_google_analitics = df_google_analitics.assign(Sesiones_google_anali = lambda dataset : dataset.Sesiones_google_anali_m.str.replace(".",""))
df_google_analitics=df_google_analitics.drop(columns=["Sesiones_google_anali_m"])

#casteamos 
df_google_analitics['Sesiones_google_anali'] = df_google_analitics['Sesiones_google_anali'].astype(int)

#funcion poner guiones en fecha 
def fecha_guion(fechaaaa):
  anho=fechaaaa[:4]
  lo_otro=fechaaaa[4:]
  salida =anho+"-"+lo_otro
  return salida
df_google_analitics=df_google_analitics.assign(F = lambda dataset: dataset.Fecha.apply( lambda linea : fecha_guion(linea)))

#funcion 2 poner guiones en fecha 
def fecha_guion_2(fechaaaa):
  dia=fechaaaa[-2:]
  lo_otro=fechaaaa[:7]
  salida =lo_otro+"-"+dia
  return salida
df_google_analitics=df_google_analitics.assign(Day = lambda dataset: dataset.F.apply( lambda linea : fecha_guion_2(linea)))

#separamos por canal
print("df_google_analitics_sin_filtro",df_google_analitics.shape)
print("suma_df_google_analitics_sin_filtro",df_google_analitics["Sesiones_google_anali"].sum())

##############################################Facebook_trafico

df_google_analitics_facebook_traffic=df_google_analitics[df_google_analitics['Canales'] =="Paid Social"]
df_google_analitics_facebook_traffic=df_google_analitics_facebook_traffic[df_google_analitics_facebook_traffic['Campanha'] =="DietsSpain-0122"]
df_google_analitics_facebook_traffic=df_google_analitics_facebook_traffic.groupby(by=["Day"]).sum()

print("Facebook_trafico_filtro",df_google_analitics_facebook_traffic.shape)
#video = OLV, social=fb traffic, filtrando por nombre de campaña

#########################################################Dv360

df_google_analitics_dv_360=df_google_analitics[ df_google_analitics['Canales'] =="Video"]
df_google_analitics_dv_360=df_google_analitics_dv_360[df_google_analitics_dv_360['Campanha'] =="dietsspain-0122"]
df_google_analitics_dv_360=df_google_analitics_dv_360.groupby(by=["Day"]).sum()

print("Dv360",df_google_analitics_dv_360.shape)
#video = OLV, social=fb traffic, filtrando por nombre de campaña

##########################################################Google ads sem

df_google_analitics_sem=df_google_analitics[df_google_analitics['Canales'] =="Paid Search"]
df_google_analitics_sem=df_google_analitics_sem.groupby(by=["Day"]).sum()

print("Google ads sem",df_google_analitics_sem.shape)
#paid search = SEM, se cogen todas las lineas sin filtrar

########################################################Google ads display

df_google_analitics_display=df_google_analitics[df_google_analitics['Canales'] =="Display"]
df_google_analitics_display=df_google_analitics_display.groupby(by=["Day"]).sum()

print("Google ads display",df_google_analitics_display.shape)
#Display=GDN, se cogen todas las lineas sin filtra
print(df_google_analitics["Campanha"].unique())

"""#Facebook_video"""

#abrimos los excel  (facebook)

df_facebook_video=pd.read_csv("/content/facebook.csv", ",")
df_facebook_video.head(1)

df_facebook_video=df_facebook_video.rename(columns={"Campaign name":"Campaign_name","Ad set name":"Ad_set_name","Ad name":"Ad_name","Result Type":"Result_Type","Amount spent (EUR)":"Amount_spent_EUR","Link clicks":"Link_clicks","Video plays at 100%":"Video_plays_at_100","Reporting starts":"Reporting_starts","Reporting ends":"Reporting_ends"})

df_facebook_video[["Campanha_nombre_parte_1","Campanha_nombre_parte_2","Campanha_nombre_parte_3"]]=df_facebook_video['Campaign_name'].str.split('|', expand=True)
#views=Video_plays_at_100 en facefoob esto es views

df_facebook_video=df_facebook_video.rename(columns={"Link_clicks": "Clics", "Amount_spent_EUR":"Coste","Video_plays_at_100": "views"})
#casteamos 

df_facebook_video['Impressions'] = df_facebook_video['Impressions'].astype(int)

df_facebook_video['Coste'] = df_facebook_video['Coste'].astype(float)
"""
#nulos por 0

df_facebook_video['Video_plays_at_100'].replace('', 0, inplace=True)
df_facebook_video['Video_plays_at_100'] = df_facebook_video['Video_plays_at_100'].fillna(0)

df_facebook_video['Video_plays_at_100'] = df_facebook_video['Video_plays_at_100'].astype(int)

#nulos por 0

df_facebook_video['Clics'].replace('', 0, inplace=True)
df_facebook_video['Clics'] = df_facebook_video['Clics'].fillna(0)

df_facebook_video['Clics'] = df_facebook_video['Clics'].astype(int)
"""

#como no nos interesa  Reach  Frequency los quitamos	
df_facebook_video=df_facebook_video.drop(columns=["Results","Reach","Frequency","Campaign_name","Ad_set_name","Ad_name","Reporting_starts","Reporting_ends","Result_Type"])
df_facebook_video

#fecha mes solo
df_facebook_video=df_facebook_video.rename(columns={"Day":"Day_m"})
df_facebook_video=df_facebook_video.assign(Day = lambda dataset: dataset.Day_m.map(lambda value : (value[:-3])))
df_facebook_video=df_facebook_video.drop(columns =["Day_m"])

#quitar impresion menor a 1 
df_facebook_video=df_facebook_video[df_facebook_video['Impressions'] > 0]

df_facebook_video=df_facebook_video.drop(columns=["Campanha_nombre_parte_1","Campanha_nombre_parte_2","Campanha_nombre_parte_3"])
#query
df_facebook_video=df_facebook_video[df_facebook_video['Objective'] =="VIDEO_VIEWS"]
df_facebook_video.head(2)

#agrupamos por dia
df_facebook_video=df_facebook_video.groupby(by=["Day"]).sum()

#creamos cpc
cpc_list_f_v=[]
for cost_f_v, cli_f_v in zip(df_facebook_video['Coste'], df_facebook_video['Clics']):
  if cli_f_v==0:
    cost_f_v=0
    cli_f_v=1
  resul_f_v=cost_f_v / cli_f_v 
  cpc_list_f_v.append(resul_f_v)
df_facebook_video['CPC']=cpc_list_f_v

#creamos ctr
ctr_list_f_v=[]
for impr_ctr_f_v, cli_ctr_f_v in zip(df_facebook_video['Impressions'], df_facebook_video['Clics']):
  if impr_ctr_f_v==0:
    impr_ctr_f_v=1
    cli_ctr_f_v=0
  resul_ctr_f_v= cli_ctr_f_v /impr_ctr_f_v 
  ctr_list_f_v.append(resul_ctr_f_v)
df_facebook_video['CTR']=ctr_list_f_v

#creamos VTR
vtr_list_f_v=[]
for vie_v, imp_v in zip(df_facebook_video['views'], df_facebook_video['Impressions']):
  if imp_v==0:
    vie_v=0
    imp_v=1
  resul_vtr_v=vie_v / imp_v 
  vtr_list_f_v.append(resul_vtr_v)
df_facebook_video['VTR']=vtr_list_f_v

#creamos CPV
cpv_list_f_v=[]
for costecito_v, vista_v in zip(df_facebook_video['Coste'], df_facebook_video['views']):
  if vista_v==0:
    costecito_v=0
    vista_v=1
  resul_cpv_v=costecito_v / vista_v 
  cpv_list_f_v.append(resul_cpv_v)
df_facebook_video['CPV']=cpv_list_f_v


# orden: Coste  Impressions Clics ctr CPC views=Video_plays_at_100 vtr CPV  

df_facebook_video.head()

# Commented out IPython magic to ensure Python compatibility.
"""
Inversion prevista
Inversion real
Variance
clics
CPC =Presupuesto total / Número de clics = CPC
sesiones = nopooo 
# % clics a sesion =sesiones/clics
clics ÷ impresiones = CTR
CPVisit
reach =forma de medir el éxito de una campaña publicitaria, además de conocer el impacto que esta produce en el público.
VTR = (Total de vistas completas / número de impresiones) x 100
# orden: Coste  Impressions Clics ctr CPC views=Video_plays_at_100 vtr CPV  
#quitar Reach  Frequency	
"""

pivotTable_face_video = pd.pivot_table(df_facebook_video, columns= "Day",aggfunc= 'sum')
first_column_facebook_video=["Facebook_video","Facebook_video","Facebook_video","Facebook_video","Facebook_video","Facebook_video","Facebook_video","Facebook_video"]
pivotTable_face_video.insert(0, 'Plataforma', first_column_facebook_video)
pivotTable_face_video=np.round(pivotTable_face_video, decimals=3)
pivotTable_face_video = pd.DataFrame(pivotTable_face_video, index=["Coste","Impressions","Clics","CTR","CPC","views","VTR","CPV"])
pivotTable_face_video

# en facebook columns Campaign_name si video view es video si no trafico trafic

"""#Facebook_trafico"""

#abrimos los excel  (facebook)

df_facebook=pd.read_csv("/content/facebook.csv", ",")

df_facebook=df_facebook.rename(columns={"Campaign name":"Campaign_name","Ad set name":"Ad_set_name","Ad name":"Ad_name","Result Type":"Result_Type","Amount spent (EUR)":"Amount_spent_EUR","Link clicks":"Link_clicks","Video plays at 100%":"Video_plays_at_100","Reporting starts":"Reporting_starts","Reporting ends":"Reporting_ends"})

df_facebook[["Campanha_nombre_parte_1","Campanha_nombre_parte_2","Campanha_nombre_parte_3"]]=df_facebook['Campaign_name'].str.split('|', expand=True)

#casteamos y quitar impresion menor a 1 

df_facebook=df_facebook.rename(columns={"Link_clicks": "Clics", "Amount_spent_EUR":"Coste","Video_plays_at_100": "views"})

df_facebook['Impressions'] = df_facebook['Impressions'].astype(int)

df_facebook=df_facebook[df_facebook['Impressions'] > 0]

#DROP

df_facebook=df_facebook.drop(columns=["Reach","Results","Frequency","Campaign_name","Ad_set_name","Ad_name","Reporting_starts","Reporting_ends","Result_Type","Campanha_nombre_parte_1","Campanha_nombre_parte_2","Campanha_nombre_parte_3"])

#cojemos solo traffic 
df_facebook=df_facebook[df_facebook['Objective'] =="LINK_CLICKS"]

df_facebook

#agrupamos

df_facebook=df_facebook.groupby(by=["Day"]).sum()
df_facebook

#hacemos el join de sesiones 
df_facebook=pd.merge(df_facebook,df_google_analitics_facebook_traffic,on='Day', how="left")

df_facebook

df_facebook.reset_index().to_csv('Day_join_face_tra_grouped.csv')

df_facebook=pd.read_csv("/content/Day_join_face_tra_grouped.csv", ",")
df_facebook=df_facebook.drop(columns=["Unnamed: 0"])

#para agrupar por mes
df_facebook=df_facebook.rename(columns={"Day":"Day_mes"})
df_facebook=df_facebook.assign(Day = lambda dataset: dataset.Day_mes.map(lambda value : (value[:-3])))
df_facebook=df_facebook.drop(columns=["Day_mes"])
df_facebook
#comprobamois que da un mes de costes 
hhh=   df_facebook[df_facebook['Day'] =="2022-01"]

print("1",hhh["Coste"].sum())
hhh=   df_facebook[df_facebook['Day'] =="2022-02"]

print("2",hhh["Coste"].sum())
hhh=   df_facebook[df_facebook['Day'] =="2022-03"]

print("3",hhh["Coste"].sum())

hhh=   df_facebook[df_facebook['Day'] =="2022-04"]

print("4",hhh["Coste"].sum())


hhh=   df_facebook[df_facebook['Day'] =="2022-05"]

print("5",hhh["Coste"].sum())


df_facebook

#agrupamos por dia
df_facebook=df_facebook.groupby(by=["Day"]).sum()

#creamos cpc
cpc_list_f=[]
for cost_f, cli_f in zip(df_facebook['Coste'], df_facebook['Clics']):
  if cli_f==0:
    cost_f=0
    cli_f=1
  resul_f=cost_f / cli_f 
  cpc_list_f.append(resul_f)
df_facebook['CPC']=cpc_list_f

#creamos ctr
ctr_list_f=[]
for impr_ctr_f, cli_ctr_f in zip(df_facebook['Impressions'], df_facebook['Clics']):
  if impr_ctr_f==0:
    impr_ctr_f=1
    cli_ctr_f=0
  resul_ctr_f= cli_ctr_f /impr_ctr_f 
  ctr_list_f.append(resul_ctr_f)
df_facebook['CTR']=ctr_list_f

#creamos VTR
vtr_list_f=[]
for vie, imp in zip(df_facebook['views'], df_facebook['Impressions']):
  if imp==0:
    vie=0
    imp=1
  resul_vtr=vie / imp 
  vtr_list_f.append(resul_vtr)
df_facebook['VTR']=vtr_list_f

#creamos CPV
cpv_list_f=[]
for costecito, vista in zip(df_facebook['Coste'], df_facebook['views']):
  if vista==0:
    costecito=0
    vista=1
  resul_cpv=costecito / vista 
  cpv_list_f.append(resul_cpv)
df_facebook['CPV']=cpv_list_f

# orden: Coste  Impressions Clics ctr CPC views=Video_plays_at_100 vtr CPV  

#creamos clics_a_sesion
list_f=[]
for sesion_f, cli_f in zip(df_facebook['Sesiones_google_anali'], df_facebook['Clics']):
   if cli_f==0:
     cli_f=1
     sesion_f=0
   resul_f=sesion_f/cli_f
   list_f.append(resul_f)  
df_facebook['Clics_a_sesion']=list_f


#CPVisit
list_f_ccc=[]
for sesion_f_ccc, coste_f_ccc in zip(df_facebook['Sesiones_google_anali'], df_facebook['Coste']):
   if sesion_f_ccc==0:
     sesion_f_ccc=1
     coste_f_ccc=0
   resul_f_ccc=coste_f_ccc/sesion_f_ccc
   list_f_ccc.append(resul_f_ccc)  
df_facebook['Cpvisit']=list_f_ccc

df_facebook

# Commented out IPython magic to ensure Python compatibility.
"""
Inversion prevista
Inversion real
Variance
clics
CPC =Presupuesto total / Número de clics = CPC
sesiones = nopooo 
# % clics a sesion =sesiones/clics
clics ÷ impresiones = CTR
CPVisit
reach =forma de medir el éxito de una campaña publicitaria, además de conocer el impacto que esta produce en el público.
VTR = (Total de vistas completas / número de impresiones) x 100
# orden: Coste  Impressions Clics ctr CPC views=Video_plays_at_100 vtr CPV  
#quitar Reach  Frequency	
"""

pivotTable_face = pd.pivot_table(df_facebook, columns= "Day",aggfunc= 'sum')
pivotTable_face=pivotTable_face
first_column_facebook=["Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic","Facebook_Traffic"]
pivotTable_face.insert(0, 'Plataforma', first_column_facebook)
pivotTable_face=np.round(pivotTable_face, decimals=3)
pivotTable_face = pd.DataFrame(pivotTable_face, index=["Coste","Impressions","Clics","CTR","CPC","views","VTR","CPV","Sesiones_google_anali","Clics_a_sesion","Cpvisit"])
pivotTable_face

"""#Dv360"""

#abrimos los excel dietas dv360 

df_dv360=pd.read_csv("/content/dv360.csv")
df_dv360=df_dv360.rename(columns={"Insertion Order":"Insertion_Order","Advertiser Currency":"Moneda","Insertion Order ID":"Insertion_Order_ID","Billable Impressions":"Billable_Impressions","Total Conversions":"Total_Conversions","Post-Click Conversions":"Post_Click_Conversions","Post-View Conversions":"Post_View_Conversions", "Line Item Type":"Line_Item_Type","Line Item ID":"Line_Item_ID"	,"Line Item":"Line_Item","Advertiser ID":"Advertiser_ID"	, "Media Cost (Advertiser Currency)":'Media_Cost_Advertiser_Currency',"Complete Views (Video)":"Complete_Views_Video","Click Rate (CTR)":"Click_Rate_CTR", "Media Cost eCPM (Adv Currency)":"Media_Cost_eCPM_Adv_Currency","Media Cost eCPC (Adv Currency)":"Media_Cost_eCPC_Adv_Currency","Revenue eCPM (Adv Currency)":"Revenue_eCPM_Adv_Currency","Revenue eCPC (Adv Currency)":"Revenue_eCPC_Adv_Currency", "Revenue (Adv Currency)":"Revenue_Adv_Currency", "Total Media Cost (Advertiser Currency)":"Total_Media_Cost_Advertiser_Currency"})
df_dv360 = df_dv360.assign(Click_Rate_CTR = lambda dataset : dataset.Click_Rate_CTR.str.replace("%",""))
df_dv360=df_dv360.rename(columns={"Insertion Order":"Insertion_Order","Advertiser Currency":"Moneda","Insertion Order ID":"Insertion_Order_ID","Billable Impressions":"Billable_Impressions","Total Conversions":"Total_Conversions","Post-Click Conversions":"Post_Click_Conversions","Post-View Conversions":"Post_View_Conversions", "Line Item Type":"Line_Item_Type","Line Item ID":"Line_Item_ID"	,"Line Item":"Line_Item","Advertiser ID":"Advertiser_ID"	, "Media Cost (Advertiser Currency)":'Media_Cost_Advertiser_Currency',"Complete Views (Video)":"Complete_Views_Video","Click Rate (CTR)":"Click_Rate_CTR", "Media Cost eCPM (Adv Currency)":"Media_Cost_eCPM_Adv_Currency","Media Cost eCPC (Adv Currency)":"Media_Cost_eCPC_Adv_Currency","Revenue eCPM (Adv Currency)":"Revenue_eCPM_Adv_Currency","Revenue eCPC (Adv Currency)":"Revenue_eCPC_Adv_Currency", "Revenue (Adv Currency)":"Revenue_Adv_Currency", "Total Media Cost (Advertiser Currency)":"Total_Media_Cost_Advertiser_Currency"})
df_dv360 = df_dv360.assign(Click_Rate_CTR = lambda dataset : dataset.Click_Rate_CTR.str.replace("%",""))

df_dv360=df_dv360.drop(columns=["Click_Rate_CTR","Advertiser","Advertiser_ID","Insertion_Order_ID","Line_Item_ID","Moneda","Insertion_Order","Total_Conversions","Line_Item","Line_Item_Type","Revenue_Adv_Currency","Billable_Impressions","Post_Click_Conversions","Post_View_Conversions"])

#quitar las columnas que sobran de los totales del final 

df_dv360.drop(df_dv360[-17:].index, inplace=True)

#quitar impresion menor a 1 

df_dv360=df_dv360[df_dv360['Impressions'] > 0]

df_dv360=df_dv360.rename(columns={"Clicks": "Clics","Media_Cost_Advertiser_Currency":"Coste"})

df_dv360['Impressions'] = df_dv360['Impressions'].astype(int)

df_dv360['Clics'] = df_dv360['Clics'].astype(int)

df_dv360.columns = ["Date","Impressions","Clics","Coste_mal","Complete_Views_Video"]
df_dv360 = df_dv360.assign(Coste = lambda dataset : dataset.Coste_mal.str.replace("€",""))

df_dv360['Coste'] = df_dv360['Coste'].astype(float)

#views=Complete_Views_Video en facefoob esto es views
df_dv360=df_dv360.rename(columns={"Complete_Views_Video": "views","Click_Rate_CTR":"CTR","Date":"Day_M"})

#CAMBIAMOS FORMATO DE FECHA
df_dv360=df_dv360.rename(columns={"Day":"Day_M"})
df_dv360 = df_dv360.assign(Day = lambda dataset : dataset.Day_M.str.replace("/","-"))
df_dv360=df_dv360.drop(columns=["Day_M"])
#agrupamos
df_dv360=df_dv360.groupby(by=["Day"]).sum()
#hacemos el join de sesiones 
df_dv360=pd.merge(df_dv360,df_google_analitics_dv_360,on='Day', how="outer")

df_dv360.reset_index().to_csv('Day_join_360_grouped.csv')

df_dv360=pd.read_csv("/content/Day_join_360_grouped.csv", ",")
df_dv360=df_dv360.drop(columns=["Unnamed: 0"])

#para agrupar por mes
df_dv360=df_dv360.rename(columns={"Day":"Day_mes"})
df_dv360=df_dv360.assign(Day = lambda dataset: dataset.Day_mes.map(lambda value : (value[:-3])))
#agrupamos
df_dv360=df_dv360.groupby(by=["Day"]).sum()
df_dv360

#creamos cpc
cpc_list=[]
for cost, cli in zip(df_dv360['Coste'], df_dv360['Clics']):
  if cli==0:
    cost=0
    cli=1
  resul=cost / cli 
  cpc_list.append(resul)
df_dv360['CPC']=cpc_list

#creamos VTR
vtr_list_360=[]
for vi, im in zip(df_dv360['views'], df_dv360['Impressions']):
  if im==0:
    vi=0
    im=1
  resul_vtr_360=vi / im 
  vtr_list_360.append(resul_vtr_360)
df_dv360['VTR']=vtr_list_360

#creamos CPV
cpv_list_360=[]
for costecito360, vista360 in zip(df_dv360['Coste'], df_dv360['views']):
  if vista360==0:
    costecito360=0
    vista360=1
  resul_cpv360=costecito360 / vista360
  cpv_list_360.append(resul_cpv360)
df_dv360['CPV']=cpv_list_360

#creamos ctr
ctr_list_360=[]
for impr_ctr_360, cli_ctr_360 in zip(df_dv360['Impressions'], df_dv360['Clics']):
  if impr_ctr_360==0:
    impr_ctr_360=1
    cli_ctr_360=0
  resul_ctr_360= cli_ctr_360 /impr_ctr_360
  ctr_list_360.append(resul_ctr_360)
df_dv360['CTR']=ctr_list_360


#creamos clics_a_sesion
list_360=[]
for sesion_360, cli_360 in zip(df_dv360['Sesiones_google_anali'], df_dv360['Clics']):
   if cli_360==0:
     cli_360=1
     sesion_360=0
   resul_360=sesion_360/cli_360
   list_360.append(resul_360)  
df_dv360['Clics_a_sesion']=list_360


#CPVisit
list_360_ccc=[]
for sesion_360_ccc, coste_360_ccc in zip(df_dv360['Sesiones_google_anali'], df_dv360['Coste']):
   if sesion_360_ccc==0:
     sesion_360_ccc=1
     coste_360_ccc=0
   resul_360_ccc=coste_360_ccc/sesion_360_ccc
   list_360_ccc.append(resul_360_ccc)  
df_dv360['Cpvisit']=list_360_ccc



df_dv360.head(5)

# Commented out IPython magic to ensure Python compatibility.
"""
Inversion prevista
Inversion real
Variance
clics
CPC =Presupuesto total / Número de clics = CPC
sesiones= noo hay
# % clics a sesion
CPVisit
CPV 
"""

pivotTable_360 = pd.pivot_table(df_dv360, columns= "Day", aggfunc= 'sum')
pivotTable_360=pivotTable_360
first_column_g_360=["Google_360","Google_360","Google_360","Google_360","Google_360","Google_360","Google_360","Google_360","Google_360","Google_360","Google_360"]
pivotTable_360.insert(0, 'Plataforma', first_column_g_360)
pivotTable_360=np.round(pivotTable_360, decimals=3)
pivotTable_360 = pd.DataFrame(pivotTable_360, index=["Coste","Impressions","Clics","CTR","CPC","views","VTR","CPV","Sesiones_google_anali","Clics_a_sesion","Cpvisit"])
pivotTable_360

"""#Google ads sem"""

df_google_ads_sem = pd.read_csv("/content/ads_sem.csv",encoding='utf-8', sep='delimiter', header=None)

df_google_ads_sem = df_google_ads_sem.drop(labels=[0,1,2], axis=0)
print("inial",np.shape(df_google_ads_sem))

df_google_ads_sem=df_google_ads_sem.rename(columns={0:"p"})
df_google_ads_sem=df_google_ads_sem.assign(p1 = lambda dataset : dataset.p.str.replace("€",""))
df_google_ads_sem=df_google_ads_sem.assign(p2 = lambda dataset : dataset.p1.str.replace("--",""))
df_google_ads_sem=df_google_ads_sem.assign(p3 = lambda dataset : dataset.p2.str.replace("%",""))
df_google_ads_sem=df_google_ads_sem.assign(p4 = lambda dataset : dataset.p3.str.replace("%",""))
df_google_ads_sem=df_google_ads_sem.assign(p5 = lambda dataset : dataset.p4.str.replace(".",""))

def coger_numeros(my_str):
  z=(re.sub('(?<=[0-9]),(?=[0-9])','.',my_str))
  return z

df_google_ads_sem=df_google_ads_sem.assign(p6 = lambda dataset: dataset.p5.apply( lambda linea : coger_numeros(linea)))

#funcion problema comas final 
def comas_comas(my_str):
  if   my_str[-1:]==" ":
    gato=my_str+"0.000"
  else:  
    gato=my_str
  return gato 

df_google_ads_sem=df_google_ads_sem.assign(p7 = lambda dataset: dataset.p6.apply( lambda linea : comas_comas(linea)))
df_google_ads_sem[["p7"]]

df_google_ads_sem=df_google_ads_sem.drop(columns =["p","p1","p2","p3","p4","p5","p6"])

split_data = df_google_ads_sem["p7"].str.split(",")
data = split_data.to_list()
names = ["Campanha","Grupo_de_anuncios","Estado_de_la_campanha","Dia","Codigo_de_moneda","Impression","Coste_m","Clics","CTR_m","CPC_medio_mal"]
df_google_ads_sem = pd.DataFrame(data, columns=names)

#Coste

df_google_ads_sem=df_google_ads_sem.assign(Coste_mal_1 = lambda dataset: dataset.Coste_m.map(lambda value : (value[1:])))
df_google_ads_sem=df_google_ads_sem.assign(Coste = lambda dataset: dataset.Coste_mal_1.map(lambda value : (value[:-1])))
df_google_ads_sem=df_google_ads_sem.drop(columns =["Coste_mal_1","Coste_m"])

#CTR_m borrar 

df_google_ads_sem=df_google_ads_sem.drop(columns =["CTR_m"])

#casteamos

df_google_ads_sem['Impression'] = df_google_ads_sem['Impression'].astype(float)

df_google_ads_sem['Clics'] = df_google_ads_sem['Clics'].astype(float)

df_google_ads_sem['Coste'] = df_google_ads_sem['Coste'].astype(float)

#renombramos
df_google_ads_sem=df_google_ads_sem.rename(columns={"Dia":"Day","Impression":"Impressions"})

#quitar las columnas que sobran de los totales del final 

df_google_ads_sem=df_google_ads_sem[~df_google_ads_sem.Estado_de_la_campanha.str.contains("Total", na=False)]

#agrupamos
df_google_ads_sem=df_google_ads_sem.groupby(by=["Day"]).sum()

#hacemos el join de sesiones 

df_google_ads_sem=pd.merge(df_google_ads_sem,df_google_analitics_sem,on='Day', how="outer")

df_google_ads_sem.reset_index().to_csv('Day_join_sem_grouped.csv')

df_google_ads_sem=pd.read_csv("/content/Day_join_sem_grouped.csv", ",")
df_google_ads_sem=df_google_ads_sem.drop(columns=["Unnamed: 0"])


#para agrupar por mes
df_google_ads_sem=df_google_ads_sem.rename(columns={"Day":"Day_mes"})
df_google_ads_sem=df_google_ads_sem.assign(Day = lambda dataset: dataset.Day_mes.map(lambda value : (value[:-3])))
df_google_ads_sem

#quitar impresion menor a 1

df_google_ads_sem=df_google_ads_sem[df_google_ads_sem['Impressions'] > 0]

#agrupamos

df_google_ads_sem=df_google_ads_sem.groupby(by=["Day"]).sum()


#creamos cpc
cpc_list_g_sem=[]
for cost_g_sem, cli_g_sem in zip(df_google_ads_sem['Coste'], df_google_ads_sem['Clics']):
  if cli_g_sem==0:
    cost_g_sem=0
    cli_g_sem=1
  resul_g_sem=cost_g_sem / cli_g_sem 
  cpc_list_g_sem.append(resul_g_sem)
df_google_ads_sem['CPC']=cpc_list_g_sem

#creamos ctr
ctr_list_g_sem=[]
for impr_ctr_g_sem, cli_ctr_g_sem in zip(df_google_ads_sem['Impressions'], df_google_ads_sem['Clics']):
  if impr_ctr_g_sem==0:
    impr_ctr_g_sem=1  
    cli_ctr_g_sem=0
  resul_ctr_g_sem= cli_ctr_g_sem /impr_ctr_g_sem
  ctr_list_g_sem.append(resul_ctr_g_sem)
df_google_ads_sem['CTR']=ctr_list_g_sem



#creamos clics_a_sesion
list_sem=[]
for sesion_sem, cli_sem in zip(df_google_ads_sem['Sesiones_google_anali'], df_google_ads_sem['Clics']):
   if cli_sem==0:
     cli_sem=1
     sesion_sem=0
   resul_sem=sesion_sem/cli_sem
   list_sem.append(resul_sem)  
df_google_ads_sem['Clics_a_sesion']=list_sem


#CPVisit
list_sem_ccc=[]
for sesion_sem_ccc, coste_sem_ccc in zip(df_google_ads_sem['Sesiones_google_anali'], df_google_ads_sem['Coste']):
   if sesion_sem_ccc==0:
     sesion_sem_ccc=1
     coste_sem_ccc=0
   resul_sem_ccc=coste_sem_ccc/sesion_sem_ccc
   list_sem_ccc.append(resul_sem_ccc)  
df_google_ads_sem['Cpvisit']=list_sem_ccc



df_google_ads_sem

pivotTable_g_ads_sem = pd.pivot_table(df_google_ads_sem, columns= "Day",aggfunc= 'sum')
first_column_g_ad_sem=["Google_ads_sem","Google_ads_sem","Google_ads_sem","Google_ads_sem","Google_ads_sem","Google_ads_sem","Google_ads_sem","Google_ads_sem"]

pivotTable_g_ads_sem.insert(0, 'Plataforma', first_column_g_ad_sem)
pivotTable_g_ads_sem=np.round(pivotTable_g_ads_sem, decimals=3)
pivotTable_g_ads_sem=pd.DataFrame(pivotTable_g_ads_sem, index=["Coste","Impressions","Clics","CTR","CPC","Sesiones_google_anali","Clics_a_sesion","Cpvisit"])

pivotTable_g_ads_sem

#GDN y SEM son de Google ads, paid social es facebook y OLV es DV360. display no hay
# google ads gdn () si display en el nombre cmapaña GDN si no sem

"""#Google ads display"""

df_google_ads = pd.read_csv("/content/ads_dis.csv",encoding='utf-8', sep='delimiter', header=None)

df_google_ads = df_google_ads.drop(labels=[0,1,2], axis=0)

df_google_ads=df_google_ads.rename(columns={0:"p"})
df_google_ads=df_google_ads.assign(p1 = lambda dataset : dataset.p.str.replace("€",""))
df_google_ads=df_google_ads.assign(p2 = lambda dataset : dataset.p1.str.replace("--",""))
df_google_ads=df_google_ads.assign(p3 = lambda dataset : dataset.p2.str.replace("%",""))
df_google_ads=df_google_ads.assign(p4 = lambda dataset : dataset.p3.str.replace("%",""))
df_google_ads=df_google_ads.assign(p5 = lambda dataset : dataset.p4.str.replace(".",""))

def coger_numeros(my_str):
  z=(re.sub('(?<=[0-9]),(?=[0-9])','.',my_str))
  return z

df_google_ads=df_google_ads.assign(p6 = lambda dataset: dataset.p5.apply( lambda linea : coger_numeros(linea)))

#funcion problema comas final 
def comas_comas(my_str):
  if   my_str[-1:]==" ":
    gato=my_str+"0.000"
  else:  
    gato=my_str
  return gato 

df_google_ads=df_google_ads.assign(p7 = lambda dataset: dataset.p6.apply( lambda linea : comas_comas(linea)))
df_google_ads[["p7"]]

df_google_ads=df_google_ads.drop(columns =["p","p1","p2","p3","p4","p5","p6"])

split_data = df_google_ads["p7"].str.split(",")
data = split_data.to_list()
names = ["Campanha","Grupo_de_anuncios","Estado_de_la_campanha","Dia","Codigo_de_moneda","Impression","Coste_m","Clics","CTR_m","CPC_medio_mal"]
df_google_ads = pd.DataFrame(data, columns=names)

#Coste

df_google_ads=df_google_ads.assign(Coste_mal_1 = lambda dataset: dataset.Coste_m.map(lambda value : (value[1:])))
df_google_ads=df_google_ads.assign(Coste = lambda dataset: dataset.Coste_mal_1.map(lambda value : (value[:-1])))
df_google_ads=df_google_ads.drop(columns =["Coste_mal_1","Coste_m"])
#CTR_m borrar 

df_google_ads=df_google_ads.drop(columns =["CTR_m"])

#casteamos

df_google_ads['Impression'] = df_google_ads['Impression'].astype(float)

df_google_ads['Clics'] = df_google_ads['Clics'].astype(float)

df_google_ads['Coste'] = df_google_ads['Coste'].astype(float)

#renombramos
df_google_ads=df_google_ads.rename(columns={"Dia":"Day","Impression":"Impressions"})

#quitar las columnas que sobran de los totales del final 

df_google_ads=df_google_ads[~df_google_ads.Estado_de_la_campanha.str.contains("Total", na=False)]

#agrupamos
df_google_ads=df_google_ads.groupby(by=["Day"]).sum()

#hacemos el join de sesiones 

df_google_ads=pd.merge(df_google_ads,df_google_analitics_display,on='Day', how="outer")

df_google_ads.reset_index().to_csv('Day_join_ads_grouped.csv')

df_google_ads=pd.read_csv("/content/Day_join_ads_grouped.csv", ",")
df_google_ads=df_google_ads.drop(columns=["Unnamed: 0"])

#para agrupar por mes
df_google_ads=df_google_ads.rename(columns={"Day":"Day_mes"})
df_google_ads=df_google_ads.assign(Day = lambda dataset: dataset.Day_mes.map(lambda value : (value[:-3])))
df_google_ads

#quitar impresion menor a 1

df_google_ads=df_google_ads[df_google_ads['Impressions'] > 0]

#agrupamos

df_google_ads=df_google_ads.groupby(by=["Day"]).sum()

#creamos cpc
cpc_list_g=[]
for cost_g, cli_g in zip(df_google_ads['Coste'], df_google_ads['Clics']):
  if cli_g==0:
    cost_g=0
    cli_g=1
  resul_g=cost_g / cli_g 
  cpc_list_g.append(resul_g)
df_google_ads['CPC']=cpc_list_g 

#creamos ctr
ctr_list_g=[]
for impr_ctr_g, cli_ctr_g in zip(df_google_ads['Impressions'], df_google_ads['Clics']):
  if impr_ctr_g==0:
    impr_ctr_g=1  
    cli_ctr_g=0
  resul_ctr_g= cli_ctr_g /impr_ctr_g
  ctr_list_g.append(resul_ctr_g)
df_google_ads['CTR']=ctr_list_g

#creamos clics_a_sesion
list_dis=[]
for sesion_dis, cli_dis in zip(df_google_ads['Sesiones_google_anali'], df_google_ads['Clics']):
   if cli_dis==0:
     cli_dis=1
     sesion_dis=0
   resul_dis=sesion_dis/cli_dis
   list_dis.append(resul_dis)  
df_google_ads['Clics_a_sesion']=list_dis


#CPVisit
list_dis_ccc=[]
for sesion_dis_ccc, coste_dis_ccc in zip(df_google_ads['Sesiones_google_anali'], df_google_ads['Coste']):
   if sesion_dis_ccc==0:
     sesion_dis_ccc=1
     coste_dis_ccc=0
   resul_dis_ccc=coste_dis_ccc/sesion_dis_ccc
   list_dis_ccc.append(resul_dis_ccc)  
df_google_ads['Cpvisit']=list_dis_ccc




df_google_ads

# Commented out IPython magic to ensure Python compatibility.
"""
Inversion prevista
Inversion real
Variance
clics
CPC =Presupuesto total / Número de clics 
ctr =
sesiones
# % clics a sesion
CPVisit =Presupuesto total / Número de visitas 
"""

pivotTable_g_ads = pd.pivot_table(df_google_ads, columns= "Day",aggfunc= 'sum')
pivotTable_g_ads=pivotTable_g_ads
first_column_g_ad=["Google_ads_display","Google_ads_display","Google_ads_display","Google_ads_display","Google_ads_display","Google_ads_display","Google_ads_display","Google_ads_display"]
pivotTable_g_ads.insert(0, 'Plataforma', first_column_g_ad)
pivotTable_g_ads=np.round(pivotTable_g_ads, decimals=3)
pivotTable_g_ads = pd.DataFrame(pivotTable_g_ads, index=["Coste","Impressions","Clics","CTR","CPC","Sesiones_google_anali","Clics_a_sesion","Cpvisit"])

pivotTable_g_ads

"""#Totales"""

df_totales = pd.concat([df_facebook,df_facebook_video, df_dv360,df_google_ads,df_google_ads_sem], axis=0, join="outer")

df_totales=df_totales.drop(columns=["CPC","CTR","VTR","CPV","Clics_a_sesion","Cpvisit"])
df_totales

df_totales=df_totales.groupby(by=["Day"]).sum()
df_totales

#creamos cpc
cpc_list_f_t=[]
for cost_f_t, cli_f_t in zip(df_totales['Coste'], df_totales['Clics']):
  if cli_f_t==0:
    cost_f_t=0
    cli_f_t=1
  resul_f_t=cost_f_t / cli_f_t
  cpc_list_f_t.append(resul_f_t)
df_totales['CPC']=cpc_list_f_t

#creamos ctr
ctr_list_f_t=[]
for impr_ctr_f_t, cli_ctr_f_t in zip(df_totales['Impressions'], df_totales['Clics']):
  if impr_ctr_f_t==0:
    impr_ctr_f_t=1
    cli_ctr_f_t=0
  resul_ctr_f_t= cli_ctr_f_t /impr_ctr_f_t 
  ctr_list_f_t.append(resul_ctr_f_t)
df_totales['CTR']=ctr_list_f_t

#creamos VTR
vtr_list_f_t=[]
for vie_t, imp_t in zip(df_totales['views'], df_totales['Impressions']):
  if imp_t==0:
    vie_t=0
    imp_t=1
  resul_vtr_t=vie_t / imp_t 
  vtr_list_f_t.append(resul_vtr_t)
df_totales['VTR']=vtr_list_f_t

#creamos CPV
cpv_list_f_t=[]
for costecito_t, vista_t in zip(df_totales['Coste'], df_totales['views']):
  if vista_t==0:
    costecito_t=0
    vista_t=1
  resul_cpv_t=costecito_t / vista_t
  cpv_list_f_t.append(resul_cpv_t)
df_totales['CPV']=cpv_list_f_t

#creamos clics_a_sesion
list_t=[]
for sesion_t, cli_t in zip(df_totales['Sesiones_google_anali'], df_totales['Clics']):
   if cli_t==0:
     cli_t=1
     sesion_t=0
   resul_t=sesion_t/cli_t
   list_t.append(resul_t)  
df_totales['Clics_a_sesion']=list_t

#CPVisit
list_t_ccc=[]
for sesion_t_ccc, coste_t_ccc in zip(df_totales['Sesiones_google_anali'], df_totales['Coste']):
   if sesion_t_ccc==0:
     sesion_t_ccc=1
     coste_t_ccc=0
   resul_t_ccc=coste_t_ccc/sesion_t_ccc
   list_t_ccc.append(resul_t_ccc)  
df_totales['Cpvisit']=list_t_ccc

df_totales

df_totales_pivot = pd.pivot_table(df_totales, columns= "Day",aggfunc= 'sum')
df_totales_pivot

df_totales_pivot=np.round(df_totales_pivot, decimals=2)
df_totales_pivot

first_column_total=["Total","Total","Total","Total","Total","Total","Total","Total","Total","Total","Total"]
df_totales_pivot.insert(0, 'Plataforma', first_column_total)

df_totales_pivot = pd.DataFrame(df_totales_pivot, index=["Coste","Impressions","Clics","CPC","CTR","views","VTR","CPV","Sesiones_google_anali","Clics_a_sesion","Cpvisit"])

df_totales_pivot

"""# IMPRIMIR EXCEL"""

escrito = pd.ExcelWriter('Informe_mensual_affinity.xlsx')
# escribir el DataFrame en excel
pivotTable_g_ads.to_excel(escrito,startrow=0)
pivotTable_g_ads_sem.to_excel(escrito,startrow=9)
pivotTable_360.to_excel(escrito,startrow=18)
pivotTable_face.to_excel(escrito,startrow=30)
pivotTable_face_video.to_excel(escrito,startrow=42)
df_totales_pivot.to_excel(escrito,startrow=51)
# guardar el excel
escrito.save()
print('El DataFrame se ha escrito con éxito en el archivo de Excel.')