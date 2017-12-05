def run_quickstart():
    # [START speech_quickstart]
    import io
    import os

    # Imports the Google Cloud client library
    # [START migration_import]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END migration_import]

    # Instantiates a client
    # [START migration_client]
    client = speech.SpeechClient()
    # [END migration_client]

    # The name of the audio file to transcribe
    # file_name = "./wav_output/Mad scientist conf intro Final.wav"
    file_name = "./wav_output/NETWORK.wav"

    print(file_name)
    print('file_name')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    #config = types.RecognitionConfig(
    #    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    #    sample_rate_hertz=44100,
    #    language_code='en-US')

    config = types.RecognitionConfig(
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]


if __name__ == '__main__':
    run_quickstart()

