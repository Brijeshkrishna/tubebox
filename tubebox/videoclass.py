import json

import numpy
import requests
from typing import Tuple, List, Union

from model import (
    ReplyClass,
    CommentsClass,
    style
)

from subclass import link

from funtions import (
    tryer,
    editedornot,
    run,
    MilliSecondConverter,
    scriptScraper,
    mimeTypeToFormate,
    urlTOCaption,
    longUrlToShort,
    justNumber,
    isvideo,
    getInnertubeApiKey, requestYoutube
)


class __info__:
    def __init__(self, videoObject):

        self.data: dict = videoObject.yt
        self.tag: numpy.ndarray = numpy.array([])
        self.tagCount: int = 0
        self.tagUrl: numpy.ndarray = numpy.array([])
        self.keywords: numpy.ndarray = numpy.array([])

        infer: dict = json.loads(
            scriptScraper(videoObject.source)[39].string.replace("var ytInitialData = ", "").replace(";", ""))

        infer = infer['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
            'videoPrimaryInfoRenderer']
        try:
            tager: list = infer['superTitleLink']['runs']

            for i in tager:
                if i['text'] != " ":
                    self.tag = numpy.append(self.tag, i['text'][1:])
                    self.tagUrl = numpy.append(self.tagUrl,
                                               "https://www.youtube.com" +
                                               i['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])

            self.tagCount = len(self.tag)
        except:
            pass

        inferExtended: dict = infer['videoActions']['menuRenderer']['topLevelButtons']

        self.like: str = inferExtended[0]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData'][
            'label']
        self.likeShort: int = inferExtended[0]['toggleButtonRenderer']['defaultText']['simpleText']

        self.dislike: str = \
            inferExtended[1]['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData'][
                'label']
        self.dislikeShort: int = inferExtended[1]['toggleButtonRenderer']['defaultText']['simpleText']

        self.live: bool = self.data['responseContext']['serviceTrackingParams'][0]['params'][0]['value']

        videoDetails: dict = self.data['videoDetails']

        self.videoDuration: float = (videoDetails['lengthSeconds'])

        self.videoId: str = videoDetails['videoId']

        self.channelId: str = videoDetails['channelId']

        self.description: str = videoDetails['shortDescription']

        self.title: str = videoDetails['title']

        self.views: int = videoDetails['viewCount'].replace("views", '')

        for i in videoDetails['keywords']:
            self.keywords = numpy.append(self.keywords, i)

        microformate: dict = self.data['microformat']['playerMicroformatRenderer']

        self.category: str = microformate['category']

        self.publishDate: str = microformate['publishDate']

        self.ownerChannelName: str = microformate['ownerChannelName']

        self.uploadDate: str = microformate['uploadDate']

        self.isFamilySafe: bool = microformate['isFamilySafe']

        self.availableCountries: numpy.ndarray = numpy.array(
            microformate['availableCountries'])

        self.isUnlisted: bool = microformate['isUnlisted']

        self.ownerProfileUrl: str = microformate['ownerProfileUrl']

        self.averageRating: float = float(videoDetails['averageRating'])

        self.allowRatings: bool = videoDetails['allowRatings']

        self.author: str = videoDetails['author']

        self.isPrivate: bool = videoDetails['isPrivate']

        thumbnailData: dict = videoDetails['thumbnail']['thumbnails']

        self.videoThumbnail_168x94: str = tryer(
            lambda: thumbnailData[0]['url'], lambda: '')
        self.videoThumbnail_196x110: str = tryer(
            lambda: thumbnailData[1]['url'], lambda: '')
        self.videoThumbnail_246x138: str = tryer(
            lambda: thumbnailData[2]['url'], lambda: '')
        self.videoThumbnail_336x188: str = tryer(
            lambda: thumbnailData[3]['url'], lambda: '')
        self.videoThumbnail_1920x1080: str = tryer(
            lambda: thumbnailData[4]['url'], lambda: '')


class __Caption__:
    def __init__(self, videoObject):
        self.yt: dict = videoObject.yt

        self.captionName: numpy.ndarray = numpy.array([])
        self.captionCount: int = 0
        self.captions: numpy.ndarray = numpy.array([])
        self.captionXmlUrl: dict = {}
        self.languageCode: numpy.ndarray = numpy.array([])
        try:
            captionPath: dict = videoObject.yt['captions']['playerCaptionsTracklistRenderer']['captionTracks']
            self.captionCount = len(captionPath)
            for i in captionPath:
                self.languageCode = numpy.append(
                    self.languageCode, i['languageCode'])
                self.captionName = numpy.append(
                    self.captionName, i['name']['simpleText'])
                self.captions = numpy.append(
                    self.captions, urlTOCaption(i['baseUrl']))
                self.captionXmlUrl[i['name']['simpleText']] = i['baseUrl']
        except Exception as e:
            print(f"Exception {e}")

    def write(self, filename: str):
        captionNumber: int = 0
        for _ in self.captions:
            with open(str(filename) + self.captionName[captionNumber] + ".txt", "w", encoding='utf8') as file:
                file.write(self.captions[captionNumber])

            captionNumber = captionNumber + 1


class __EndScreen__:
    def __init__(self, videoObject):

        self.endScreenData: dict = {}
        self.endScreenTime: int = 0
        self.endScreenElementNumber: int = 0
        self.endScreenElementType: numpy.ndarray = numpy.array([])
        self.endScreenElementThumbnail_250x250: numpy.ndarray = numpy.array([])
        self.endScreenElementThumbnail_400x400: numpy.ndarray = numpy.array([])
        self.endScreenElementTitle: numpy.ndarray = numpy.array([])
        self.endScreenEndpointUrl: numpy.ndarray = numpy.array([])

        if 'endscreen' in videoObject.yt:

            self.endScreenData: dict = videoObject.yt['endscreen']['endscreenRenderer']

            self.endScreenTime = MilliSecondConverter(
                self.endScreenData['startMs'])

            self.endScreenElementNumber = int(
                len(self.endScreenData['elements']))

            for i in self.endScreenData['elements']:
                temp: dict = i['endscreenElementRenderer']

                self.endScreenElementType = numpy.append(
                    self.endScreenElementType, temp['style'])
                self.endScreenElementTitle = numpy.append(
                    self.endScreenElementTitle, temp['title']['simpleText'])

                if temp['style'] == "CHANNEL":
                    self.endScreenEndpointUrl = numpy.append(self.endScreenEndpointUrl,
                                                             "https://www.youtube.com" +
                                                             temp['endpoint']['commandMetadata']['webCommandMetadata'][
                                                                 'url'])

                elif temp['style'] == "WEBSITE":
                    self.endScreenEndpointUrl = numpy.append(self.endScreenEndpointUrl,
                                                             longUrlToShort(temp['endpoint']['urlEndpoint']['url']))

                elif temp['style'] == "VIDEO":
                    self.endScreenEndpointUrl = numpy.append(self.endScreenEndpointUrl,
                                                             "https://www.youtube.com/watch?v = " +
                                                             temp['endpoint']['watchEndpoint']['videoId'])

                elif temp['style'] == "PLAYLIST":
                    self.endScreenEndpointUrl = numpy.append(self.endScreenEndpointUrl,
                                                             'https://www.youtube.com/playlist?list = ' +
                                                             temp['endpoint']['watchEndpoint']['playlistId'])

                temp = temp['image']['thumbnails']
                self.endScreenElementThumbnail_250x250 = numpy.append(
                    self.endScreenElementThumbnail_250x250, temp[0]['url'])
                self.endScreenElementThumbnail_400x400 = numpy.append(self.endScreenElementThumbnail_400x400,
                                                                      temp[1]['url'])


class __Card__:
    def __init__(self, videoObject):

        self.attributes = self.attr = [
            'cardName', 'cardUrl', 'cardCount', 'cardDetail']
        self.cardVisible: bool = False
        self.cardName: numpy.ndarray = numpy.array([])
        self.cardUrl: numpy.ndarray = numpy.array([])
        self.cardCount: int = 0
        self.cardDetail: numpy.ndarray = numpy.array([])

        if "cards" in videoObject.yt:
            cards = videoObject.yt['cards']['cardCollectionRenderer']['cards']
            self.cardVisible = True
            for i in cards:
                self.cardDetail = numpy.append(self.cardDetail, i)
                self.cardName = numpy.append(self.cardName,
                                             i['cardRenderer']['teaser']
                                             ['simpleCardTeaserRenderer']
                                             ['message']['simpleText'])
                self.cardUrl = numpy.append(self.cardUrl,
                                            tryer(lambda: 'https://www.youtube.com' + i['cardRenderer']['content']
                                                  ['videoInfoCardContentRenderer']['action']['commandMetadata']
                                                  ['webCommandMetadata']['url'],
                                                  lambda: longUrlToShort(i['cardRenderer']['content']
                                                                         ['simpleCardContentRenderer']['command']
                                                                         ['urlEndpoint']['url'])))

            self.cardCount = len(self.cardName)


class __VideoUrls__:
    def __init__(self, videoObject):

        self.videoData: dict = videoObject.yt['streamingData']['adaptiveFormats']

        self.videoUrl: numpy.ndarray = numpy.array([])
        self.videoQuality: numpy.ndarray = numpy.array([])
        self.videoFormat: numpy.ndarray = numpy.array([])
        self.videoResolution: numpy.ndarray = numpy.array([])
        self.videoLastModified: numpy.ndarray = numpy.array([])
        self.videoFps: numpy.ndarray = numpy.array([])

        self.audioUrl: numpy.ndarray = numpy.array([])
        self.audioQuality: numpy.ndarray = numpy.array([])
        self.audioFormat: numpy.ndarray = numpy.array([])
        self.audioLastModified: numpy.ndarray = numpy.array([])
        # self.videoSize.append(int(i['contentLength']) / 1e+6)
        for i in self.videoData:

            if isvideo(i['mimeType']):
                self.videoUrl = numpy.append(self.videoUrl, i['url'])
                self.videoQuality = numpy.append(
                    self.videoQuality, i['quality'])
                self.videoFormat = numpy.append(
                    self.videoFormat, mimeTypeToFormate(i['mimeType']))
                self.videoLastModified = numpy.append(
                    self.videoLastModified, i['lastModified'])
                self.videoFps = numpy.append(self.videoFps, i['fps'])
                self.videoResolution = numpy.append(
                    self.videoResolution, f"{i['width']}X{i['height']}")

            else:
                self.audioUrl = numpy.append(self.audioUrl, i['url'])
                self.audioQuality = numpy.append(
                    self.audioQuality, i['quality'])
                self.audioFormat = numpy.append(
                    self.audioFormat, mimeTypeToFormate(i['mimeType']))
                self.audioLastModified = numpy.append(
                    self.audioLastModified, i['lastModified'])

    def json(self, return_numpy: bool = False) -> Union[dict, str]:
        jsonData: numpy.ndarray = numpy.array([])
        for i in range(len(self.videoUrl)):
            jsonData = numpy.append(jsonData, {
                "videoUrl": self.videoUrl[i],
                "videoQuality": self.videoQuality[i],
                "videoFormat": self.videoFormat[i],
                "videoLastModified": self.videoLastModified[i],
                "videoFps": self.videoFps[i],
                "videoResolution": self.videoResolution[i]

            })
        for i in range(len(self.audioUrl)):
            jsonData = numpy.append(jsonData, {
                "audioUrl": self.audioUrl[i],
                "audioQuality": self.audioQuality[i],
                "audioFormat": self.audioFormat[i],
                "audioLastModified": self.audioLastModified[i],

            })
        if return_numpy:
            return {"data": jsonData}
        else:
            return json.dumps({"data": jsonData.tolist()})


# -#-#-#-#-#--#--#--#---#---#########  GET (commentCount ,replyCount) #-#-#-#-#-#--#--#--#---#---#########

# frist funtion
def getFrist(response: str) -> tuple[str, str]:
    '''

    :param session:  requests.Session object
    :return: fristcontinuation and  comments request url
    :rtype: tuple

    '''
    SCRIPTCODE = 39
    firtJsonstr: str = (scriptScraper(response)[SCRIPTCODE]).string.replace("var ytInitialData = ",
                                                                            "").replace(";", "")
    firtJsondict: dict = json.loads(firtJsonstr)
    fristcontinuation: str = '0'

    try:
        for i in firtJsondict['contents']['twoColumnWatchNextResults']['results']['results']['contents']:
            try:
                fristcontinuation = i[
                    'itemSectionRenderer']['contents'][0]['continuationItemRenderer']['continuationEndpoint'][
                    'continuationCommand']['token']
                break
            except:
                pass
    except:
        try:
            fristcontinuation = \
                firtJsondict['contents']['twoColumnWatchNextResults']['results']['results']['contents'][2][
                    'itemSectionRenderer']['continuations'][0]['nextContinuationData']['continuation']
        except Exception as e:
            print(e)

    return (
        fristcontinuation, f"https://www.youtube.com/youtubei/v1/next?key={getInnertubeApiKey(responsetext=response)}")


# ------------------------------------------------------------------------------------------------------------#
def collecterdf(i, code=1):
    collecter = {}

    # for comments
    if code:
        commtesData = i['commentThreadRenderer']['comment']['commentRenderer']
    else:
        commtesData = i['commentRenderer']

    collecter['commentId'] = commtesData['commentId']
    collecter['name'] = tryer(
        lambda: commtesData['authorText']['simpleText'], lambda: ' ')

    # print(collecter['name'])

    collecter['comment'] = run(commtesData['contentText']['runs'], 'text')
    collecter['edited'], collecter['date'] = editedornot(
        commtesData['publishedTimeText']['runs'][0]['text'])

    collecter['likeCount'] = int(justNumber(tryer(lambda: commtesData['voteCount']['simpleText'], lambda:
                                                  commtesData['actionButtons']['commentActionButtonsRenderer']['likeButton']['toggleButtonRenderer'][
        'defaultServiceEndpoint']['performCommentActionEndpoint']['clientActions'][0]['updateCommentVoteAction'][
        'voteCount']['simpleText'], lambda: 0)))

    collecter['isHeart'] = tryer(
        lambda: commtesData['actionButtons']['commentActionButtonsRenderer']['creatorHeart']['creatorHeartRenderer'][
            'isHearted'], lambda: False)
    collecter['thumbnail_48x48'] = commtesData['authorThumbnail']['thumbnails'][0]['url']
    collecter['thumbnail_88x88'] = commtesData['authorThumbnail']['thumbnails'][1]['url']
    collecter['thumbnail_176x176'] = commtesData['authorThumbnail']['thumbnails'][2]['url']
    collecter['IsChannelOwner'] = commtesData['authorIsChannelOwner']
    collecter['commenterChannelUrl'] = tryer(lambda: "https://www.youtube.com{}".format(
        commtesData['authorEndpoint']['commandMetadata']['webCommandMetadata']['url']), lambda: 0)

    def _pinertrue():
        piner = commtesData['pinnedCommentBadge']['pinnedCommentBadgeRenderer']['label']['runs']
        collecter['ispinned'] = True
        collecter['pinnedBy'] = piner[1]['text']

    def _pinerflase():
        collecter['ispinned'] = False
        collecter['pinnedBy'] = ""

    tryer(_pinertrue, _pinerflase)
    collecter['replyCount'] = tryer(
        lambda: commtesData['replyCount'], lambda: 0)
    # onResponseReceivedEndpoints►1►reloadContinuationItemsCommand►continuationItems►0►commentThreadRenderer►replies►commentRepliesRenderer►contents►0►continuationItemRenderer►continuationEndpoint►continuationCommand►token

    collecter['reply'] = []

    collecter['replycontinuation'] = tryer(lambda: i['commentThreadRenderer']['replies']['commentRepliesRenderer'][
        'contents'][0]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token'], lambda: '0')

    return collecter


# ------------------------------------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------------------------------------#


# ------------------------------------------------------------------------------------------------------------#


# gets all data  and return (Continuationlist, ResponseList)
def getAllData(fristContinuation: str, count: int, session: requests.Session, commentsURL: str) -> Tuple[
        List[dict],
        List[dict], int]:
    """

        :param fristContinuation: frist countinuation token
        :param commentsCount:   commentsCount takes interger form 0 to inf , 0 for maximum
        :return: list of CommentsClass object

    """

    Continuationlist: numpy.ndarray = numpy.array([])
    ResponseList: numpy.ndarray = numpy.array([])
    continuation: str = fristContinuation
    responseJson: dict
    count_INC: int = 0
    comment_count: int = -1
    while continuation != '0':
        if count_INC > count:
            break
        responseJson = requestYoutube(continuation, session, commentsURL)
        # onResponseReceivedEndpoints►0►reloadContinuationItemsCommand►continuationItems►0►commentsHeaderRenderer►countText►runs►0►text
        # onResponseReceivedEndpoints►0►reloadContinuationItemsCommand►continuationItems►0►commentsHeaderRenderer►countText►runs►0►text
        ResponseList = numpy.append(ResponseList, responseJson)

        try:
            comment_count = int(
                run(responseJson['onResponseReceivedEndpoints'][0]['reloadContinuationItemsCommand'][
                    'continuationItems'][0][
                    'commentsHeaderRenderer']['countText']['runs'], 'text').replace(' Comments', '').replace(',',
                                                                                                             ''))

        except:
            pass

        Continuationlist = numpy.append(Continuationlist, continuation)

        try:
            continuation = \
                responseJson['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction'][
                    'continuationItems'][20][
                    'continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except:
            try:
                continuation = \
                    responseJson['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand'][
                        'continuationItems'][20][
                        'continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except:
                try:
                    if responseJson['error']['code'] == 400:
                        print(
                            "FAILED_PRECONDITION Continuation is incorrect code 400")
                except:
                    pass
                continuation = '0'

        count_INC += 20
    return ResponseList, Continuationlist, comment_count


# ------------------------------------------------------------------------------------------------------------#

def replyBluePrint(responseJson: dict, replyCount: int, replyCount_INC: int) -> Tuple[list[ReplyClass], int]:
    """
    :param responseJson:  response of youtube
    :return:  CommentsClass object

    """
    comments: numpy.ndarray = numpy.array([])

    try:
        for response in responseJson['onResponseReceivedEndpoints'][1]['reloadContinuationItemsCommand'][
                'continuationItems']:
            if replyCount_INC >= replyCount:
                break
            if not ("continuationItemRenderer" in response):
                replyData: ReplyClass = ReplyClass(
                    **(collecterdf(response, code=0)))
                replyData.replyCount = -1
                comments = numpy.append(comments, replyData)
            replyCount_INC += 1

    except:
        try:
            for response in responseJson['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction'][
                    'continuationItems']:
                if replyCount_INC >= replyCount:
                    break
                if not ("continuationItemRenderer" in response):
                    replyData = ReplyClass(**(collecterdf(response, code=0)))
                    replyData.replyCount = -1
                    comments = numpy.append(comments, replyData)

                replyCount_INC += 1

        except:
            raise "ReplyBluePrint Error"

    return comments, replyCount_INC - 1


# ------------------------------------------------------------------------------------------------------------#

def replyGeter(fristContinuation: str, replyCount: int, session, commentsURL) -> list[ReplyClass]:
    comments: numpy.ndarray = numpy.array([])
    tempData: numpy.ndarray[dict]
    commentsContinuation: str
    tempData, commentsContinuation, _ = getAllData(
        fristContinuation, replyCount, session, commentsURL)
    replyCount_INC: int = 0
    for i in tempData:
        replyData, replyCount_INC = replyBluePrint(
            responseJson=i, replyCount=replyCount, replyCount_INC=replyCount_INC)
        comments = numpy.append(comments, replyData)

    return comments


# ------------------------------------------------------------------------------------------------------------#

def commentsBluePrint(responseJson: dict, commentCount: int, replyCount: int, commentsCount_INC: int, session,
                      commentsURL) \
        -> tuple[numpy.ndarray, int]:
    """
    :rtype: object
    :param responseJson:  response of youtube
    :return:  CommentsClass object

    """
    comments: numpy.ndarray = numpy.array([])

    responseJson = responseJson['onResponseReceivedEndpoints']

    try:
        for response in responseJson[1]['reloadContinuationItemsCommand'][
                'continuationItems']:

            if commentsCount_INC > commentCount:
                break

            if not ("continuationItemRenderer" in response):
                obj: CommentsClass = CommentsClass(**(collecterdf(response)))
                obj.reply = replyGeter(fristContinuation=obj.replycontinuation, replyCount=replyCount, session=session,
                                       commentsURL=commentsURL)

                comments = numpy.append(comments, obj)
            commentsCount_INC += 1

    except:
        try:

            for response in responseJson[0]['appendContinuationItemsAction'][
                    'continuationItems']:

                if commentsCount_INC > commentCount:
                    break
                if not ("continuationItemRenderer" in response):
                    obj = CommentsClass(**(collecterdf(response)))
                    obj.reply = replyGeter(fristContinuation=obj.replycontinuation, replyCount=replyCount,
                                           session=session, commentsURL=commentsURL)
                    comments = numpy.append(comments, obj)

                commentsCount_INC += 1

        except:
            print(responseJson)
#            raise Exception("CommentsBluePrint Error")

    return (comments, commentsCount_INC - 1)


# ------------------------------------------------------------------------------------------------------------#

# full data geting from
def commentsGeter(fristContinuation, commentCount: int, replyCount: int, session: requests.Session, commentsURL) \
        -> Tuple[list[CommentsClass], int]:
    comments: numpy.ndarray = numpy.array([])
    tempData: numpy.ndarray[dict]
    commentsContinuation: str
    comment_count: int
    tempData, commentsContinuation, comment_count = getAllData(
        fristContinuation, commentCount, session, commentsURL)
    commentsCount_INC: int = 0

    for i in tempData:
        commentsData, commentsCount_INC = commentsBluePrint(i, commentCount=commentCount, replyCount=replyCount,
                                                            commentsCount_INC=commentsCount_INC, session=session,
                                                            commentsURL=commentsURL)
        comments = numpy.append(comments, commentsData)

    return comments, comment_count


# ------------------------------------------------------------------------------------------------------------#
# ------------------------------------------------------------------------------------------------------------#

# -#-#-#-#-#--#--#--#---#---#########  GET (commentCount ,replyCount) #-#-#-#-#-#--#--#--#---#---#########


class __getcomments__(object):
    def __init__(self, videoObject, commentCount: int, replyCount: int):
        self.commentCount = commentCount
        self.replyCount = replyCount
        self.fristContinuationToken, self.commentsURL = getFrist(
            videoObject.source)
        self.linkobj = link(videoObject.url)
        self.session: requests.Session = videoObject.session

        headers: requests.structures.CaseInsensitiveDict = requests.structures.CaseInsensitiveDict()

        headers["authority"] = "www.youtube.com"
        headers["x-youtube-client-name"] = "1"
        headers["x-youtube-client-version"] = "2.20210811.00.00"
        headers[
            "user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        headers["content-type"] = "application/json"
        headers["accept"] = "*/*"
        headers["sec-gpc"] = "1"
        headers["origin"] = "https://www.youtube.com"

        self.session.headers = headers

    def get(self) -> style:
        self.commentsclassobj, self.comment_count = commentsGeter(self.fristContinuationToken,
                                                                  commentCount=self.commentCount,
                                                                  replyCount=self.replyCount, session=self.session,
                                                                  commentsURL=self.commentsURL)

        return style(self)
