# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:30:26 2020

@author: sindrev
"""

class LoadWorkToScratch(object): 
    def __init__(self,data,work_dir,ces_dir):
        from shutil import copy
        import numpy as np
        import os
        
        for ts in np.unique(data['name']):
            print(ts)
            
            #Make the folder structure
            if not (os.path.exists(os.path.join(work_dir,ts))): 
                os.makedirs(os.path.join(work_dir,ts))
            for cruise in data[data['name'] == ts]['cruiseid']:
                print(cruise)
                if not (os.path.exists(os.path.join(work_dir,ts,cruise[0:4]))): 
                    os.makedirs(os.path.join(work_dir,ts,cruise[0:4]))
                if not (os.path.exists(os.path.join(work_dir,ts,cruise[0:4],cruise))): 
                    os.makedirs(os.path.join(work_dir,ts,cruise[0:4],cruise))
                if not (os.path.exists(os.path.join(work_dir,ts,cruise[0:4],cruise,'INTERPRETATION'))): 
                    os.makedirs(os.path.join(work_dir,ts,cruise[0:4],cruise,'INTERPRETATION'))
                if not (os.path.exists(os.path.join(work_dir,ts,cruise[0:4],cruise,'INTERPRETATION','LSSS'))): 
                    os.makedirs(os.path.join(work_dir,ts,cruise[0:4],cruise,'INTERPRETATION','LSSS'))
                    
                #Path to where to store the interpretation
                int_path = os.path.join(work_dir,ts,cruise[0:4],cruise,'INTERPRETATION','LSSS')
                
                #If year exist in ces
                if os.path.exists(os.path.join(ces_dir,cruise[0:4])):
                    
                    #Path to ces server
                    ces_paths = (os.listdir(os.path.join(ces_dir,cruise[0:4])))
                    
                    #Get all vessels with the same cruise number
                    vessel = ([s for s in ces_paths if cruise in s])
                    
                    #Logic test if there is only one cruise
                    if(len(vessel)>0): 
                        ces_paths = os.path.join(ces_dir,cruise[0:4],vessel[0])
                        go = True
                    else:
                        print(vessel)
                        go = False
                        
                    #Do the copying
                    if go == True: 
                        
                        #List all work and lsss filders in directory
                        listOfFiles_work = list()
                        listOfFiles_lsss = list()
                        for (dirpath, dirnames, filenames) in os.walk(ces_paths):
                            listOfFiles_work += [dirpath for file in filenames if file.endswith('.work')]
                            listOfFiles_lsss += [dirpath for file in filenames if file.endswith('.lsss')]
                        listOfFiles_work = np.unique(listOfFiles_work)
                        listOfFiles_lsss = np.unique(listOfFiles_lsss)
                        
                        
                        #Remove profos interpretation
                        listOfFiles_work=[folder for folder in listOfFiles_work if not 'profos' in folder]
                        
                        
                        #copy lsss files
                        print('copying lsss configuration')
                        work_v = 0
                        if len(listOfFiles_lsss)>0:
                            for f in listOfFiles_lsss: 
                                for file in os.listdir(f):
                                    if file.endswith('.lsss'):
                                        try: 
                                            copy(os.path.join(f,file), os.path.join(int_path,'LSSS_V'+str(work_v)+'.lsss'))
                                        except PermissionError: 
                                            d=1
                                        work_v = work_v+1
                                
                            
                        #copy work files
                        print('copying work files')
                        work_v = 0
                        for f in listOfFiles_work: 
                            new_work_dir = os.path.join(int_path,'WORK_V'+str(work_v))
                            
            
                            if not (os.path.exists(new_work_dir)): 
                                os.makedirs(new_work_dir)
                                
                            for file in os.listdir(f):
                                try:
                                    try:
                                        copy(os.path.join(f,file), os.path.join(new_work_dir,file))
                                    except IsADirectoryError:
                                        d=1
                                except PermissionError: 
                                    d=1
                            work_v = work_v +1
                            
                        
                        