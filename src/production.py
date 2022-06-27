import requests , re ,os 
from clint.textui import progress
from pystyle import Colorate, Colors, Write
try :
    os.mkdir("downloads")
except FileExistsError :
    pass

cwd= os.getcwd()
hd ={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}

def clean():
    os.system("cls||clear")

def close(msg):
    input(msg)
    exit()

def getId(url):
    if ('@') and ('?') in url:
        return re.search('video/(.*?)\?' ,url).group(1)
    elif ('@') and not ('?') in url:
        return url.split('/')[-1]
    else : 
        return re.search('share_item_id=(.*?)&',requests.get(url , headers=hd , allow_redirects=True).url).group(1)

def getTikJson(id):
    requrl = f'https://api-t2.tiktokv.com/aweme/v1/aweme/detail/?aweme_id={id}'  
    r = requests.get(requrl , headers=hd )
    return r.json()

def openFolder(path):
    os.system(f'explorer "{os.path.realpath(path)}"')


def setupDownload(id):
    try :
        os.mkdir("downloads/{}".format(id))
    except FileExistsError :
        print("Folder already exist {}".format(id))
        menu = """ 
        [1].Open folder
        [2].Download again
        [3].Exit
        """
        try:
            choic = int(input(menu))
        except ValueError :
            clean()
            setupDownload(id)
        
        if choic == 1:
            path = cwd + "/downloads/{}".format(id)
            openFolder(path)
            close("Press Enter To Close ...")
        elif choic == 2:
            pass
        elif choic == 3:
            exit()

def getTagsOfVideo(j):
    counter = 0
    for x in j :
        print('#{}'.format(x['hashtag_name']) , file=open(cwd +"/downloads/{}/{}-hashtags.txt".format(videoId,videoId) , 'a' ,encoding='utf-8'))
        counter += 1
    print("Total Tags : {}".format(counter))

def downloadGlobal(url , filetype):
    r = requests.get(url ,stream=True )
    print('Downloading {}'.format(url))
    with open(cwd +"/downloads/{}/{}.{}".format(videoId,videoId ,filetype), 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()



if __name__ == "__main__":

    banner = """
    ████████▀▀▀████
    ████████────▀██
    ████████──█▄──█
    ███▀▀▀██──█████
    █▀──▄▄██──█████
    █──█████──█████
    █▄──▀▀▀──▄█████
    ███▄▄▄▄▄███████
    ╔══╦╦╦╗╔══╦═╦╦╗
    ╚╗╔╣║═╣╚╗╔╣║║═╣
    ═╚╝╚╩╩╝═╚╝╚═╩╩╝
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    TikTok Scrapper by @cr1
    This tool is made for educational purposes only.
    Im not responsible for any damage caused by this tool.
    """
    print(Colorate.Vertical(Colors.red_to_white, banner))
    videoURL = Write.Input(" « Video Link »  ", Colors.blue, interval=0.05)
    videoId = getId(videoURL)
    setupDownload(videoId)
    allJson = getTikJson(videoId)
    noWaterMarkUrl = allJson['aweme_detail']['video']['play_addr']['url_list'][0]
    musicUrl = allJson['aweme_detail']['music']['play_url']['uri']
    menu = """
        [1].Download Video Only
        [2].Download Music Only
        [3].Download hashtags
        [4].Download all
    """
    choice = int(input(menu))
    if choice == 1:
        downloadGlobal(noWaterMarkUrl , '.mp4')
    elif choice == 2:
        downloadGlobal(musicUrl , '.mp3')
    elif choice == 3:
        getTagsOfVideo(allJson['aweme_detail'] ['text_extra'])
    elif choice == 4:
        downloadGlobal(noWaterMarkUrl , '.mp4')
        downloadGlobal(musicUrl , '.mp3')
        getTagsOfVideo(allJson['aweme_detail'] ['text_extra'])
    else:
        print("Invalid Choice")
    path = cwd + "/downloads/{}".format(videoId)
    openFolder(path)
    close('Download Complete ... \nPress Enter to exit ...')





