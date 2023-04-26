import datetime
from fastapi import HTTPException
import youtube_dl
import uuid
from pathlib import Path
from os import fspath, utime
from ..model.download_parameters import DownloadParameters
from ..model.download_response import DownloadResponse
from ..model.supported_format import SupportedFormat
from ..configuration.settings import settings


def download_service(params: DownloadParameters) -> DownloadResponse:
    video_formats = SupportedFormat.get_supported_video_formats()
    audio_formats = SupportedFormat.get_supported_audio_formats()

    url = params.url
    options = params.options

    warning = None

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

    file_uuid = str(uuid.uuid4())
    location_local = Path(settings.download_location_local) / file_uuid
    location_remote = (Path(settings.download_location_remote) / file_uuid).with_suffix(f'.{target_format}')

    # If the target format is already available remotely, we can just download it
    if target_format in available_formats:
        format_string = set_format_string(target_format, video_formats)
        ydl_opts.update({ 'format': format_string })
        if target_format in audio_formats:
            outtmpl = fspath(location_local.with_suffix(f'.{target_format}'))
        else:
            outtmpl = fspath(location_local)
    # If not, for audio we download and re-encode, for video we return an error as it would take too long
    else:
        if target_format in audio_formats:
            ydl_opts.update({
                'keepvideo': False,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': target_format,
                }],
            })
            outtmpl = fspath(location_local) + '.' + '%(EXT)s'
        else:
            other_formats = list(video_formats.intersection(available_formats))
            if other_formats:
                warning = (f'Video provided as {other_formats[0]} due to {target_format} '
                           'being unavailable for download')
                target_format = other_formats[0]
                outtmpl = fspath(location_local)
            else:
                raise HTTPException(status_code=500, detail=(f'{target_format} unavailable and other formats {available_formats} '
                                                             'either not video or unsupported'))

    ydl_opts.update({
        'outtmpl': outtmpl,
        'writesubtitles': options.embedSubs,
        'noplaylist': True
    })
    if options.embedSubs:
        ydl_opts['postprocessors'].append({ 'key': 'FFmpegEmbedSubtitle' })

    # Download the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Explicitly set the mtime of download videos to now, don't rely on youtube-dl download to implement updatetime (--no-mtime)
    now = datetime.datetime.now().timestamp()
    file_path = fspath(location_local.with_suffix(f'.{target_format}'))
    utime(file_path, (now, now))

    return DownloadResponse(
        path=fspath(location_remote),
        format=target_format,
        media='audio' if target_format in audio_formats else 'video',
        thumbnail=thumbnail if options.getThumbnail else None,
        warning=warning
    )

def set_format_string(target_format: str, video_formats: set) -> str:
    compatible_audio_format = 'm4a' if target_format == 'mp4' else 'webm'
    video_format_string = f'bestvideo[ext={target_format}]+bestaudio[ext={compatible_audio_format}]'
    audio_format_string =f'bestaudio[ext={target_format}]'
    return video_format_string if target_format in video_formats else audio_format_string