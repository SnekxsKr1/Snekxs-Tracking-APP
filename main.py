import requests
from dhooks import Webhook, Embed
from pprint import pprint
import json
import time

hook = Webhook("https://discord.com/api/webhooks/926197272172167178/MsQoq6fEUegMHdxZoHYnPmZoCloZTsfRHtbf74cBVre1AwWGLPqNzq4jnXcSpuXZ8wST")
logs = Webhook("https://discord.com/api/webhooks/917896501034893362/GtZ6awW0cP-GoTByptzXyV_tH5T4_osODBngJmkyd3GL_hDjE_Yg7ALBHHgvJ6Bm6Zx9")
logs.send("Online")

headers = {'aftership-api-key': "a43bb64c-8642-4b85-be00-4484558a3df2",
'Content-Type': 'application/json',
'Accept': 'application/json'}


tracking = "1Z291E2A2001820603"
carrier = "ups"
url = f"https://api.aftership.com/v4/trackings/{carrier}/{tracking}"

r = requests.get(url,headers=headers)

data = json.loads(r.text)


tracking = data["data"]["tracking"]["tracking_number"]
expected = data["data"]["tracking"]["expected_delivery"]
status = data["data"]["tracking"]["checkpoints"][-1]["message"]
location = data["data"]["tracking"]["checkpoints"][-1]["location"]



last_data = status
while True:
    
    try:
        time.sleep(3600)
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