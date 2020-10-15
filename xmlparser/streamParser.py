import xmltodict
import pathlib


class AudioRecording():
    def __init__(self,filename,startTime):
        self.filename = filename.split('/')[1] + '.flv'
        self.delay = int(startTime)

class VideoRecording():
    def __init__(self,filename,startTime):
        self.filename = filename.split('/')[1] + '.flv'
        self.delay = int(startTime)

def parseindexstream(path):
    with open(str(pathlib.Path(path))) as fd:
        index = xmltodict.parse(fd.read())
    audio = []
    for item in index['root']['Message']:
        if item.get('String') and item.get('String') == 'streamAdded':
            if 'cameravoip' in str(item['Array']['Object']['streamName']).lower():
                audio.append(AudioRecording(item['Array']['Object']['streamName'],item['Array']['Object']['startTime']))
    video = []
    for item in index['root']['Message']:
        if item.get('String') and item.get('String') == 'streamAdded':
            if 'screenshare' in str(item['Array']['Object']['streamName']).lower():
                video.append(VideoRecording(item['Array']['Object']['streamName'],item['Array']['Object']['startTime']))
    print({'audio':sorted(audio,key=lambda audio:audio.delay),'video':sorted(video,key=lambda video:video.delay)})
    return {'audio':sorted(audio,key=lambda audio:audio.delay),'video':sorted(video,key=lambda video:video.delay)}