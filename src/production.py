import requests, re, os, json
from clint.textui import progress
from pystyle import Colorate, Colors, Write
from datetime import datetime

try:
    os.mkdir("downloads")
except FileExistsError:
    pass

cwd = os.getcwd()
hd = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'accept': 'application/json'
}

def clean():
    os.system("cls||clear")

def close(msg):
    input(msg)
    exit()

def getId(url):
    if ('@') and ('?') in url:
        return re.search(r'video/(.*?)\?', url).group(1)
    elif ('@') and not ('?') in url:
        return url.split('/')[-1]
    else:
        return re.search('share_item_id=(.*?)&', requests.get(url, headers=hd, allow_redirects=True).url).group(1)

def getTikJson(id):
    requrl = f'https://api22-normal-c-alisg.tiktokv.com/aweme/v1/feed/?aweme_id={id}&iid=7238789370386695942&device_id=7238787983025079814&resolution=1080*2400&channel=googleplay&app_name=musical_ly&version_code=350103&device_platform=android&device_type=Pixel+7&os_version=13'
    r = requests.get(requrl, headers=hd)
    data = r.json()
    if data.get('aweme_list') and len(data['aweme_list']) > 0:
        return data['aweme_list'][0]
    raise Exception("Video not found or API response invalid")

def openFolder(path):
    os.system(f'explorer "{os.path.realpath(path)}"')

def setupDownload(id):
    try:
        os.mkdir("downloads/{}".format(id))
    except FileExistsError:
        print("Folder already exists {}".format(id))
        menu = """
        [1].Open folder
        [2].Download again
        [3].Exit
        """
        try:
            choic = int(input(menu))
        except ValueError:
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

def getVideoInfo(json_data):
    info = {
        'author': json_data.get('author', {}).get('nickname', 'Unknown'),
        'desc': json_data.get('desc', ''),
        'create_time': datetime.fromtimestamp(json_data.get('create_time', 0)).strftime('%Y-%m-%d %H:%M:%S'),
        'likes': json_data.get('statistics', {}).get('digg_count', 0),
        'comments': json_data.get('statistics', {}).get('comment_count', 0),
        'shares': json_data.get('statistics', {}).get('share_count', 0)
    }
    
    with open(f"{cwd}/downloads/{videoId}/info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=4, ensure_ascii=False)
    print("\nVideo Information:")
    print(f"Author: {info['author']}")
    print(f"Description: {info['desc']}")
    print(f"Created: {info['create_time']}")
    print(f"Likes: {info['likes']}")
    print(f"Comments: {info['comments']}")
    print(f"Shares: {info['shares']}\n")

def getTagsOfVideo(json_data):
    hashtags = []
    if 'text_extra' in json_data:
        for tag in json_data['text_extra']:
            if 'hashtag_name' in tag:
                hashtags.append(f"#{tag['hashtag_name']}")
    
    with open(f"{cwd}/downloads/{videoId}/{videoId}-hashtags.txt", 'w', encoding='utf-8') as f:
        f.write('\n'.join(hashtags))
    print(f"Total Tags: {len(hashtags)}")
    return hashtags

def downloadGlobal(url, filetype):
    r = requests.get(url, stream=True)
    print('Downloading {}'.format(url))
    with open(cwd + "/downloads/{}/{}.{}".format(videoId, videoId, filetype), 'wb') as f:
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
    TikTok Scrapper v2.0
    Enhanced with detailed video info
    """
    print(Colorate.Vertical(Colors.red_to_white, banner))
    videoURL = Write.Input(" « Video Link »  ", Colors.blue, interval=0.05)
    videoId = getId(videoURL)
    setupDownload(videoId)
    
    try:
        video_data = getTikJson(videoId)
        noWaterMarkUrl = video_data['video']['play_addr']['url_list'][0]
        musicUrl = video_data['music']['play_url']['uri']
        
        menu = """
        [1].Download Video Only
        [2].Download Music Only
        [3].Download hashtags
        [4].View Video Info
        [5].Download All (Video + Music + Info + Tags)
        [6].Exit
        """
        choice = int(input(menu))
        
        if choice == 1:
            downloadGlobal(noWaterMarkUrl, 'mp4')
        elif choice == 2:
            downloadGlobal(musicUrl, 'mp3')
        elif choice == 3:
            getTagsOfVideo(video_data)
        elif choice == 4:
            getVideoInfo(video_data)
        elif choice == 5:
            downloadGlobal(noWaterMarkUrl, 'mp4')
            downloadGlobal(musicUrl, 'mp3')
            hashtags = getTagsOfVideo(video_data)
            getVideoInfo(video_data)
        elif choice == 6:
            exit()
        else:
            print("Invalid Choice")
        
        path = cwd + "/downloads/{}".format(videoId)
        openFolder(path)
        close('Download Complete ... \nPress Enter to exit ...')
    except Exception as e:
        print(f"Error: {str(e)}")
        close('Press Enter to exit ...')
