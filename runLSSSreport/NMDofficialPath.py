

class NMDofficialPath(object): 
    def __init__(self,url='http://tomcat7.imr.no:8080/apis/nmdapi/reference/v2/dataset/acousticCategory?version=2.0',file = []):
        
        import xmltodict
        import pandas as pd
        import urllib.request
        
        if file == []: 
            doc =xmltodict.parse(urllib.request.urlopen('http://tomcat7.imr.no:8080/apis/nmdapi/reference/v2/dataset/acousticCategory?version=2.0').read())
        else:             
            with open(file) as fd:
                doc = xmltodict.parse(fd.read())
            
        
        df = pd.DataFrame([])
        for row in doc['list']['row']:
            d = {'cruiseseries':[row['cruiseseries']],'year':[row['year']],'cruise':[row['cruise']],
                 'raw_version':[row['raw_version']],'work_version':[row['work_version']],
                 'lsss_file_version':[row['lsss_file_version']],'lsss_version':[row['lsss_version']],
                 'official':[row['official']]}
            df = df.append(pd.DataFrame(d))

        self.df = df
         
        
    #Return function    
    def __int__(self):
        return int(self.df)
