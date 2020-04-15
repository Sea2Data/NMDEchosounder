# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:47:21 2020

@author: sindrev
"""



class runReport(object): 
    
    
    def __init__(self,lsssFile,
                 workFile,
                 rawFile,
                 reportDir,
                 lufFileName,
                 vertical_resolution=10,
                 horizontal_resolution = 0.1, 
                 frequency = 38,
                 reportType=[20,25], 
                 URLprefix = 'http://localhost:8000'):

        
        
        import requests, json, os
        from datetime import date
#        from runLSSSreport import startLSSS
#        import xmltodict
        
                
            
        
        def get(path, params=None):
            url = URLprefix + path
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)
        
        
        def post(path, params=None, json=None, data=None):
            url = URLprefix + path
            response = requests.post(url, params=params, json=json, data=data)
            if response.status_code == 200:
                return response.json()
            if response.status_code == 204:
                return None
            raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)
        
        
        def delete(path, params=None):
            url = URLprefix + path
            response = requests.delete(url, params=params)
            if response.status_code == 200:
                return None
            raise ValueError(url + ' returned status code ' + str(response.status_code) + ': ' + response.text)
    
    
    
        #Grab lsss verssion
        r = requests.get(URLprefix + '/lsss/application/info')
        lsss_version = json.loads(r.content)['version']
        
    
        #Make the REPORTS directory if it does not exist
        if not os.path.exists(os.path.join(reportDir,'REPORTS')): 
            os.makedirs(os.path.join(reportDir,'REPORTS'))
        reportDir = os.path.join(reportDir,'REPORTS')
        
        
        #Make the REPORTS directory if it does not exist
        if not os.path.exists(os.path.join(reportDir,lsss_version)): 
            os.makedirs(os.path.join(reportDir,lsss_version))
        
        reportDir = os.path.join(reportDir,lsss_version)
        print(reportDir)
        
        print("Disconnected database")
        post("/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
        
        print("Create a new database")
        post('/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
        
        print("Connect to the new database")
        r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
        print("Connect to the new database: " + str(r.status_code))
        
        print("Opening survey")
        post('/lsss/survey/open', json={'value':lsssFile})
        
        
        print('Load interpretation data')
        post('/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile})
        
        print('Load echosounder data')
        post('/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':rawFile})
        
        
        #set ping mapping to distance
        #This is to make sure that the correct ping mapping is correctly 
        post('/lsss/survey/config/unit/SurveyMiscConf/parameter/PingMapping',json={'value':'Distance'})
        post('/lsss/survey/config/unit/GridConf/parameter/HorizontalGridUnit',json={'value':'nmi'})
        
        #Set to pelagic mode
        post('/lsss/survey/config/unit/SurveyMiscConf/parameter/PelagicMode',json={'value':'True'})
        
        
            
        #Hack to load all files
        #LSSS only load those files set in the .lsss file. T
        #Underneath will load the whole survey
        r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/files')
        firstIndex = 0
        lastIndex = len(r.json()) - 1
        post('/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':firstIndex, 'lastIndex':lastIndex})
            
        
        
            
        # Wait until the program is ready for further processing
        get('/lsss/data/wait')
    
    
        #Set the grid size        
        post('/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', 
                          json={'value':vertical_resolution})
        
        post('/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizeBottom', 
                          json={'value':horizontal_resolution})
                   
        
        # Wait until the program is ready for further processing
        get('/lsss/data/wait')
            
        
        # Store to local LSSS DB
        print('Storing to database (This takes time)')
        post('/lsss/module/InterpretationModule/database', json={'resolution':horizontal_resolution,
                                                                                          'quality':1,
                                                                                          'frequencies':[frequency, frequency]
                                                                                          })
        
        
        # Wait until the program is ready for further processing
        get('/lsss/data/wait')
    
        
        #This has to be cleened
        if type(reportType)==int: 
            
            luf25file = os.path.join(reportDir,str(reportType)+lufFileName)
                
            print('Making luf:'+ str(reportType))
            r = requests.get(URLprefix + '/lsss/database/report/'+str(reportType))
            print("Generating LUF"+str(reportType)+" from RAW: " + str(r.status_code))
            
             # Write it to disk
            if r.status_code == 200:
                print('Write report')
                with open(luf25file+'.xml', 'w+') as f:
                    f.write(r.text)
        elif type(reportType)==list:
            
            for luftype in reportType: 
                
                luf25file = os.path.join(reportDir,str(luftype)+lufFileName)
        
                print('Making luf:'+ str(luftype))
                r = requests.get(URLprefix + '/lsss/database/report/'+str(luftype))
                print("Generating LUF"+str(luftype)+" from RAW: " + str(r.status_code))
                
                 # Write it to disk
                if r.status_code == 200:
                    print('Write report')
                    with open(luf25file+'.xml', 'w+') as f:
                        f.write(r.text)
        print('Finnished writing report')
    
        get('/lsss/data/wait')
        
        post('/lsss/survey/close')
        