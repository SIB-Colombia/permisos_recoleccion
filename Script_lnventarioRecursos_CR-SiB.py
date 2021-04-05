# -*- coding: utf-8 -*-
"""
Created on Sat May  9 12:55:44 2020

@author: Natalia Medina A.
"""
#-----------------------librerias----------------------------------------------
import os
import pandas as pd
from xml.dom import minidom
from xml.parsers.expat import ExpatError

#--------------------Se establece el directorio de trabajo---------------------
#Reemplace D:\cr-sib\PRUEBA\resources por la ruta del directorio. Mantenga el 
#sentido de la barra en diagonal

os.chdir(r"C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python\Recursos")
Directorio = os.getcwd()
os.getcwd()

#---------------------Se listan los subdirectorios-----------------------------

Nombres_carpetas = os.listdir(Directorio)

#-------------se crean los DataFrames para info de eml.xml---------------------

datadirTitle=pd.DataFrame()
datadirOrg=pd.DataFrame()
datadirFecha=pd.DataFrame()
datadirCitID=pd.DataFrame()
datadirInfoAd=pd.DataFrame()
datadirEml=pd.DataFrame()

datadirEmlVacios=pd.DataFrame()

#-------------se crean los DataFrames para info de eml-1.xml---------------------

datadirTitle_1=pd.DataFrame()
datadirOrg_1=pd.DataFrame()
datadirFecha_1=pd.DataFrame()
datadirCitID_1=pd.DataFrame()
datadirInfoAd_1=pd.DataFrame()
datadirEml_1=pd.DataFrame()

datadirEml_1NoExiste=pd.DataFrame()

#----------------se crean los DataFrames para info de resorce.xml--------------

datadirCert=pd.DataFrame()
datadirRegis=pd.DataFrame()
datadirResource=pd.DataFrame()

datadirResourceNoExiste=pd.DataFrame()

#--------------------EXRAE INFO DE ARCHIVO eml.xml PARA CADA RECURSO-----------
#Reemplace D:/cr-sib/PRUEBA/resources/ por la ruta del directorio. Mantenga el 
#sentido de la barra en diagonal

for nombre in Nombres_carpetas:
    Rutas = ["C:/Users/Laura Sánchez/OneDrive/Documentos/PASANTÍA/Python/Recursos/" + nombre]
    
    for ruta in Rutas :
        
        subdir = os.chdir(ruta)
        
        try: 
             x = minidom.parse('eml.xml')
            
#----------------extrae los titulos de los recursos----------------------------
             
             titulo = x.getElementsByTagName("title")
        
             if (titulo.length > 0):
               tit = pd.Index([titulo[0].firstChild.data])
               d_tit = tit.to_frame(name= 'Título').reset_index()
               d_tit[('Recurso')]= nombre
               datadirTitle = pd.concat([datadirTitle,d_tit],sort=False)
               
# Se hace para los archivos que no contienen titulo 
               
             else:
               tit = pd.Index(["No_documenta"])
               d_tit = tit.to_frame(name= 'Título').reset_index()
               d_tit['Recurso']= nombre
               datadirTitle = pd.concat([datadirTitle,d_tit],sort=False)  
                
#----------------extrae el nombre de la organizacion de los recursos-----------
               
             organizacion = x.getElementsByTagName("organizationName")
        
             if (organizacion.length > 0):
               org = pd.Index([organizacion[0].firstChild.data])
               d_org = org.to_frame(name= 'Organización').reset_index()
               d_org['Recurso']= nombre
               datadirOrg = pd.concat([datadirOrg,d_org],sort=False)
               
# Se hace para los archivos que no contienen nombre de organizacion
               
             else:
               org = pd.Index(["No_documenta"])
               d_org = org.to_frame(name= 'Organización').reset_index()
               d_org['Recurso']= nombre
               datadirOrg = pd.concat([datadirOrg,d_org],sort=False)

#------------extrae la fecha de publcacion de los recursos---------------------              
               
             fecha= x.getElementsByTagName("pubDate")
        
             if (fecha.length > 0):
               fech=pd.Index([fecha[0].firstChild.data])
               d_fech = fech.to_frame(name= 'Fecha').reset_index()
               d_fech['Recurso']= nombre
               datadirFecha = pd.concat([datadirFecha,d_fech],sort=False)

# Se separa el año de la fecha
               
               foo = lambda x: pd.Series([i for i in (x.split('- '))])
               datadirFecha['Año'] = datadirFecha['Fecha'].apply(foo)
               foo = lambda x: pd.Series([i for i in (x.split('-'))])
               datadirFecha['Año'] = datadirFecha['Fecha'].apply(foo)
               
