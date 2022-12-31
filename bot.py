import tweepy
import requests
from PIL import Image, ImageFont, ImageDraw
import time

import keys


URL = 'https://rest.coinapi.io/v1/assets'
# this key is a secreat
HEADERS = {'X-CoinAPI-Key' : ''}


def get_price(asset_id: str="BTC") -> int:
    print("[+] Getting the price.") 
    print(" [>] Making request.. ", end='') 
    t = time.perf_counter()
    response = requests.get(URL, headers=HEADERS)
    print('..Response took\u001b[32m', round(time.perf_counter() - t, ndigits=3), '\u001b[0mseconds')

    price = None

    for asset in response.json():
        if asset['asset_id'] == asset_id:
            price = int(asset['price_usd'])
            print(' [>] price found in response')
    
    return price


class Bot:
    def __init__(self) -> None:
        print("[+] Bot initialized")
        self.api = tweepy.API(self.get_auth())
        self.last_price = None
    
    def get_auth(self) -> tweepy.auth.OAuth1UserHandler:
        auth = tweepy.OAuth1UserHandler(keys.api_key, keys.api_key_secret)
        auth.set_access_token(keys.acccess_token, keys.access_token_secret)

        print(" [>] auth set up")
        return auth
    
    def _tweet(self, message: str, image_path: str = None):
        print("[+] trying to tweet.. ", end="")
        t = time.perf_counter()
        if image_path is not None:
            self.api.update_status_with_media(message, image_path)
        else:
            self.api.update_status(message)
        print("..tweet done after\x1b[34m", round(time.perf_counter() - t, ndigits=4), "\x1b[0mseconds")
    
    def _generate_image(self, price):
        print("[+] starting image generation process.. ", end="")

        img = Image.open('assets/template.png')
        W, H = img.size  # w, h
        font = ImageFont.truetype('assets/Montserrat-ExtraBold.otf', 550)

        draw = ImageDraw.Draw(img)
        text = '$'+'{:,}'.format(price)
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        draw.text(((W-w)/2, (H-h)/2), text, (9, 9, 9), font=font)

        img.save('output.png')
        print("..done")
        
        return "output.png"
    
    def tweet(self):
        price = get_price()
        image = self._generate_image(price)

        if self.last_price is not None:
            diff = price - self.last_price
            if diff > 0:
                emoji = f"📈"
            elif diff == "":
                emoji = ""
            else:
                emoji = f"📉"
        else:
            emoji = ""

        self._tweet(f"#bitcoin price {'{:,}'.format(price)} USD " + emoji, image)
        self.last_price = price
