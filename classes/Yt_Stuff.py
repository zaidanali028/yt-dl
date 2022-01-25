# WILL CONTINUE SOON ...
# KVNGRTHR!VE ROCKS
import re
import sys
import requests as requests
from pytube.exceptions import RegexMatchError
from tqdm import tqdm
from time import sleep
import simple_chalk as color
from classes.Messages import Messages
from pytube import YouTube, Playlist
from pytube.cli import on_progress
import math
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()


# https://www.youtube.com/watch?v=WPT15U2kI0g&list=PL9CBADA811A131FEB
# https://www.youtube.com/watch?v=Ja44RJZUFVU&list=PLRD0dHezDHDTkwlHn1lVxdPzrAUlk3X_9
# https://www.youtube.com/watch?v=IGQBtbKSVhY
# https://www.youtube.com/watch?v=A6RU-u8fHjE
# [{'file_size_0': '42.74 KB', 'file_resolution_0': '144p'}, {'file_size_1': '315.64 KB', 'file_resolution_1': '360p'}, {'file_size_2': '1.33 MB', 'file_resolution_2':
# '720p'}]


# This works good but not coherant with doc
def progress_function(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    current = ((filesize - bytes_remaining) / filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


def completed_function(stream, file_path):
    msg.success_msg("DOWNLOAD COMPLETED,THANK YOU FOR USING YT-DL")


msg = Messages()


class Yt_Stuff:

    def __init__(self):
        self.dispose_self()

    def is_float(self, element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    def dispose_self(self):
        self.selected_option = ""
        self.single_media_url = ""
        self.multiple_media_url = ""
        self.selected_resolution = ""
        self.available_resolutions = []
        self.new_stream = []

    def index_exists(self, ls, i):
        return (0 <= i < len(ls)) or (-len(ls) <= i < 0)

    def use_cli(self):
        # Download A Youtube Video(Video + Audio(Mixed)).=>Default option
        stick = color.chalk
        msg.info_msg("App Loading...")

        text = ""
        for char in tqdm(["a", "b", "c", "d", "a", "b", "c", "d"]):
            sleep(0.1)
            text = text + char
        query_msg = """
                Please specify what you will like to do
                1 => Download A Youtube Video(Video + Audio(Mixed)).
                2 => Download A Youtube Video->(Audio Only).
                3 => Download A Youtube PlayList(Video + Audio(Mixed)).
                4 => Download A Youtube PlayList->(Audio Only)."""

        while self.selected_option == "":
            msg.yt_menu(query_msg)
            try:
                self.selected_option = int(input(""))
            except ValueError:
                msg.error_msg("INVALID/EMPTY RESPONSE(PLEASE PROVIDE/SELECT AT LEAST ONE(1) OPTION)")
                continue
            finally:
                if self.selected_option == 1:
                    while self.single_media_url == "" or self.single_media_url.isnumeric() or self.is_float(
                            self.single_media_url):

                        msg.info_msg("Please Provide Video's URL")
                        try:
                            self.single_media_url = input("")
                            self.download_single_video(self.single_media_url)

                        except ValueError:
                            msg.error_msg("PLEASE PROVIDE A URL")
                            continue
                if self.selected_option == 2:
                    while self.single_media_url == "" or self.single_media_url.isnumeric() or self.is_float(
                            self.single_media_url):
                        msg.info_msg("Please Provide The  URL")
                        try:
                            self.single_media_url = input("")
                            self.download_single_audio(self.single_media_url)

                        except ValueError:
                            msg.error_msg("PLEASE PROVIDE A URL")
                            continue
                if self.selected_option == 3:
                    while self.multiple_media_url == "" or self.multiple_media_url.isnumeric() == int or self.is_float(
                            self.multiple_media_url):
                        msg.info_msg("Please Provide The  PLAYLIST URL")
                        try:
                            self.multiple_media_url = input("")

                            self.download_playlist_video(self.multiple_media_url)

                        except ValueError:
                            msg.error_msg("An issue with your input")
                            continue

                if self.selected_option == 4:
                    while self.multiple_media_url == "" or self.multiple_media_url.isnumeric() == int or self.is_float(
                            self.multiple_media_url):
                        msg.info_msg("Please Provide The  PLAYLIST URL")
                        try:
                            self.multiple_media_url = input("")

                            self.download_playlist_audio(self.multiple_media_url)

                        except ValueError:
                            msg.error_msg("An issue with your input")
                            continue

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def check_url_isValid(self, yt_url):
        req = requests.get(yt_url)
        return "Video unavailable" in req.text

    def check_playlist_url_isValid(self, yt_url):

        p = "/ ^ (?:https?:\ / \ /)?(?:m\.| www\.)?(?:youtu\.be\ / | youtube\.com\ / (?:embed\ / | v\ / | watch\?v= | watch\?.+ & v=))((\w | -){11})(?:\S +)?$ /";
        p = re.compile(p)
        if (yt_url.match(p)):
            return yt_url.match(p)[1];
        else:
            return False
        # https://www.youtube.com/playlist?list=PLlrxD0HtieHhS8VzuMCfQD4uJ9yne1mE6

    def download_single_video(self, yt_url: str):
        download_res = dict()

        query_msg_list = []
        final_query_str = "Select Your Preferred Download Resolution(HIGHER RESOLUTION -> BETTER QUALITY)\n"
        try:
            msg.info_msg("Checking Url validity for " + yt_url) if yt_url != "" else print("")
            is_YtUrl = self.check_url_isValid(yt_url)
            msg.success_msg("[200]ok! Valid Youtube Video") if not is_YtUrl else msg.error_msg(
                "[404]gross!The Url You Provided Is Invalid :(")
            if is_YtUrl:
                return
            else:
                yt = YouTube(yt_url, on_progress_callback=progress_function, on_complete_callback=completed_function)
                video_title = yt.title
                msg.info_msg(f"processing video with title {video_title}")
                video_audio_streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
                # msg.info_msg(f"streams {video_audio_streams}")
                # am filtering from highest to lowest resolution
                for stream in video_audio_streams:
                    # self.convert_size() converts the bytes to mb,gb,kb etc
                    # print(stream.resolution)
                    download_res['file_size'] = self.convert_size(stream.filesize)
                    download_res['file_resolution'] = stream.resolution
                    download_res['file_stream'] = stream
                    self.available_resolutions.append(download_res)
                    # msg.info_msg(f"This stream, {download_res}")
                    download_res = dict()

                single_query_msg = ""
                for index, download_dict in enumerate(self.available_resolutions):
                    single_query_msg = f"{index + 1} => File Size {download_dict['file_size']} ,File Resolution {download_dict['file_resolution']} "
                    # index + 1(to prevent users form seeing options from 0 but 1)
                    query_msg_list.append(single_query_msg)
                for query_str in query_msg_list:
                    final_query_str += f'{query_str} \n'
                while self.selected_resolution == "":
                    msg.yt_menu(final_query_str)
                    try:
                        self.selected_resolution = int(input("")) - 1
                        default_path = f"{os.environ['UserProfile']}/Desktop"
                        msg.info_msg('Opening file explorer')
                        user_path = filedialog.askdirectory()
                        if user_path != "":
                            user_path = user_path.replace(os.sep, '/')
                            # inclase a user gives a path with a backslash

                        else:
                            user_path = ""
                        path = user_path if user_path != "" else default_path
                        msg.info_msg('downloading to {path},please wait'.format(path=path))
                        selected_stream = self.available_resolutions[self.selected_resolution]['file_stream']
                        file_resolution = self.available_resolutions[self.selected_resolution]['file_resolution']

                        selected_stream.download(output_path=path,
                                                 filename=f"yt-dl-{video_title}-[{file_resolution}].mp4")
                        self.dispose_self()

                        # int(input(""))-1 to remove user input's increased number to get the corrected index

                    except ValueError:
                        msg.error_msg("PLEASE SELECT A SPECIFIC RESOLUTION")
                        continue

        except RegexMatchError:
            msg.error_msg("A YOUTUBE URL WAS NOT PROVIDED")

    def download_single_audio(self, yt_url: str):
        download_res = dict()
        path_to_save = ""
        query_msg_list = []
        final_query_str = "Select Your Preferred Download Resolution(HIGHER RESOLUTION -> BETTER QUALITY)\n"
        try:
            msg.info_msg("Checking Url validity for " + yt_url) if yt_url != "" else print("")
            is_YtUrl = self.check_url_isValid(yt_url)
            msg.success_msg("[200]ok! Valid Youtube Video") if not is_YtUrl else msg.error_msg(
                "[404]gross!The Url You Provided Is Invalid :(")
            if is_YtUrl:
                return
            else:
                yt = YouTube(yt_url, on_progress_callback=progress_function, on_complete_callback=completed_function)
                video_title = yt.title
                msg.info_msg(f"processing video with title {video_title}")
                video_audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()

                # msg.info_msg(f"streams {video_audio_streams}")
                # am filtering from highest to lowest resolution
                for stream in video_audio_streams:
                    # self.convert_size() converts the bytes to mb,gb,kb etc
                    download_res['file_size'] = self.convert_size(stream.filesize)
                    download_res['file_resolution'] = stream.abr
                    download_res['file_stream'] = stream
                    self.available_resolutions.append(download_res)
                    # msg.info_msg(f"This stream, {download_res}")
                    download_res = dict()

                single_query_msg = ""
                for index, download_dict in enumerate(self.available_resolutions):
                    single_query_msg = f"{index + 1} => File Size {download_dict['file_size']} ,File Resolution {download_dict['file_resolution']} "
                    # index + 1(to prevent users form seeing options from 0 but 1)
                    query_msg_list.append(single_query_msg)
                for query_str in query_msg_list:
                    final_query_str += f'{query_str} \n'
                while self.selected_resolution == "":
                    msg.yt_menu(final_query_str)
                    try:
                        self.selected_resolution = int(input("")) - 1
                        default_path = f"{os.environ['UserProfile']}/Desktop"
                        msg.info_msg('Opening file explorer')
                        user_path = filedialog.askdirectory()
                        if user_path != "":
                            user_path = user_path.replace(os.sep, '/')
                            # inclase a user gives a path with a backslash

                        else:
                            user_path = ""
                        path = user_path if user_path != "" else default_path
                        msg.info_msg('downloading to {path},please wait'.format(path=path))
                        selected_stream = self.available_resolutions[self.selected_resolution]['file_stream']
                        file_resolution = self.available_resolutions[self.selected_resolution]['file_resolution']

                        selected_stream.download(output_path=path,
                                                 filename=f"yt-dl-{video_title}-[{file_resolution}].mp3")
                        self.dispose_self()

                        # int(input(""))-1 to remove user input's increased number to get the corrected index

                    except ValueError:
                        msg.error_msg("PLEASE SELECT A SPECIFIC RESOLUTION")
                        continue

        except RegexMatchError:
            msg.error_msg("A YOUTUBE URL WAS NOT PROVIDED")

    def download_playlist_audio(self, yt_playlist_url):
        download_info = dict()
        playlist_stream = []
        resolutions = []
        query_msg = "Select Your Preferred Download Resolution(HIGHER RESOLUTION -> BETTER QUALITY)\n"
        playlist_videos = Playlist(yt_playlist_url)
        playlist_title = playlist_videos.title
        msg.info_msg(f"Processing {playlist_title}")
        # # get any first video just to get resolutions
        v = playlist_videos.videos[0]
        streams = v.streams.filter(only_audio=True).order_by('abr')
        for s in streams:
            resolutions.append(s.abr)
        for i, resolution in enumerate(resolutions):
            query_msg += f'            {i + 1}. ====> {resolution} \n'
        #
        selected_resoultion = -50
        # CHECkING IF SELECTED RESOLUTION EXISTS AMONG AVAILABLE RESOLUTIONS
        while not self.index_exists(resolutions, selected_resoultion):
            msg.info_msg(query_msg)
            selected_resoultion = int(input("")) - 1
        try:
            for i, resolution in enumerate(resolutions):
                query_msg += f'            {i + 1}. ====> {resolution} \n'

            while not self.index_exists(resolutions, selected_resoultion):
                msg.info_msg(query_msg)
                selected_resoultion = int(input("")) - 1

            msg.info_msg(f"You selected [{resolutions[selected_resoultion]}],Processing")

            for video in playlist_videos.videos:
                video.register_on_progress_callback(progress_function)

                video_title = video.title
                selected_stream = streams[selected_resoultion]
                download_info['video_title_'] = video_title
                download_info['selected_stream_'] = selected_stream
                streams = video.streams
                streams_file_size = self.convert_size(streams[selected_resoultion].filesize)
                download_info['streams_file_size_'] = streams_file_size
                playlist_stream.append(download_info)
                download_info = dict()

            videos_msg = "Video(s) About To Get Downloaded: \n"

            for i, stream in enumerate(playlist_stream):
                streams_filesize = stream['streams_file_size_']
                streams_title = stream['video_title_']

                single_msg = f'            {i + 1}. ====> {streams_title}\'s size {streams_filesize}\n  '

                videos_msg += single_msg
            msg.info_msg(videos_msg)
            msg.info_msg("""Specify the videos(BY NUMBERS) you have/have downloaded already(PLEASE DIFFERENTIATE BY 
                                    COMMAS(,) Skip if you have downloaded none by proceeding ) 
                                    """)

            already_downloaded_streams = input("").split(',')
            if not already_downloaded_streams == "":
                try:
                    for num in already_downloaded_streams:
                        index = int(num) - 1

                        while not self.index_exists(playlist_stream, index):
                            msg.info_msg(
                                f"{already_downloaded_streams}, => Number[{index + 1}] <= is not a video index,please "
                                f"provide valid video index(es) ") if not already_downloaded_streams == "" else \
                                msg.info_msg("""Specify the videos(BY NUMBERS) you have/have downloaded already(PLEASE 
                                       DIFFERENTIATE BY 
                                       COMMAS(,) Skip if you have downloaded none by proceeding ) 
                                       """)
                            already_downloaded_streams = input("").split(',')
                            if len(already_downloaded_streams) > 0:
                                break
                    already_downloaded_streams_ = [playlist_stream[int(index) - 1] for index in
                                                   already_downloaded_streams]
                    self.new_stream = [stream for stream in playlist_stream if
                                       stream not in already_downloaded_streams_]

                    videos_msg = "Video(s) About To Get Downloaded(REFORMATTED)[PLEASE NOTE THAT YOU MAY NOT SEE THE COMPLETE LIST BUT BE REST ASSURED THE SYSTEM WILL REMEMBER YOUR CHOICE]: \n"

                    for i, stream in enumerate(self.new_stream):
                        streams_filesize = stream['streams_file_size_']
                        streams_title = stream['video_title_']

                        single_msg = f'            {i + 1}. ====> {streams_title}\'s size {streams_filesize}\n  '
                        videos_msg += single_msg
                    msg.info_msg(videos_msg)
                    self.playlist_downloader_video(playlist_stream,True)
                except ValueError:
                    # meanin user pressed enter
                    self.playlist_downloader_video(playlist_stream,True)
        except KeyError:
            msg.error_msg("A YOUTUBE PLAYLIST URL WAS NOT PROVIDED")

    def download_playlist_video(self, yt_playlist_url):
        download_info = dict()
        playlist_stream = []
        resolutions = []
        query_msg = "Select Your Preferred Download Resolution(HIGHER RESOLUTION -> BETTER QUALITY)\n"
        playlist_videos = Playlist(yt_playlist_url)
        playlist_title = playlist_videos.title
        msg.info_msg(f"Processing {playlist_title}")
        # get any first video just to get resolutions
        v = playlist_videos.videos[0]
        streams = v.streams.filter(progressive=True).order_by('resolution')
        for s in streams:
            resolutions.append(s.resolution)
        for i, resolution in enumerate(resolutions):
            query_msg += f'            {i + 1}. ====> {resolution} \n'

        selected_resoultion = -50
        # CHECkING IF SELECTED RESOLUTION EXISTS AMONG AVAILABLE RESOLUTIONS
        while not self.index_exists(resolutions, selected_resoultion):
            msg.info_msg(query_msg)
            selected_resoultion = int(input("")) - 1
        try:
            for i, resolution in enumerate(resolutions):
                query_msg += f'            {i + 1}. ====> {resolution} \n'

            while not self.index_exists(resolutions, selected_resoultion):
                msg.info_msg(query_msg)
                selected_resoultion = int(input("")) - 1

            msg.info_msg(f"You selected [{resolutions[selected_resoultion]}],Processing")

            for video in playlist_videos.videos:
                video.register_on_progress_callback(progress_function)

                video_title = video.title
                selected_stream = streams[selected_resoultion]
                download_info['video_title_'] = video_title
                download_info['selected_stream_'] = selected_stream
                streams = video.streams
                streams_file_size = self.convert_size(streams[selected_resoultion].filesize)
                download_info['streams_file_size_'] = streams_file_size
                playlist_stream.append(download_info)
                download_info = dict()

            videos_msg = "Video(s) About To Get Downloaded: \n"

            for i, stream in enumerate(playlist_stream):
                streams_filesize = stream['streams_file_size_']
                streams_title = stream['video_title_']

                single_msg = f'            {i + 1}. ====> {streams_title}\'s size {streams_filesize}\n  '

                videos_msg += single_msg
            msg.info_msg(videos_msg)
            msg.info_msg("""Specify the videos(BY NUMBERS) you have/have downloaded already(PLEASE DIFFERENTIATE BY 
                            COMMAS(,) Skip if you have downloaded none by proceeding ) 
                            """)

            already_downloaded_streams = input("").split(',')
            if not already_downloaded_streams == "":
                try:
                    for num in already_downloaded_streams:
                        index = int(num) - 1

                        while not self.index_exists(playlist_stream, index):
                            msg.info_msg(
                                f"{already_downloaded_streams}, => Number[{index + 1}] <= is not a video index,please "
                                f"provide valid video index(es) ") if not already_downloaded_streams == "" else \
                                msg.info_msg("""Specify the videos(BY NUMBERS) you have/have downloaded already(PLEASE 
                               DIFFERENTIATE BY 
                               COMMAS(,) Skip if you have downloaded none by proceeding ) 
                               """)
                            already_downloaded_streams = input("").split(',')
                            if len(already_downloaded_streams) > 0:
                                break
                    already_downloaded_streams_ = [playlist_stream[int(index) - 1] for index in
                                                   already_downloaded_streams]
                    self.new_stream = [stream for stream in playlist_stream if
                                       stream not in already_downloaded_streams_]

                    videos_msg = "Video(s) About To Get Downloaded(REFORMATTED)[PLEASE NOTE THAT YOU MAY NOT SEE THE COMPLETE LIST BUT BE REST ASSURED THE SYSTEM WILL REMEMBER YOUR CHOICE]: \n"

                    for i, stream in enumerate(self.new_stream):
                        streams_filesize = stream['streams_file_size_']
                        streams_title = stream['video_title_']

                        single_msg = f'            {i + 1}. ====> {streams_title}\'s size {streams_filesize}\n  '
                        videos_msg += single_msg
                    msg.info_msg(videos_msg)
                    self.playlist_downloader_video(playlist_stream,False)
                except ValueError:
                    # meanin user pressed enter
                    self.playlist_downloader_video(playlist_stream,False)
        except KeyError:
            msg.error_msg("A YOUTUBE PLAYLIST URL WAS NOT PROVIDED")

    def playlist_downloader_video(self, playlist_stream, is_audio: bool):
        stream_to_download = playlist_stream if len(self.new_stream) == 0 else self.new_stream
        msg.info_msg("About to begin download(s)")
        sleep(3)
        msg.info_msg('Opening file explorer')
        sleep(1)
        user_path = filedialog.askdirectory()
        for stream in stream_to_download:
            video_title = stream['video_title_']
            video_file_size = stream['streams_file_size_']
            msg.info_msg(f'DOWNLOADING {video_title} => [{video_file_size}] ,please wait... ')
            default_path = f"{os.environ['UserProfile']}/Desktop"

            if user_path != "":
                user_path = user_path.replace(os.sep, '/')
                # incase a user gives a path with a backslash

            else:
                user_path = ""
            path = user_path if user_path != "" else default_path

            stream['selected_stream_'].download(output_path=path,
                                                filename=f"yt-dl-{video_title}.mp4") if not is_audio else stream[
                'selected_stream_'].download(output_path=path,)
        else:
            msg.success_msg('PLAYLIST DOWNLOAD COMPLETE,THANKS FOR USING THIS SERVICE')
            self.dispose_self()
