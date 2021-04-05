# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 17:36:44 2021

@author: Laura Sánchez G.
"""

#-----------------------librerias----------------------------------------------
import os
import pandas as pd
from xml.dom import minidom

#-----------------Se establecen los directorios de trabajo---------------------
#---------------MANTENGA EL SENTIDO DE LAS BARRAS EN DIAGONAL------------------

#----directorio_1 = ruta de trabajo donde están los recursos (carpetas)-------
#---directorio_2 = ruta para determinar donde están los archivos occurrence---
#---------------ruta_salida = ruta de los archivos de salida-------------------

directorio_1 = r"C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python\DATADIR\resources\resources"
directorio_2 ="C:/Users/Laura Sánchez/OneDrive/Documentos/PASANTÍA/Python/DATADIR/resources/resources/"
ruta_salida = r"C:\Users\Laura Sánchez\OneDrive\Documentos\PASANTÍA\Python"

os.chdir(directorio_1)
Directorio = os.getcwd()
os.getcwd()

#---------------------Se listan los subdirectorios-----------------------------

Nombres_carpetas = os.listdir(Directorio)

#--------------------Se crea el dataframe general-----------------------------

Conjunto_Datos_CRSiB = pd.DataFrame()

#------------------------Se recorre cada carpeta-------------------------------

consolidado = []
for nombre in Nombres_carpetas:    
    
    try:
        
#-----Se determina la ruta para la carpeta sources donde están los archivos occurrence
        
        Rutas = directorio_2 + nombre + "/sources/"  
        
#------------------Se busca el archivo .txt separado por Tab-------------------

        occurence = pd.read_csv(Rutas+'occurrence.txt', sep = '\t')
        occurence.dropna(how='all', axis=1,inplace= True)
        occurence["nombre_corto"] = nombre
        
#--------Se determina la ruta para hacer la búsqueda en los archivos xml------

        Rutas_2 = directorio_2 + nombre  
        subdir = os.chdir(Rutas_2)
        
#-----------En el archivo eml.xml se extrae la información del título---------
        try:
            x = minidom.parse('eml.xml')
            titulo = x.getElementsByTagName("title")
            if (titulo.length > 0):
                occurence["Titulo"] = titulo[0].firstChild.data
            else:
                occurence["Titulo"] = 'No documenta'
                
#-----------------Mismo proceso anterior pero en eml-1.xml--------------------
        except:
            try:
                z = minidom.parse('eml-1.xml')
                titulo = z.getElementsByTagName("title")
                if (titulo.length > 0):
                    occurence["Titulo"] = titulo[0].firstChild.data
                else:
                    occurence["Titulo"] = 'No documenta'
            except:
                occurence["Titulo"] = 'No documenta'
                
#--Condicional: si ANULADO no se encuentra en el título, entonces agréguelo a--
#---------------------------la lista "consolidado"-----------------------------
                
        if "ANULADO" not in titulo[0].firstChild.data:
            consolidado.append(occurence)
            
    except: 
        next    
        
#------ Se concatena el dataframe principal con la lista "consolidado"--------
       
Conjunto_Datos_CRSiB = pd.concat(consolidado,axis=0)

#---------Se listan todos los elementos del estándar para poder ordenar las columnas------

lista = ["nombre_corto","Titulo","id","basisOfRecord","institutionCode","collectionCode","catalogNumber","type",
         "modified","language","license","rightsHolder","accessRights","bibliographicCitation","references","institutionID",
         "collectionID","datasetID","datasetName","ownerInstitutionCode","informationWithheld","dataGeneralizations",
         "dynamicProperties","occurrenceRemarks","recordNumber","recordedBy","organismID","individualCount",
         "organismQuantityType","organismQuantity","organismName","organismScope","associatedOrganisms","organismRemarks",
         "sex","lifeStage","reproductiveCondition","behavior","establishmentMeans","occurrenceStatus","preparations",
         "disposition","otherCatalogNumbers","previousIdentifications","associatedMedia","associatedReferences",
         "associatedOccurrences","associatedSequences","associatedTaxa","materialSampleID","parentEventID","eventID",
         "samplingProtocol","sampleSizeValue","sampleSizeUnit","samplingEffort","eventDate","eventTime","startDayOfYear",
         "endDayOfYear","year","month","day","verbatimEventDate","habitat","fieldNumber","fieldNotes","eventRemarks",
         "locationID","higherGeographyID","higherGeography","continent","waterBody","islandGroup","island","country",
         "countryCode","stateProvince","county","municipality","locality","verbatimLocality","verbatimElevation",
         "minimumElevationInMeters","maximumElevationInMeters","verbatimDepth","minimumDepthInMeters",
         "maximumDepthInMeters","minimumDistanceAboveSurfaceInMeters","maximumDistanceAboveSurfaceInMeters",
         "locationAccordingTo","locationRemarks","verbatimCoordinates","verbatimLatitude","verbatimLongitude",
         "verbatimCoordinateSystem","verbatimSRS","decimalLatitude","decimalLongitude","geodeticDatum",
         "coordinateUncertaintyInMeters","coordinatePrecision","pointRadiusSpatialFit","footprintWKT","footprintSRS",
         "footprintSpatialFit","georeferencedBy","georeferencedDate","georeferenceProtocol","georeferenceSources",
         "georeferenceVerificationStatus","georeferenceRemarks","geologicalContextID","earliestEonOrLowestEonothem",
         "latestEonOrHighestEonothem","earliestEraOrLowestErathem","latestEraOrHighestErathem","earliestPeriodOrLowestSystem",
         "latestPeriodOrHighestSystem","earliestEpochOrLowestSeries","latestEpochOrHighestSeries","earliestAgeOrLowestStage",
         "latestAgeOrHighestStage","lowestBiostratigraphicZone","highestBiostratigraphicZone","lithostratigraphicTerms",
         "group","formation","member","bed","identificationID","identifiedBy","dateIdentified","identificationReferences",
         "identificationVerificationStatus","identificationRemarks","identificationQualifier","typeStatus","taxonID",
         "scientificNameID","acceptedNameUsageID","parentNameUsageID","originalNameUsageID","nameAccordingToID",
         "namePublishedInID","taxonConceptID","taxonMatchType","scientificName","acceptedNameUsage","parentNameUsage",
         "originalNameUsage","nameAccordingTo","namePublishedIn","namePublishedInYear","higherClassification",
         "kingdom","phylum","class","order","family","genus","subgenus","specificEpithet","infraspecificEpithet",
         "taxonRank","verbatimTaxonRank","scientificNameAuthorship","vernacularName","nomenclaturalCode",
         "taxonomicStatus","nomenclaturalStatus","taxonRemarks","preservationDateBegin","preservationType",
         "preservationTemperature","volume","volumeUnit","associatedSequences"]

#-Bucle: si el elemento se encuentra en la lista creada previamente (len > 0),-
#----------------------se agrega en el orden determinado-----------------------

lista_ordenada = []
for item in lista:
    matching = [s for s in Conjunto_Datos_CRSiB.columns if item == s]
    if len(matching) > 0:
        lista_ordenada.append(matching[0])
        
Conjunto_Datos_CRSiB = Conjunto_Datos_CRSiB[lista_ordenada]                

Conjunto_Datos_CRSiB.dropna(how='all', axis=1,inplace= True)

Conjunto_Datos_CRSiB.to_csv(ruta_salida + "Conjunto_datos_CR_SiB.txt", encoding = "UTF-8")

#  Se listan todos los elementos obligatorios y recomendados del estándar para 
#------------------------poder ordenar las columnas---------------------------

lista_resumida = ["nombre_corto","Titulo","id","basisOfRecord","institutionCode","collectionCode","catalogNumber","type","institutionID","collectionID",
"datasetID","datasetName","recordNumber","recordedBy","individualCount","organismQuantityType",
"organismQuantity","occurrenceStatus","preparations","disposition","eventID","samplingProtocol","eventDate","eventTime","habitat","continent","waterBody","country","countryCode",
"stateProvince","county","municipality","locality","minimumElevationInMeters","maximumElevationInMeters","minimumDepthInMeters",
"maximumDepthInMeters","decimalLatitude","decimalLongitude","geodeticDatum","georeferencedBy","identifiedBy","identificationQualifier","taxonMatchType","scientificName","kingdom","phylum","class","order",
"family","genus","subgenus","specificEpithet","infraspecificEpithet","taxonRank","verbatimTaxonRank","scientificNameAuthorship","vernacularName"]

#-Bucle: si el elemento se encuentra en lista_resumida (len > 0), se agrega en
#---------------------------el orden determinado------------------------------

lista_ordenada = []
for item in lista_resumida:
    matching = [s for s in Conjunto_Datos_CRSiB.columns if item == s]
    if len(matching) > 0:
        lista_ordenada.append(matching[0])
        
Conjunto_Datos_CRSiB_resumido = Conjunto_Datos_CRSiB[lista_ordenada]

Conjunto_Datos_CRSiB_resumido.to_csv(ruta_salida + "Conjunto_datos_CR_SiB_resumido.txt", encoding = "UTF-8")                          

                            
