import json
import numpy as np
from typing import List, Dict, Tuple
import requests
from funtions import (
    scriptScraper,
    justNumber,
    remove,
    tryer,
    run,
    getInnertubeApiKey,
    requestYoutube
)
from model import channelVideo

headers = {
    'authority': 'www.youtube.com',
    'x-youtube-client-name': '1',
    'x-youtube-client-version': '2.20210913.01.00',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'sec-gpc': '1',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'same-origin',
    'accept-language': 'en-US,en;q=0.9',

}


# __Video__
def getAllData(fristContinuation: str, video_count: int, session: "requests.Session", commentsURL: str) -> Tuple[
    List[Dict], List[str]]:
    Continuationlist: np.ndarray = np.array([])
    ResponseList: np.ndarray = np.array([])
    continuation: str = fristContinuation
    responseJson: dict
    count_INC: int = 0

    while continuation != '0':

        if count_INC >= video_count:
            break

        responseJson = requestYoutube(continuation, session, commentsURL)

        ResponseList = np.append(ResponseList, responseJson)

        Continuationlist = np.append(Continuationlist, continuation)
        responseJson = responseJson['onResponseReceivedActions'][0]['appendContinuationItemsAction'][
            'continuationItems']
        try:
            continuation = \
                responseJson[30][
                    'continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

        except Exception:
            try:
                if responseJson['error']['code'] == 400:
                    print("FAILED_PRECONDITION Continuation is incorrect code 400")

                continuation = '0'
            except:

                continuation = '0'

        count_INC += 29

    return ResponseList, Continuationlist


def channel_video_filler(data: dict) -> Dict:
    videoId = data["videoId"]
    return {'videoId': videoId, 'title': run(data['title']['runs'], 'text'),
            'title_long': data['title']['accessibility']['accessibilityData']['label'],
            'publishDate': data['publishedTimeText']['simpleText'], 'view_count': int(
            str(data['viewCountText']['simpleText']).replace('views', '').replace(' ', '').replace(',', '')),
            'view_count_short': data['shortViewCountText']['simpleText'],
            'thumbnail_120x90': f"https://img.youtube.com/vi/{videoId}/default.jpg",
            'thumbnail_168x94': tryer(lambda: data['thumbnail']['thumbnails'][0]['url'], lambda: ' '),
            'thumbnail_196x110': tryer(lambda: data['thumbnail']['thumbnails'][1]['url'], lambda: ' '),
            'thumbnail_246x138': tryer(lambda: data['thumbnail']['thumbnails'][2]['url'], lambda: ' '),
            'thumbnail_320x180': f"https://img.youtube.com/vi/{videoId}/mqdefault.jpg",
            "thumbnail_336x188": tryer(lambda: data['thumbnail']['thumbnails'][3]['url'], lambda: ' '),
            "thumbnail_1280x720": f'https://img.youtube.com/vi/{videoId}/maxresdefault.jpg',
            "video_url": f'https://www.youtube.com/watch?v={videoId}'}


def channel_video_blueprint(ResponseList: List) -> Tuple[List[channelVideo], str]:
    ResponseListUpdated = np.array([])
    continuation_token = '0'

    for response in ResponseList:
        try:

            ResponseListUpdated = np.append(ResponseListUpdated,
                                            channelVideo(
                                                **channel_video_filler(response['gridVideoRenderer'])))
        except Exception:
            if "continuationItemRenderer" in response:
                continuation_token = \
                    response['continuationItemRenderer']['continuationEndpoint']['continuationCommand'][
                        'token']

    return ResponseListUpdated, continuation_token


class __Home__(object):
    def __init__(self, videoObject):

        data = json.loads(
            (scriptScraper(videoObject.source))[32].string.replace("var ytInitialData = ", "").replace(";", ""))

        data_set = data['header']['c4TabbedHeaderRenderer']

        self.channelId = data_set['channelId']

        self.subscriberLabel = data_set['subscriberCountText']['accessibility']['accessibilityData']['label']
        self.subscriber = data_set['subscriberCountText']['simpleText'].replace("subscribers", "")
        self.subscriberNumber = int(justNumber(self.subscriber))

        self.title = self.name = data_set['title']

        data_set = data['metadata']['channelMetadataRenderer']

        self.description = data_set['description']
        self.keyword = self.tag = remove(data_set['keywords'].split("\""))
        self.familySafe = data_set['isFamilySafe']

        self.availableCountries = data_set['availableCountryCodes']

        self.androidlink = data_set['androidDeepLink']
        self.ioslink = data_set['iosAppindexingLink']

        try:
            self.tooltip = \
                data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content'][
                    'sectionListRenderer']['contents'][1]['itemSectionRenderer']['contents'][0][
                    'shelfRenderer'][
                    'content']['horizontalListRenderer']['items'][0]['gridVideoRenderer']['ownerBadges'][0][
                    'metadataBadgeRenderer']['tooltip']
            self.isverified, self.tick = True, '✔️'

        except:
            self.tooltip = "Not Verified"
            self.isverified, self.tick = False, '✖️'

        thumbnail = data['header']['c4TabbedHeaderRenderer']
        thumbnailBanner = thumbnail['banner']['thumbnails']

        self.banner_1060x175 = thumbnailBanner[0]['url']
        self.banner_1138x188 = thumbnailBanner[1]['url']
        self.banner_1707x283 = thumbnailBanner[2]['url']
        self.banner_2120x351 = thumbnailBanner[3]['url']
        self.banner_2276x377 = thumbnailBanner[4]['url']
        self.banner_2560x424 = thumbnailBanner[5]['url']

        thumbnail = thumbnail['avatar']['thumbnails']

        self.thumbnail_48x48 = self.thumbnailSmall = thumbnail[0]['url']
        self.thumbnail_88x88 = self.thumbnailMedium = thumbnail[1]['url']
        self.thumbnail_176x176 = self.thumbnailLarge = thumbnail[2]['url']


class __Video__:
    def __init__(self, channel_object):
        self.session: requests.Session = channel_object.session
        self.frist_response_list: List
        self.fristContinuation: str
        self.response_video: str = self.session.get(channel_object.url + "/videos").text
        self.ResponseList: List
        self.Continuationlist: List
        self.videoData: Dict = json.loads(
            (scriptScraper(self.response_video))[32].string.replace('var ytInitialData = ', '').replace(';', ''))

        self.frist_response_list, self.fristContinuation = channel_video_blueprint(
            self.videoData['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content'][
                'sectionListRenderer'][
                'contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer']['items'])

    def get(self, video_count: int) -> List[channelVideo]:
        self.ResponseList, self.Continuationlist = getAllData(
            fristContinuation=self.fristContinuation,
            session=self.session,
            video_count=video_count,
            commentsURL=f"https://www.youtube.com/youtubei/v1/browse?key={getInnertubeApiKey(self.response_video)}")

        ResponseListUpdated: np.ndarray = np.array(self.frist_response_list)
        ResponseListUpdatedRV: np.ndarray

        for response in self.ResponseList:
            ResponseListUpdatedRV, _ = channel_video_blueprint(
                response['onResponseReceivedActions'][0]['appendContinuationItemsAction']['continuationItems'])
            ResponseListUpdated = np.append(ResponseListUpdated, ResponseListUpdatedRV)

        return ResponseListUpdated
