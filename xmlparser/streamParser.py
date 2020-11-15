import xmltodict
import pathlib


class AudioRecording():
    def __init__(self,filename,startTime):
        self.filename = filename.split('/')[1] + '.flv'
        self.new_filename = None
        self.delay = int(startTime)

class VideoRecording():
    def __init__(self,filename,startTime):
        self.filename = filename.split('/')[1] + '.flv'
        self.new_filename = None
        self.delay = int(startTime)

def parseindexstream(path=None, bytesdata=None):
    if not bytesdata:
        with open(str(pathlib.Path(path))) as fd:
            index = xmltodict.parse(fd.read())
    else:
        index = xmltodict.parse(bytesdata)

    audio = []
    for item in index['root']['Message']:
        if item.get('String') and item.get('String') == 'streamAdded':
            if 'cameravoip' in str(item['Array']['Object']['streamName']).lower():
                audio.append(AudioRecording(item['Array']['Object']['streamName'],item['Array']['Object']['startTime']))
    sorted_audio = sorted(audio, key=lambda audio: audio.delay)
    for i, item in enumerate(sorted_audio):
        sorted_audio[i].new_filename = f"audio_{i}"

    video = []
    for item in index['root']['Message']:
        if item.get('String') and item.get('String') == 'streamAdded':
            if 'screenshare' in str(item['Array']['Object']['streamName']).lower():
                video.append(VideoRecording(item['Array']['Object']['streamName'],item['Array']['Object']['startTime']))
    sorted_video = sorted(video, key=lambda video: video.delay)
    for i, item in enumerate(sorted_video):
        sorted_video[i].new_filename = f"video_{i}"

    return {'audio':sorted_audio,'video':sorted_video}