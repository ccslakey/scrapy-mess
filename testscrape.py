from lxml import html
import requests
import math
import ipdb

headers = {
    'User-Agent': 'ConnorBot',
    'From': 'cslakeydev@gmail.com'
}

def get_absolute_paths(unfilteredlinks, city):
    return [make_absolute_path(link, city) for link in unfilteredlinks]

def make_absolute_path(link, city):
    if link:
        if("forums" not in link):
            if "http://" not in link:
                return "http://" + city + ".craiglist.org" + link
    # if link[0:8] is "https://":
    #     return link
    elif "http://" not in link:
            return "http://" + city + ".craiglist.org" + link
    return link

def lists_to_dict(list_a, list_b):
    # creates a dict with list a as the keys, list b as the vals
    if len(list_a) == len(list_b):
        return dict(zip(list_a, list_b))

class front_page_scraper:
    def __init__(self, city):
        page = requests.get('http://' + city + '.craigslist.org/', headers=headers)
        tree = html.fromstring(page.content)

        links = tree.xpath('//section[@id="pagecontainer"]/' +
                                'div[@id="center"]/div/div/div/ul/li/a/@href')

        self.categories_titles = tree.xpath(
            '//section[@id="pagecontainer"]/div[@id="center"]/div/div/div/ul/' +
            'li/a/span/text()')

        categories = get_absolute_paths(links, city)
        self.links = categories
        # this is probably a Bad Thing
        self.category_dict = lists_to_dict(self.categories_titles, self.links)
        self.listed = [{"title": k, "link": v, "api_query": (str(k).split(" ")[0])} for k, v in self.category_dict.items()]
        self.city = city

    def print_self(self):
        for k, v in self.category_dict.items():
            print(k, ": ", v)

    def print_links(self):
        for link in self.links:
            if (link):
                print(link + "\n")

    def print_categories(self):
        print("\n".join(self.categories_titles))

    def create_children(self):
        items = list(self.category_dict.items())
        length = len(items)
        self.children = []
        for i in range(length):
            item = {'url': items[i][1], 'title': items[i][0]}

            if (item['url']) and ("org/i/" not in item['url']):
                cat_scraper = category_page_scraper(item['url'], item['title'], self.city)
                self.children.append(cat_scraper)

class category_page_scraper:

    def __init__(self, category_url, category_title, city, limit=100):
        self.city = city
        self.title = category_title
        self.titles = []
        self.links = []
        self.url = category_url
        if "forums" not in category_url:
            self.type = "search or i"
            self.page = requests.get(category_url, headers=headers)
            self.tree = html.fromstring(self.page.content)
            result_count = self.tree.xpath(
                "//span[@class='totalcount']/text()"
            )
            if limit is None:
                self.result_count = result_count[0]
            else:
                self.result_count = limit
            if self.result_count:
                # round up to nearest hundred for pagination
                self.rounded_count = int(math.ceil(int(self.result_count)/100.0)) * 100

                for i in range(0, self.rounded_count, 100):

                    page = requests.get(category_url + '?s=' + str(i), headers=headers)
                    self.next_tree = html.fromstring(page.content)

                    self.titles += self.next_tree.xpath(
                        "//p[@class='row']/span/span/a[@class='hdrlnk']/text()"
                    )
                    self.links += get_absolute_paths(self.next_tree.xpath(
                        "//p[@class='row']/span/span/a[@class='hdrlnk']/@href"
                    ), city)
            self.category_dict = lists_to_dict(self.titles, self.links)
            self.listed = [{"title": k, "link": v, "type": self.type} for k, v in self.category_dict.items()]

        elif "forums" in category_url:
            self.title = "Forums - " + category_title
            self.type = "forums"
            self.url = category_url



    def children(self):
        self.children = []
        if(self.links):
            for i in range(int(len(self.links))):
                post = posting_scraper(self.links[i], self.city)
                self.children.append(post.serialize())
        elif self.type is "forums":
            self.children = [self.title, self.url]
    def print_self(self):
        print("\n".join(self.titles))

    def print_links(self):
        print("\n".join(self.links))


class posting_scraper:

    def __init__(self, url, city):
        self.url = url
        page = requests.get(self.url)
        self.tree = html.fromstring(page.content)
        description = self.tree.xpath(
            "//section[@id='postingbody']/text()|//b/text()"
        )
        self.description = "\n".join(description)
        self.title = self.tree.xpath(
            "//span[@class='postingtitletext']/span[@id='titletextonly']/text()"
        )
        self.images = self.tree.xpath(
            "//div[@id='thumbs']/a/@href"
        )
        self.location_text = self.tree.xpath(
            "//div[@class='mapAndAttrs']/div[@class='mapbox']/div/text()"
        )
        self.maps_href = self.tree.xpath(
            "//div[@class='mapAndAttrs']/div[@class='mapbox']/p/small/a/@href"
        )
        self.attrs = self.tree.xpath(
            "//div[@class='mapAndAttrs']/p[@class='attrgroup']/span/text()|//b/text()"
        )
    def serialize(self):
        return {
            'title': self.title or '',
            'url': self.url or '',
            'images': self.images or [],
            'location_text': self.location_text or '',
            'maps_href': self.maps_href or '',
            'attrs': self.attrs or [],
            'description': self.description or '',
        }



# print(self.title)
# myS = category_page_scraper('http://sacramento.craiglist.org/search/ats', 'artists',
 # 'sacramento')
# fp = front_page_scraper('sacramento')
# fp.print_links()
# fp.create_children()
# print(fp.children)
# ipdb.set_trace()

# cs = category_page_scraper("craigslist.org/search/hea", "health jobs", "sacramento")
# cs.print_links()
# cs.children()
# ps = posting_scraper("craigslist.org/ctd/5750445828.html", "sacramento")
