#-.-coding:utf-8

import os
import json

dir = r"C:/Users/Administrator/Documents/EgretProjects/eui_font_test/resource/fonts"
spriteSheetJson = r"C:/Users/Administrator/Documents/EgretProjects/eui_font_test/resource/fonts/fonts.json"

imgDict = {}
spriteImg = ""

def getFileName(file):
    fileInfo = file.split(r'.')
    length = len(fileInfo)
    if length <= 2:
        return fileInfo[0]
    else:
        return r'.'.join(fileInfo[0:length-1])

def getFileExt(file):
    fileInfo = file.split(r'.')
    length = len(fileInfo)
    if length > 1:
        return fileInfo[length - 1]
    else:
        return ""

def getFileByExt(dir, ext):
    files = os.listdir(dir)
    return filter(lambda x: getFileExt(x) == ext, files)

def readFile(file):
    print r"readFile: [{}]".format(file)
    fd = os.open(file,os.O_RDONLY)
    info = ""
    while(1):
        string = os.read(fd,1024)
        if string:
            info += string
        else:
            break
    os.close(fd)

    try:
        return json.loads(info)
    except Exception,e:
        print r"json loads error: %s" % e.message

def parseSpriteInfo(info):
    global spriteImg
    global imgDict
    spriteImg = info["file"]
    frames = info['frames']
    for k,v in frames.iteritems():
        imgDict[k] = v

def main():
    spriteInfo = readFile(spriteSheetJson)
    parseSpriteInfo(spriteInfo)
    fntFiles = getFileByExt(dir,"fnt")
    for fntFile in fntFiles:
        absFileName = os.path.join(os.path.abspath(dir),fntFile)
        fileInfo = readFile(absFileName)
        imgFile = fileInfo["file"]
        if imgFile:
            name = getFileName(imgFile)
            ext = getFileExt(imgFile)
            resName = r"{}_{}".format(name,ext)
            if(imgDict.has_key(resName)):
                fileInfo["file"] = spriteImg
                for k,v in fileInfo["frames"].iteritems():
                    v["x"] += imgDict.get(resName).get("x",0) - imgDict.get(resName).get("offX",0)
                    v["y"] += imgDict.get(resName).get("y",0) - imgDict.get(resName).get("offY",0)
                fp = file(absFileName,"w")
                json.dump(fileInfo,fp)
                print r"convert file [{}] success".format(absFileName)
            else:
                print r"convert file [{}] failed".format(absFileName)
        else:
            print r"convert file [{}] failed".format(absFileName)


if __name__ == "__main__":
    main()

