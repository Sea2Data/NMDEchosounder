
class getNMDinfo: 
    
    def __init__(self):
        ''' Constructor for this class. '''
        
#        import urllib.request
        import xmltodict
        import urllib3
        import pandas as pd
        import numpy as np
        
        
        
        self.server =  "http://tomcat7.imr.no:8080/apis/nmdapi/reference/v2/dataset/cruiseseries?version=2.0"
    
    
        http = urllib3.PoolManager()
        f =  http.request('GET',self.server)
        data = xmltodict.parse(f.data)
            
        
        df = pd.DataFrame([])
        for i in range(0,len(data['list']['row'])):       
            name = data['list']['row'][i]['name']
            
            cruise_id = []
            for ii in range(0,len(data['list']['row'][i]['samples']['sample'])):
                
                for iii in range(0,len(data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise'])):
                    try: 
                        cruise_id=np.hstack((cruise_id,data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise'][iii]['cruisenr']))
                    except KeyError: 
                        cruise_id=np.hstack((cruise_id,data['list']['row'][i]['samples']['sample'][ii]['cruises']['cruise']['cruisenr']))
            cruise_id = (np.unique(cruise_id))
            
        
            d = {'name':name,'cruiseid':list(cruise_id)}
            
            df = df.append(pd.DataFrame(d))
        
        self.df = df
         
        
    #Return function    
    def __int__(self):
        return int(self.df)
