import datetime
import json
import os
import shutil
import time

try:
    import requests
    from pytube import YouTube, Playlist
    from selenium.webdriver.common.by import By
    from selenium import webdriver
except ImportError:
    os.system('pip install pytube selenium requests')
    import requests
    from pytube import YouTube, Playlist
    from selenium.webdriver.common.by import By
    from selenium import webdriver

current_time_str = datetime.datetime.now().strftime('%Y-%m-%d')
ti = datetime.datetime.strptime(current_time_str, '%Y-%m-%d')
from_main = False
os.system('cls')
print("""HNPlayer Handler, Version 1.0.1, by drohan""")
if not os.path.exists('res/Music-Data.json'):
    os.system('mkdir res')
    with open('res/Music-Data.json', 'w') as d:
        print("Created \"res/Music-Data.json\", Reason [json file was deleted/haven't run"
              " \"setup.py\" before/json files location was changed]")
        json.dump({'loc': os.getcwd() + '/Music/', 'loc_song': os.getcwd() + '/Music/thumbnails/'}, d)

with open('res/Music-Data.json') as d:
    list_ = json.load(d)

if not os.path.exists(list_['loc_song']):
    os.mkdir(list_['loc'])
    os.mkdir(list_['loc_song'])


def Setup():
    print("""
Before running "main.py," ensure you have at least one song installed. You can add songs to the system using simple commands:

To download one song: dwd  -f  https://www.youtube.com/watch?v=----VIDEO_ID----
To download all songs from a playlist: dwd  -l  https://www.youtube.com/playlist?list=----list_ID----
For more commands, type "help."

This script stores user activity in "Music-data.json" in the "res/" directory. Make sure not to remove this file. The JSON file contains information about songs, you interaction on songs, for recommendation. You can use simple commands to download, remove, change the location, or reinstall mistakenly removed items, along with the thumbnail of the item from YouTube.

All the downloaded item are stored on "Music" directory "./Music", use command to change the location else not

Try the command "help" for more details.
""")


def save():
    with open('res/Music-Data.json', 'w') as ds:
        json.dump(list_, ds)


class Download:
    def clear(self, string):
        rSt = ''
        for fg in string:
            if fg not in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                rSt += fg
        return rSt

    def download(self, url, options=None, force=False):
        if options is None:
            options = {}
        fvc = list_.get(url.split('v=')[1])
        print(f'Download "{url}"', end='')
        if fvc and not force:
            if os.path.exists(fvc['src']['lsrc']):
                print(' [Skipped]')
                return
        try:
            rfc = YouTube(url)
            t_l = self.clear(rfc.title)
            rfc.streams.filter(only_audio=True).first().download(list_['loc'], filename_prefix=t_l, filename='.mp3')
        except Exception as e:
            print(f' [Failed] [Reason => {e}]')
            return
        img_ = requests.get(rfc.thumbnail_url).content
        lim_ = f"{list_['loc_song']}{t_l}.jpg"
        with open(lim_, 'wb') as _:
            _.write(img_)
        act_ = (list_.get(rfc.video_id) or {})
        title = options.get('title') or (act_.get('t') or {}).get('c') or rfc.title
        act_ = act_.get('act') or {"count": 0, "d": []}
        list_[rfc.video_id] = {
            'src': {
                'csrc': rfc.watch_url,
                'lsrc': list_['loc'] + t_l + '.mp3',
                'img': {
                    'cimg': rfc.thumbnail_url,
                    'limg': lim_
                },
                'len': rfc.length
            },
            't': {
                'c': title,
                'l': t_l,
            },
            "act": {
                "count": act_.get("count") + 1,
                "d": act_.get('d'),
                "dur": (act_.get("dur") or 0) + 50
            }
        }
        save()
        print(" [Done]")


