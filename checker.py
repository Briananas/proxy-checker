import requests
import time
import urllib3
import os.path
from _thread  import start_new_thread


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def_url = "https://authserver.mojang.com"
def_timeout = 2
def_threads = 32


check_url = ""
timeout_ = 0
current_threads = 0
max_threads = 0

#how many proxies are in proxies.txt
proxies_count = 0

working_proxies = 0

print("")
print("""\

888888b.         d8b                   88888888888             888        
888  "88b        Y8P                       888                 888        
888  .88P                                  888                 888        
8888888K. 888d888888 8888b. 88888b.        888  .d88b.  .d88b. 888.d8888b 
888  "Y88b888P"  888    "88b888 "88b       888 d88""88bd88""88b88888K     
888    888888    888.d888888888  888       888 888  888888  888888"Y8888b.
888   d88P888    888888  888888  888       888 Y88..88PY88..88P888     X88
8888888P" 888    888"Y888888888  888       888  "Y88P"  "Y88P" 888 88888P'
                                                                          
""")
print("")

if not os.path.isfile("proxies.txt"):
    print("ERROR File 'proxies.txt' not found!!!")
    exit()
	
	
#count proxies
with open("proxies.txt") as f:
    for proxy in f:
        proxy = proxy.replace("\n","")
        proxies_count +=1

if proxies_count == 0:
    print("ERROR File 'proxies.txt' is Empty!!")
    exit()
else:
    print("Found " + str(proxies_count) + " Proxies")
	


print("Proxy Checker by Brian")
print("")
max_threads = int(input("Max Threads (default 32): ")  or def_threads)
check_url = input("Check Url (default monjang auth server): " ) or def_url
timeout_ = int(input("Timeout (default 2 Seconds): " ) or def_timeout) 
print("")







def save_proxy(proxy):
    global working_proxies
    working_proxies += 1
    with open("proxies_working.txt","a") as f:
        f.write(proxy+"\n")
        f.close()
        
def check_proxy(proxy):
    global check_url
    global current_threads
    global timeout_
    global proxies_count
    
    try:
        proxies = {"http": "http://"+proxy,
                "https": "http://"+proxy}

        requests.get(check_url, proxies=proxies,verify=False, timeout=timeout_)
    
    except IOError:
        print("["+str(proxies_count)+"]: " + proxy+": Connection error!")
    else:
        print("["+str(proxies_count)+"]: " +proxy+": Working!")
        save_proxy(proxy)
        
    current_threads -= 1
    proxies_count -= 1
    




#start checking
with open("proxies.txt") as f:
    for proxy in f:
        proxy = proxy.replace("\n","")
        
        
        while max_threads <= current_threads:
            time.sleep(0.1)
            
        current_threads+=1
        start_new_thread(check_proxy,(proxy,))
        

#wait to finish
while current_threads > 0 :
            time.sleep(0.1)

print("Done!")
print("Found " + str(working_proxies) + " working proxies")


        



