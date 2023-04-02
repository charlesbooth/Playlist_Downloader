from pytube import Playlist, YouTube, exceptions
import os
import unicodedata
import re
import tkinter as tk
from tkinter import filedialog

#region - slugify (convert video title to file format)
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
#endregion

#region - download_video/download_playlist
def download_video_helper(video, proposed, already_tried=False):
    video.streams.filter\
        (progressive=True, file_extension='mp4')\
            .order_by('resolution')[-1]\
            .download(filename=proposed)
    
def download_video(video, file_format):
    filename = slugify(video.title)
    proposed = '.'.join([filename, file_format])
    current = os.listdir(os.getcwd())
    copy_number = 0
    while proposed in current:
        copy_number += 1
        proposed = \
            '.'.join([f'{filename}({copy_number})', 
                        file_format])
    print(f'\tDownloading {proposed}...')
    download_video_helper(video, proposed)
        
def download_playlist(playlist, save_path, file_format):
    os.chdir(save_path)
    videos_downloaded = 0
    for link in playlist.video_urls:
        try:
            video = YouTube(link)
        except(exceptions.PytubeError):
            print('\n\n', f'Could not download video titled "{video.title}."')
            continue
        download_video(video, file_format)
        videos_downloaded += 1
        print(f'\t{videos_downloaded}/{len(playlist.video_urls)} videos downloaded', '\n')
    print(f'Done! {videos_downloaded} videos saved to {save_path} from playlist named "{playlist.title}."', 'Goodbye!', sep='\n')
#endregion

def check_with_user(your_text):
    check_input = ''
    while check_input not in ('y', 'n'):
        check_input = \
            input(f'{your_text} \n Enter Y for Yes, N for No \n').lower()
        if check_input not in ('y', 'n'):
            print('\n', 'Invalid Character', '\n')
    if check_input == 'y':
        return True
    elif check_input == 'n':
        return False
    
def setup_source(link, save_path, file_format):
    if 'playlist?list' in link:
        source = Playlist(link)
        prompt_text = f'Do you want to download {len(source.video_urls)} videos from playlist titled "{source.title}" as {file_format}?'
        if not check_with_user(prompt_text):
            print('Playlist will not be downloaded.', 'Goodbye!', sep='\n')
            return
        download_playlist(source, save_path, file_format)
    elif 'watch?v' in link:
        os.chdir('downloaded')
        source = YouTube(link)
        download_video(source, file_format)
        print(f'Done! {source.title} has been downloaded.')
    else:
        print('Link is not recognized as a video or playlist. Restart program with new link.')


def download_media(link, save_path, file_format, attempts=0):
    try:
        setup_source(link, save_path, file_format)
    except(exceptions.PytubeError):
        if attempts < 10:
            download_media(link, save_path, file_format, attempts+1)
        else:
            print('Could not reach link.')

def main():
    pass

if __name__ == '__main__':
    main()