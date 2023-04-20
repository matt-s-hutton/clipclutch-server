class SupportedFormat(object):
    _supported_audio_format = {'mp3', 'm4a'}
    _supported_video_format = {'mp4', 'webm'}

    @classmethod
    def get_supported_audio_formats(cls) -> set:
        return cls._supported_audio_format

    @classmethod
    def get_supported_video_formats(cls) -> set:
        return cls._supported_video_format

    @classmethod
    def get_supported_formats(cls) -> set:
        return cls.get_supported_audio_formats().union(cls.get_supported_video_formats())