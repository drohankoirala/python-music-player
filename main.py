import os

if not os.path.exists('res\\Music-data.json'):
    import setup

    setup.from_main = True
    setup.Setup()
    setup.runShell()
    exit()

import datetime
import json
import random
import time
import string
from flask import Flask, jsonify, request, abort, send_from_directory, send_file, make_response, render_template

app = Flask(__name__)
dataCopy = None
list_ = []


class SHandler:
    def __init__(self):
        with open('res\\Music-data.json') as d:
            self.data = json.load(d)
            if len([_ for _ in self.data.keys()]) <= 3:
                import setup
                setup.from_main = True
                setup.Setup()
                setup.runShell()
                exit()
        self.this = self.generate_unique_id()
        if not self.data.get("act"):
            self.data['act'] = {}
        self.data["act"][self.this] = self.data.get('act', {}).get(self.this) or {}
        self.ine = {}
        self.recommend_ = None
        self.added = []
        self.arrange = None

    @staticmethod
    def generate_unique_id():
        random_chars = ''.join(random.choices(string.ascii_letters + string.ascii_letters, k=8))
        return random_chars

    @staticmethod
    def checkValidation(key: str):
        if key:
            try:
                curMilliSec = int(time.time())
                argMilliSec = int(key, 24) / 1000
                if (curMilliSec - 5) < argMilliSec < (curMilliSec + 5):
                    return True
            except Exception:
                pass
        return False

    def saveMusic(self):
        with open('res\\Music-data.json', 'w') as df:
            json.dump(self.data, df)

    def rec_(self):
        rData = {}
        for kl in self.data:
            if type(self.data[kl]) is dict:
                cvb = self.data[kl].get('act')
                if cvb and not rData.get(kl):
                    rData[kl] = (cvb.get('dur') or 0) * (cvb.get('count') or 0)

        self.arrange = [song_id for song_id, _ in sorted(rData.items(), key=lambda x: x[1], reverse=True)]
        return self.arrange

    def recommend_songs(self, force=False, options=None):
        if options is None:
            options = {}
        if self.recommend_ and not force:
            return self.recommend_
        id_ = options.get('user', datetime.datetime.now().strftime("%Y%m%d%h"))
        if self.ine.get(id_):
            print('returned')
            return self.ine[id_]
        user_data = self.data.get("act", {})
        today = user_data.get(id_)
        if not today:
            self.recommend_ = []
            return self.recommend_
        filtered_data = {
            user: {song: duration for song, duration in songs.items() if duration > 20}
            for user, songs in user_data.items()
        }
        our_user = set(today.keys())
        most_common = [
            [user, len(set(data_.keys()) & our_user)] for user, data_ in filtered_data.items() if user != today
        ]
        most_common.sort(key=lambda x: x[1], reverse=True)
        found_songs = {}
        for user, _ in most_common[:30]:
            for song, duration in filtered_data[user].items():
                if song not in our_user and song not in found_songs and song not in self.added:
                    found_songs[song] = duration

        self.recommend_ = [song_id for song_id, _ in sorted(found_songs.items(), key=lambda x: x[1], reverse=True)][:20]
        if len(self.recommend_) < 20:
            for __ in range(20 - len(self.recommend_)):
                if len(self.arrange) >= __: break
                self.recommend_.append(self.arrange[__] if len(self.arrange) < __ else 0)
        random.shuffle(self.recommend_)
        self.added += self.recommend_
        self.ine[id_] = self.recommend_
        return self.recommend_


ghn = SHandler()
ghn.rec_()


def respo(code=404, file='400.html'):
    response = make_response(render_template(file))
    response.status_code = code
    return response


@app.errorhandler(400)
def notfound(n):
    return respo(400, '400.html')


@app.errorhandler(404)
def notfound(n):
    return respo(404, '400.html')


@app.route('/thumb')
def thumbnail():
    loc = request.args.get('id')
    if not loc or not ghn.data.get(loc):
        abort(400)
    img = ghn.data[loc]['src']['img']['limg'].split('\\')[-1]
    return send_from_directory("Music\\thumbnails\\", img)


@app.route('/api/lists')
def list__():
    id_ = request.args.get('id')
    if not id_:
        abort(400)
    elif id_ == '_':
        rData = ghn.data.get('lists', {})
    else:
        rData = ghn.data.get('lists', {}).get(id_, {})
    return jsonify(rData), 200