# Se hace para los archivos que no contienen fecha de publicacion
               
             else:
               fech= pd.Index(["No_documenta"])
               d_fech = org.to_frame(name= 'Fecha').reset_index()
               d_fech['Recurso']= nombre
               datadirFecha = pd.concat([datadirFecha,d_fech],sort=False)
         
               
#-------------------extrae el DOI de cada recurso------------------------------
               
             citationID = x.getElementsByTagName("alternateIdentifier")
        
             if (citationID.length > 0):
               citID = pd.Index([citationID[0].firstChild.data])
               d_citID  = citID.to_frame(name= 'DOI').reset_index()
               d_citID['Recurso']= nombre
               datadirCitID = pd.concat([datadirCitID,d_citID], sort=False)
               
# Se hace para los archivos que no contienen DOI
               
             else:
               citID= pd.Index(["No_documenta"])
               d_citID = citID.to_frame(name= 'DOI').reset_index()
               d_citID['Recurso']= nombre
               datadirCitID = pd.concat([datadirCitID,d_citID],sort=False) 
               
#---------------------extrae la datos del permiso------------------------------
               
             InfoAdicional = x.getElementsByTagName("para")
        
             if (InfoAdicional.length > 1):
               infoAd = pd.Index([InfoAdicional[1].firstChild.data])
               d_infoAd  = infoAd.to_frame(name= 'Datos permiso').reset_index()
               d_infoAd['Recurso'] = nombre
               datadirInfoAd = pd.concat([datadirInfoAd,d_infoAd], sort=False)
               
# Se hace para los archivos que no contienen información del permiso     
               
             else:
               infoAd= pd.Index(["No_documenta"])
               d_infoAd = infoAd.to_frame(name= 'Datos permiso').reset_index()
               d_infoAd['Recurso']= nombre
               datadirInfoAd = pd.concat([datadirInfoAd,d_infoAd],sort=False)  

#names = ["Autoridad ambiental", "Numero del permiso", "Titular del permiso", "Nit o cedula", "Fecha de emision del permiso"]               
 

#-----------Se hace para los archivos eml.xml que estan vacios-----------------
              
        except:
               ExpatError
#               print ('El archivo eml.xml de ' + nombre +' esta vacio')
               emlVacios= pd.Index(["El archivo eml.xml esta vacio"])
               d_emlVacios = emlVacios.to_frame(name= 'Observación').reset_index()
               d_emlVacios['Recurso']= nombre
               datadirEmlVacios = pd.concat([datadirEmlVacios,d_emlVacios],sort=False)
  
    
#----------EXTRAE INFORMACION DEL ARCHIVO resource.xml PARA CADA RECURSO-------
        
        try:
             y = minidom.parse('resource.xml')
        
#-------------------extrae el nombre del certificado---------------------------
             
             certificado = y.getElementsByTagName("certNameFile")
        
             if (certificado.length > 0):
               cert = pd.Index([certificado[0].firstChild.data])
               d_cert = cert.to_frame(name= 'Certificado').reset_index()
               d_cert['Recurso']= nombre
               datadirCert = pd.concat([datadirCert,d_cert], sort=False)
              
# Se hace para los archivos que no contienen nombre de certificado
               
             else:
               cert= pd.Index(["No_documenta"])
               d_cert = cert.to_frame(name= 'Certificado').reset_index()
               d_cert['Recurso']= nombre
               datadirCert = pd.concat([datadirCert,d_cert],sort=False) 

#----------------------extrae el numero de registros--------------------------- 
               
             registros = y.getElementsByTagName("recordsPublished")
        
             if (registros.length > 0):
               reg = pd.Index([registros[0].firstChild.data])
               d_reg = reg.to_frame(name= 'Registros').reset_index()
               d_reg['Recurso']= nombre
               datadirRegis = pd.concat([datadirRegis,d_reg], sort=False)
               
# Se hace para los archivos que no contienen registros
               
             else:
               reg= pd.Index(["No_documenta"])
               d_reg = reg.to_frame(name= 'Registros').reset_index()
               d_reg['Recurso']= nombre
               datadirRegis = pd.concat([datadirRegis,d_reg],sort=False)   

#-----------Se hace para los archivos resource.xml que no existen--------------
               
        except:
               FileNotFoundError
#               print ('El archivo resource.xml de ' + nombre +' no existe')               
               resourceNoExiste= pd.Index(["El archivo resource.xml no existe"])
               d_resourceNoExiste = resourceNoExiste.to_frame(name= 'Observación').reset_index()
               d_resourceNoExiste['Recurso']= nombre
               datadirResourceNoExiste = pd.concat([datadirResourceNoExiste,d_resourceNoExiste],sort=False)

