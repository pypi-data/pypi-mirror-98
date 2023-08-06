# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import core_helper.helper_general as hg  
from simpledbf import Dbf5


def get_df_servicios():
    url =   get_path_BD() + "\\03.Servicios\\_data_\\Padron_web.dbf"
    print(url)
    dbf_ser = Dbf5(url , codec='ISO-8859-1')
    df_servicios = dbf_ser.to_dataframe()
    df_servicios = df_servicios[["COD_MOD","ANEXO","CODGEO","CODCCPP","GESTION","DAREACENSO",'D_TIPSSEXO']].copy() 
    df_servicios["ANEXO"] =df_servicios['ANEXO'].astype("int8")
    df_servicios["GESTION"] =df_servicios['GESTION'].astype("int8")    

    #df_servicios["AREA_CENSO"] =df_servicios['AREA_CENSO'].astype("int8")
    df_servicios['ES_PUBLICO'] = np.where(df_servicios['GESTION'].isin([1,2]),1,0)
    df_servicios['ES_URBANA'] = np.where(df_servicios['DAREACENSO']=='Urbana',1,0)
    df_servicios['ES_MIXTO'] = np.where(df_servicios['D_TIPSSEXO']=='Mixto',1,0)
    df_servicios['COD_MOD']=df_servicios['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    
    return df_servicios


def get_sisfoh():
    url_sisfoh = get_path_BD()+'\\04.SISFOH\\_data_\\NOMINAL_SISFOH.csv'
    cols = ['PERSONA_NRO_DOC','SISFOH_CSE']    
    df_sisfoh = pd.read_csv(url_sisfoh ,usecols=cols, encoding='utf-8', dtype={'PERSONA_NRO_DOC':str})
    return df_sisfoh


def get_distancia_prim_sec():
    
    url_ddist = get_path_BD() + "\\03.Servicios\\_data_\\SecundariaCerca.csv"
    df_sec_cerca =pd.read_csv(url_ddist, encoding="utf-8",index_col=0) 

    df_sec_cerca.loc[(df_sec_cerca['Distancia'] == 0), 'GRUPO_DISTANCIA'] = '0K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 0) & (df_sec_cerca['Distancia'] <= 1000), 'GRUPO_DISTANCIA'] = 'MENOR_1K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 1000) & (df_sec_cerca['Distancia'] <= 5000), 'GRUPO_DISTANCIA'] = '1K_5K'
    df_sec_cerca.loc[(df_sec_cerca['Distancia'] > 5000), 'GRUPO_DISTANCIA'] = 'MAYOR_5K'

    df_sec_cerca.columns = [x.upper() for x in df_sec_cerca.columns]

    df_sec_cerca[['COD_MOD','ANEXO']] = df_sec_cerca.CODIGOLUGAR.str.split("-",expand=True)
    df_sec_cerca['ANEXO'] = df_sec_cerca['ANEXO'].astype('uint8')

    df_sec_cerca['COD_MOD']=df_sec_cerca['COD_MOD'].apply(lambda x: '{0:0>7}'.format(x))
    del df_sec_cerca['SECUNDARIACERCA']
    del df_sec_cerca['CODIGOLUGAR']
    
    
    return df_sec_cerca


def get_path_BD_siagie_homo():
    path_file =get_path_BD() +"\\01.SIAGIE\\_data_\\02.Depurado"
    return path_file

def get_path_BD_siagie_original():
    path_file =get_path_BD() +"\\01.SIAGIE\\_data_\\01.Original"
    return path_file

def get_path_BD():
    path_file =hg.get_base_path()+"\\src\\Prj_BD"
    return path_file



df_dps = get_distancia_prim_sec()