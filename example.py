# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:41:07 2020

@author: sindrev
"""

import runLSSSreport
import numpy as np
import os, sys, time
#import pyreadr


test = runLSSSreport.NMDofficialPath.NMDofficialPath(file='official.txt')
print(test.df)

#Grab the diretories to ces.
if sys.platform == 'linux': 
    work_dir = '//data/mea/2018_Redus/WorkData'
    survey_dir = '//data/mea/2018_Redus/SurveyData'
    survey_dir = '//data/mea/2018_Redus/WorkData'
    ces_dir = '//data/cruise_data'
else: 
    work_dir = '//ces.imr.no/mea/2018_Redus/WorkData'
    survey_dir = '//ces.imr.no/mea/2018_Redus/SurveyData'
    survey_dir = '//ces.imr.no/mea/2018_Redus/WorkData'
    ces_dir = '//ces.imr.no/cruise_data'




#Get nmd info about each time series
tmp = runLSSSreport.getNMDinfo.getNMDinfo()
#while(True): 
#    old_tmp = len(tmp.df)
#    time.sleep(60*60*24)
#    tmp = runLSSSreport.getNMDinfo.getNMDinfo()
#    if len(tmp.df)>old_tmp: 
#        print('asdf')

    

#Subsett for teh herring survey
timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar'
tmp.df = tmp.df[tmp.df['name'] == timeSeries]

#Load work to scratch disk
#runLSSSreport.LoadWorkToScratch.LoadWorkToScratch(tmp.df,work_dir,ces_dir)


#Load raw data to scratch disk
for timeSeries in np.unique(tmp.df['name']):
    cruiseid = np.unique(tmp.df[tmp.df['name'] == timeSeries]['cruiseid'])
#    cruiseid = cruiseid[16:]
    runLSSSreport.DownloadSurveyRaw.DownloadSurveyRaw(survey_dir,timeSeries,cruiseid)
    

asdf
#User selectionn on which time series to execute
timeSeries = 'Norwegian Sea NOR Norwegian spring-spawning herring spawning cruise in Feb_Mar'
cruiseid = np.unique(tmp.df[tmp.df['name'] == timeSeries]['cruiseid'])
cruiseid = cruiseid[12:]




#Start LSSS
path2LSSS = 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'
runLSSSreport.startLSSS.startLSSS(path2LSSS,time_s = 20)



#Fix mapping of LSSS to ICES 




import runLSSSreport
for cruise in cruiseid: 
    dir2raw = os.path.join(survey_dir,timeSeries,cruise[0:4],cruise,'RAWDATA')
    dir2work = os.path.join(work_dir,timeSeries,cruise[0:4],cruise,'INTERPRETATION','LSSS')

    if (os.path.exists(dir2raw)+os.path.exists(dir2work))==2: 
        
        lsss_files = [file for file in os.listdir(dir2work) if file.endswith(".lsss")]
        work_folders = [work for work in os.listdir(dir2work) if 'WORK' in work]
        raw_folders = [raw for raw in os.listdir(dir2raw) if 'RAWDATA' in raw]
        
        for lsssFile in lsss_files: 
            for workFile in work_folders: 
                for rawFile in raw_folders: 
                    
                    
                    #if not file exist: 
                    
                    lufFileName = 'echosounder_'+workFile + '_'+rawFile+'_'+lsssFile[0:-5]
                    print(lufFileName)
                    if not os.path.exists(os.path.join(dir2work,'REPORTS','2.8.0-alpha','20'+lufFileName+'.xml')): 
            #                    import runLSSSreport
                        runLSSSreport.runReport.runReport(
                                lsssFile= os.path.join(dir2work,lsssFile),
                                 workFile=os.path.join(dir2work,workFile),
                                 rawFile=os.path.join(dir2raw,rawFile),
                                 reportDir = dir2work,
                                 lufFileName=lufFileName,
                                 reportType=[20] 
                                 )
