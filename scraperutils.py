####### UTILITY FUNCTIONS ########
# TODO: MOVE THEM SOMEWHERE else
# MAYBE MAKE A BASE CLASS OR RECLASSIFY

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
