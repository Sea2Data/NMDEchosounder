class DownloadSurveyRaw(object): 
    def __init__(self,survey_dir,timeSeries,cruiseid):
        import os, sys
        from distutils.dir_util import copy_tree
        from shutil import copy as cp
        import numpy as np
        if sys.platform == 'linux': 
            main_dir = '//data/cruise_data'
        else: 
            main_dir = '//ces.imr.no/cruise_data'
        if not os.path.exists(os.path.join(survey_dir,timeSeries)):
            os.makedirs(os.path.join(survey_dir,timeSeries))
        #Loop through each cruise
        for cruise in cruiseid: 
            #Make folder structure
            year = cruise[0:4]
            #Grab the cruise directory
            ces_cruise = os.listdir(os.path.join(main_dir,year))
            ces_cruise = [i for i in ces_cruise if cruise in i] 
            ces_cruise = [i for i in ces_cruise if not '.txt' in i]
            print(ces_cruise)
            #If only one cruise folder
            if(len(ces_cruise)==1): 
                print('Scanning')
                listOfFiles = list()
                for (dirpath, dirnames, filenames) in os.walk(os.path.join(main_dir,year,ces_cruise[0])):
                    listOfFiles += [dirpath for file in filenames if file.endswith('.raw')]
                listOfFiles = np.unique(listOfFiles)
                print('Scanned')
                raw_version = 0
                korona_version = 0
                print(len(listOfFiles))
                for listof in listOfFiles: 
                    copy=True
                    if('CALIBRATION' in listof): 
                        copy = False
                    if('Kalibrering' in listof): 
                        copy = False
                    if('pretoktdata' in listof): 
                        copy = False
                    if('TOPAS' in listof): 
                        copy = False
                    if('ME70' in listof): 
                        copy = False
                    if('MS70' in listof): 
                        copy = False
                    if('NOISE' in listof): 
                        copy = False
                    if('Noise' in listof): 
                        copy = False
                    if('TS_PROBE' in listof): 
                        copy = False
                    if('SU90' in listof): 
                        copy = False
                    if('SX90' in listof): 
                        copy = False
                    if('SX93' in listof): 
                        copy = False
                    if('SH90' in listof): 
                        copy = False
                    if('EC150' in listof): 
                        copy = False
                    if('OBSERVATION' in listof): 
                        copy = False
                    if(cruise=='2017840'):
                        if(os.path.basename(listof)=='2017840'):
                            copy=False
                        if(os.path.basename(listof)=='201840'):
                            copy=False
                    
                    if copy == True: 
                        #Make folder structure
                        if not os.path.exists(os.path.join(survey_dir,timeSeries,year)):
                            os.makedirs(os.path.join(survey_dir,timeSeries,year))
                        if not os.path.exists(os.path.join(survey_dir,timeSeries,year,cruise)):
                            os.makedirs(os.path.join(survey_dir,timeSeries,year,cruise))
                        if not os.path.exists(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA')):
                            os.makedirs(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA'))
                        print(listof)
                        if('KORONA' in listof): 
                            if not os.path.exists(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('KORONA_V'+str(korona_version)))):
                                print('Start copying')
                                print(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('KORONA_V'+str(korona_version))))
                                os.makedirs(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('KORONA_V'+str(korona_version))))
                                text_file = open(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('KORONA_V'+str(korona_version)),'loadedFrom.txt'),'w')
                                text_file.write(listof)
                                text_file.close()
                            for file in os.listdir(listof): 
                                if not os.path.exists(os.path.join(listof,file)): 
                                    
                                    if not os.path.isdir(os.path.join(listof,file)): 
                                        print(file)
                                        cp(os.path.join(listof,file),os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('KORONA_V'+str(raw_version))))
                            korona_version=korona_version+1
                            
                            
                        else: 
                            if not os.path.exists(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version)))):
                                print('Start copying')
                                print(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version))))
                                os.makedirs(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version))))
                                text_file = open(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version)),'loadedFrom.txt'),'w')
                                text_file.write(listof)
                                text_file.close()
#                                copy_tree(listof, os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version))))
                            
                            for file in os.listdir(listof): 
                                #Check if file has allready been downloaded
                                if not os.path.exists(os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version)),file)): 
                                    #Logic test if this is a file or a directory
                                    if not os.path.isdir(os.path.join(listof,file)): 
                                        print(file)
                                        cp(os.path.join(listof,file),os.path.join(survey_dir,timeSeries,year,cruise,'RAWDATA',('RAWDATA_V'+str(raw_version))))
                                    
                            raw_version=raw_version+1
