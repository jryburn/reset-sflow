#! /usr/bin/env python3            

# This script is designed to use check for my Juniper EX switch adapting its                                                                  
# sflow rate to something other than 4096 for and put it back to 4096  
#                                  
# Written by: Justin Ryburn (justin@ryburn.org)                        

# standard modules                 
import time                        
from jnpr.junos import Device      
from jnpr.junos.utils.config import Config                             

switch = '' # IP for switch                                 
username = '' #Username for device                              
password = '' #Password for the Device                           

dev = Device(host=switch, user=username, password=password)            
print('Logging in to ' + switch)   
dev.open()                         

# Check for sflow sampling rate    
result = dev.rpc.get_sflow_interface()                                 
print('sflow data pulled from device')                                 

reset_flow = False                 
for i in result.xpath('.//interface-adapt-sample-rate-ingress'):       
    if i.text > '4096':            
        reset_flow = True          

# Set sampling rate back to 4096   
if reset_flow is True:             
    # Disable sflow protocol       
    print('Disabling sflow')       
    cu = Config(dev)               
    data = """protocols {          
        inactive: sflow {          
        }                          
    }                              
    """                            
    cu.load(data, format='text')   
    print('Committing... ')        
    cu.pdiff()                     
    cu.commit(timeout=60)          

    # Wait 10 seconds              
    time.sleep(10)                 

    # Enable the interface         
    cu.rollback(1)                 
    print('Committing... ')        
    cu.pdiff()                     
    cu.commit(timeout=60)          

    # Close the device             
    dev.close()                    
else:                              
    print('sflow does not need resetting')                             
    dev.close()                    
