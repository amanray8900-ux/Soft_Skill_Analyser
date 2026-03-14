import whisper
import warnings
import os
import imageio_ffmpeg

warnings.filterwarnings("ignore")

# Point ffmpeg to the bundled binary from imageio-ffmpeg (no system install needed)
_ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = os.path.dirname(_ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

class AudioTranscriber:
    def __init__(self, model_name="tiny.en"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, file_path):
        result = self.model.transcribe(file_path, word_timestamps=True)
        return {
            "text": result["text"].strip(),
            "segments": result["segments"]
        }
