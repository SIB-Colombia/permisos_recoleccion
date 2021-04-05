# -*- coding: utf-8 -*-
"""
Editor de Spyder
Este es un archivo temporal.
"""
#Nombre de Rutina: Cuantificación del Indice de Calidad Aparente#
#Lenguaje de programación: Python (Entorno de Desarrollo: Spyder)
#Creado: 2019-07-29
#Última Actualización: 2020-06-08

#ESTA RUTINA:#

#1. Valida los parametros de calidad: Completitud, Coherencia y Precisión de los elementos y categorias DwC
#3. Determina el valor de calidad aparente para cada una de las categorías DwC
#4. Determina el índice de calidad aparente del conjunto de datos
#5. Genera los graficos comparativos de los resultados obtenidos

#REQUERIMIENTOS#

#1. los datos originales y procesados deben estar en formato Excel (xls. o xlsx.).
#2. Los datos originales y procesados deben estar documentados bajo los estandares Darwin Core (DwC)
#3. Se deben aplicar  previamente a los datos las siguientes rutinas de validación en OpenRefine
  
   #Validación Taxonomica: https://github.com/SIB-Colombia/data-quality-open-refine/blob/master/ValTaxonomicAPIGBIF_ValTaxonomicaAPIGBIF.txt#
   #Validación de nombres Geograficos: https://github.com/SIB-Colombia/data-quality-open-refine/blob/master/ValNamesGeo_ValNombresGeo.txt#
   #Conversión de Fechas: https://github.com/SIB-Colombia/data-quality-open-refine/blob/master/DateTransform_TransformFechas.txt#
   #Validación QGIS(Creación de columna 'countyValidation'): Validación de la coherencia de las coordenadas con la informacion geografica superiror registrada#

#4.Asegurese que los datos de entrada y salida tengan las siguientes columnas como minimo (48):
   
   #occurrenceID, basisOfRecord, institutionCode, collectionCode, institutionID, collectionID, catalogNumber, 
   #otherCatalogNumbers,preparations, recordedBy, geodeticDatum, minimumElevationInMeters, maximumElevationInMeters, 
   #eventDate, eventDateISO, year, month, day, decimalLatitude, decimalLongitude, country, stateProvince, county, municipality, locality, 
   #countyValidation, countyValiationDIVIPOLA, stateProvinceValidationDIVIPOLA, municipalityValidationDIVIPOLA
   #taxonRank, scientifiName, kingdom, phylum, class, order, family, genus, specificEpithet, infraspecificEpithet
   #taxonRankSuggested, taxonMatchType, kingdomValidation, phylumValidation, classValidation, orderValidation, familyValidation, genusValidation, specificEpithetValidation#

#PROCEDIMEINTOS PREVIOS A REALIZAR EL SCRIPT#
   
#1. Remplace las rutas de los datos originales y procesados que seran validados y comparados:
   
   #Ruta de Almacenamiento: Realice el siguiente procedimiento#
   
   #Utilice la herramienta "Buscar">"Reemplazar Texto", ubicada en el panel de herramientas superior
   #Busque: ...
   #Reemplazar: Digite la Ruta donde se almacenara la carpeta con resultados" Ejemplo: C:\Users\Javier Murillo\Documents
   #Seleccione: Reemplazar todo
   
#2. Nombre de la Carpeta de Resultados: Realice el siguiente procedimiento#
   
   #Utilice la herramienta "Buscar">"Reemplazar Texto", ubicada en el panel de herramientas superior
   #Busque: .-.
   #Reemplazar: Digite el nombre de la carpeta donde almacenara los resultados" Ejemplo: Resultados SiB Colombia
   #Asegurese que no exista una carpeta con el mismo nombre en la ruta de almacenamiento#
   #Seleccione: Reemplazar todo
   
#3. Ejecute el Codigo con el boton "Ejecutar Archivo (f5)", ubicado en el panel de herramientas superior

#RESULTADOS#  
   
#Los resultado de la validación seran almacenados en diferentes Dataframes# 
   
 # DataFrame (daf3E): Parametros de calidad por elemento DwC, Datos Originales
 # DataFrame (daf4E): Parametros de calidad por Categoría DwC, Datos Originales 
 # DataFrame (daf5E): Calidad Aparente para cada Categoría DwC y de los datos en su totalidad, Datos Originales
 # DataFrame (daf3S): Parametros de calidad por elemento DwC, Datos Procesados
 # DataFrame (daf4S): Parametros de calidad por Categoría DwC, Datos Procesados
 # DataFrame (daf5S): Calidad Aparente para cada Categoría DwC y del datos en su totalidad, Datos Procesados
 # DataFrame (daf5A):Calidad Aparente para cada Categoría DwC y del datos en su totalidad, comparativo Datos Originales vs Datos Procesados

# IMPORTAR HERRAMIENTAS DE MANEJO DE DATOS#
 
#Paquetes#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# PROCEDIMIENTO DE CARGA DE LOS DATOS#

#Reemplace Ruta_Datos_Originales con: la ruta correspondiente a donde estan almacenados los datos originales (antes del proceso de limpieza y validación)#
#Ejemplo Ruta_Datos_Originales: C:\Users\Javier Murillo\Documents

#Reemplace Nombre_Archivo_Original con: el nombre del archivo excel con los datos originales#
#Verifique La extencion del formato (.xls o .xlsx), de ser necesario Reemplace el .xls con .xlsx, en la linea de codificación
#Ejemplo Nombre de Archivo: Datos Biologicos

#Ejemplo Linea de codificación: 
# datosEntrada= pd.read_excel(r"C:\Users\Javier Murillo\Documents\Datos Biologicos.xls", header=0)

datosEntrada= pd.read_excel(r"Ruta_Datos_Originales\Nombre_Archivo_Original.xls", header=0)

#Reemplace Ruta_Datos_Salida con: la ruta correspondientea donde estan almacenados los datos procesados (despues del proceso de limpieza y validación)#
#Ejemplo Ruta_Datos_Salida: C:\Users\Javier Murillo\Documents

#Reemplace Nombre_Archivo_Procesado con: el nombre del archivo excel con los datos procesados#
#Verifique La extencion del formato (.xls o .xlsx), de ser necesario Reemplace el .xls con .xlsx, en la linea de codificación
#Ejemplo Nombre de Archivo: Datos Biologicos Validado

#Ejemplo Linea de codificacióm: 
# datosSalida= pd.read_excel(r"C:\Users\Javier Murillo\Documents\Datos Biologicos Validado.xls", header=0)

datosSalida= pd.read_excel(r"Ruta_Datos_Salida\Nombre_Archivo_Procesado.xls", header=0)


#ALMACENAMIENTO DE DATOS ORIGINALES Y PROCESADOS EN DATAFRAMES#

#daf1E: Datos originales de entrada# 
#daf1S: Datos depurados de salida#

daf1E=pd.DataFrame(datosEntrada)
daf1S=pd.DataFrame(datosSalida)

#Script: Datos Originales#

#RBT:Cantitdad Total de Registros originales#
RBT= daf1E.shape[0]

#ALMACENAMIENTO DE CALCULOS PARA DETERMINAR EL VALOR DE LOS PARAMETROS DE CALIDAD 
#PARA CADA REGISTRO DE LOS DATOS ORIGINALES#

#daf2E: Resultados de los calculos de los parametros de calidad.
Index= daf1E['occurrenceID']
daf2E=pd.DataFrame(Index)

#ALMACENAMIENTO DE LOS RESULTADOS DE LA VALORACION DE LOS PARAMETROS DE CALIDAD 
#POR ELEMENTO DwC PARA LOS DATOS ORIGINALES#