#---------------------Extrae informacion de eml-1------------------------------

namesEml_1=datadirEmlVacios['Recurso'].values.tolist()

#Reemplace D:/cr-sib/PRUEBA/resources/ por la ruta del directorio. Mantenga el 
#sentido de la barra en diagonal

for name in namesEml_1:
    RutasEml_1 = ["C:/Users/Laura Sánchez/OneDrive/Documentos/PASANTÍA/Python/Recursos/" + name]
    
    for rutaEml in RutasEml_1 :
        
        subdir = os.chdir(rutaEml)
        
        try: 
             z = minidom.parse('eml-1.xml')

#----------------extrae los titulos de los recursos----------------------------
             
             titulo_1 = z.getElementsByTagName("title")
        
             if (titulo_1.length > 0):
               tit_1 = pd.Index([titulo_1[0].firstChild.data])
               d_tit_1 = tit_1.to_frame(name= 'Título').reset_index()
               d_tit_1['Recurso']= name
               datadirTitle_1 = pd.concat([datadirTitle_1,d_tit_1],sort=False)
               
# Se hace para los archivos que no contienen titulo 
               
             else:
               tit_1 = pd.Index(["No_documenta"])
               d_tit_1 = tit_1.to_frame(name= 'Título').reset_index()
               d_tit_1['Recurso']= name
               datadirTitle_1 = pd.concat([datadirTitle_1,d_tit_1],sort=False)  
                
#----------------extrae el nombre de la organizacion de los recursos-----------
               
             organizacion_1 = z.getElementsByTagName("organizationName")
        
             if (organizacion_1.length > 0):
               org_1 = pd.Index([organizacion_1[0].firstChild.data])
               d_org_1 = org_1.to_frame(name= 'Organización').reset_index()
               d_org_1['Recurso']= name
               datadirOrg_1 = pd.concat([datadirOrg_1,d_org_1],sort=False)
               
# Se hace para los archivos que no contienen nombre de organizacion
               
             else:
               org_1 = pd.Index(["No_documenta"])
               d_org_1 = org_1.to_frame(name= 'Organización').reset_index()
               d_org_1['Recurso']= name
               datadirOrg_1 = pd.concat([datadirOrg_1,d_org_1],sort=False)

#------------extrae la fecha de publcacion de los recursos---------------------              
               
             fecha_1= z.getElementsByTagName("pubDate")
        
             if (fecha_1.length > 0):
               fech_1=pd.Index([fecha_1[0].firstChild.data])
               d_fech_1 = fech_1.to_frame(name= 'Fecha').reset_index()
               d_fech_1['Recurso']= name
               datadirFecha_1 = pd.concat([datadirFecha_1,d_fech_1],sort=False)

# Se separa el año de la fecha
               
               foo1 = lambda x: pd.Series([i for i in (x.split('- '))])
               datadirFecha_1['Año'] = datadirFecha_1['Fecha'].apply(foo1)
               foo1 = lambda x: pd.Series([i for i in (x.split('-'))])
               datadirFecha_1['Año'] = datadirFecha_1['Fecha'].apply(foo)
               
# Se hace para los archivos que no contienen fecha de publicacion
               
             else:
               fech_1= pd.Index(["No_documenta"])
               d_fech_1 = org_1.to_frame(name= 'Fecha').reset_index()
               d_fech_1['Recurso']= name
               datadirFecha_1 = pd.concat([datadirFecha_1,d_fech_1],sort=False)
         
               
#-------------------extrae el DOI de cada recurso------------------------------
               
             citationID_1 = z.getElementsByTagName("alternateIdentifier")
        
             if (citationID_1.length > 0):
               citID_1 = pd.Index([citationID_1[0].firstChild.data])
               d_citID_1  = citID_1.to_frame(name= 'DOI').reset_index()
               d_citID_1['Recurso']= name
               datadirCitID_1 = pd.concat([datadirCitID_1,d_citID_1], sort=False)
               
# Se hace para los archivos que no contienen DOI
               
             else:
               citID_1= pd.Index(["No_documenta"])
               d_citID_1 = citID_1.to_frame(name= 'DOI').reset_index()
               d_citID_1['Recurso']= name
               datadirCitID_1 = pd.concat([datadirCitID_1,d_citID_1],sort=False) 
               
