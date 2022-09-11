import requests
import json
from telegram import notifSignals
from xbet import overSearcher
import time
import schedule

file = "db.json"


def signals():
    with open(file, 'r', encoding='utf-8') as f:
        my_db = json.load(f)
    headers = {
        'authority':
        'games.scoretrend.net',
        'accept':
        '*/*',
        'accept-language':
        'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
        'cache-control':
        'no-cache',
        'origin':
        'https://scoretrend.net',
        'pragma':
        'no-cache',
        'sec-ch-ua':
        '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile':
        '?0',
        'sec-ch-ua-platform':
        '"Windows"',
        'sec-fetch-dest':
        'empty',
        'sec-fetch-mode':
        'cors',
        'sec-fetch-site':
        'same-site',
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    response = requests.get('https://games.scoretrend.net/',headers=headers,timeout=10).text
    data = json.loads(response)
    for d in data[0]:
        #pprint(d)
        try:
            if 50 <= d["goalInterceptor"] and (
                    d['score'] == '0:0' or d['score'] == '1:0'
                    or d['score'] == '0:1') and 5 <= d['timer']['tm'] <= 75:

                response = requests.get('https://api.scoretrend.net/event/' +
                                        d['eventid'],
                                        headers=headers).text
                event = json.loads(response)
                print("########################")
                print("League: " + event["data"][1])
                print("Match: " + event["data"][2] + " VS " + event["data"][3])
                print("Score: " + d["score"])
                print("GT: " + str(d["goalInterceptor"]))
                print("time: " + str(d['timer']['tm']) + "'")
                if (d['score'] == '1:0' or d['score'] == '0:1'):
                    over15, link = overSearcher(
                        event["data"][2] + " " + event["data"][3], 1.5)
                    print("Over 1.5: " + str(over15))
                    exist=False
                    for r in my_db["Data"]:
                     if r["Match"]== event["data"][2] + " VS " + event["data"][3] and r["Over"]==1.5:
                       exist=True
                    if exist==False:   
                     row = {
                        "League":
                        event["data"][1],
                        "Match":
                        event["data"][2] + " VS " + event["data"][3],
                        "Score":
                        d["score"],
                        "GT":
                        round(d["goalInterceptor"], 2),
                        "Time":
                        d['timer']['tm'],
                        "Over":
                        1.5,
                        "ODDS":
                        over15,
                        "Link":
                        link,
                        "Sent":
                        "No"
                    }
                    my_db["Data"].append(row)  

                        
               
                elif d['score'] == '0:0':
                    over05, link = overSearcher(
                        event["data"][2] + " " + event["data"][3], 0.5)
                    print("Over 0.5: " + str(over05))
                    exist=False
                    for r in my_db["Data"]:
                     if r["Match"]== event["data"][2] + " VS " + event["data"][3] and r["Over"]==0.5  :
                       exist=True
                    if exist==False:  
                     row = {
                        "League":
                        event["data"][1],
                        "Match":
                        event["data"][2] + " VS " + event["data"][3],
                        "Score":
                        d["score"],
                        "GT":
                        round(d["goalInterceptor"], 2),
                        "Time":
                        d['timer']['tm'],
                        "Over":
                        0.5,
                        "ODDS":
                        over05,
                        "Link":
                        link,
                        "Sent":
                        "No"
                    }
                     my_db["Data"].append(row)

        except:
            pass
    #print(my_db)
    i = 0
    ids = []
    for id, row in enumerate(my_db["Data"]):
        if row["Sent"] == "No":
            i = i + 1
            #row["Sent"] = "Yes"
            ids.append(id)
            #print(msg)

        if i == 3:
            notifSignals(my_db["Data"][ids[0]], my_db["Data"][ids[1]], my_db["Data"][ids[2]])
            my_db["Data"][ids[0]]["Sent"]= "Yes"
            my_db["Data"][ids[1]]["Sent"]= "Yes"
            my_db["Data"][ids[2]]["Sent"]= "Yes"
            ids = []
            i=0
    #Cleaner      
    #for idx, row in enumerate(my_db["Data"]):
    #    if row["Sent"] == "Yes":
    #       my_db["Data"].pop(idx)
    f.close()
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(my_db, indent=2))
    f.close()  


# scheduling steps
schedule.every(1).minutes.do(signals)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
