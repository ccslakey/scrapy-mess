from lxml import html
import requests


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
# call by city next
    def __init__(self, city):
        # city will need to be dynamic in order to get relative links and create child spiders
        page = requests.get('http://sacramento.craigslist.org/')
        tree = html.fromstring(page.content)

        categories = tree.xpath('//section[@id="pagecontainer"]/' +
                                'div[@id="center"]/div/div/div/ul/li/a/@href')

        category_titles = tree.xpath(
            '//section[@id="pagecontainer"]/div[@id="center"]/div/div/div/ul/' +
            'li/a/span/text()')

        categories = get_absolute_paths(categories)
        self.category_dict = lists_to_dict(categories, category_titles)

    def print_self(self):
        for k, v in self.category_dict.items():
            print(k, ": ", v)

    def children(self):
        items = list(self.category_dict.items())
        length = len(items)
        self.children = []
        for i in range(length):
            item = {'url': items[i][0], 'title': items[i][1]}
            self.children.append(item)


class category_page_scraper:

    def __init__(self, category_url, category_title):
        page = requests.get(category_url)
        tree = html.fromstring(page.content)
        self.titles = tree.xpath(
            "//p[@class='row']/span/span/a/span/text()"
        )
        self.links = get_absolute_paths(tree.xpath(
            "//p[@class='row']/span/span/a[@class='hdrlnk']/@href"
        ))
        self.title = category_title

        pagination_limit = tree.xpath(
            "//span[@class='totalcount']/text()"
        )[0]

    def print_self(self):
        print("\n".join(self.titles))

    def print_links(self):
        print("\n".join(self.links))


class posting_scraper:

    def __init__(self, url):
        page = requests.get(url)
        self.tree = html.fromstring(page.content)

        description = self.tree.xpath(
            "//section[@id='postingbody']/text()"
        )
        self.description = "\n".join(description)
        print("\n".join(self.body))



# fp = front_page_scraper('sacramento')
# fp.children()
# print(fp.children)
# fp.print_self()
# page_scraper = category_page_scraper('http://sacramento.craiglist.org/search/apa', 'materials')
# page_scraper.print_links()

post_scraper = posting_scraper('http://sacramento.craiglist.org/apa/5749097502.html')
