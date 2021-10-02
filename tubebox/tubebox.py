from core.youtube import (
    Video,
    Channel

)
import requests


class tubebox:
    def Video(url_or_id: str, session: requests.Session = requests.Session()):
        return Video(url_or_id, session)

    def Channel(url_or_id: str, session: requests.Session = requests.Session()):
        return Channel(url_or_id, session)