#---------------------extrae la datos del permiso------------------------------
               
             InfoAdicional_1 = z.getElementsByTagName("para")
        
             if (InfoAdicional_1.length > 1):
               infoAd_1 = pd.Index([InfoAdicional_1[1].firstChild.data])
               d_infoAd_1  = infoAd_1.to_frame(name= 'Datos permiso').reset_index()
               d_infoAd_1['Recurso'] = name
               datadirInfoAd_1 = pd.concat([datadirInfoAd_1,d_infoAd_1], sort=False)
               
# Se hace para los archivos que no contienen información del permiso     
               
             else:
               infoAd_1= pd.Index(["No_documenta"])
               d_infoAd_1 = infoAd_1.to_frame(name= 'Datos permiso').reset_index()
               d_infoAd_1['Recurso']= name
               datadirInfoAd_1 = pd.concat([datadirInfoAd_1,d_infoAd_1],sort=False)  

#names = ["Autoridad ambiental", "Numero del permiso", "Titular del permiso", "Nit o cedula", "Fecha de emision del permiso"]               
 

#-----------Se hace para los archivos eml.xml que estan vacios-----------------
              
        except:
               FileNotFoundError
#               print ('El archivo eml-1.xml de ' + name +' no existe')               
               Eml_1NoExiste= pd.Index(["El archivo eml-1.xml no existe"])
               d_Eml_1NoExiste = Eml_1NoExiste.to_frame(name= 'Observación').reset_index()
               d_Eml_1NoExiste['Recurso']= name
               datadirEml_1NoExiste = pd.concat([datadirEml_1NoExiste,d_Eml_1NoExiste],sort=False)

#------------------------Borra colunmas duplicadas (index)---------------------         

datadirTitle = datadirTitle.drop(['index'], axis=1)
datadirOrg = datadirOrg.drop(['index'], axis=1)
datadirFecha = datadirFecha.drop(['index'], axis=1)
datadirCitID = datadirCitID.drop(['index'], axis=1)
datadirInfoAd = datadirInfoAd.drop(['index'], axis=1) 

datadirTitle_1 = datadirTitle_1.drop(['index'], axis=1)
datadirOrg_1 = datadirOrg_1.drop(['index'], axis=1)
datadirFecha_1 = datadirFecha_1.drop(['index'], axis=1)
datadirCitID_1= datadirCitID_1.drop(['index'], axis=1)
datadirInfoAd_1= datadirInfoAd_1.drop(['index'], axis=1) 

datadirCert= datadirCert.drop(['index'], axis=1)
datadirRegis= datadirRegis.drop(['index'], axis=1)

datadirEmlVacios = datadirEmlVacios.drop(['index'], axis=1)
datadirResourceNoExiste = datadirResourceNoExiste.drop(['index'], axis=1)

#---------------------------- Une DataFrames-----------------------------------


datadirEml= datadirTitle.merge(datadirOrg.merge(datadirFecha.merge(datadirCitID.merge(datadirInfoAd, on= 'Recurso'), on='Recurso'), on='Recurso'), on= 'Recurso')

datadirEml_1= datadirTitle_1.merge(datadirOrg_1.merge(datadirFecha_1.merge(datadirCitID_1.merge(datadirInfoAd_1, on= 'Recurso'), on='Recurso'), on='Recurso'), on= 'Recurso')
datadirEml= pd.concat([datadirEml, datadirEml_1])
datadirEml.index = range(datadirEml.shape[0])

datadirResource= pd.merge(datadirCert,datadirRegis, on='Recurso')


#-------------------------Generar Datadir--------------------------------------
      

datadir=pd.DataFrame()
datadirErrores=pd.DataFrame()
datadirErrores1=pd.DataFrame()

datadir=pd.merge(datadirEml,datadirResource, on='Recurso')


datadirErrores=datadirEmlVacios.merge(datadirEml_1NoExiste.merge(datadirResourceNoExiste, on='Recurso'), on='Recurso')
datadirErrores1=datadirEmlVacios.merge(datadirEml_1NoExiste.merge(datadirResource, on='Recurso'), on='Recurso')

datadirErrores= datadirErrores.drop(['index'], axis=1)
datadirErrores1= datadirErrores1.drop(['index'], axis=1)

import numpy as np
#------------------------Creación de los substrings---------------------------
sub ='[numero]'
sub1 = '[titular]'
sub2 = '[nit o cedula]'
sub3 = '[fecha]'
#-----------------Búsqueda de los substrings dentro del string-----------------
#---------------Determinación de la posición de los elementos fijos------------

datadir["Número_del_Permiso"]= datadir["Datos permiso"].str.find(sub)
datadir["Titular_del_Permiso"]= datadir["Datos permiso"].str.find(sub1) 
datadir["NIT_o_Cédula"]= datadir["Datos permiso"].str.find(sub2) 
datadir["Fecha_de_emisión_permiso"]= datadir["Datos permiso"].str.find(sub3)