def runShell():
    while True:
        multiArgs = input(f"\n{ti} > ").split('  ')

        def get_argument(index):
            try:
                return multiArgs[index]
            except IndexError:
                return None

        cmd = get_argument(0)

        if cmd == 'curl':
            return


        elif cmd == 'move':
            target_dir = get_argument(1)
            if not target_dir or not os.path.exists(target_dir) or (target_dir[-1] != '/' and target_dir[-1] != '\\'):
                print('Error: (Invalid Path/Not ended with backslash) for move --move-dir--')
                continue
            skp = 0
            if not os.path.exists(target_dir + 'thumbnails/'):
                os.mkdir(target_dir + 'thumbnails/')
            move_song_only = get_argument(2) == '--song'
            move_img_only = get_argument(2) == '--img'
            for kl in list_:
                if type(list_[kl]) is dict:
                    if type(list_[kl].get('src')) is not dict:
                        continue
                    cur = list_[kl]['src']['lsrc']
                    cur_song = list_[kl]['src']['img']['limg']
                    if not os.path.exists(cur) or not os.path.exists(cur_song):
                        skp += 1
                        continue
                    chg = list_[kl]['src']['lsrc'].replace(list_['loc'], target_dir)
                    print(list_[kl]['src']['img']['limg'], list_['loc_song'])
                    chg_song = list_[kl]['src']['img']['limg'].replace(list_['loc_song'], target_dir)
                    if move_img_only:
                        print(cur_song, ' => ', chg_song)
                        shutil.move(cur_song, chg_song)
                        list_[kl]['src']['img']['limg'] = chg_song
                    elif move_song_only:
                        shutil.move(cur, chg)
                        list_[kl]['src']['lsrc'] = chg
                    else:
                        print('Error: Missing parameters.')
                        continue
            if move_img_only:
                list_['loc_song'] = target_dir
            if skp:
                print(f'Items were restored to {target_dir}, {skp} items were not found on {list_["loc"]}\nRun "scan" '
                      f'for details.')

            list_['loc'] = target_dir
            save()

        elif cmd == 'scan':
            if get_argument(1) == '-u':
                continue
            j = 0
            miss = []
            for kl in list_:
                if type(list_[kl]) is dict:
                    if type(list_[kl].get('src')) is not dict:
                        continue
                    cur = list_[kl]
                    songEx = os.path.exists(cur['src']['lsrc'])
                    thumEx = os.path.exists(cur['src']['img'].get('limg') or 'Invalid/path')
                    if not songEx or not thumEx:
                        j += 1
                        miss.append([
                            f"""[404 ==> {"song" if not songEx else "_img"}] "{cur['t']['c'][:35]}"-  [Failed] for ({cur['src']['lsrc']})""",
                            kl])
                    else:
                        if get_argument(1) != '-r':
                            print(f"""[200] [Succes] "{cur['t']['c']}"-""")

            for _ in miss:
                if get_argument(1) == '-r':
                    del list_[_[1]]
                print(_[0])
            if j:
                print(f"""\nRun "dwd  -m" to reinstall missing songs
    Run "dwd  -t  -m" to reinstall missing songs img,
    Run "scan  -r" to remove missing items,
    {j} items are missing\n""")
            else:
                print('\nEverything looks good.\n')
            save()

        elif cmd == 'dwd':
            if get_argument(1) == '-m':
                for kl in list_:
                    if type(list_[kl]) is dict:
                        if type(list_[kl].get('src')) is not dict:
                            continue
                        Download().download(list_[kl].get('src')['csrc'],
                                            force=True if get_argument(2) == '-f' else False)
                print('\nAll missing items were restored.')

            elif get_argument(1) == '-l' and '?list=' in get_argument(2):
                l = Playlist(get_argument(2))
                if not l.video_urls:
                    print('Error: (Private list/No Internet/Empty list) "help" for more.')
                    continue
                list_['lists'][l.playlist_id] = {"t": l.title, "l": []}
                for k in l.video_urls:
                    list_['lists'][l.playlist_id]['l'].append(k.split('v=')[-1])
                    Download().download(k, force=True if get_argument(3) == '-f' else False)
                save()
            elif get_argument(1) == '-f' and 'v=' in get_argument(2):
                Download().download(get_argument(2), force=True if get_argument(3) == '-f' else False)

            elif get_argument(1) == '-t':
                if get_argument(2) == '-m':
                    for kl in list_:
                        if type(list_[kl]) is dict:
                            if type(list_[kl].get('src')) is not dict:
                                continue
                            cur = list_[kl]['src']['img'].get('limg') or 'invalid/path'
                            if not os.path.exists(cur):
                                limg = f"{list_['loc']}thumbnails/{list_[kl]['t']['l']}.jpg"
                                cimg = list_[kl]['src']['img']['cimg']
                                print(f'Download "{cimg}"', end='')
                                img = requests.get(cimg).content
                                with open(limg, 'wb') as d:
                                    d.write(img)
                                list_[kl]['src']['img']['limg'] = limg
                                print(" [Done]")
                                save()

            else:
                print('Error: Missing parameters')

        elif cmd == 'help':
            print("""HNPlayer Handler, Version 1.0.1, by drohan

curl -url-: [only for me]
Downloads music files from a specified URL. The URL should contain ?v= and list= parameters.
Example: curl https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID

move --move-dir--:
Moves downloaded music files to a specified directory. The directory path should end with a backslash (/).
Example: move C:/Users/username/Music/

scan:
Scans for missing music files. It checks if the files listed in the JSON file exist in the current directory.

dwd -m:
Downloads missing music files. It downloads the files listed in the JSON file that are missing from the current directory.

dwd -l url:
Downloads music files from a playlist URL. The URL should contain ?v= and list= parameters.
Example: dwd -l https://www.youtube.com/playlist?list=PLAYLIST_ID
Note: Your Playlist should be Unlisted or Public.

dwd -f url:
Downloads a specific music file from a URL. The URL should contain a ?v= parameter.
Example: dwd -f https://www.youtube.com/watch?v=VIDEO_ID

exit:
Exits the program.

Note: Don't run any command marked [only for me] and use 2 space for args,
Eg: dwd -f -url- [use of single space is not allowed].
: dwd  -f  -url- [use of double space is only allowed].
""")

        elif cmd == 'exit':
            break

        else:
            print(f'Error: (Unknown/Invalid/Single Space separation), Run "help" for details.')


if __name__ == '__main__':
    runShell()
