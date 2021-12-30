import requests
from dhooks import Webhook, Embed
from pprint import pprint
import json
import time

hook = Webhook("https://discord.com/api/webhooks/926197272172167178/MsQoq6fEUegMHdxZoHYnPmZoCloZTsfRHtbf74cBVre1AwWGLPqNzq4jnXcSpuXZ8wST")
logs = Webhook("https://discord.com/api/webhooks/925842247931539466/tbONU1k2vHdvaC0ah1kx45Xv-E_1WOkcHsDLVViz1u0vXOiMUkBud4riOUQnJDbJOF4S")


headers = {'aftership-api-key': "b59f7e6f-1657-4011-bb90-d960e98452bc",
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

embed=Embed(title="Tracking Number: ", description=str(tracking), color=0x00ff00)
embed.add_field(name="Expected Delivery: ", value=str(expected), inline=False)
embed.add_field(name="Status: ", value=str(status), inline=False)
embed.add_field(name="Location: ", value=str(location), inline=False)
hook.send(embed=embed)

last_data = status
while True:
    
    try:
        time.sleep(3600)
        hook.send("Checking...")
        if last_data != status:
            hook.send("Status Changed") 
            last_data = status
    except BaseException as e:
        logs.send(e)