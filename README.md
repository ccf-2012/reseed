# Reseed
* rename the torcp-ed dir back to torrent folder/file


## requirements
```sh
pip install -r requirements.txt
```

## run
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
# 在 `~/reseed` 目录下，建立一个 `reseedlink` 目录，将源目录symbol link到此目录下
reseed.py -s ~/reseed/tordir -t 'https://some.pt/download.php?id=.......'
```