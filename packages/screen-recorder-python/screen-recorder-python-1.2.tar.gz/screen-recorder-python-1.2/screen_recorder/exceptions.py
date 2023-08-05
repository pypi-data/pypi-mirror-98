class ffmpegerror(Exception):
    file_types = ("mp4","flv","mkv","mov","wmv","avi")
    def __init__(self):
        super().__init__(f"filetype not supported")

class stereomixerror(Exception):
    message = "Stereo Mix is not enabled"
    def __init__(self):
        super().__init__(self.message)

