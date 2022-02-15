'''
This code was written by Yufei Gu
Browred from COMP0016_IXN_2022_Team_9
UCL Computer Science Department
'''

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)

import time
import file

from azure.cognitiveservices.speech import audio

# Set up the subscription info for the Speech Service:
# F0-Speech-Resource
speech_key, service_region = "da33ad50c223413fbd1777c04d2035a9", "uksouth"
# S0-Speech-Resource
#speech_key, service_region = "57c175e5c83048659fa4dcbe47fb450a", "uksouth"


# Set up the speech configuration according to subscription key and resource region
def set_speech_config():
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    return speech_config

# Set up the audio file configuration according to the file name (path)
def set_audio_file_config(*, file_name):
    audio_config = speechsdk.audio.AudioConfig(filename=file_name)
    return audio_config

# Creates a speech recognizer using microphone as audio input.
# The default language is "en-us".
def creare_speech_recognizer(*, speech_config):
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    return speech_recognizer

# Creates a speech recognizer using an audio file as audio input
# The default language is "en-us".
def creare_audio_recognizer(*, speech_config, audio_config):
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    return speech_recognizer

# SpeechRecognizeOnceFromMic
# Performs one-shot speech recognition from the default microphone
def speech_recognize_once_from_mic():
    speech_config = set_speech_config()

    speech_recognizer = creare_speech_recognizer(speech_config=speech_config)

    # Remind the user to say something
    print("Say something...")

    # Starts speech recognition, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed.  The task returns the recognition text as result. 
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query. 
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # print("Recognized: {}".format(result.text))
        pass
    elif result.reason == speechsdk.ResultReason.NoMatch:
        # print("No speech could be recognized")
        pass
    elif result.reason == speechsdk.ResultReason.Canceled:
        # cancellation_details = result.cancellation_details
        # print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        # if cancellation_details.reason == speechsdk.CancellationReason.Error:
        #     print("Error details: {}".format(cancellation_details.error_details))
        pass
    # </SpeechRecognitionWithMicrophone>


# SpeechContinuousRecognitionWithFile
# Performs continuous speech recognition with the given awv file
# Write the result to the given output txt file
def speech_recognize_continuous_from_file(*, input_file_name, output_file_name):
    speech_config = set_speech_config()
    audio_config = set_audio_file_config(file_name=input_file_name)

    speech_recognizer = creare_audio_recognizer(speech_config=speech_config, audio_config=audio_config)

    done = False

    def stop_cb(evt):
        """callback that signals to stop continuous recognition upon receiving an event `evt`"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    # Intermediate recognition attempt
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))

    # If a recognition attempt is successful
    # Print event log to terminal
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt.result.text)))
    #Write result text to output file
    speech_recognizer.recognized.connect(lambda evt: file.write_txt_file(output_file_name=output_file_name, 
                                                            text = '{}\n'.format(evt.result.text), append=True))

    # If a recognition session has started
    speech_recognizer.session_started.connect('''lambda evt: print('SESSION STARTED: {}'.format(evt))''')
    # If a recognition session ha
    # s stopped
    speech_recognizer.session_stopped.connect('''lambda evt: print('SESSION STOPPED {}'.format(evt))''')

    # If a recognition attempt was canceled as a result or a direct cancellation request 
    # or, alternatively, a transport or protocol failure
    speech_recognizer.canceled.connect('''lambda evt: print('CANCELED {}'.format(evt))''')

    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # Stop continous speech recognition
    speech_recognizer.stop_continuous_recognition()
    # </SpeechContinuousRecognitionWithFile>





def speech_to_text(*, inputfile, outputfile):
    if not file.exists_file(inputfile):
        raise IOError('speech_to_text: audio file not exists: {}'.format(inputfile))

    if not file.check_file_type(inputfile, 'wav'):
        raise IOError('speech_to_text: audio file type error: {} should be of type wav'.format(inputfile))
    
    if not file.exists_file(outputfile):
        raise IOError('speech_to_text: output file not exists: {}'.format(outputfile))

    if file.check_file_type(outputfile, 'txt'):
        file.write_txt_file(output_file_name=outputfile, text='', append=False)
    else:
        raise IOError('speech_to_text: output file type error: {} should be of type txt'.format(outputfile))

    speech_recognize_continuous_from_file(input_file_name=inputfile, output_file_name=outputfile)

