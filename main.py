import requests
from dhooks import Webhook, Embed
from pprint import pprint
import json
import time

hook = Webhook("https://discord.com/api/webhooks/935683434507018250/hnpk23_ge-kZWsQ2wBDwdZdFGHRdpcXH3UpdoJK_JTvWI0oXR-8_iRW6A_1UXiYwetvo")
logs = Webhook("https://discord.com/api/webhooks/925842247931539466/tbONU1k2vHdvaC0ah1kx45Xv-E_1WOkcHsDLVViz1u0vXOiMUkBud4riOUQnJDbJOF4S")
logs.send("Online")

headers = {'aftership-api-key': "ca7cb231-00c0-4e74-b7b8-8549ca62a203",
'Content-Type': 'application/json',
'Accept': 'application/json'}


tracking = "289086480346"
carrier = "fedex"
url = f"https://api.aftership.com/v4/trackings/{carrier}/{tracking}"

print(tracking,carrier)

r = requests.get(url,headers=headers)

data = json.loads(r.text)
print(data)

tracking = data["data"]["tracking"]["tracking_number"]
expected = data["data"]["tracking"]["expected_delivery"]
status = data["data"]["tracking"]["checkpoints"][-1]["message"]
location = data["data"]["tracking"]["checkpoints"][-1]["location"]
print(location)


last_data = status
while True:

    r = requests.get(url,headers=headers)

    data = json.loads(r.text)

    tracking = data["data"]["tracking"]["tracking_number"]
    expected = data["data"]["tracking"]["expected_delivery"]
    status = data["data"]["tracking"]["checkpoints"][-1]["message"]
    location = data["data"]["tracking"]["checkpoints"][-1]["location"]
    
    
    try:
        time.sleep(1800)
        logs.send("Checking...")
        if last_data != status:
            hook.send("Status Changed")
            embed=Embed(title="Tracking Number: ", description=str(tracking), color=0x00ff00)
            embed.add_field(name="Expected Delivery: ", value=str(expected), inline=False)
            embed.add_field(name="Status: ", value=str(status), inline=False)
            embed.add_field(name="Location: ", value=str(location), inline=False)
            hook.send(embed=embed)
            last_data = status
        else:
            logs.send("No new status")
    except BaseException as e:
        
        logs.send(e)
