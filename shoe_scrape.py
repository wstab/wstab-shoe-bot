# Import packages
import requests
import json
from datetime import datetime
import pytz

# Gets Nike data

url = 'https://api.nike.com/product_feed/threads/v3/?filter=marketplace(US)&filter=language(en)&filter=upcoming(true)&filter=channelId(010794e5-35fe-4e32-aaff-cd2c74f89d61)'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

r = requests.get(url, headers=headers)

data = json.loads(r.text)

# Shoe class for shoes
class Shoe:
    def __init__ (self, time, link, style, image, price, sizes):
        self.time = time
        self.link = link
        self.style = style
        self.image = image
        self.price = price
        self.sizes = sizes

    def __eq__(self, other):
        if self.time == other.time and self.style == other.style and self.image == other.image and self.link == other.link and self.price == other.price:
            return True
        return False

    # Converts time to EST
    def convertTime(self):
        self.sort(key=lambda x:x.time, reverse = False)
        for shoe in self:
            shoe.time = datetime.fromisoformat(shoe.time.replace('Z', '+00:00')).astimezone(pytz.timezone('America/New_York')).strftime('%B %d, %Y - %I:%M %p (EST)')

class ShoeSizes:
     def __init__ (self, size, avail):
          self.size = size
          self.avail = avail
 


class ShoeData:
    # Makes list of Nike Shoe objects
    def nikeData(self:list):
        for i in range(len(data['objects'])):
            try:
                for k in range(len(data['objects'][i]['productInfo'])):
                    try:
                        time = data['objects'][i]['productInfo'][k]['launchView']['startEntryDate']
                        style = data['objects'][i]['publishedContent']['properties']['products'][0]['styleColor']
                        image = data['objects'][i]['publishedContent']['nodes'][0]['nodes'][0]['properties']['squarishURL']
                        link = data['objects'][i]['publishedContent']['properties']['seo']['slug']
                        price = data['objects'][i]['productInfo'][k]['merchPrice']['fullPrice']
                        nikeSizes = []
                        for c in range(len(data['objects'][i]['productInfo'][k]['skus'])):
                            for z in range(len(data['objects'][i]['productInfo'][k]['availableGtins'])):
                                if data['objects'][i]['productInfo'][k]['skus'][c]['gtin'] == data['objects'][i]['productInfo'][k]['availableGtins'][z]['gtin']:
                                    nikeSizes.append(ShoeSizes(data['objects'][i]['productInfo'][k]['skus'][c]['countrySpecifications'][0]['localizedSize'], data['objects'][i]['productInfo'][k]['availableGtins'][z]['level']))
                        if (Shoe(time, link, style, image, price, nikeSizes) not in self):
                                self.append(Shoe(time, link, style, image, price, nikeSizes))
                    except:
                        pass
            except:
                pass
        Shoe.convertTime(self)
        return self
    
