from cProfile import run
from psychopy import visual, core, event, logging, monitors  # import some libraries from PsychoPy import os
import random
import time
import os
import pandas as pd
from datetime import datetime
from psychopy.hardware.emulator import launchScan
from psychopy import prefs
prefs.hardware['audioLib'] = ['pyo','PTB','sounddevice','pygame']
prefs.saveUserPrefs()
from psychopy import sound
print (sound.Sound)


startingTime=time.time()
oldrel=0


def writeTimeEvent(event,start=False,cevap=False):
    global data, startingTime,oldrel
    now = datetime.now()
    if start:
        startingTime=time.time()
        log={"event":event,"AbsTime":now,"RelTime":0}
    else:
        rel=time.time()-startingTime
        rel=float("%.5f" % rel) 
        dur=float("%.5f" % (rel-oldrel)) 
        log={"event":event,"AbsTime":now,"RelTime":rel,"duration":dur}
        if cevap:
            log["answer"]=cevap
        oldrel=rel
    data=data.append(log, ignore_index=True)

initialData={"Subject No:":"","Session No:":"","Run No:":""}
def getInitialData():
    for i in initialData:
        val=input(f"Please enter {i}: ")
        initialData[i]=val
    return initialData

dir_path = os.path.dirname(os.path.realpath(__file__))


mon = monitors.Monitor('Experiment',width=66,distance=50)
mon.setSizePix([1920,1080])
mywin = visual.Window([1920,1080], monitor=mon, screen=1, units="deg",fullscr=True)
mywin.mouseVisible = False





def loadVideos():
    
    videos=os.listdir(dir_path+"/videos")
    videos_load=[]
    for i in videos:
        vid=visual.MovieStim3(mywin, dir_path+"/videos/"+i, size=(550,340), flipHoriz=True, autoLog = True)
        vid.name=i
        videos_load.append(vid)
    return videos_load

def isi():
    total = 0
    while total != 35*8:
        arr=random.sample(range(30,40),8)
        total=sum(arr)
    return [x/10  for x in arr]

def showText(text,t): 
    stim = visual.TextStim(mywin, text,flipHoriz=True)
    stim.wrapWidth=100
    clock = core.Clock()
    while clock.getTime() < t: 
        stim.draw()
        mywin.flip()

def showPlus(t):
    fix_stim = visual.TextStim(mywin, text="+", units="pix",height=64,color="black")
    clock = core.Clock()
    while clock.getTime() < t: 
        fix_stim.draw()
        mywin.flip()




def showPhoto(path,t): 
    path=dir_path+"/photos/"+path
    stim = visual.ImageStim(mywin, path, size=(0.8,0.8))
    stim.draw()
    mywin.flip()
    core.wait(t)


def getResponse(text,video,part): 
    stim = visual.TextStim(mywin, text, flipHoriz=True)
    stim.wrapWidth=100
    res=[]
    stim.draw()
    mywin.update()
    for i in range(24):
        deneme=event.getKeys(keyList=["1","2","3","4"])
        core.wait(0.1)
        if deneme!=[]:
            res=deneme
            cevap=str(parts[part]["answer"][video]==res[0])
            writeTimeEvent(f"Button Pressed:{res[0]}",cevap=cevap)
        
    if res==[]:
        writeTimeEvent(f"No button Pressed!!!")
        

fixation = visual.GratingStim(mywin, tex=None, mask='gauss', sf=0, size=0.5,
    name='fixation', autoLog=False)
fixation.color="black"


def showVideo(video): 
    video.play()
    #time.sleep(0.05)
    writeTimeEvent(f"video başladı: {video.name}")
    # while video.status != visual.FINISHED:
    #     video.draw()
    #     fixation.draw()
    #     mywin.flip()    
    clock = core.Clock()
    while clock.getTime() < 3.0: 
        video.draw()
        fixation.draw()
        mywin.flip()
    writeTimeEvent(f"video bitti: {video.name}")
    mywin.clearBuffer()

videos_load=loadVideos()

def showAllVideosInRandom(responseText,part):
    random.shuffle(videos_load)
    isi_list=isi()
    for video in videos_load:
        showVideo(video)
        # video.stop()
        # video.seek(0)
        video.reset()
        writeTimeEvent(f"Response başladı: {video.name}")
        getResponse(responseText,video.name,part)
        writeTimeEvent(f"response bitti: {video.name}")
        isi_selected=isi_list.pop()
        writeTimeEvent(f"ISI başladı {isi_selected}: {video.name}")
        showPlus(isi_selected)
        writeTimeEvent(f"ISI bitti: {video.name}")



