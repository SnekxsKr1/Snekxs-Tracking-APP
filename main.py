import requests
from dhooks import Webhook, Embed
from pprint import pprint
import json
import time

hook = Webhook("https://discord.com/api/webhooks/926197272172167178/MsQoq6fEUegMHdxZoHYnPmZoCloZTsfRHtbf74cBVre1AwWGLPqNzq4jnXcSpuXZ8wST")
logs = Webhook("https://discord.com/api/webhooks/946621024710062140/szxUMuudVuGE0foRhGQ9GMa8XpWZPG6njM4Pu8cCxXvj8OWApT8kJshEWXtKkT3nMbk0")
logs.send("Online")


headers = {'aftership-api-key': "31a87f821-a1f2-4c13-8fef-a95ad3e81f97",
'Content-Type': 'application/json',
'Accept': 'application/json'}


tracking = "289997558187"
carrier = "fedex"
url = f"https://api.aftership.com/v4/trackings/{carrier}/{tracking}"

print(tracking,carrier)

r = requests.get(url,headers=headers)

data = json.loads(r.text)
discord_name = "<@177520581447647232>"

tracking = data["data"]["tracking"]["tracking_number"]
expected = data["data"]["tracking"]["expected_delivery"]
status = data["data"]["tracking"]["checkpoints"][-1]["message"]
location = data["data"]["tracking"]["checkpoints"][-1]["location"]
link = data["data"]["tracking"]["courier_tracking_link"]
statustime = data["data"]["tracking"]["checkpoints"][-1]["checkpoint_time"]
logs.send(f"Current Location: {location}")
logs.send(f"Checking Status: {status}")


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
            hook.send(f"Status Changed {discord_name}")
            embed=Embed(title="Tracking Number: ", description=str(tracking), color=0x00ff00)
            embed.add_field(name="Expected Delivery: ", value=str(expected), inline=False)
            embed.add_field(name="Status: ", value=str(status), inline=False)
            
            embed.add_field(name="Location: ", value=str(location), inline=False)
            
            
            hook.send(embed=embed)
            last_data = status
        else:
            logs.send("No new status")
            logs.send(f"Current Location: {location}")
            logs.send(f"Current Status:  {status}")
    except BaseException as e:
        
        logs.send(e)
