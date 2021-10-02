
from bs4 import BeautifulSoup as bs
import json
from typing import Optional
from subclass import link
import requests


def mimeTypeToFormate(mimeType):
    return mimeType[mimeType.find("/") + 1: mimeType.find(" ")]


def isvideo(mimeType: str) -> bool:
    return True if mimeType.split("/")[0] == 'video' else False


def request(url: str):
    res = requests.get(url)
    return res.text, res.status_code


def scriptScraper(source) -> list:
    return bs(source, "lxml").findAll("script")


def helper(source):
    return bs(source, "lxml").findAll("a",
                                      class_="yt-simple-endpoint style-scope ytd-video-primary-info-renderer")  # ,class_="yt-simple-endpoint style-scope yt-formatted-string")#.find("yt-formatted-string",class_="super-title style-scope ytd-video-primary-info-renderer")


def urlTOCaption(url) -> str:
    data, _ = request(url)
    data = bs(data, "lxml")
    caption = ""
    for i in data.findAll("text"):
        caption = caption + " " + i.text

    # &#39; - > '

    def unknowToKnow(caption) -> str:
        captionList = list(caption)
        i = 0
        try:
            while i < len(captionList):
                if captionList[i] == "&" and captionList[i + 1] == "#":
                    j = i + 2
                    num = ""
                    while captionList[j] != ";" and j < i + 5:
                        num = num + captionList[j]
                        j = j + 1

                    captionList[i] = ""
                    captionList[i + 1] = ""
                    captionList[i + 2] = chr(int(num))

                    q = i + 3
                    while q < j:
                        captionList[q] = ''
                        q = q + 1

                    captionList[q] = ''
                    mainStr = ''
                    for captions in captionList:
                        mainStr = mainStr + captions
                i = i + 1
            return mainStr
        except:
            return caption

    caption_ = unknowToKnow(caption)
    # removing the spaces
    while caption_[0] == " ":
        caption_ = caption_[1:]

    # to make frist charecter to upper
    # str(caption).capitalize()

    return caption_


def SecondConverter(sec) -> tuple:
    # to int
    sec = int(sec)
    # hour
    hour = int(sec / 3600)
    sec = int(sec % 3600)

    return (hour, int(sec / 60), int(sec % 60))


def MilliSecondConverter(milli):
    # to int
    milli = int(milli)
    # hour
    hours = int(milli / 3.6e+6)
    milli = int(milli % 3.6e+6)
    # minute
    min = int(milli / 60000)
    milli = int(milli % 60000)

    return (hours, min, int(milli / 1000))


def toJson(text):
    return json.loads(text)


def longUrlToShort(url):
    return url.split("q=")[1].replace("%3A", ":").replace("%2F", "/")


def justNumber(string):
    string = list(str(string).strip().upper())
    num = ''
    for i in string:
        try:
            int(i)
            num = num + i
        except:
            pass
        if i == "K":
            num = num + "e+3"
        elif i == "M":
            num = num + "e+6"
        elif i == "B":
            num = num + "e+9"
        elif i == ".":
            num = num + "."
    return float(num)


def remove(lister):
    listers = []
    for i in lister:
        if i != ' ' and i != '':
            listers.append(i.strip())

    return listers


def pyfile(filename: str, extension: str) -> str:
    if "." + extension in filename:
        return filename
    else:
        return filename + '.' + extension


def tryer(succes, fail, middel=lambda: None):
    try:
        return succes()
    except:
        try:
            return fail()
        except:
            return middel()


def run(runer: list, append: str) -> str:
    returnStr: str = ''
    for i in runer:
        returnStr += i[append]
    return returnStr


def editedornot(datestring: str) -> tuple[bool, str]:
    if datestring.find("edited") != -1:

        return True, datestring[:-14]
    else:
        return False, datestring[:-4]


