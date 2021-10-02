from pydantic import BaseModel
from funtions import tojson,tohtml

class ReplyClass(BaseModel):
    commentId: str
    name: str
    comment: str
    date: str
    edited: bool
    likeCount: int
    isHeart: bool
    thumbnail_48x48: str
    thumbnail_88x88: str
    thumbnail_176x176: str
    IsChannelOwner: bool
    commenterChannelUrl: str
    ispinned: bool
    pinnedBy: str
    reply: list = []
    replyCount: int = -1
    replycontinuation: str = '0'


class CommentsClass(BaseModel):
    commentId: str
    name: str
    comment: str
    date: str
    edited: bool
    likeCount: int
    isHeart: bool
    thumbnail_48x48: str
    thumbnail_88x88: str
    thumbnail_176x176: str
    IsChannelOwner: bool
    commenterChannelUrl: str
    ispinned: bool
    pinnedBy: str
    reply: list[ReplyClass]
    replyCount: int
    replycontinuation: str


class channelVideo(BaseModel):
    videoId: str
    thumbnail_120x90: str
    thumbnail_168x94: str
    thumbnail_196x110: str
    thumbnail_246x138: str
    thumbnail_320x180: str
    thumbnail_336x188: str
    thumbnail_1280x720: str
    title: str
    title_long: str
    view_count: int
    publishDate: str
    video_url: str
    view_count_short: str

class style:
    def __init__(self, obj):
        self.obj = obj
        self.comment_count = obj.comment_count
        self.comment = self.obj.commentsclassobj

    def json(self,indent:int=4):
        return tojson(self.obj,indent=indent)

    def tojson(self, filename: str = 'comments.json',indent:int=4):
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(tojson(self.obj,indent=indent))


    def tohtml(self, filename: str = 'comments.html'):
        tohtml(self.obj.commentsclassobj, self.obj.linkobj, filename)

    def html(self):
        return tohtml(self.obj.commentsclassobj, self.obj.linkobj, filename='0')

