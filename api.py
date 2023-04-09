import youtube_dl
import uuid
from fastapi import FastAPI
import uvicorn
from pathlib import Path
from os import fspath

from config import settings
from downloadparameters import DownloadParameters
from supportedformat import SupportedFormat

ccserv = FastAPI()

@ccserv.post(
    settings.api_path,
    description="This endpoint accepts JSON in the request body. "
        "Despite being a POST endpoint, it is used for data retrieval. "
        "This is because transmitting the JSON via GET is less maintainable. "
        "The JSON object must have the following structure: "
        "{"
        "  'url': <string>, "
        "  'options': {"
        "    'convertFormat': <string>, "
        "    'embedSubs': <bool>, "
        "    'getThumbnail': <bool>"
        "  }"
        "}"
)
async def download(params: DownloadParameters):
    video_formats = SupportedFormat.get_supported_video_formats()
    audio_formats = SupportedFormat.get_supported_audio_formats()

    url = params.url
    options = params.options

    # Get info
    with youtube_dl.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
    available_formats = set(
        [format.get('ext') for format in info.get('formats', [])]
    )

    thumbnail = info['thumbnails'][-1]['url']
    ydl_opts = {'postprocessors': []}

    # Check if target format is supported by the video
    target_format = options.convertFormat

    # If the target format is already available remotely, we can just download it
    if target_format in available_formats:
        format_string = set_format_string(target_format, video_formats)
        ydl_opts.update({ 'format': format_string })
    # If not, for audio we download and re-encode, for video we return an error as it would take too long
    # TODO: warn user that it will take a long time to re-encode the video and allow them to continue if they want
    else:
        if target_format in audio_formats:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': target_format,
                    'preferredquality': '192',
                }],
            })
        else:
            return {"error": "Target format not available and cannot be converted to"}

    file_uuid = str(uuid.uuid4())
    outtmpl = Path(f'{settings.download_path}{file_uuid}')
    path = outtmpl.with_suffix(f'.{target_format}')

    ydl_opts.update({
        'outtmpl': fspath(outtmpl),
        'writesubtitles': options.embedSubs,
        'noplaylist': True,
        'progress_hooks': [hook]
    })
    if options.embedSubs:
        ydl_opts['postprocessors'].append({ 'key': 'FFmpegEmbedSubtitle' })

    # Download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return_value = {
        'path': fspath(path),
        'format': target_format,
        'media': 'audio' if target_format == 'mp3' else 'video'
    }

    return {"message": return_value}

def hook(status: dict):
    if status['status'] == 'downloading':
        pass

def set_format_string(target_format: str, video_formats: set) -> str:
    compatible_audio_format = 'm4a' if target_format == 'mp4' else 'webm'
    video_format_string = f'bestvideo[ext={target_format}]+bestaudio[ext={compatible_audio_format}]'
    audio_format_string =f'bestaudio[ext={target_format}]'
    return video_format_string if target_format in video_formats else audio_format_string

if __name__ == "__main__":
    uvicorn.run("api:ccserv", host=settings.host, port=settings.port, workers=settings.workers, headers=[("server", "ccserv")])