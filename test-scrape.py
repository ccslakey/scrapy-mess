from lxml import html
import requests
import math
import ipdb

headers = {
    'User-Agent': 'ConnorBot',
    'From': 'cslakeydev@gmail.com'  # This is another valid field
}

def get_absolute_paths(unfilteredlinks):
    return list(map(make_absolute_path, unfilteredlinks))

def make_absolute_path(link):
    if link[0:8] == "https://":
        return link[8:-1]
    else:
        return "craiglist.org" + link

def lists_to_dict(list_a, list_b):
    if len(list_a) == len(list_b):
        return dict(zip(list_a, list_b))

class front_page_scraper:
    def __init__(self, city):
        page = requests.get('http://' + city + '.craigslist.org/', headers=headers)
        tree = html.fromstring(page.content)

        categories = tree.xpath('//section[@id="pagecontainer"]/' +
                                'div[@id="center"]/div/div/div/ul/li/a/@href')

        category_titles = tree.xpath(
            '//section[@id="pagecontainer"]/div[@id="center"]/div/div/div/ul/' +
            'li/a/span/text()')

        categories = get_absolute_paths(categories)
        self.category_dict = lists_to_dict(categories, category_titles)
        self.city = city

    def print_self(self):
        for k, v in self.category_dict.items():
            print(k, ": ", v)

    def children(self):
        items = list(self.category_dict.items())
        length = len(items)
        self.children = []
        for i in range(length):
            item = {'url': items[i][0], 'title': items[i][1]}
            cat_scraper = category_page_scraper(item['url'], item['title'], self.city)
            cat_scraper.children()
            self.children.append(cat_scraper)

class category_page_scraper:

    def __init__(self, category_url, category_title, city):
        if "forums" not in category_url:
            # sorry forums
            page = requests.get("http://" + city + "." + category_url, headers=headers)
            tree = html.fromstring(page.content)
            result_count = tree.xpath(
                "//span[@class='totalcount']/text()"
            )
            self.city = city
            self.titles = []
            self.links = []

            self.title = category_title
            if result_count:
                result_count = result_count[0]
                rounded_count = int(math.floor(int(result_count)/100.0)) * 100
                # print(str(result_count) + ":" + str(rounded_count))
                for i in range(0, rounded_count, 100):
                    page = requests.get("http://" + city + "." + category_url + '?s=' + str(i), headers=headers)
                    next_tree = html.fromstring(page.content)
                    self.titles += next_tree.xpath(
                        "//p[@class='row']/span/span/a[@class='hdrlnk']/text()"
                    )
                    self.links += get_absolute_paths(next_tree.xpath(
                        "//p[@class='row']/span/span/a[@class='hdrlnk']/@href"
                    ))
                    # print("http://" + city + "." + category_url + '?s=' + str(i))
                # print(self.links)
                # print(str(len(self.titles)) + ": " + str(len(self.linksx)))
    def children(self):
        self.children = []
        if(self.links):
            for i in range(int(len(self.links))):
                post = posting_scraper(self.links[i], self.city)
                self.children.append(post)

    def print_self(self):
        print("\n".join(self.titles))

    def print_links(self):
        print("\n".join(self.links))

    # def children(self):
    # make some baby spiders

class posting_scraper:

    def __init__(self, url, city):
        page = requests.get("http://" + city + "." + url)
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
        )[0]
        self.maps_href = self.tree.xpath(
            "//div[@class='mapAndAttrs']/div[@class='mapbox']/p/small/a/@href"
        )[0]
        self.attrs = self.tree.xpath(
            "//div[@class='mapAndAttrs']/p[@class='attrgroup']/span/text()|//b/text()"
        )
        print(self.description)
# fp = front_page_scraper('sacramento')
# fp.children()
ps = posting_scraper("craigslist.org/ctd/5750445828.html", "sacramento")
