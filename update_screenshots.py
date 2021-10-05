from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import os, time

os.system("bash start_server.sh &")
time.sleep(3)
print("Done")

hostName = "localhost"
serverPort = 8000


import glob
fnames=glob.glob("*.html")

for fname in fnames:
    print(fname)
    fbase=os.path.splitext(fname)[0]
    browserHandler = webdriver.Firefox()
    browserHandler.get("http://{hostName}:{serverPort}/{fname}".format(hostName=hostName, serverPort=serverPort, fname=fname))
    time.sleep(2)
    try:
        browserHandler.get_screenshot_as_file("screenshots/{fbase}.png".format(fbase=fbase))
    except WebDriverException:
        print("WebDriverException caught while trying to get a screenshot")
    browserHandler.quit()