#------------------Creación de ciclos para cada elemento-----------------------
#-------------De acuerdo a la posición previamente determinada de--------------
#----------cada elemento se define el rango desde donde a donde debe ir--------

Autoridad_Ambiental = []
for i,row in datadir.iterrows():
    pos1 = datadir.at[i,"Número_del_Permiso"]
    dato = datadir.at[i,"Datos permiso"][11:pos1]
    Autoridad_Ambiental.append(dato)
    
Número_del_Permiso = []
for i,row in datadir.iterrows():
    pos1 = datadir.at[i,"Número_del_Permiso"] + 8
    pos2 = datadir.at[i,"Titular_del_Permiso"]
    dato = datadir.at[i,"Datos permiso"][pos1:pos2]
    Número_del_Permiso.append(dato)
    
Titular_del_Permiso = []
for i,row in datadir.iterrows():
    pos1 = datadir.at[i,"Titular_del_Permiso"] + 9
    pos2 = datadir.at[i,"NIT_o_Cédula"]
    dato = datadir.at[i,"Datos permiso"][pos1:pos2]
    Titular_del_Permiso.append(dato)
    
NIT_o_Cédula = []
for i,row in datadir.iterrows():
    pos1 = datadir.at[i,"NIT_o_Cédula"] + 14
    pos2 = datadir.at[i,"Fecha_de_emisión_permiso"]
    dato = datadir.at[i,"Datos permiso"][pos1:pos2]
    NIT_o_Cédula.append(dato)

Fecha_de_emisión_permiso = []
for i,row in datadir.iterrows():
    pos1 = datadir.at[i,"Fecha_de_emisión_permiso"] +7
    dato = datadir.at[i,"Datos permiso"][pos1:]
    Fecha_de_emisión_permiso.append(dato)
del datadir["Número_del_Permiso"],datadir["Titular_del_Permiso"],datadir["NIT_o_Cédula"],datadir["Fecha_de_emisión_permiso"]


datadir["Autoridad_Ambiental"] = Autoridad_Ambiental
datadir["Número_del_Permiso"] = Número_del_Permiso
datadir["Titular_del_Permiso"] = Titular_del_Permiso
datadir["NIT_o_Cédula"] = NIT_o_Cédula
datadir["Fecha_de_emisión_permiso"] = Fecha_de_emisión_permiso

del Autoridad_Ambiental, Número_del_Permiso, Titular_del_Permiso, NIT_o_Cédula, Fecha_de_emisión_permiso

#-------Se define que se complete con "No_documenta" para las celdas que se encuentran vacías---------

datadir["Autoridad_Ambiental"] = np.where(datadir["Datos permiso"] == 'No_documenta','No_documenta',datadir["Autoridad_Ambiental"])
datadir["Número_del_Permiso"] = np.where(datadir["Datos permiso"] == 'No_documenta','No_documenta',datadir["Número_del_Permiso"])
datadir["Titular_del_Permiso"] = np.where(datadir["Datos permiso"] == 'No_documenta','No_documenta',datadir["Titular_del_Permiso"])
datadir["NIT_o_Cédula"] = np.where(datadir["Datos permiso"] == 'No_documenta','No_documenta',datadir["NIT_o_Cédula"])
datadir["Fecha_de_emisión_permiso"] = np.where(datadir["Datos permiso"] == 'No_documenta','No_documenta',datadir["Fecha_de_emisión_permiso"])

#---Condicional para que solo aparezca el DOI en la columna correspondiente----
datadir["DOI"] = np.where(datadir["DOI"].str[0:8]=='10.15472',
                          datadir["DOI"].str[0:15],
                          "No_documenta")

del datadir["Datos permiso"]

datadirErrores=datadirEmlVacios.merge(datadirEml_1NoExiste.merge(datadirResourceNoExiste, on='Recurso'), on='Recurso')
datadirErrores1=datadirEmlVacios.merge(datadirEml_1NoExiste.merge(datadirResource, on='Recurso'), on='Recurso')

datadirErrores= datadirErrores.drop(['index'], axis=1)
datadirErrores1= datadirErrores1.drop(['index'], axis=1)


datadir.to_csv(r'C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python\INVENTARIO_CR_SiB.csv', encoding = "UTF-8")
datadirErrores.to_csv(r'C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python\RECURSOS_SIN_INFO_CR_SiB.csv', encoding = "UTF-8")
datadirErrores1.to_csv(r'C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python\RECURSOS_CON_INFO_PERMISO_CR_SiB.csv', encoding = "UTF-8")



