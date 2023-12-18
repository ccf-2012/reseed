import os, re
import requests as pyrequests
from http.cookies import SimpleCookie
import bencodepy
import argparse


ARGS = None
# 下载种子
def downloadTorrentData(downloadLink, sitecookie=None):
    if sitecookie:
        cookie = SimpleCookie()
        cookie.load(sitecookie)
        cookies = {k: v.value for k, v in cookie.items()}
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Content-Type': 'text/html; charset=UTF-8'
        }

        response = pyrequests.get(downloadLink, headers=headers, cookies=cookies)
    else:
        response = pyrequests.get(downloadLink)

    if not response.status_code == 200:
        return ''

    return response.content

def getFileWithPattern(dirpath, pattern):
    for filename in os.listdir(dirpath):
        m = re.match(pattern,  filename, re.I)
        if m:
            return os.path.join(dirpath, filename)
    return ''

def torrentReseed(torrent_data):
    decoded_torrent = bencodepy.decode(torrent_data)
    print('created by: ' + decoded_torrent[b'created by'].decode('utf-8'))
    m = re.match(r'(https?://[^/]+/)', decoded_torrent[b'announce'].decode('utf-8'))
    if m:
        astr = m.group(1)
        print('announce (host only): ' + astr)

    # data = tp.parse_torrent_file(torrent_filepath)
    if b'info' in decoded_torrent:
        info = decoded_torrent[b'info']
        if b'name' in info:
            basedir = info[b'name'].decode('utf-8')
            print(f"文件夹名: {basedir}")
        if ARGS.srcpath:
            renpath = os.path.join(os.path.dirname(ARGS.destpath), basedir)
            print(f"symlink: {ARGS.srcpath} -> {renpath}")
            os.symlink(ARGS.srcpath, renpath)

        if b'files' in info:
            print("文件列表:")
            for file_info in info[b'files']:
                if b'path' in file_info:
                    file_path = '/'.join([x.decode('utf-8') for x in file_info[b'path']])
                    print(file_path)
                    if ARGS.srcpath:
                        m = re.match(r'S\d+E\d+', file_path, re.I)
                        if m:
                            pattern = m.groups(1)
                            srcfile = getFileWithPattern(ARGS.srcpath, pattern)
                            if srcfile:
                                renpath = os.path.join(os.path.dirname(ARGS.destpath), file_path)
                                print(f"symlink: {srcfile} -> {renpath}")
                                os.symlink(srcfile, renpath)
                            else:
                                print(f"pattern {pattern} not found in {ARGS.srcpath}")

    else:
        print("无法解析.torrent文件")

def ensureDir(file_path):
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    if not os.path.exists(file_path):
        os.makedirs(file_path)


def loadArgs():
    global ARGS
    parser = argparse.ArgumentParser(
        description='download torrent file and rename local file to reseed')
    parser.add_argument('-s', '--srcpath', type=str,  help='the local folder to be reseed.')
    parser.add_argument('-d', '--destpath', type=str,  help='the dest folder to be symbol-linked.')
    parser.add_argument('-t', '--torrenturl', type=str, required=True, default='', help='the torrent url.')
    # parser.add_argument('--info', action='store_true', help='display the torrent info.')
    ARGS = parser.parse_args()
    if ARGS.srcpath:
        ARGS.srcpath = os.path.expanduser(ARGS.srcpath)
        if not os.path.exists(ARGS.srcpath):
            print(f"Local file not exists: {ARGS.srcpath}")
            exit(1)
        if not ARGS.destpath:
            ARGS.destpath = os.path.join(os.path.dirname(ARGS.srcpath), 'reseedlink')
            print("dest path = " + ARGS.destpath)
            ensureDir(ARGS.destpath)


def main():
    loadArgs()
    url = ARGS.torrenturl
    torbytes = downloadTorrentData(url)
    if torbytes:
        torrentReseed(torbytes)
    # else:



if __name__ == '__main__':
    main()