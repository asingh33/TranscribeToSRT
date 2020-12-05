import proto
import json
import time
from google.cloud import speech
from google.protobuf.json_format import MessageToDict

DURATION = 4

def proto_message_to_dict(message: proto.Message) -> dict:
     return json.loads(message.__class__.to_json(message))

def getDuration(start, end):
    s = float(start.replace('s',''))
    e = float(end.replace('s',''))

    return (e - s)

def getSRT_Time(value):
    #print(value)
    
    secmsec = value.replace('s','')
    t = secmsec.split('.',1)
    seconds = int(t[0])
    hms = time.strftime('%H:%M:%S', time.gmtime(seconds))
    if len(t) > 1:
        return '{},{}'.format(hms,t[1])
    else:
        return '{},{}'.format(hms,'000')


def onewordSRT(filename, data):
    index = 1
    word_list = []
    with open(filename, 'a') as srtfile:
        for result in data['results']:
            for word in result['alternatives'][0]['words']:
                srtfile.write("\n{}\n{}  -->  {}\n".format(index, getSRT_Time(word['startTime']), getSRT_Time(word['endTime'])))
                srtfile.write("{}\n".format(word['word']))

                index = index + 1

def youtubeStyleSRT(filename, data):
    index = 1
    word_list = []
    with open(filename, 'a') as srtfile:
        for result in data['results']:
            for word in result['alternatives'][0]['words']:
                if len(word_list) > 10:
                    word_list = []

                word_list.append(u"{}".format(word['word']))
                sentence = " ".join(word_list)
                srtfile.write("\n{}\n{}  -->  {}\n".format(index, getSRT_Time(word['startTime']), getSRT_Time(word['endTime'])))
                srtfile.write("{}\n".format(sentence))

                index = index + 1


def transcribe_gcs(gcs_uri, lang, creds):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    #client = speech.SpeechClient()
    client = speech.SpeechClient.from_service_account_json(creds)

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        #encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code=lang,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=250)

    data = proto_message_to_dict(response)
    with open('response.json', 'w') as f:
         json.dump(data, f)



    with open('response.json', 'r') as f:
         data = json.load(f)
    

    onewordSRT('abhi_oneword.srt', data)
    youtubeStyleSRT('abhi_yt.srt', data)
    