import panel as pn
import pickle


class ButtonAudio:
    def __init__(self, start_time, audio_url):
        self.start_time = start_time
        self.audio_url = audio_url
        self.chapter = chapter

        self.button = pn.widgets.Button(
            name=str(int(start_time / 1000)), button_type="primary"
        )
        self.chapter_audio = pn.pane.Audio(
            audio_url, name="Audio", time=round(start_time / 1000)
        )
        self.button.on_click(self.move_audio_head)

    def move_audio_head(self, event):
        self.chapter_audio.time = self.start_time / 1000


class Analysis:
    def __init__(self, data, audio_url):
        self.data = data
        self.audio_url = audio_url

    @staticmethod
    def load_file():
        try:
            with open(file_path, "rb") as file:
                data = pickle.load(file)
                return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            # Handle other exceptions (e.g., unpickling errors) here
            print(f"An error occurred: {e}")

    def audio_chapter_summary():
        chapters = self.data["chapters"]
        # create chapter summary layout
        chapters_layout = pn.Column(pn.pane.Markdown("### Auto Chapter Summary"))
        
        for chapter in chapters:
            chapter_summary = pn.widgets.StaticText(value=chapter["summary"], width=1000, height_policy='fit')
            button_audio = ButtonAudio(chapter["start"],self.audio_url)
            button = button_audio.button
            chapter_audio = button_audio.chapter_audio
            chapters_layout.append(pn.Row(pn.Column(button), pn.Column(chapter_audio), pn.Column(chapter_summary)))

        return chapters_layout


