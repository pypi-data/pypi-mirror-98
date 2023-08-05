import subprocess
from .exceptions import ffmpegerror
from os import getcwd
class FFMPEG:
    ffmpeg = __file__.replace('_ffmpeg.py','') + 'ffmpeg'
    file_types = ("mp4","flv","mkv","mov","wmv","avi")
    def __init__(self,input_video,input_audio,output_file_name):
        self.input_video = input_video
        self.input_audio = input_audio
        self.output_file_name = output_file_name
        print(self.input_video)
        if self.output_file_name.strip()[-3:].lower() not in self.file_types:
            raise ffmpegerror
    def compile(self):
        video_param = " -i " + self.input_video
        audio_param = " -i  " + self.input_audio
        a_code_v_codec_param = " -c:v copy -c:a aac "
        cmd = self.ffmpeg + video_param + audio_param + a_code_v_codec_param + getcwd()+ "/" + self.output_file_name
        try:
             subprocess.Popen(cmd)
        except Exception as e:
            raise e
    def run(self):
        self.compile()