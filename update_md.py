import pandas as pd
import re 
import glob

outfile="README.md"

intro="""
# Matthias' jsPsych plugins

Homepage: https://ihrke.github.io/jspsych-plugins-mm/

Github: https://github.com/ihrke/jspsych-plugins-mm

Matthias: https://ihrke.github.io/

"""

fnames=glob.glob("plugins/*.js")

output=intro
for fname in fnames:
    print(fname)
    data=open(fname).read()

    six=data.find("plugin.info")
    while data[six]!="{": six+=1

    pc=0
    for i in range(six,len(data)):
        if data[i]=="{":
            pc += 1
        elif data[i]=="}":
            pc -= 1
        if pc==0:
            eix=i
            break

    info=data[six:eix]
    a=re.search("parameters\s*:\s*", info, re.DOTALL)
    six=a.end()
    pc=0
    for i in range(six,len(info)):
        if info[i]=="{":
            pc += 1
        elif info[i]=="}":
            pc -= 1
        if pc==0:
            eix=i
            break
    parameters=info[(six+1):eix]
    rinfo=info[0:a.start()]+info[eix:]
    rinfo=rinfo.replace("{", "").replace("}","")

    infos=re.findall("([\w_]+):(.*?),",rinfo,re.DOTALL)
    info={k:v.strip().strip('\"').strip("\'") for k,v in dict(infos).items()}


    pars=re.findall("([\w_]+):\s*{(.*?)}", parameters, re.DOTALL)
    pars=dict(pars)
    for k,v in pars.items():
        a=re.findall("([\w_]+):(.*)", v)
        pars[k]={k2:v2.strip().strip(",").strip('\"').strip("\'") for k2,v2 in dict(a).items()}


    partable=pd.DataFrame(pars).transpose().to_markdown()
    info["partable"]=partable
    info["screenshotlink"]="screenshots/example-{name}.png".format(**info)
    info["demolink"]="example-{name}.html".format(**info)
    out="""
    
## {name}
<img src='{screenshotlink}' width="200px">

{description}

[Demo]({demolink})

{partable}
""".format(**info)
    output+=out



with open(outfile, "w") as f:
    f.write(output)