parts={}

parts["target"]={"title":"Eylem insana mı objeye mi uygulanıyor?"+"\n\n"+"İnsansa sola objeyse sağa basın.", "soru":"İnsan?"+"\t"*7+"Obje?"}
parts["target"]["answer"]={"01.mp4":"1","02.mp4":"4","03.mp4":"1","04.mp4":"4","05.mp4":"1","06.mp4":"4","07.mp4":"1","08.mp4":"4"}

parts["actor"]={"title":"Eylemi yapan kişi kadın mı erkek mi?"+"\n\n"+ "Kadınsa sola erkekse sağa basın.", "soru":"Kadın?"+"\t"*7+"Erkek?"}
parts["actor"]["answer"]={"01.mp4":"1","02.mp4":"1","03.mp4":"1","04.mp4":"1","05.mp4":"4","06.mp4":"4","07.mp4":"4","08.mp4":"4"}

parts["effector"]={"title":"Oyuncu eylemi elle mi ayakla mı gerçekleştiriyor?"+"\n\n"+ "Else sola ayaksa sağa basın.", "soru":"El?"+"\t"*7+"Ayak?"}
parts["effector"]["answer"]={"01.mp4":"4","02.mp4":"4","03.mp4":"1","04.mp4":"1","05.mp4":"4","06.mp4":"4","07.mp4":"1","08.mp4":"1"}


def playASection():
    partsName=list(parts.keys())
    random.shuffle(partsName)
    for i in partsName:
        writeTimeEvent(f"part başladı:{i}")
        showText(parts[i]["title"],4)
        showAllVideosInRandom(parts[i]["soru"],i)
        writeTimeEvent(f"part bitti:{i}")


def playBlockDouble(n=2):
    for i in range(n):
        writeTimeEvent(f"Blok {i+1} başladı")
        playASection()
        if i==0:
            showPlus(12)
        writeTimeEvent(f"Blok {i+1} bitti")


def runExperiment(dataName):
    global data
    data=pd.DataFrame()
    writeTimeEvent("Deney başladı",start=True)
    writeTimeEvent("Initial rest başladı")
    showPlus(12)
    writeTimeEvent("Initial rest bitti")
    writeTimeEvent("Initial instruction başladı")
    showText("Birazdan itme eyleminin yapıldığı videolar göreceksin."+"\n\n"+ "8 video içeren bloklar olacak ve her bloktan önce bir soru ekranı gelecek."+"\n\n"+" Örneğin 'Eylemi yapan kişi kadın mı erkek mi?' gibi."+"\n\n"+"Soru ekranı geldiğinde lütfen soruyu cevaplayınız.",8) 
    writeTimeEvent("Initial instruction bitti")
    playBlockDouble(n=2)
    writeTimeEvent("Final rest başladı")
    showPlus(12)
    writeTimeEvent("Final rest bitti")
    writeTimeEvent("Deney bitti")
    destination_directory="/home/ccnlab/experiment/exp/output/sub-{}/main".format(initialData["Subject No:"])
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
    os.chdir(destination_directory)
    data.to_csv(f"{dataName}.csv")




#runExperiment("deneme")

getInitialData()

MR_settings = {
    'TR': 3,
    'volumes': 168, #??
    'sync': '6'
}

print("Waiting for trigger.")
vol = launchScan(mywin, MR_settings, globalClock=core.Clock(), mode='Scan', esc_key='escape', wait_msg='...', wait_timeout=300)
print("Trigger received.")

logName="Sub{}-Ses{}-Run{}".format(initialData["Subject No:"],initialData["Session No:"],initialData["Run No:"])
runExperiment(logName)


""""
To Do list

deneyi durdurmak için bir tuş
add waiting for trigger routine
launchScan()
If a globalClock is given (highly recommended), it is reset to 0.0 when the first sync pulse is detected.
does the scanner give trigger at the beginning of every TR?
psychopy.hardware.emulator.launchScan(win, settings, globalClock=None, simResponses=None, mode=None, esc_key='escape', instr='select Scan or Test, press enter', wait_msg='waiting for scanner...', wait_timeout=300, log=True)
use global clock instead of relative one
"""
