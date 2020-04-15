# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 11:23:56 2020

@author: sindrev
"""


class startLSSS(object): 
    """
    startLSSS function: 
        
        Input: 
            path2LSSS : string to where the LSSS.bat is formatet
                e.g. 'cmd.exe /c "C:/Program Files/Marec/lsss-2.8.0-alpha/lsss/LSSS.bat"&'
                
            time_s : number of seconds to wait untill LSSS has started
    
    """
    
    def __init__(self,path2LSSS,time_s = 10):
        import subprocess
        import time
        
        subprocess.Popen(path2LSSS,shell=False,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=None)
        time.sleep(time_s)





