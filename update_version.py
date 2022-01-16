from ast import arg
import os, sys

#retrieve current version
# with open('set_version.bat','r') as f: envs = f.readlines()
# envs = "".join(envs).replace('set ','').split()
# envs = {i.split('=')[0]:i.split('=')[1] for i in envs}
envVal = sys.argv[1] if len(sys.argv) > 1 else os.environ["DOM_API_APIVERSION"]
envs = {"DOM_API_APIVERSION": envVal}

output = ''
with open('.env','r') as f: 
    dotenv = f.readlines()
    dotenv = "".join(dotenv).split()
    dotenv = {i.split('=')[0]:i.split('=')[1] for i in dotenv}
    for k in envs.keys():
        if k in dotenv: dotenv[k] = envs[k]
    output = "\n".join([f"{k}={dotenv[k]}" for k in dotenv.keys()])
    print(output)

with open('.env','w') as f: 
    f.write(output)
    
    
