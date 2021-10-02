import re


def isurl(url: str):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url) is not None:
        return True
    else:
        return False


def protocol(url: str):
    return url.split("://")[0]


def maindomain(url: str):
    return url.split("/")[2]


def domain(domain: str):
    data = domain.split(".")
    top = data.pop()
    root = data[-1]
    sub = data[:-1]
    return [sub, root, top]


def querya(s: str, dic: dict):
    s1: list[str] = s.split("?")
    path: str = s1[0]

    try:

        for i in s1[1].split("&"):
            temp = i.split("=")
            dic[temp[0]] = temp[1]
    except:
        pass

    return path, dic


def pathANDquery(url: str):
    url1: list[str] = url.split("/")[3:]

    paths: list[str] = []
    q: dict['str', 'str'] = {}
    for i in url1:
        p, q = querya(i, q)
        paths.append(p)

    return [paths, q]


class link:
    def __init__(self, url):
        self.url: str = url
        self.isurl: bool = isurl(self.url)
        if self.isurl:
            self.protocol: str = protocol(self.url)
            self.domain: str = maindomain(self.url)

            data: list = domain(self.domain)

            self.subDomain: list = data[0]
            self.rootDomain: str = data[1]
            self.topDomain: str = data[2]

            data: list = pathANDquery(self.url)

            self.path: list = data[0]
            self.query: dict = data[1]
        else:
            self.protocol: str = ''
            self.domain: str = ''
            self.subDomain: list = []
            self.rootDomain: str = ''
            self.topDomain: str = ''
            self.path: list = []
            self.query: dict = {}
