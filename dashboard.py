import param
import panel as pn
from secret_ import API_TOKEN
import requests
import time
import pickle
from io import StringIO

from analysis import Analysis

file_path = 'speech_data.pkl'

class AudioDashboard(param.Parameterized):
    data = param.Dict()
  
    file_input = param.Parameter()
    
    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.TextInput(), **params)
        self.transcript = pn.pane.Str(max_width = 600, height_policy = "fit")
        self.download = pn.widgets.FileDownload(name="Download transcript", filename="transcript.txt", callback=self._download_callback, button_type="primary")

    @pn.depends("file_input.value", watch=True)
    def _parse_file_input(self):
        print("parse input ")
        print(self.file_input)
        value = self.file_input.value
        if value:
            print("in parse")
            self.data = self.get_and_analyze_transcript()
            print(self.data)
            
        else:
            print("error")

    @pn.depends('data', watch=True)
    def get_transcript(self):
        print("get transcript ")
        self.transcript.object = self.data["text"]
        
        
    def _download_callback(self):
        print("download")
        if self.data is not None:
            buffer = StringIO()
            buffer.write(self.data["text"])
            buffer.seek(0)
            print("return buffer")

            return buffer  
        else:
            return
        
    def get_and_analyze_transcript(self):
        audio_url = self.file_input.value
        
        if audio_url:
            # AssemblyAI transcript endpoint (where we submit the file)
            transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

            # request parameters 
            data = {
                "audio_url": audio_url, # You can also use a URL to an audio or video file on the web
                "auto_highlights": True,
                "sentiment_analysis": True,
                "auto_chapters": True,
                "iab_categories": True
            }

            # HTTP request headers
            headers={
              "Authorization": API_TOKEN,
              "Content-Type": "application/json"
            }

            # submit for transcription via HTTP request
            response = requests.post(transcript_endpoint,
                                     json=data,
                                     headers=headers)

            # polling for transcription completion
            polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{response.json()['id']}"

            while True:
                transcription_result = requests.get(polling_endpoint, headers=headers).json()

                if transcription_result['status'] == 'completed':
                    # print the results
                    # print(json.dumps(transcription_result, indent=2))
                    break
                elif transcription_result['status'] == 'error':
                    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")
                else:
                    time.sleep(3)
                    
            # save data into a file

            with open(file_path, 'wb') as file:
                pickle.dump(transcription_result.copy(), file)

                    
        else:
            print("no")
            return
                
        return transcription_result
        
        
    def view(self):
        return pn.Column(
            "## Transcript",
            self.transcript,
        )
    