def tohtml(commentdata, linkobj: Optional[link], filename: str):
    commentfiller: str = ''
    CRC = 1

    for i in commentdata:
        replyfiller = ''

        for j in i.reply:
            reply_html = f'''
            <div  style="padding-left: 5px; border:thin solid; padding-top: 10px;width:100%;border-radius: 10px;border-color: green;border-width: 1px;">
               <div class="media mt-4">
                  <a href="{j.commenterChannelUrl}" target="_blank" > 
                    <img class="rounded-circle" alt="Bootstrap Media Another Preview" src="{j.thumbnail_48x48}" />
                  </a>
                  <div class="media-body">
                     <div class="row">
                        <div class="col-6 d-grid">
                           <h5 style="font-family: 'Staatliches', cursive; color: #545454; font-size: xx-large;" >{j.name}</h5> 
                           <span>{j.date} ago</span>
                           <span style="padding-left:15px;padding-right:5px">{j.likeCount}</span> <span> <svg
                           viewBox="0 0 15 14"  style="width: 6.7%;padding-bottom: 10px; "> <g> <path d="M12.42,
                           14A1.54,1.54,0,0,0,14,12.87l1-4.24C15.12,7.76,15,7,14,7H10l1.48-3.54A1.17,1.17,0,0,0,
                           10.24,2a1.49,1.49,0,0,0-1.08.46L5,7H1v7ZM9.89,3.14A.48.48,0,0,1,10.24,3a.29.29,0,0,1,
                           .23.09S9,6.61,9,6.61L8.46,8H14c0,.08-1,4.65-1,4.65a.58.58,0,0,1-.58.35H6V7.39ZM2,
                           8H5v5H2Z" ></path> </g> </svg> </span> </div> </div> <div style="font-weight: 
                           600;padding-bottom: 3px;color: darkgreen;font-size: larger;"> {j.comment} 
                     </div>
                  </div>
               </div>
            </div>
            '''
            replyfiller += reply_html

        ids: str = "none" if len(replyfiller) == 0 else 'block'

        comment_html = f'''
        <div class="comment" style="padding-bottom: 25px; border:thin solid; padding-top: 10px;width:100%; border-radius: 10px;border-color: blue;border-width: 1px;">
           <div class="col-md-12">
              <div class="media">
                 <a href="{i.commenterChannelUrl}" target="_blank" >   <img class="mr-3 rounded-circle" 
                 alt="Bootstrap Media Preview" src="{i.thumbnail_176x176}" /></a> 
                 <div class="media-body">
                    <div class="row">
                       <div class="col-6 d-grid">
                          <h5 style="font-family: 'Staatliches', cursive; color: #545454; font-size: xx-large;">{i.name} 
                          </h5> 
                          <span > {i.date} ago</span>
                          <span style="padding-left:15px;font-weight: 900;" >{i.likeCount}</span> <span 
                          style="colour:blue;"> <svg viewBox="0 0 15 14"  style=" width: 6.8%;padding-bottom: 10px; 
                          "> <g> <path d="M12.42,14A1.54,1.54,0,0,0,14,12.87l1-4.24C15.12,7.76,15,7,14,
                          7H10l1.48-3.54A1.17,1.17,0,0,0,10.24,2a1.49,1.49,0,0,0-1.08.46L5,7H1v7ZM9.89,3.14A.48.48,0,
                          0,1,10.24,3a.29.29,0,0,1,.23.09S9,6.61,9,6.61L8.46,8H14c0,.08-1,4.65-1,4.65a.58.58,0,0,
                          1-.58.35H6V7.39ZM2,8H5v5H2Z" ></path> </g> </svg> </span> </div> <div class="col-4" 
                          style='display:{ids}'> 
                          <div class="pull-right reply" > <button class="glow-on-hover" onclick="onreply('CRC-{CRC}')">  
                          <i class="fa fa-reply"></i> reply </button> </div> </div> </div> <div style="font-weight: 600;
                          padding-bottom:5px;color: darkblue; font-size: larger;">{i.comment}</div> 

                    <!--reply section -->
                    <div id="CRC-{CRC}" style="display: none;">
                       {replyfiller}
                    </div>
                    <!--reply section -->

                 </div>
              </div>
           </div>
        </div>
        '''
        commentfiller += comment_html
        CRC += 1

    script: str = '''
    <script type="text/javascript">
    function onreply(id) {
         var x = document.getElementById(id);
      if (x.style.display === "none") {
        x.style.display = "block";
      } else {
        x.style.display = "none";
      }
    }
    </script>
    '''
    stylestr = '''

            html,
            body {
                height: 100%;



            }

            body {
                display: grid;
                place-items: center;



            }
            .card {
                position: relative;
                display: flex;
                padding: 25px;
                flex-direction: column;
                min-width: 0;
                word-wrap: break-word;



                width:auto;
                background-clip: border-box;
                border: 1px solid #d2d2dc;
                border-radius: 11px;
                -webkit-box-shadow: 0px 0px 5px 0px rgb(249, 249, 250);
                -moz-box-shadow: 0px 0px 5px 0px rgba(212, 182, 212, 1);
                box-shadow: 0px 0px 5px 0px rgb(161, 163, 164)
            }

            .media img {
                width: 60px;
                height: 60px
            }

            .reply a {
                text-decoration: none
            }


             .glow-on-hover {
                width: 100px;
                height: 35px;
                border: none;
                outline: none;
                color: #fff;
                background: #111;
                cursor: pointer;
                position: relative;
                z-index: 0;
                border-radius: 10px;
            }

            .glow-on-hover:before {
                content: '';
                background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
                position: absolute;
                top: -2px;
                left:-2px;
                background-size: 400%;
                z-index: -1;
                filter: blur(5px);
                width: calc(100% + 4px);
                height: calc(100% + 4px);
                animation: glowing 20s linear infinite;
                opacity: 0;
                transition: opacity .3s ease-in-out;
                border-radius: 5px;
            }

            .glow-on-hover:active {
                color: #000
            }

            .glow-on-hover:active:after {
                background: transparent;
            }

            .glow-on-hover:hover:before {
                opacity: 0.5;
            }

            .glow-on-hover:after {
                z-index: -1;
                content: '';
                position: absolute;
                width: 100%;
                height: 100%;
                background: #111;
                left: 0;
                top: 0;
                border-radius: 5px;
            }

            @keyframes glowing {
                0% { background-position: 0 0; }
                50% { background-position: 400% 0; }
                100% { background-position: 0 0; }
            }
    '''
    html_page = f'''
   <!DOCTYPE html>
   <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Yotube Comment - {linkobj.query['v']}</title>
       </head>
       <link rel="stylesheet" href="style.css">
       <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
       <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
       <link href="https://fonts.googleapis.com/css2?family=Staatliches&display=swap" rel="stylesheet">
       <link rel="preconnect" href="https://fonts.googleapis.com">
       <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
       <link href="https://fonts.googleapis.com/css2?family=Wallpoet&display=swap" rel="stylesheet">
       <link rel="preconnect" href="https://fonts.googleapis.com">
       <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
       <link href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@100&display=swap" rel="stylesheet">
       <style>
            {stylestr}
       </style>
       <body  style="font-family: 'Azeret Mono', monospace;background: #0e1225db;" >
          <div class="container mb-5 
             mt-5">
             <div class="card" style="background-color:#ccc;">
                <div class="row" >
                   <div class="col-md-12">
                      <h1 
                         class="text-center mb-5" style="font-family: 'Staatliches', cursive;"  > Comments Section   
                         <span style="color: aqua" >(</span>     <span style="color: darkorange" >{linkobj.query['v']}</span>       
                          <span style="color: aqua" >)</span> </h1>
                      <div class="row">
                         <!-- comments section -->
                         {commentfiller}
                         <!-- comments section -->
                      </div>
                   </div>
                </div>
             </div>
          </div>
       </body>
       {script}
    </html>
    '''
    if filename != '0':
        with open(pyfile(filename, "html"), 'w', encoding="utf-8") as file:
            file.write(bs(html_page, "lxml").prettify())
    else:
        return bs(html_page, "lxml").prettify()


def tojson(obj, indent: int) -> str:
    tempC = []
    tempR = []

    for comments in obj.commentsclassobj:

        for reply in comments.reply:
            tempR.append(json.loads(reply.json()))

        comments.reply = tempR

        tempC.append(json.loads(comments.json()))

    return json.dumps({"comment_count": obj.comment_count, "comments": tempC}, indent=indent, ensure_ascii=False)


def getInnertubeApiKey(responsetext: str) -> str:
    """

    :param responsetext: html page of youtube
    :rtype str
    :return: InnertubeApiKey
    """
    innertubedata = scriptScraper(responsetext)[9].string
    start = innertubedata.find("INNERTUBE_API_KEY")

    return innertubedata[start + 20: innertubedata.find('","', start)]


# request the and return the json
def requestYoutube(continuation: str, session: requests.Session, commentsURL) -> dict:
    data = '{"context":{"client":{"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20210811.00.00","osName":"Windows","osVersion":"10.0","platform":"DESKTOP","browserName":"Chrome",}, },"continuation":' + f'"{continuation}"' + '}'

    try:
        respsonce = session.post(commentsURL, data=data)
        return respsonce.json()

    except Exception as e:
        print("Youtube request is not json.", e)
        return {}
