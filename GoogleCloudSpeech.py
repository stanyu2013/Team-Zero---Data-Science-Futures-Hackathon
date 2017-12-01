def transcribe_gcs(gcs_uri):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    import time
    start = time.time()
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=9000000)

    filename = gcs_uri.split('/')[3][0:-5]
    with open(filename+".txt","w") as gsp:
        for result in response.results:
            gsp.write(result.alternatives[0].transcript)
    end = time.time()
    print(end-start)

if __name__ == '__main__':

    gcs_uri="gs://remainingaudiofiles/TRADOC Mad Scientist 2015 Welcome Remarks w_ LTG Mangumm.wav"
    transcribe_gcs(gcs_uri)




    

    

