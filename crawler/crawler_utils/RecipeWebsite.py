from urllib.robotparser import RobotFileParser
import urllib.request as request


class RecipeWebsite:

    def __init__(self, base_url):
        self.base_url = base_url
        self.parsing_protocol = self._parse_robots()
        self.sitemaps = self._locate_sitemaps()
        

    def _parse_robots(self):
        rp = RobotFileParser()
        rp.set_url(self.base_url + '/robots.txt')

        return rp.read()

    def _locate_sitemaps(self):
        robots_data = request.urlopen(self.base_url + '/robots.txt')
        sitemaps = [''.join(
                e for e in line.decode('utf-8').strip('Sitemap: ') 
                if e.isalnum() or e in ('/', '.', ':', '_', '-')
            ) for line in robots_data if 'Sitemap:' in line.decode('utf-8')
        ]
        return sitemaps

    
        
class FoodNetwork(RecipeWebsite):
    def __init__(self):
        super().__init__("http://foodnetwork.com")
        self.name = "Food Network"

if __name__ == '__main__':
    fn = FoodNetwork()
    print(fn.sitemaps)