@app.route('/api/views')
def views():
    rData = {"ls": [], 'vd_top': {'ls': []}, 'vd_lss': {'ls': []}, 'vd_mid': {'ls': []}}

    trf_ = [kjh for kjh in ghn.data.get('act', [])]
    random.shuffle(trf_)
    sKeys = [ghn.arrange[0]]
    for ind, ijh in enumerate(trf_):
        rfg = ghn.recommend_songs(True, {'user': ijh})
        if not rfg:
            continue
        id_ = rfg[0]
        if id_ in sKeys:
            continue
        rfg = ghn.data[id_]
        rData['ls'].append({
            "ur": ijh + '?play=' + id_,
            'tl': rfg['t']['c'], })
        sKeys.append(id_)

    ghn.ine["recommended"] = sKeys
    sKeys = []
    iuj = ghn.arrange[:50]
    random.shuffle(iuj)
    for jhn in iuj:
        if len(sKeys) >= 12:
            break
        elif jhn in sKeys:
            continue
        cur = ghn.data[jhn]
        rData['vd_top']['ls'].append({'ig': cur['src']['img']['limg'],
                                      "ur": jhn,
                                      'tl': cur['t']['c']})
        sKeys.append(jhn)
    rData['vd_top']['lst'] = sKeys
    sKeys = []
    iuj = ghn.arrange[-50:]
    random.shuffle(iuj)
    for jhn in iuj:
        if len(sKeys) >= 12:
            break
        elif jhn in sKeys:
            continue
        cur = ghn.data[jhn]
        rData['vd_lss']['ls'].append({'ig': cur['src']['img']['limg'],
                                      "ur": jhn,
                                      'tl': cur['t']['c']})
        sKeys.append(jhn)
    rData['vd_lss']['lst'] = sKeys
    sKeys = []
    iuj = ghn.arrange[50:-50]
    random.shuffle(iuj)
    for jhn in iuj:
        if len(sKeys) >= 24:
            break
        elif jhn in sKeys:
            continue
        cur = ghn.data[jhn]
        rData['vd_mid']['ls'].append({'ig': cur['src']['img']['limg'],
                                      "ur": jhn,
                                      'tl': cur['t']['c']})
        sKeys.append(jhn)
    rData['vd_mid']['lst'] = sKeys

    return jsonify(rData), 200


@app.route('/api/view')
def view():
    hgf = request.args.get('view_id')
    if not hgf:
        abort(400)
    rData = ghn.recommend_songs(True, options={'user': hgf})
    return jsonify(rData), 200


@app.route('/api/get_songs')
def get_songs():
    global dataCopy, list_
    if not dataCopy:
        dataCopy = dataCopy or {}
        tTemp = ghn.data.copy()
        for jk in tTemp:
            if jk not in ['loc', 'act', 'loc_song', 'lists']:
                dataCopy[jk] = tTemp[jk]
                list_.append(jk)
    ghn.added = []
    songs = {"files": dataCopy, 'fetched': time.time(), 'playlist': list_}
    return jsonify(songs)


@app.route("/api/opt", methods=["POST"])
def add_opt():
    jk = request.json.get('option')
    typeOFRequest = jk.get('type')
    if not ghn.data.get(jk.get('id', '----')):
        abort(400)
    stem = ghn.data[jk.get('id')]
    ui = (stem.get('act')) or {'count': 0, 'd': [], 'dur': 0}
    if typeOFRequest == 'change':
        ui['d'].append(jk['cdur'])

    elif typeOFRequest == 'interval':
        fvb = (jk.get('Pdur') / stem['src']['len'])
        fvb = 100 if fvb > 1 else (fvb * 100)
        ui['dur'] = (ui.get('dur') or 0) + fvb
        ghn.data['act'][ghn.this][jk.get('id')] = fvb + ghn.data['act'][ghn.this].get(jk.get('id'), 0)

    elif typeOFRequest == 'click':
        ui['count'] += 1
        ui['dur'] += 10

    elif typeOFRequest == 'item_skip':
        ui['count'] -= (1 if ui.get('count', 0) > 5 else 0)
        ui['dur'] -= (5 * (stem['src']['len'] / 100)) if ui.get('dur', 0) > 20 else 0

    elif typeOFRequest == 'song-ended':
        ui['dur'] += (5 * (stem['src']['len'] / 100))

    ghn.data[jk['id']]['act'] = ui
    ghn.saveMusic()
    return '', 200


@app.route("/api/audio")
def stream_audio():
    file = request.args.get('id')
    if not file or not ghn.data.get(file):
        abort(400)
    file = ghn.data[file]['src']['lsrc'].split('\\')[-1]
    return send_from_directory("Music\\", file)


@app.route("/")
def player():
    return send_file("templates/index.html")


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Origin, Accept'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response


# Only for Fun/No use
@app.before_request
def check():
    if '/api' not in request.path:
        return
    key = request.args.get('key')
    if not ghn.checkValidation(key or ''):
        abort(400)


if __name__ == '__main__':
    import webbrowser; webbrowser.open('http://localhost:5000/')
    print('---- Listening on "http://localhost:5000/" Enjoy! ----')
    app.run(host='0.0.0.0', port=5000, debug=True)
