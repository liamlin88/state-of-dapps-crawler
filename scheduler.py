import schedule
import time
import subprocess

def echo():
    print(time.strftime("%Y-%m-%d %H:%M"))
def crawl():
    subprocess.call(['./crawl.sh'])

schedule.every(60).minutes.do(echo)
schedule.every().day.at("09:00").do(crawl)

while True:
    schedule.run_pending()
    time.sleep(1)
