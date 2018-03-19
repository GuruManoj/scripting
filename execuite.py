import subprocess

# some code here
search_prase = "car"
limit = 100

pid = subprocess.Popen('googleimagesdownload --keywords %s --limit %d'%(search_prase, limit), shell=True)