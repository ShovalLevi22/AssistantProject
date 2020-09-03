import requests
import speech_recognition as sr

class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.stop_sign = False
        self.serv_addr = 'http://192.168.1.46:8000'

    def recognize_speech_from_mic(self):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = self.recognizer.recognize_google(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    def exec_custom_py(self, command):
        requests.get(f'{self.serv_addr}/{command}')

    def start(self):
        while not self.stop_sign:
            pharse = self.recognize_speech_from_mic()
            if pharse["transcription"]:
                print(f'You said - {pharse["transcription"]}')
                self.exec_custom_py(pharse["transcription"])
            if not pharse["success"]:
                print('not success')

            # if there was an error, stop the game
            if pharse["error"]:
                if pharse["error"] != "Unable to recognize speech":
                    print("ERROR: {}".format(pharse["error"]))
                    return
                else:
                    print("Listening...")

    def stop(self):
        self.stop_sign = True

task = Listener()
task.start()

