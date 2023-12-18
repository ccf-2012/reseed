# Reseed
* 当一些种子为了刮削作了目录结构的重组并修改了文件名，本程序尝试把这样的媒体文件夹以软链(symbol link)方式重组成原种子文件所定义的文件夹和文件名


## requirements
```sh
pip install -r requirements.txt
```

## 运行
```sh
python reseed.py -h

usage: reseed.py [-h] [-s SRCPATH] [-d DESTPATH] -t TORRENTURL

download torrent file and rename local file to reseed

options:
  -h, --help            show this help message and exit
  -s SRCPATH, --srcpath SRCPATH
                        the local folder to be reseed.
  -d DESTPATH, --destpath DESTPATH
                        the dest folder to be symbol-linked.
  -t TORRENTURL, --torrenturl TORRENTURL
                        the torrent url.
```


## examples
```sh
# 在 `~/gd` 目录下，建立一个 `relink` 目录，将源目录symbol link到此，并将其中的mkv/mp4文件，按集数对应到种子文件的源文件名
python3 reseed.py -s ~/gd/'The Lying Life of Adults (2023) {tmdb-103416}'/S01  -d ~/gd/relink -t 'https://some.pt/download.php?id=101452&downhash='


# 不加 -s -d 参数则下载种子然后解析种子中的信息
python3 reseed.py  -t 'https://some.pt/download.php?id=236338&downhash='
```