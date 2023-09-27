import param
import panel as pn
import pandas as pd
import time
import requests
import pickle

from io import StringIO

import plotly.express as px

pn.extension('plotly', 'tabulator', sizing_mode="stretch_width")
from dashboard import AudioDashboard, file_path
from analysis import  ButtonAudio, Analysis

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


def main():
    audio_app = AudioDashboard()

    audio_app_view = audio_app.view()
    audio_app_view

    description = '''
    This is my app 😀
    '''
    component = pn.Column(
        description,
        audio_app_view,
        sizing_mode='stretch_both'
    )

    template = pn.template.FastListTemplate(
        title='Audio Content Summarizer',
        sidebar=[pn.pane.Markdown("### Input a link:"),
                audio_app.file_input,
                audio_app.download],
        
        main=[component],
        accent_base_color="#88d8b0",
        header_background="#88d8b0",
    )

    template.show()

if __name__ == "__main__":
    main()