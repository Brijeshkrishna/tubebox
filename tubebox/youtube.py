import json

import requests
from gunlink import link
from funtions import (

    scriptScraper,
)

from videoclass import (
    __EndScreen__,
    __info__,
    __VideoUrls__,
    __Caption__,
    __Card__,
    __getcomments__

)

from homeclass import (
    __Home__,
    __Video__
)


class Video:
    def __init__(self, url_or_id: str, session: requests.Session = requests.Session()):
        self.url: str = url_or_id
        self.session: requests.Session = session
        self.data: str
        self.yt: dict
        self.source: str
        self.url: str

        try:
            self.source = self.session.get(url=self.url).text

        except:
            self.url = "https://www.youtube.com/watch?v={}".format(self.url)
            self.source = self.session.get(url=self.url).text

        self.data = scriptScraper(self.source)[18].string.replace(
            "var ytInitialPlayerResponse = ", "").replace(";", "")

        self.yt = json.loads(self.data)

    def Info(self):
        return __info__(self)

    def Caption(self):
        return __Caption__(self)

    def EndScreen(self):
        return __EndScreen__(self)

    def Card(self):
        return __Card__(self)

    def VideoUrl(self):
        return __VideoUrls__(self)

    def Comments(self, commentCount: int = 10, replyCount: int = 10):
        return __getcomments__(self, commentCount=commentCount, replyCount=replyCount).get()


class Channel:
    def __init__(self, url_or_id, session: requests.Session = requests.Session()):
        self.url = "https://www.youtube.com/channel/{}/".format(url_or_id) if not link(
            url_or_id).is_valid_link else url_or_id
        self.session = session
        self.source = self.session.get(self.url).text

    def Home(self) -> __Home__:
        return __Home__(self)

    def Video(self) -> __Video__:
        return __Video__(self)


def main():
    import cProfile
    import pstats

    with cProfile.Profile() as p:
        yt = Video(url_or_id="https://www.youtube.com/watch?v=eh3bxXHqF2U")
        d = yt.Comments(10, 0)
        print(d.comment.__len__())
        d.tohtml(filename='eh3bxXHqF2U.html')

    st = pstats.Stats(p)
    # st.sort_stats(pstats.SortKey.CUMULATIVE)
    # st.print_stats()
    # st.dump_stats("c.prof")


main()