#daf3E: Parametros de Calidad a nivel de Elemento DwC para los datos originales 
ElementoDwC = {'Elemento DwC':["occurrenceID", "basisOfRecord", "institutionCode", "collectionCode", "institutionID", "collectionID", "catalogNumber", "otherCatalogNumbers","preparations", "recordedBy", "geodeticDatum", "minimumElevationInMeters", "maximumElevationInMeters", "eventDate", "decimalLatitude", "decimalLongitude", "country", "stateProvince", "county", "municipality", "locality", "Georreferenciación", "taxonRank", "scientifiName", "kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "infraspecificEpithet"]}
daf3E= pd.DataFrame(ElementoDwC)
daf3E['Completitud']= ""
daf3E['Precisión']= ""
daf3E['Coherencia']= ""

#COMPLETITUD DE LOS ELEMENTOS DwC PARA LOS DATOS ORIGINALES#

#COI:Completitud occurrenceID# 
COI =daf1E.occurrenceID.isnull().sum()
daf3E.loc[0, 'Completitud'] = ((RBT-COI)*100)/RBT

#CBR:Completitud basisOfRecord#
CBR =daf1E.basisOfRecord.isnull().sum()
daf3E.loc[1, 'Completitud'] = ((RBT-CBR)*100)/RBT

#CICO:Completitud institutionCode#
CICO =daf1E.institutionCode.isnull().sum()
daf3E.loc[2, 'Completitud'] = ((RBT-CICO)*100)/RBT

#CCOCO:Completitud collectionCode#
CCOCO =daf1E.collectionCode.isnull().sum()
daf3E.loc[3, 'Completitud'] = ((RBT-CCOCO)*100)/RBT

#CIID:Completitud institutionID#
CIID =daf1E.institutionID.isnull().sum()
daf3E.loc[4, 'Completitud'] = ((RBT-CIID)*100)/RBT

#CCID:Completitud collectionID#
CCID =daf1E.collectionID.isnull().sum()
daf3E.loc[5, 'Completitud'] = ((RBT-CCID)*100)/RBT

#CCN:Completitud catalogNumber#
CCN =daf1E.catalogNumber.isnull().sum()
daf3E.loc[6, 'Completitud'] = ((RBT-CCN)*100)/RBT

#COCN:Completitud otherCatalogNumbers#
COCN =daf1E.otherCatalogNumbers.isnull().sum()
daf3E.loc[7, 'Completitud'] = ((RBT-COCN)*100)/RBT

#CPR:Completitud preparations#
CPR =daf1E.preparations.isnull().sum()
daf3E.loc[8, 'Completitud'] = ((RBT-CPR)*100)/RBT

#CRB:Completitud recordedBy#
CRB =daf1E.recordedBy.isnull().sum()
daf3E.loc[9, 'Completitud'] = ((RBT-CRB)*100)/RBT

#CGD:Completitud geodeticDatum#
CGD =daf1E.geodeticDatum.isnull().sum()
daf3E.loc[10, 'Completitud'] = ((RBT-CGD)*100)/RBT

#CMIE:Completitud minimumElevatinInMeters#
CMIE =daf1E.minimumElevationInMeters.isnull().sum()
daf3E.loc[11, 'Completitud'] = ((RBT-CMIE)*100)/RBT

#CMAE:Completitud maximumElevatinInMeters#
CMAE =daf1E.maximumElevationInMeters.isnull().sum()
daf3E.loc[12, 'Completitud'] = ((RBT-CMAE)*100)/RBT

#CEV:Completitud eventDate#
CEV =daf1E.eventDate.isnull().sum()
daf3E.loc[13, 'Completitud'] = ((RBT-CEV)*100)/RBT

#CDLA:Completitud decimalLatitude#
CDLA =daf1E.decimalLatitude.isnull().sum()
daf3E.loc[14, 'Completitud'] = ((RBT-CDLA)*100)/RBT

#CDLO:Completitud decimalLongitude#
CDLO =daf1E.decimalLongitude.isnull().sum()
daf3E.loc[15, 'Completitud'] = ((RBT-CDLO)*100)/RBT

#CCP:Completitud country#
CCP =daf1E.country.isnull().sum()
daf3E.loc[16, 'Completitud'] = ((RBT-CCP)*100)/RBT

#CSP:Completitud stateProvince#
CSP =daf1E.stateProvince.isnull().sum()
daf3E.loc[17, 'Completitud'] = ((RBT-CSP)*100)/RBT

#CCM:Completitud county#
CCM =daf1E.county.isnull().sum()
daf3E.loc[18, 'Completitud'] = ((RBT-CCM)*100)/RBT

#CM:Completitud municipality#
CM =daf1E.municipality.isnull().sum()
daf3E.loc[19, 'Completitud'] = ((RBT-CM)*100)/RBT

#CLO:Completitud locality#
CLO =daf1E.locality.isnull().sum()
daf3E.loc[20, 'Completitud'] = ((RBT-CLO)*100)/RBT

#CTR:Completitud taxonRank#
CTR =daf1E.taxonRank.isnull().sum()
daf3E.loc[22, 'Completitud'] = ((RBT-CTR)*100)/RBT

#CSNM:Completitud scientificName#
CSNM =daf1E.scientificName.isnull().sum()
daf3E.loc[23, 'Completitud'] = ((RBT-CSNM)*100)/RBT

#CK:Completitud kingdom#
CK =daf1E.kingdom.isnull().sum()
daf3E.loc[24, 'Completitud'] = ((RBT-CK)*100)/RBT

#CPH:Completitud phylum#
CPH=daf1E.phylum.isnull().sum()
daf3E.loc[25, 'Completitud'] = ((RBT-CPH)*100)/RBT

#CCL:Completitud class#
CCL =daf1E['class'].isnull().sum()
daf3E.loc[26, 'Completitud'] = ((RBT-CCL)*100)/RBT

#CO:Completitud order#
CO =daf1E.order.isnull().sum()
daf3E.loc[27, 'Completitud'] = ((RBT-CO)*100)/RBT

#CF:Completitud family#
CF =daf1E.family.isnull().sum()
daf3E.loc[28, 'Completitud'] = ((RBT-CF)*100)/RBT

#CG:Completitud genus#
CG =daf1E.genus.isnull().sum()
daf3E.loc[29, 'Completitud'] = ((RBT-CG)*100)/RBT

#CSE:Completitud specificEpithet#
CSE =daf1E.specificEpithet.isnull().sum()
daf3E.loc[30, 'Completitud'] = ((RBT-CSE)*100)/RBT

#CISE:Completitud infraspecificEpithet#
CISE =daf1E.infraspecificEpithet.isnull().sum()
daf3E.loc[31, 'Completitud'] = ((RBT-CISE)*100)/RBT

#COHERENCIA DE LOS ELEMENTOS DwC PARA LOS DATOS ORIGINALES#

#CohOI:Coherencia occurrenceID#
Duplicados= daf1E.occurrenceID.duplicated().sum() 
if Duplicados >= 1: 
    CohOI=0
else:
    CohOI=1
daf3E.loc[0, "Coherencia"]=(CohOI)

#CBOR:Coherencia basisOfRecord(2013)#
def CBOR(x):
    if (x) == ("Espécimen preservado"):
       CBOR=1
    elif (x) == ("Muestra del espécimen"):
       CBOR=1
    elif (x) == ("Espécimen vivo"):
       CBOR=1
    elif (x) == ("PreservedSpecimen"):
       CBOR=1
    elif (x) == ("FossilSpecimen"):
       CBOR=1
    elif (x) == ("LivingSpecimen"):
       CBOR=1
    elif (x) == ("HumanObservation"):
       CBOR=1
    elif (x) == ("MachineObservation"):
       CBOR=1
    elif (x) == ("Sample"):
       CBOR=1
    elif (x) == ("nan"):
       CBOR=0
    else:
       CBOR=0
    return (CBOR)

daf2E['CBOR'] = daf1E["basisOfRecord"].apply(CBOR)
daf3E.loc[1, "Coherencia"]= daf2E['CBOR'].mean()

#Coherencia de formato institutionID(NIT)#
#Valida la correspondencia de la cantidad de puntos y el guion en el formato de NIT#
daf1E['institutionID'].fillna(0.0, inplace=True)

def VPuntos(x):
    if x.find(".")==0:
            VPuntos=0
    elif x.find(".")<2:
            VPuntos=0
    else:
            VPuntos=1
    return VPuntos

daf2E['puntosNIT'] = daf1E["institutionID"].apply(VPuntos)

def VGuion(x):
    if x.find("-")==0:
            VGuion=0
    elif x.find("-")<1:
            VGuion=0
    else:
            VGuion=1
    return VGuion

daf2E['guionNIT'] = daf1E["institutionID"].apply(VGuion)
daf2E['NIT'] = daf2E['puntosNIT']*daf2E['guionNIT']

def CohNIT(x):
    if x==1:
        cohNIT=1
    else:
        cohNIT=0
    return cohNIT

daf2E['CohNIT'] = daf2E['NIT'].apply(CohNIT)
daf3E.loc[4, "Coherencia"]= daf2E['CohNIT'].mean()
    
#CFED:Coherencia de Formato eventDate" 
daf1E['eventDateISO'].fillna(0, inplace=True)  
   
def CFED(x):
    if (x) == 0:
       VED= 0
    else:
       VED= 1   
    return VED

daf2E['CFED'] = daf1E["eventDateISO"].apply(CFED)
daf3E.loc[13, "Coherencia"]= daf2E['CFED'].mean()

#Para la valoracion de coherencia de los siguientes parametros, es necesario restar
#del total de los registros los valores nulos para que se realice el calculo estipulado.

#Coherencia Formato Coordenadas#
daf3E.loc[14, "Coherencia"]= (RBT-(daf1E.countyValidation.isnull().sum()))/(RBT)
daf3E.loc[15, "Coherencia"]= (RBT-(daf1E.countyValidation.isnull().sum()))/(RBT)

#Coherencia stateProvince"
daf3E.loc[17, "Coherencia"] = ((list(daf1E['stateProvinceValidationDIVIPOLA'])).count(1))/(RBT-(daf1E.stateProvinceValidationDIVIPOLA.isnull().sum()))

#Coherencia county#
daf3E.loc[18, "Coherencia"] = ((list(daf1E['countyValidationDIVIPOLA'])).count(1))/(RBT-(daf1E.countyValidationDIVIPOLA.isnull().sum()))

#Coherencia municipality#
daf1E['municipalityValidationDIVIPOLA'].fillna(0, inplace=True) 
daf3E.loc[19, "Coherencia"] = ((list(daf1E['municipalityValidationDIVIPOLA'])).count(1))/(RBT-(daf1E.municipalityValidationDIVIPOLA.isnull().sum()))

#Coherencia countyValidation#
daf3E.loc[21, "Coherencia"] = ((list(daf1E['countyValidation'])).count(1))/(RBT-(daf1E.countyValidation.isnull().sum()))

#CVTR:Coherencia del vocabulario de taxonRank#
def CVTR(x):
    if (x) == ("Especie"):
       CTR=1
    elif (x) == ("Subespecie"):
       CTR=1
    elif (x) == ("Variedad"):
       CTR=1
    elif (x) == ("Subvariedad"):
       CTR=1
    elif (x) == ("Forma"):
       CTR=1
    elif (x) == ("Subforma"):
       CTR=1
    elif (x) == ("Género"):
       CTR=0.85
    elif (x) == ("Genero"):
       CTR=0.85
    elif (x) == ("Subgénero"):
       CTR=0.85
    elif (x) == ("Sección"):
       CTR=0.85
    elif (x) == ("Subsección"):
       CTR=0.85
    elif (x) == ("Serie"):
       CTR=0.85
    elif (x) == ("Subserie"):
       CTR=0.85
    elif (x) == ("Familia"):
       CTR=0.7
    elif (x) == ("Subfamilia"):
       CTR=0.7
    elif (x) == ("Tribu"):
       CTR=0.7
    elif (x) == ("Subtribu"):
       CTR=0.7
    elif (x) == ("Orden"):
       CTR=0.6
    elif (x) == ("Suborden"):
       CTR=0.6
    elif (x) == ("Clase"):
       CTR=0.45
    elif (x) == ("Subclase"):
       CTR=0.45
    elif (x) == ("Filo"):
       CTR=0.3
    elif (x) == ("División"):
       CTR=0.3
    elif (x) == ("Subfilo"):
       CTR=0.3
    elif (x) == ("Subdivisión"):
       CTR=0.3
    elif (x) == ("Reino"):
       CTR=0.15
    elif (x) == ("Subreino"):
       CTR=0.15
    elif (x) == ("nan"):
       CTR= 0
    else:
       CTR= 0
    return (CTR)

daf2E['CVTR'] = daf1E["taxonRank"].apply(CVTR)
daf3E.loc[22, "Coherencia"]= daf2E['CVTR'].mean()

#CohSNM:Coherencia scientificName"
def CohSNM(x):
    if (x) == ("EXACT"):
       CohSNM=1
    elif (x) == ("FUZZY"):
       CohSNM=0.6
    elif (x) == ("HIGHERRANK"):
       CohSNM=0.3
    elif (x) == ("NONE"):
       CohSNM=0
    else:
       CohSNM=0
    return (CohSNM)

daf2E['CohSNM'] = daf1E["taxonMatchType"].apply(CohSNM)
daf3E.loc[23, "Coherencia"]= daf2E['CohSNM'].mean()

#Para la valoracion de coherencia de los siguientes parametros, es necesario restar
#del total de los registros los valores nulos para que se realice el calculo estipulado.

#Coherencia kingdom"
daf3E.loc[24, "Coherencia"] = ((list(daf1E['kingdomValidation'])).count(1))/((RBT)-(daf1E.kingdomValidation.isnull().sum()))

#Coherencia phylum"
daf3E.loc[25, "Coherencia"] = ((list(daf1E['phylumValidation'])).count(1))/((RBT)-(daf1E.phylumValidation.isnull().sum()))

#Coherencia class"
daf3E.loc[26, "Coherencia"] = ((list(daf1E['classValidation'])).count(1))/((RBT)-(daf1E.classValidation.isnull().sum()))

#Coherencia order"
daf3E.loc[27, "Coherencia"] = ((list(daf1E['orderValidation'])).count(1))/((RBT)-(daf1E.orderValidation.isnull().sum()))

#Coherencia family"
daf3E.loc[28, "Coherencia"] = ((list(daf1E['familyValidation'])).count(1))/((RBT)-(daf1E.familyValidation.isnull().sum()))

#Coherencia genus"
daf3E.loc[29, "Coherencia"] = ((list(daf1E['genusValidation'])).count(1))/((RBT)-(daf1E.genusValidation.isnull().sum()))

#Coherencia specificEpithet"
daf3E.loc[30, "Coherencia"] = ((list(daf1E['specificEpithetValidation'])).count(1))/((RBT)-(daf1E.specificEpithetValidation.isnull().sum()))
daf3E["Coherencia"].fillna(0.0, inplace=True)

#PRECISIÓN DE LOS ELEMENTOS DwC PARA LOS DATOS ORIGINALES"

#Precisión eventDate" 
#se ejecuta la asignacion de un valor a cada componente de fecha (año, mes y dia)
#si estos cumplen con la condicion de formato. Si no asigna "0". Posteriormente se suman
#los valores y se obtiene el valor de precision para el formato de fecha

#AÑO#
daf1E['year'].fillna(0, inplace=True)
def AAAA(x):
    return str(x)

daf2E['AAAA']= daf1E['year'].apply(AAAA)

def QZero(x):
    QZ= x.replace(".0","")
    return QZ

daf2E['AAAA']=daf2E['AAAA'].apply(QZero)

def PAED(x):
    if (x) == 0:
        PAED = 0
    elif len(x) == 4:
       PAED= 0.1  
    else:
       PAED= 0
    return PAED

daf2E['PAED'] = daf2E["AAAA"].apply(PAED)

#MES#
daf1E['month'].fillna(0, inplace=True)
def MM(x):
    return str(x)

daf2E['MM']= daf1E['month'].apply(MM)
daf2E['MM']=daf2E['MM'].apply(QZero)

def PMED(x):
    if (x) == "0":
        PMED = 0
    elif len(x) == 2:
       PMED = 0.5
    elif len(x) == 1:
       PMED = 0.5
    else:
       PMED = 0     
    return PMED

daf2E['PMED'] = daf2E["MM"].apply(PMED)

#DIA#
daf1E['day'].fillna(0, inplace=True)

def DD(x):
    return str(x)

daf2E['DD']= daf1E['day'].apply(DD)
daf2E['DD']=daf2E['DD'].apply(QZero)

def PDED(x):
    if (x) == "0":
        PDED = 0
    elif len(x) <= 2:
       PDED= 0.4
    else:
       PDED= 0   
    return PDED

daf2E['PDED'] = daf2E["DD"].apply(PDED)
  

daf2E['PED']= daf2E['PAED']+ daf2E['PMED'] + daf2E['PDED']
daf3E.loc[13, 'Precisión']= daf2E['PED'].mean()

#Precision Numerica Coordenadas Latitud"
daf1E['decimalLatitude'].fillna(0.0, inplace=True)

def SCDLa(x):
    return str(x)

daf2E['decStrLa'] = daf1E["decimalLatitude"].apply(SCDLa)

def CDLa(x):
    if x == "0.0":
       CDLa = 0
    elif x.find(".") < 1:
       CDLa = 0
    else:
        CDLa = ((x.split("."))[1])
    return CDLa

daf2E['decimalesLatitude'] = daf2E["decStrLa"].apply(CDLa)

def PNLat(x):
    if x == 0:
       PNLa = 0 
    elif len(x) >=4:
       PNLa=1
    elif len(x) ==3:
       PNLa=0.6
    elif len(x) <=2:
       PNLa=0.2
    else:
       PNLa=0
    return PNLa

daf2E['PNLat'] = daf2E["decimalesLatitude"].apply(PNLat)
daf3E.loc[14, 'Precisión']= daf2E['PNLat'].mean()

#Precision Numerica Coordenadas Longitud"
daf1E['decimalLongitude'].fillna(0.0, inplace=True)

def SCDLo(x):
    return str(x)

daf2E['decStrLo'] = daf1E["decimalLongitude"].apply(SCDLo)

def CDLo(x):
    if x == "0.0":
       CDLo = 0
    elif x.find(".") < 1:
       CDLo = 0
    else:
        CDLo = ((x.split("."))[1])
    return CDLo

daf2E['decimalesLongitud'] = daf2E["decStrLo"].apply(CDLo)

def PNLon(x):
    if x == 0:
       PNLo = 0 
    elif len(x) >=4:
       PNLo=1
    elif len(x) ==3:
       PNLo=0.6
    elif len(x) <=2:
       PNLo=0.2
    else:
       PNLo=0
    return PNLo

daf2E['PNLon'] = daf2E["decimalesLongitud"].apply(PNLon)
daf3E.loc[15, 'Precisión']= daf2E['PNLon'].mean()

#Precision taxonRank#
def Traduccion(x):
    if (x) == 'SPECIES':
        TRA= "Especie"
    elif (x) == 'GENUS':
        TRA= "Género"
    elif (x) == 'FAMILY':
        TRA= "Familia"
    elif (x) == 'ORDER':
        TRA= "Orden"
    elif (x) == 'CLASS':
        TRA= "Clase"
    elif (x) == 'PHYLUM':
        TRA= "Filo"
    elif (x) == 'KINGDOM':
        TRA= "Reino"
    elif (x) == 'Species':
        TRA= "Especie"
    elif (x) == 'Genus':
        TRA= "Género"
    elif (x) == 'Family':
        TRA= "Familia"
    elif (x) == 'Order':
        TRA= "Orden"
    elif (x) == 'Class':
        TRA= "Clase"
    elif (x) == 'Phylum':
        TRA= "Filo"
    elif (x) == 'Kingdom':
        TRA= "Reino"
    else:
        TRA= 0
    return  (TRA)

daf1E['TRTRA']= daf1E['taxonRankSuggested'].apply(Traduccion)
    
TRS=daf1E['TRTRA']
TR=daf1E['taxonRank']
daf2E['PTRR']= np.where(daf1E['TRTRA'] == daf1E['taxonRank'], 1, 0)
daf3E.loc[22, 'Precisión']= daf2E['PTRR'].mean()

#PSNM:Precision scientificName"
def PSNM(x):
    if (x) == ("Especie"):
       PSNM=1
    elif (x) == ("Género"):
       PSNM=0.85
    elif (x) == ("Familia"):
       PSNM=0.7
    elif (x) == ("Orden"):
       PSNM=0.6
    elif (x) == ("Clase"):
       PSNM=0.45
    elif (x) == ("Filo"):
       PSNM=0.3
    elif (x) == ("Reino"):
       PSNM=0.15
    else:
       PSNM=0
    return (PSNM)

daf2E['PSNM'] = daf1E["TRTRA"].apply(PSNM)
daf3E.loc[23, "Precisión"] = daf2E['PSNM'].mean()

#CÁLCULO DE PARAMETROS DE CALIDAD POR CATEGORIA DwC PARA LOS DATOS ORIGINALES#

#DataFrame 4E: Parametros de calidad por Categoría DwC paa los datos originales#
Ejes={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica"]}
daf4E= pd.DataFrame(Ejes)
daf4E['Completitud']= ""
daf4E['Precisión']= ""
daf4E['Coherencia']= ""

#Categoría DwC Registro#
#Completitud Categoría DwC Registro#
daf4E.loc[0, 'Completitud']= ((daf3E.loc[0, "Completitud"])+(daf3E.loc[1, "Completitud"])+(daf3E.loc[2, "Completitud"])+(daf3E.loc[3, "Completitud"])+(daf3E.loc[4, "Completitud"])+(daf3E.loc[5, "Completitud"])+(daf3E.loc[6, "Completitud"])+(daf3E.loc[7, "Completitud"])+(daf3E.loc[8, "Completitud"])+(daf3E.loc[9, "Completitud"]))/(10)

#Coherencia#
daf4E.loc[0, "Coherencia"]= ((daf3E.loc[0, "Coherencia"])*0.6)+((daf3E.loc[4, "Coherencia"])*0.2)+((daf3E.loc[1, "Coherencia"])*0.2)

#Categoría DwC TEMPORAL"
#Completitud Categoría DwC temporal#
daf4E.loc[1, 'Completitud']= daf3E.loc[13, "Completitud"]

#Precisión Categoría DwC temporal#
daf4E.loc[1, 'Precisión']= daf3E.loc[13, "Precisión"]

#Coherencia Categoría DwC temporal"
daf4E.loc[1, 'Coherencia']= daf3E.loc[13, "Coherencia"]

#Categoría DwC Geográfica#
#Completitud Categoría DwC Geográfica#
daf4E.loc[2, 'Completitud']= ((daf3E.loc[10, "Completitud"])+(daf3E.loc[11, "Completitud"])+(daf3E.loc[12, "Completitud"])+(daf3E.loc[14, "Completitud"])+(daf3E.loc[15, "Completitud"])+(daf3E.loc[16, "Completitud"])+(daf3E.loc[17,"Completitud"])+(daf3E.loc[18, "Completitud"])+(daf3E.loc[19, "Completitud"])+(daf3E.loc[20, "Completitud"]))/(10)

#Precisión Categoría DwC Geográfica#
daf4E.loc[2, 'Precisión']= ((daf3E.loc[14, "Precisión"])*0.5)+((daf3E.loc[15, "Precisión"])*0.5)

#Coherencia Categoría DwC Geográfica"
daf4E.loc[2, 'Coherencia']= ((daf3E.loc[21, "Coherencia"])*0.5)+((daf3E.loc[17, "Coherencia"])*0.15)+((daf3E.loc[18, "Coherencia"])*0.15)+((daf3E.loc[19, "Coherencia"])*0.1)+((daf3E.loc[14, "Coherencia"])*0.05)+((daf3E.loc[15, "Coherencia"])*0.05)

#Categoría DwC TAXONÓMICA#
#Completitud Categoría DwC Taxonómica#
daf4E.loc[3, 'Completitud']= ((daf3E.loc[22, "Completitud"])+(daf3E.loc[23, "Completitud"])+(daf3E.loc[24, "Completitud"])+(daf3E.loc[25,"Completitud"])+(daf3E.loc[26, "Completitud"])+(daf3E.loc[27, "Completitud"])+(daf3E.loc[28, "Completitud"])+(daf3E.loc[29, "Completitud"])+(daf3E.loc[30, "Completitud"])+(daf3E.loc[31, "Completitud"]))/(10)

#Precisión Categoría DwC Taxonómica#
daf4E.loc[3, 'Precisión']= ((daf3E.loc[23, "Precisión"])*0.6)+((daf3E.loc[22, "Precisión"])*0.4)

#Coherencia Categoría DwC Taxonómica"
daf4E.loc[3, 'Coherencia']= (((daf3E.loc[23, "Coherencia"])*0.4)+((daf3E.loc[22, "Coherencia"])*0.25)+((daf3E.loc[24, "Coherencia"])*0.05)+((daf3E.loc[25, "Coherencia"])*0.05)+((daf3E.loc[26, "Coherencia"])*0.05)+((daf3E.loc[27, "Coherencia"])*0.05)+((daf3E.loc[28, "Coherencia"])*0.05)+((daf3E.loc[29, "Coherencia"])*0.05)+((daf3E.loc[30, "Coherencia"])*0.05))

#DataFrame 5: Calidad Aparente para cada Categoría"
Ejes={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica", "Conjunto Datos"]}
daf5E= pd.DataFrame(Ejes)
daf5E['Calidad Aparente']=""

#CÁLCULO DE CALIDAD APARENTE POR CATEGORIA DwC#

#Categoría DwC Registro#
daf5E.loc[0, "Calidad Aparente"]= (((daf4E.loc[0, "Completitud"])*0.8)/100)+((daf4E.loc[0, "Coherencia"])*0.2)

#Categoría DwC Temporal
daf5E.loc[1, "Calidad Aparente"]= ((daf4E.loc[1, "Precisión"])*0.5)+(((daf4E.loc[1, "Completitud"])*0.3)/100)+((daf4E.loc[1, "Coherencia"])*0.2)

#Categoría DwC Geográfica"
daf5E.loc[2, "Calidad Aparente"]= ((daf4E.loc[2, "Precisión"])*0.2)+(((daf4E.loc[2, "Completitud"])*0.2)/100)+((daf4E.loc[2, "Coherencia"])*0.6)

#Categoría DwC Taxonómica#
daf5E.loc[3, "Calidad Aparente"]= ((daf4E.loc[3, "Precisión"])*0.35)+(((daf4E.loc[3, "Completitud"])*0.3)/100)+((daf4E.loc[3, "Coherencia"])*0.35)

#Calidad Aparente del Conjunto Datos#
daf5E.loc[4, "Calidad Aparente"]= ((daf5E.loc[0, "Calidad Aparente"])*0.15)+((daf5E.loc[1, "Calidad Aparente"])*0.2)+((daf5E.loc[2, "Calidad Aparente"])*0.3)+((daf5E.loc[3, "Calidad Aparente"])*0.35)


#Script: Datos Procesados, posterior a la validacion y limpieza de los datos#

#Cantitdad Total de Registros#
RBTs= daf1S.shape[0]

#DataFrame 2: Calculo de paramteros de calidad para cada Registro#
Indexs= daf1S['occurrenceID']
daf2S=pd.DataFrame(Indexs)

#DataFrame 3:Parametros de calidad por elemento DwC#
ElementoDwC = {'Elemento DwC':["occurrenceID", "basisOfRecord", "institutionCode", "collectionCode", "institutionID", "collectionID", "catalogNumber", "otherCatalogNumbers","preparations", "recordedBy", "geodeticDatum", "minimumElevationInMeters", "maximumElevationInMeters", "eventDate", "decimalLatitude", "decimalLongitude", "country", "stateProvince", "county", "municipality", "locality", "Georreferenciación", "taxonRank", "scientifiName", "kingdom", "phylum", "class", "order", "family", "genus", "specificEpithet", "infraspecificEpithet"]}
daf3S= pd.DataFrame(ElementoDwC)
daf3S['Completitud']= ""
daf3S['Precisión']= ""
daf3S['Coherencia']= ""

#CÁLCULO DE LOS PARAMETROS DE CALIDAD PARA LOS ELEMENTOS DwC DE LOS DATOS DEPURADOS# 

#COMPLETITUD DE LOS ELEMENTOS DwC PARA LOS DATOS DEPURADOS#

#Completitud occurrenceID# 
COIs =daf1S.occurrenceID.isnull().sum()
daf3S.loc[0, 'Completitud'] = ((RBT-COIs)*100)/RBT

#Completitud basisOfRecord#
CBRs =daf1S.basisOfRecord.isnull().sum()
daf3S.loc[1, 'Completitud'] = ((RBT-CBRs)*100)/RBT

#Completitud institutionCode#
CICOs =daf1S.institutionCode.isnull().sum()
daf3S.loc[2, 'Completitud'] = ((RBT-CICOs)*100)/RBT

#Completitud collectionCode#
CCOCOs =daf1S.collectionCode.isnull().sum()
daf3S.loc[3, 'Completitud'] = ((RBT-CCOCOs)*100)/RBT

#Completitud institutionID#
CIIDs =daf1S.institutionID.isnull().sum()
daf3S.loc[4, 'Completitud'] = ((RBT-CIIDs)*100)/RBT

#Completitud collectionID#
CCID =daf1S.collectionID.isnull().sum()
daf3S.loc[5, 'Completitud'] = ((RBT-CCID)*100)/RBT

#Completitud catalogNumber#
CCNs =daf1S.catalogNumber.isnull().sum()
daf3S.loc[6, 'Completitud'] = ((RBT-CCNs)*100)/RBT

#Completitud otherCatalogNumbers#
COCNs =daf1S.otherCatalogNumbers.isnull().sum()
daf3S.loc[7, 'Completitud'] = ((RBT-COCNs)*100)/RBT

#Completitud preparations#
CPRs =daf1S.preparations.isnull().sum()
daf3S.loc[8, 'Completitud'] = ((RBT-CPRs)*100)/RBT

#Completitud recordedBy#
CRBs =daf1S.recordedBy.isnull().sum()
daf3S.loc[9, 'Completitud'] = ((RBT-CRBs)*100)/RBT

#Completitud geodeticDatum#
CGDs =daf1S.geodeticDatum.isnull().sum()
daf3S.loc[10, 'Completitud'] = ((RBT-CGDs)*100)/RBT

#Completitud minimumElevatinInMeters#
CMIEs =daf1S.minimumElevationInMeters.isnull().sum()
daf3S.loc[11, 'Completitud'] = ((RBT-CMIEs)*100)/RBT

#Completitud maximumElevatinInMeters#
CMAEs =daf1S.maximumElevationInMeters.isnull().sum()
daf3S.loc[12, 'Completitud'] = ((RBT-CMAEs)*100)/RBT

#Completitud eventDate#
CEVs =daf1S.eventDate.isnull().sum()
daf3S.loc[13, 'Completitud'] = ((RBT-CEVs)*100)/RBT

#Completitud decimalLatitude#
CDLAs =daf1S.decimalLatitude.isnull().sum()
daf3S.loc[14, 'Completitud'] = ((RBT-CDLAs)*100)/RBT

#Completitud decimalLongitude#
CDLOs =daf1S.decimalLongitude.isnull().sum()
daf3S.loc[15, 'Completitud'] = ((RBT-CDLOs)*100)/RBT

#Completitud country#
CCPs =daf1S.country.isnull().sum()
daf3S.loc[16, 'Completitud'] = ((RBT-CCPs)*100)/RBT

#Completitud stateProvince#
CSPs =daf1S.stateProvince.isnull().sum()
daf3S.loc[17, 'Completitud'] = ((RBT-CSPs)*100)/RBT

#Completitud county#
CCMs =daf1S.county.isnull().sum()
daf3S.loc[18, 'Completitud'] = ((RBT-CCMs)*100)/RBT

#Completitud municipality#
CMs =daf1S.municipality.isnull().sum()
daf3S.loc[19, 'Completitud'] = ((RBT-CMs)*100)/RBT

#Completitud locality#
CLOs =daf1S.locality.isnull().sum()
daf3S.loc[20, 'Completitud'] = ((RBT-CLOs)*100)/RBT

#Completitud taxonRank#
CTRs =daf1S.taxonRank.isnull().sum()
daf3S.loc[22, 'Completitud'] = ((RBT-CTRs)*100)/RBT

#Completitud scientificName#
CSNMs =daf1S.scientificName.isnull().sum()
daf3S.loc[23, 'Completitud'] = ((RBT-CSNMs)*100)/RBT

#Completitud kingdom#
CKs =daf1S.kingdom.isnull().sum()
daf3S.loc[24, 'Completitud'] = ((RBT-CKs)*100)/RBT

#Completitud phylum#
CPHs =daf1S.phylum.isnull().sum()
daf3S.loc[25, 'Completitud'] = ((RBT-CPHs)*100)/RBT

#Completitud class#
CCLs =daf1S['class'].isnull().sum()
daf3S.loc[26, 'Completitud'] = ((RBT-CCLs)*100)/RBT

#Completitud order#
COs =daf1S.order.isnull().sum()
daf3S.loc[27, 'Completitud'] = ((RBT-COs)*100)/RBT

#Completitud scientificName#
CFs =daf1S.family.isnull().sum()
daf3S.loc[28, 'Completitud'] = ((RBT-CFs)*100)/RBT

#Completitud genus#
CGs =daf1S.genus.isnull().sum()
daf3S.loc[29, 'Completitud'] = ((RBT-CGs)*100)/RBT

#Completitud specificEpithet#
CSEs =daf1S.specificEpithet.isnull().sum()
daf3S.loc[30, 'Completitud'] = ((RBT-CSEs)*100)/RBT

#Completitud infraspecificEpithet#
CISEs =daf1S.infraspecificEpithet.isnull().sum()
daf3S.loc[31, 'Completitud'] = ((RBT-CISEs)*100)/RBT

#COHERENCIA DE LOS ELEMENTOS DwC PARA LOS DATOS DEPURADOS#

#Coherencia occurrenceID#
DuplicadosS= daf1S.occurrenceID.duplicated().sum() 
if Duplicados >= 1: 
    CohOIs=0
else:
    CohOIs=1
daf3S.loc[0, "Coherencia"]=(CohOIs)

#Coherencia basisOfRecord(2015)#
def CBORs(x):
    if (x) == ("PreservedSpecimen"):
       CBORs=1
    elif (x) == ("FossilSpecimen"):
       CBORs=1
    elif (x) == ("LivingSpecimen"):
       CBORs=1
    elif (x) == ("HumanObservation"):
       CBORs=1
    elif (x) == ("MachineObservation"):
       CBORs=1
    elif (x) == ("Sample"):
       CBORs=1
    elif (x) == ("nan"):
       CBORs=0
    else:
       CBORs=0
    return (CBORs)

daf2S['CBOR'] = daf1S["basisOfRecord"].apply(CBORs)
daf3S.loc[1, "Coherencia"]= daf2S['CBOR'].mean()

#Coherencia de formato institutionID(NIT)#

daf1S['institutionID'].fillna(0.0, inplace=True)

def VPuntos(x):
    if x.find(".")==0:
            VPuntos=0
    elif x.find(".")<2:
            VPuntos=0
    else:
            VPuntos=1
    return VPuntos

daf2S['puntosNIT'] = daf1S["institutionID"].apply(VPuntos)

def VGuion(x):
    if x.find("-")==0:
            VGuion=0
    elif x.find("-")<1:
            VGuion=0
    else:
            VGuion=1
    return VGuion

daf2S['guionNIT'] = daf1S["institutionID"].apply(VGuion)
daf2S['NIT'] = daf2S['puntosNIT']*daf2S['guionNIT']

def CohNIT(x):
    if x==1:
        cohNIT=1
    else:
        cohNIT=0
    return cohNIT

daf2S['CohNIT'] = daf2S['NIT'].apply(CohNIT)
daf3S.loc[4, "Coherencia"]= daf2S['CohNIT'].mean()

#Coherencia de Formato eventDate" 
daf1S['eventDateISO'].fillna(0, inplace=True)   
  
def CFEDs(x):
    if (x) == 0:
       VEDs= 0
    else:
       VEDs= 1   
    return VEDs

daf2S['CFED'] = daf1S["eventDateISO"].apply(CFEDs)
daf3S.loc[13, "Coherencia"]= daf2S['CFED'].mean()

#Coherencia Formato Coordenadas#
daf3S.loc[14, "Coherencia"]= (RBT-(daf1S.countyValidation.isnull().sum()))/(RBT)
daf3S.loc[15, "Coherencia"]= (RBT-(daf1S.countyValidation.isnull().sum()))/(RBT)

#Coherencia stateProvince"
daf3S.loc[17, "Coherencia"] = ((list(daf1S['stateProvinceValidationDIVIPOLA'])).count(1))/(RBT-(daf1S.stateProvinceValidationDIVIPOLA.isnull().sum()))

#Coherencia county#
daf3S.loc[18, "Coherencia"] = ((list(daf1S['countyValidationDIVIPOLA'])).count(1))/(RBT-(daf1S.countyValidationDIVIPOLA.isnull().sum()))

#Coherencia municipality#
daf1S['municipalityValidationDIVIPOLA'].fillna(0, inplace=True) 
daf3S.loc[19, "Coherencia"] = ((list(daf1S['municipalityValidationDIVIPOLA'])).count(1))/(RBT-(daf1S.municipalityValidationDIVIPOLA.isnull().sum()))

#Coherencia countyValidation"
daf3S.loc[21, "Coherencia"] = (((list(daf1S['countyValidation'])).count(1))/(RBT-(daf1S.countyValidation.isnull().sum())))
 
#Coherencia con vocabulario taxonRank#
def CVTRs(x):
    if (x) == ("Especie"):
       CTRs=1
    elif (x) == ("Subespecie"):
       CTRs=1
    elif (x) == ("Variedad"):
       CTRs=1
    elif (x) == ("Subvariedad"):
       CTRs=1
    elif (x) == ("Forma"):
       CTRs=1
    elif (x) == ("Subforma"):
       CTRs=1
    elif (x) == ("Género"):
       CTRs=0.85
    elif (x) == ("Genero"):
       CTRs=0.85
    elif (x) == ("Subgénero"):
       CTRs=0.85
    elif (x) == ("Sección"):
       CTRs=0.85
    elif (x) == ("Subsección"):
       CTRs=0.85
    elif (x) == ("Serie"):
       CTRs=0.85
    elif (x) == ("Subserie"):
       CTRs=0.85
    elif (x) == ("Familia"):
       CTRs=0.7
    elif (x) == ("Subfamilia"):
       CTRs=0.7
    elif (x) == ("Tribu"):
       CTRs=0.7
    elif (x) == ("Subtribu"):
       CTRs=0.7
    elif (x) == ("Orden"):
       CTRs=0.6
    elif (x) == ("Suborden"):
       CTRs=0.6
    elif (x) == ("Clase"):
       CTRs=0.45
    elif (x) == ("Subclase"):
       CTRs=0.45
    elif (x) == ("Filo"):
       CTRs=0.3
    elif (x) == ("División"):
       CTRs=0.3
    elif (x) == ("Subfilo"):
       CTRs=0.3
    elif (x) == ("Subdivisión"):
       CTRs=0.3
    elif (x) == ("Reino"):
       CTRs=0.15
    elif (x) == ("Subreino"):
       CTRs=0.15
    elif (x) == ("nan"):
       CTRs= 0
    else:
       CTRs= 0
    return (CTRs)

daf2S['CVTR'] = daf1S["taxonRank"].apply(CVTRs)
daf3S.loc[22, "Coherencia"]= daf2S['CVTR'].mean()

#Coherencia scientificName"
def CohSNMs(x):
    if (x) == ("EXACT"):
       CohSNMs=1
    elif (x) == ("FUZZY"):
       CohSNMs=0.6
    elif (x) == ("HIGHERRANK"):
       CohSNMs=0.3
    elif (x) == ("NONE"):
       CohSNMs=0
    else:
       CohSNMs=0
    return (CohSNMs)

daf2S['CohSNM'] = daf1S["taxonMatchType"].apply(CohSNMs)
daf3S.loc[23, "Coherencia"]= daf2S['CohSNM'].mean()

#Coherencia kingdom"
daf3S.loc[24, "Coherencia"] = ((list(daf1S['kingdomValidation'])).count(1))/((RBT)-(daf1S.kingdomValidation.isnull().sum()))

#Coherencia phylum"
daf3S.loc[25, "Coherencia"] = ((list(daf1S['phylumValidation'])).count(1))/((RBT)-(daf1S.phylumValidation.isnull().sum()))

#Coherencia class"
daf3S.loc[26, "Coherencia"] = ((list(daf1S['classValidation'])).count(1))/((RBT)-(daf1S.classValidation.isnull().sum()))

#Coherencia order"
daf3S.loc[27, "Coherencia"] = ((list(daf1S['orderValidation'])).count(1))/((RBT)-(daf1S.orderValidation.isnull().sum()))

#Coherencia family"
daf3S.loc[28, "Coherencia"] = ((list(daf1S['familyValidation'])).count(1))/((RBT)-(daf1S.familyValidation.isnull().sum()))

#Coherencia genus"
daf3S.loc[29, "Coherencia"] = ((list(daf1S['genusValidation'])).count(1))/((RBT)-(daf1S.genusValidation.isnull().sum()))

#Coherencia specificEpithetm"
daf3S.loc[30, "Coherencia"] = ((list(daf1S['specificEpithetValidation'])).count(1))/((RBT)-(daf1S.specificEpithetValidation.isnull().sum()))
daf3S["Coherencia"].fillna(0.0, inplace=True)

#PRECISIÓN DE LOS ELEMENTOS DwC PARA LOS DATOS DEPURADOS"

#Precisión eventDate" 
#AÑO#
daf1S['year'].fillna(0, inplace=True)

def AAAAs(x):
    return str(x)

daf2S['AAAA']= daf1S['year'].apply(AAAAs)

def QZeros(x):
    QZs= x.replace(".0","")
    return QZs

daf2S['AAAA']=daf2S['AAAA'].apply(QZeros)

def PAEDs(x):
    if (x) == 0:
        PAEDs = 0
    elif len(x) == 4:
       PAEDs= 0.1 
    else:
       PAEDs= 0
    return PAEDs

daf2S['PAED'] = daf2S["AAAA"].apply(PAEDs)

#MES#
daf1S['month'].fillna(0, inplace=True)

def MMs(x):
    return str(x)

daf2S['MM']= daf1S['month'].apply(MMs)
daf2S['MM']=daf2S['MM'].apply(QZeros)

def PMEDs(x):
    if (x) == "0":
       PMEDs = 0
    elif len(x) == 2:
       PMEDs= 0.5
    elif len(x) == 1:
       PMEDs= 0.5
    else:
       PMEDs= 0     
    return PMEDs

daf2S['PMED'] = daf2S["MM"].apply(PMEDs)

#DIA#
daf1S['day'].fillna(0, inplace=True)

def DDs(x):
    return str(x)

daf2S['DD']= daf1S['day'].apply(DDs)
daf2S['DD']=daf2S['DD'].apply(QZeros)

def PDEDs(x):
    if (x) == "0":
        PDEDs = 0
    elif len(x) <= 2:
       PDEDs= 0.4
    else:
       PDEDs= 0   
    return PDEDs

daf2S['PDED'] = daf2S["DD"].apply(PDEDs)
daf2S['PED']= daf2S['PAED']+ daf2S['PMED'] + daf2S['PDED']
daf3S.loc[13, 'Precisión']= daf2S['PED'].mean()

#Precision Numerica Coordenadas Latitud"
daf1S['decimalLatitude'].fillna(0.0, inplace=True)

def SCDLas(x):
    return str(x)

daf2S['decStrLa'] = daf1S["decimalLatitude"].apply(SCDLa)

def CDLas(x):
    if x == "0.0":
       CDLass = 0
    elif x.find(".") < 1:
       CDLass = 0
    else:
        CDLass = ((x.split("."))[1])
    return CDLass

daf2S['decimalesLatitude'] = daf2S["decStrLa"].apply(CDLas)

def PNLats(x):
    if x == 0:
       PNLas = 0 
    elif len(x) >=4:
       PNLas=1
    elif len(x) ==3:
       PNLas=0.6
    elif len(x) <=2:
       PNLas=0.2
    else:
       PNLas=0
    return PNLas

daf2S['PNLat'] = daf2S["decimalesLatitude"].apply(PNLats)
daf3S.loc[14, 'Precisión']= daf2S['PNLat'].mean()

#Precision Numerica Coordenadas Longitud"
daf1S['decimalLongitude'].fillna(0.0, inplace=True)

def SCDLos(x):
    return str(x)

daf2S['decStrLo'] = daf1S["decimalLongitude"].apply(SCDLo)

def CDLos(x):
    if x == "0.0":
       CDLos = 0
    elif x.find(".") < 1:
       CDLos = 0
    else:
        CDLos = ((x.split("."))[1])
    return CDLos

daf2S['decimalesLongitud'] = daf2S["decStrLo"].apply(CDLos)

def PNLons(x):
    if x == 0:
       PNLos = 0 
    elif len(x) >=4:
       PNLos=1
    elif len(x) ==3:
       PNLos=0.6
    elif len(x) <=2:
       PNLos=0.2
    else:
       PNLos=0
    return PNLos

daf2S['PNLon'] = daf2S["decimalesLongitud"].apply(PNLons)
daf3S.loc[15, 'Precisión']= daf2S['PNLon'].mean()

#Precision taxonRank#
def Traduccions(x):
    if (x) == 'SPECIES':
        TRAs= "Especie"
    elif (x) == 'GENUS':
        TRAs= "Género"
    elif (x) == 'FAMILY':
        TRAs= "Familia"
    elif (x) == 'ORDER':
        TRAs= "Orden"
    elif (x) == 'CLASS':
        TRAs= "Clase"
    elif (x) == 'PHYLUM':
        TRAs= "Filo"
    elif (x) == 'KINGDOM':
        TRAs= "Reino"
    elif (x) == 'Species':
        TRAs= "Especie"
    elif (x) == 'Genus':
        TRAs= "Género"
    elif (x) == 'Family':
        TRAs= "Familia"
    elif (x) == 'Order':
        TRAs= "Orden"
    elif (x) == 'Class':
        TRAs= "Clase"
    elif (x) == 'Phylum':
        TRAs= "Filo"
    elif (x) == 'Kingdom':
        TRAs= "Reino"
    else:
        TRAs= 0
    return  (TRAs)

daf1S['TRTRA']= daf1S['taxonRankSuggested'].apply(Traduccions)
    
TRSs=daf1S['TRTRA']
TRs=daf1S['taxonRank']
daf2S['PTRR']= np.where(daf1S['TRTRA'] == daf1S['taxonRank'], 1, 0)
daf3S.loc[22, 'Precisión']= daf2S['PTRR'].mean()

#Precisión scientificName"
def PSNMs(x):
    if (x) == ("Especie"):
       PSNMs=1
    elif (x) == ("Género"):
       PSNMs=0.85
    elif (x) == ("Familia"):
       PSNMs=0.7
    elif (x) == ("Orden"):
       PSNMs=0.6
    elif (x) == ("Clase"):
       PSNMs=0.45
    elif (x) == ("Filo"):
       PSNMs=0.3
    elif (x) == ("Reino"):
       PSNMs=0.15
    else:
       PSNMs=0
    return (PSNMs)

daf2S['PSNM'] = daf1S["TRTRA"].apply(PSNMs)
daf3S.loc[23, "Precisión"] = daf2S['PSNM'].mean()

#CÁLCULO DE PARAMETROS DE CALIDAD POR CATEGORIA DwC PARA LOS DATOS DEPURADOS#

#DataFrame 4S: Parametros de calidad por Categoría DwC para los datos depurados#
Ejes={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica"]}
daf4S= pd.DataFrame(Ejes)
daf4S['Completitud']= ""
daf4S['Precisión']= ""
daf4S['Coherencia']= ""

#Calculo: Parametros de Calidad por Categoría DwC#

#Categoría DwC Registrol#
#Completitud Categoría DwC Registro#
daf4S.loc[0, 'Completitud']= ((daf3S.loc[0, "Completitud"])+(daf3S.loc[1, "Completitud"])+(daf3S.loc[2, "Completitud"])+(daf3S.loc[3, "Completitud"])+(daf3S.loc[4, "Completitud"])+(daf3S.loc[5, "Completitud"])+(daf3S.loc[6, "Completitud"])+(daf3S.loc[7, "Completitud"])+(daf3S.loc[8, "Completitud"])+(daf3S.loc[9, "Completitud"]))/(10)

#Coherencia#
daf4S.loc[0, "Coherencia"]= ((daf3S.loc[0, "Coherencia"])*0.6)+((daf3S.loc[4, "Coherencia"])*0.2)+((daf3S.loc[1, "Coherencia"])*0.2)

#Categoría DwC TEMPORAL"
#Completitud Categoría DwC temporal#
daf4S.loc[1, 'Completitud']= daf3S.loc[13, "Completitud"]

#Precisión Categoría DwC temporal#
daf4S.loc[1, 'Precisión']= daf3S.loc[13, "Precisión"]

#Coherencia Categoría DwC temporal"
daf4S.loc[1, 'Coherencia']= daf3S.loc[13, "Coherencia"]

#Categoría DwC Geográfica#
#Completitud Categoría DwC Geográfica#
daf4S.loc[2, 'Completitud']= ((daf3S.loc[10, "Completitud"])+(daf3S.loc[11, "Completitud"])+(daf3S.loc[12, "Completitud"])+(daf3S.loc[14, "Completitud"])+(daf3S.loc[15, "Completitud"])+(daf3S.loc[16, "Completitud"])+(daf3S.loc[17,"Completitud"])+(daf3S.loc[18, "Completitud"])+(daf3S.loc[19, "Completitud"])+(daf3S.loc[20, "Completitud"]))/(10)

#Precisión Categoría DwC Geográfica#
daf4S.loc[2, 'Precisión']= ((daf3S.loc[14, "Precisión"])*0.5)+((daf3S.loc[15, "Precisión"])*0.5)

#Coherencia Categoría DwC Geográfica"
daf4S.loc[2, 'Coherencia']= ((daf3S.loc[21, "Coherencia"])*0.5)+((daf3S.loc[17, "Coherencia"])*0.15)+((daf3S.loc[18, "Coherencia"])*0.15)+((daf3S.loc[19, "Coherencia"])*0.1)+((daf3S.loc[14, "Coherencia"])*0.05)+((daf3S.loc[15, "Coherencia"])*0.05)

#Categoría DwC TAXONÓMIO#
#Completitud Categoría DwC Taxonómica#
daf4S.loc[3, 'Completitud']= ((daf3S.loc[22, "Completitud"])+(daf3S.loc[23, "Completitud"])+(daf3S.loc[24, "Completitud"])+(daf3S.loc[25,"Completitud"])+(daf3S.loc[26, "Completitud"])+(daf3S.loc[27, "Completitud"])+(daf3S.loc[28, "Completitud"])+(daf3S.loc[29, "Completitud"])+(daf3S.loc[30, "Completitud"])+(daf3S.loc[31, "Completitud"]))/(10)

#Precisión Categoría DwC Taxonómica#
daf4S.loc[3, 'Precisión']= ((daf3S.loc[23, "Precisión"])*0.6)+((daf3S.loc[22, "Precisión"])*0.4)

#Coherencia Categoría DwC Taxonómical"
daf4S.loc[3, 'Coherencia']= (((daf3S.loc[23, "Coherencia"])*0.4)+((daf3S.loc[22, "Coherencia"])*0.25)+((daf3S.loc[24, "Coherencia"])*0.05)+((daf3S.loc[25, "Coherencia"])*0.05)+((daf3S.loc[26, "Coherencia"])*0.05)+((daf3S.loc[27, "Coherencia"])*0.05)+((daf3S.loc[28, "Coherencia"])*0.05)+((daf3S.loc[29, "Coherencia"])*0.05)+((daf3S.loc[30, "Coherencia"])*0.05))

#DataFrame 5: Calidad Aparente para cada Categoría DwC"
Ejes={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica", "Conjunto Datos"]}
daf5S= pd.DataFrame(Ejes)
daf5S['Calidad Aparente']=""
#Calidad Aparente para cada Categoría DwC#
#Categoría DwC Registro#
daf5S.loc[0, "Calidad Aparente"]= (((daf4S.loc[0, "Completitud"])*0.8)/100)+((daf4S.loc[0, "Coherencia"])*0.2)

#Categoría DwC Temporal
daf5S.loc[1, "Calidad Aparente"]= ((daf4S.loc[1, "Precisión"])*0.5)+(((daf4S.loc[1, "Completitud"])*0.3)/100)+((daf4S.loc[1, "Coherencia"])*0.2)

#Categoría DwC Geográfica"
daf5S.loc[2, "Calidad Aparente"]= ((daf4S.loc[2, "Precisión"])*0.2)+(((daf4S.loc[2, "Completitud"])*0.2)/100)+((daf4S.loc[2, "Coherencia"])*0.6)

#Categoría DwC Taxonómica#
daf5S.loc[3, "Calidad Aparente"]= ((daf4S.loc[3, "Precisión"])*0.35)+(((daf4S.loc[3, "Completitud"])*0.3)/100)+((daf4S.loc[3, "Coherencia"])*0.35)

#Calidad Aparente del Conjunto Datos#
daf5S.loc[4, "Calidad Aparente"]= ((daf5S.loc[0, "Calidad Aparente"])*0.15)+((daf5S.loc[1, "Calidad Aparente"])*0.2)+((daf5S.loc[2, "Calidad Aparente"])*0.3)+((daf5S.loc[3, "Calidad Aparente"])*0.35)

Ejes={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica", "Conjunto Datos"]}
daf5A= pd.DataFrame(Ejes)
daf5A['Calidad aparente datos originales']= daf5E['Calidad Aparente'] 
daf5A['Calidad aparente datos procesados']= daf5S['Calidad Aparente'] 

#Calculo de porcentaje de mejoria de la Calidad Aparente#
daf5A.loc[0, 'Porcentaje de Mejora (%)'] = ((daf5A.loc[0, 'Calidad aparente datos procesados'])-(daf5A.loc[0, 'Calidad aparente datos originales']))*100
daf5A.loc[1, 'Porcentaje de Mejora (%)'] = ((daf5A.loc[1, 'Calidad aparente datos procesados'])-(daf5A.loc[1, 'Calidad aparente datos originales']))*100
daf5A.loc[2, 'Porcentaje de Mejora (%)'] = ((daf5A.loc[2, 'Calidad aparente datos procesados'])-(daf5A.loc[2, 'Calidad aparente datos originales']))*100
daf5A.loc[3, 'Porcentaje de Mejora (%)'] = ((daf5A.loc[3, 'Calidad aparente datos procesados'])-(daf5A.loc[3, 'Calidad aparente datos originales']))*100
daf5A.loc[4, 'Porcentaje de Mejora (%)'] = ((daf5A.loc[4, 'Calidad aparente datos procesados'])-(daf5A.loc[4, 'Calidad aparente datos originales']))*100


#Manejo de Decimales en los DataFrames#
def decimals(x):
    if (x) == "":
        ZZ = ("")
    elif isinstance (x , int):
        ZZ = (x)
    elif isinstance (x, float):
        ZZ = round(x, 2)
    else:
        ZZ = ("")
    return ZZ

#Agrupacion de DataFrames#
daf3E['Completitud']=daf3E['Completitud'].apply(decimals); daf3E['Precisión']=daf3E['Precisión'].apply(decimals); daf3E['Coherencia']=daf3E['Coherencia'].apply(decimals)
daf3S['Completitud']=daf3S['Completitud'].apply(decimals); daf3S['Precisión']=daf3S['Precisión'].apply(decimals); daf3S['Coherencia']=daf3S['Coherencia'].apply(decimals)
daf4E['Completitud']=daf4E['Completitud'].apply(decimals); daf4E['Precisión']=daf4E['Precisión'].apply(decimals); daf4E['Coherencia']=daf4E['Coherencia'].apply(decimals)
daf4S['Completitud']=daf4S['Completitud'].apply(decimals); daf4S['Precisión']=daf4S['Precisión'].apply(decimals); daf4S['Coherencia']=daf4S['Coherencia'].apply(decimals)
daf5E['Calidad Aparente']=daf5E['Calidad Aparente'].apply(decimals)
daf5S['Calidad Aparente']=daf5S['Calidad Aparente'].apply(decimals)
daf5A['Calidad aparente datos originales']=daf5A['Calidad aparente datos originales'].apply(decimals); daf5A['Calidad aparente datos procesados']=daf5A['Calidad aparente datos procesados'].apply(decimals); daf5A['Porcentaje de Mejora (%)']=daf5A['Porcentaje de Mejora (%)'].apply(decimals)

#DataFrame 4A: Compilacion Dataframes 4E y 4S#
Ejes4A={'Categoría DwC':["Registro", "Temporal", "Geográfica", "Taxonómica"]}
daf4A= pd.DataFrame(Ejes4A)
daf4A['Completitud datos originales']= daf4E['Completitud']
daf4A['Completitud datos procesados']= daf4S['Completitud']
daf4A['Mejora completitud (%)']= ((daf4S['Completitud'])-(daf4E['Completitud']))
daf4A['Precisión datos originales']= daf4E['Precisión']
daf4A['Precisión datos procesados']= daf4S['Precisión']
daf4A.loc[1, 'Mejora precisión (%)']= ((daf4S.loc[1,'Precisión'])-(daf4E.loc[1,'Precisión']))*100
daf4A.loc[2, 'Mejora precisión (%)']= ((daf4S.loc[2,'Precisión'])-(daf4E.loc[2,'Precisión']))*100
daf4A.loc[3, 'Mejora precisión (%)']= ((daf4S.loc[3,'Precisión'])-(daf4E.loc[3,'Precisión']))*100
daf4A['Coherencia datos originales']= daf4E['Coherencia']
daf4A['Coherencia datos procesados']= daf4S['Coherencia']
daf4A['Mejora coherencia (%)']= ((daf4S['Coherencia'])-(daf4E['Coherencia']))*100

#Almacenamiento de Resultados#
#Creación de la carpeta  de almacenamiento de los resultados: Tablas y Graficos#
os.makedirs(r"...\Resultados_Conjunto Datos")

#Creacion Archivo Excel#
SalidaExcel = pd.ExcelWriter(r"...\Resultados_Conjunto Datos\Calidad Aparente Conjunto Datos.xlsx", engine='xlsxwriter')
daf5A.to_excel(SalidaExcel, sheet_name='Calidad Aparente CD Total')
daf4A.to_excel(SalidaExcel, sheet_name='Calidad Aparente Cat-Par')
daf5E.to_excel(SalidaExcel, sheet_name='Calidad Aparente CD Ent')
daf4E.to_excel(SalidaExcel, sheet_name='Parametros calidad CatDwC Ent')
daf3E.to_excel(SalidaExcel, sheet_name='Parametros calidad EleDwC Ent')
daf5S.to_excel(SalidaExcel, sheet_name='Calidad Aparente CD Sal')
daf4S.to_excel(SalidaExcel, sheet_name='Parametros calidad CatDwC Sal')
daf3S.to_excel(SalidaExcel, sheet_name='Parametros calidad EleDwC Sal')
SalidaExcel.save()

#VISUALIZACIÓN DE RESULTADOS: GRAFICOS#
#Comparación Calidad Aparente del Conjunto Datos: Datos Originales vs Datos Procesados#

fig1= plt.figure(figsize=(10,7))
ax1= fig1.add_subplot(111)

Ejeax1= ["Registro","Temporal","Geográfica","Taxonómica", "Conjunto Datos"]
X = np.arange(5)
ax1.bar(X + 0.00, daf5A['Calidad aparente datos originales'], color = "yellowgreen", width = 0.25)
ax1.bar(X + 0.25, daf5A['Calidad aparente datos procesados'], color = "forestgreen", width = 0.25)
ax1.set_ylabel('Calidad Aparente del Conjunto Datos', size=14)
ax1.set_ylim(0, 1.2)
ax1.set_xlabel('Categoría Darwin Core', size=13)
ax1.set_xticks(X+0.12)
ax1.set_xticklabels(Ejeax1, size=12)
ax1.legend(['Datos Originales', 'Datos Procesados'], prop={'size':13})

#Comparación Completitud: Datos Originales vs Datos Procesados
fig2= plt.figure(2)
ax2= fig2.add_subplot(111)
Ejeax2= ["Registro","Temporal","Geográfica","Taxonómica"]
Xa = np.arange(4)
ax2.bar(Xa + 0.00, daf4E['Completitud'], color = "yellowgreen", width = 0.25)
ax2.bar(Xa + 0.25, daf4S['Completitud'], color = "forestgreen", width = 0.25)
ax2.set_ylabel('Completitud')
ax2.set_ylim(0, 120)
ax2.set_xlabel('Categoría Darwin Core')
ax2.set_xticks(Xa+0.13)
ax2.set_xticklabels(Ejeax2)
ax2.legend(['Datos Originales', 'Datos Procesados'], loc="upper right") 

#Comparación Precisión: Datos Originales vs Datos Procesados#
EjesP={'Categoría DwC':["Temporal", "Geográfica", "Taxonómica"]}
dafPG= pd.DataFrame(EjesP)
dafPG['PrecisiónEntrada']=""
dafPG['PrecisiónSalida']=""
dafPG.loc[0, 'PrecisiónEntrada']= daf4E.loc[1, 'Precisión']
dafPG.loc[1, 'PrecisiónEntrada']= daf4E.loc[2, 'Precisión']
dafPG.loc[2, 'PrecisiónEntrada']= daf4E.loc[3, 'Precisión']
dafPG.loc[0, 'PrecisiónSalida']= daf4S.loc[1, 'Precisión']
dafPG.loc[1, 'PrecisiónSalida']= daf4S.loc[2, 'Precisión']
dafPG.loc[2, 'PrecisiónSalida']= daf4S.loc[3, 'Precisión']

fig3= plt.figure(3)
ax3= fig3.add_subplot(111)
Ejeax3= ["Temporal","Geográfica","Taxonómica"]
Xb = np.arange(3)
ax3.bar(Xb + 0.00, dafPG['PrecisiónEntrada'], color = "yellowgreen", width = 0.25)
ax3.bar(Xb + 0.25, dafPG['PrecisiónSalida'], color = "forestgreen", width = 0.25)
ax3.set_ylabel('Precisión')
ax3.set_ylim(0, 1.2)
ax3.set_xlabel('Categoría Darwin Core')
ax3.set_xticks(Xb+0.13)
ax3.set_xticklabels(Ejeax3)
ax3.legend(['Datos Originales', 'Datos Procesados'], loc="upper right") 

#Comparación Coherencia: Datos Originales vs Datos Procesados#
fig4= plt.figure(4)
ax4= fig4.add_subplot(111)
Ejeax2= ["Registro","Temporal","Geográfica","Taxonómica"]
Xa = np.arange(4)
ax4.bar(Xa + 0.00, daf4E['Coherencia'], color = "yellowgreen", width = 0.25)
ax4.bar(Xa + 0.25, daf4S['Coherencia'], color = "forestgreen", width = 0.25)
ax4.set_ylabel('Coherencia')
ax4.set_ylim(0, 1.2)
ax4.set_xlabel('Categoría Darwin Core')
ax4.set_xticks(Xa+0.13)
ax4.set_xticklabels(Ejeax2)
ax4.legend(['Datos Originales', 'Datos Procesados'], loc="upper right") 

#Almacenamiento de Graficos#
fig1.savefig(r"...\Resultados_Conjunto Datos\CalidadAparente.jpg")
fig2.savefig(r"...\Resultados_Conjunto Datos\Completitud.jpg")
fig3.savefig(r"...\Resultados_Conjunto Datos\Precisión.jpg")
fig4.savefig(r"...\Resultados_Conjunto Datos\Coherencia.jpg")

#Remplazo del nombre del Archivo#
os.rename(r"...\Resultados_Conjunto Datos",
          #Remplace: ... por el nombre de la carpeta donde almacenrada los graficos#
          r"...\.-.")

