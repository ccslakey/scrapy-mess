from lxml import html
import requests


def get_absolute_paths(unfilteredlinks):
    return list(map(make_absolute_path, unfilteredlinks))


def make_absolute_path(link):
    if link[0:8] == "https://":
        return link[8:-1]
    else:
        return "craiglist.org" + link


def comprehend_lists(list_a, list_b):
    if len(list_a) == len(list_b):
        return dict(zip(list_a, list_b))


class front_page_scraper:
# call by city next
    def __init__(self):
        page = requests.get('http://sacramento.craigslist.org/')
        tree = html.fromstring(page.content)

        categories = tree.xpath('//section[@id="pagecontainer"]/' +
                                'div[@id="center"]/div/div/div/ul/li/a/@href')

        category_titles = tree.xpath(
            '//section[@id="pagecontainer"]/div[@id="center"]/div/div/div/ul/' +
            'li/a/span/text()')

        categories = get_absolute_paths(categories)
        self.category_dict = comprehend_lists(categories, category_titles)

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
            "//body/section[@id='pagecontainer']/"+
            "form[@id='searchform']/div[@class='content']/div[@class='rows']/p[@class='row']/span/span/a/span/text()"
        )
        self.links = get_absolute_paths(tree.xpath(
            "//body/section[@id='pagecontainer']/"+
            "form[@id='searchform']/div[@class='content']/div[@class='rows']/p[@class='row']/span/span/a[@class='hdrlnk']/@href"
        ))
        self.title = category_title

    def print_self(self):
        print("\n".join(self.titles))

    def print_links(self):
        print("\n".join(self.links))

page_scraper = category_page_scraper('http://sacramento.craiglist.org/search/apa', 'materials')
page_scraper.print_links()


# pagination_limit = tree.xpath('//font[@color="green"]/text()')[-1]
# for k,v in category_dict.items():
# print(k, ": ", v)
# print("\n".join(categorytitles))
