# WILL CONTINUE SOON ...
#KVNGRTHR!VE ROCKS


import sys
import requests as requests
from pytube.exceptions import RegexMatchError
from tqdm import tqdm
from time import sleep
import simple_chalk as color
from classes.Messages import Messages
from pytube import YouTube
from pytube.cli import on_progress

import math
import tkinter as tk
from tkinter import filedialog
import os
root = tk.Tk()
root.withdraw()



# https://www.youtube.com/watch?v=IGQBtbKSVhY
# https://www.youtube.com/watch?v=A6RU-u8fHjE
# [{'file_size_0': '42.74 KB', 'file_resolution_0': '144p'}, {'file_size_1': '315.64 KB', 'file_resolution_1': '360p'}, {'file_size_2': '1.33 MB', 'file_resolution_2':
# '720p'}]



# This works good but not coherant with doc
def progress_function(stream, chunk, bytes_remaining):
    filesize=stream.filesize
    current = ((filesize - bytes_remaining) / filesize)
    percent = ('{0:.1f}').format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()
def completed_function(stream, file_path):
    msg.success_msg("DOWNLOAD COMPLETED,THANK YOU FOR USING YT-DL")


msg=Messages()

class Yt_Stuff:
    def __init__(self):
        self.selected_option = ""
        self.single_media_url= ""
        self.selected_resolution=""
        self.available_resolutions=[]



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
                    while self.single_media_url == "" or type(self.single_media_url)==int or type(self.single_media_url)==float:
                        msg.info_msg("Please Provide Video's URL")
                        try:
                            self.single_media_url = input("")
                            self.download_single_video(self.single_media_url)

                        except ValueError:
                            msg.error_msg("PLEASE PROVIDE A URL")
                            continue
                if self.selected_option == 2:
                    while self.single_media_url == "" or type(self.single_media_url)==int or type(self.single_media_url)==float:
                        msg.info_msg("Please Provide The  URL")
                        try:
                            self.single_media_url = input("")
                            self.download_single_audio(self.single_media_url)

                        except ValueError:
                            msg.error_msg("PLEASE PROVIDE A URL")
                            continue

            # print(self.selected_option)

    def convert_size(self,size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])

    def check_url_isValid(self,yt_url):
        req=requests.get(yt_url)
        return "Video unavailable" in req.text


    def download_single_video(self, yt_url:str):
        download_res = dict()
        path_to_save=""
        query_msg_list=[]
        final_query_str="Select Your Preferred Download Resolution(HIGHER FILESIZE -> BETTER QUALITY)\n"
        try:
            msg.info_msg("Checking Url validity for " + yt_url) if yt_url!="" else print("")
            is_YtUrl=self.check_url_isValid(yt_url)
            msg.success_msg("[200]ok! Valid Youtube Video") if not is_YtUrl else msg.error_msg("[404]gross!The Url You Provided Is Invalid :(")
            if is_YtUrl:
                return
            else:
                yt = YouTube(yt_url, on_progress_callback=on_progress, on_complete_callback=completed_function)
                video_title = yt.title
                msg.info_msg(f"processing video with title {video_title}")
                video_audio_streams = yt.streams.filter(progressive=True).order_by('resolution').desc()
                # msg.info_msg(f"streams {video_audio_streams}")
                # am filtering from highest to lowest resolution
                for stream in video_audio_streams:
                    # self.convert_size() converts the bytes to mb,gb,kb etc
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
                                                 filename=f"yt_dl_{video_title}_[{file_resolution}].mp4")
                        self.available_resolutions=[]
                        # int(input(""))-1 to remove user input's increased number to get the corrected index

                    except ValueError:
                        msg.error_msg("PLEASE SELECT A SPECIFIC RESOLUTION")
                        continue

        except RegexMatchError:
            msg.error_msg("A YOUTUBE URL WAS NOT PROVIDED")

    def download_single_audio(self, yt_url:str):
        download_res = dict()
        path_to_save=""
        query_msg_list=[]
        final_query_str="Select Your Preferred Download Resolution(HIGHER FILESIZE -> BETTER QUALITY)\n"
        try:
            msg.info_msg("Checking Url validity for " + yt_url) if yt_url!="" else print("")
            is_YtUrl=self.check_url_isValid(yt_url)
            msg.success_msg("[200]ok! Valid Youtube Video") if not is_YtUrl else msg.error_msg("[404]gross!The Url You Provided Is Invalid :(")
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
                                                 filename=f"YT_DL_{video_title}_[{file_resolution}].mp3")
                        self.available_resolutions=[]

                        # int(input(""))-1 to remove user input's increased number to get the corrected index

                    except ValueError:
                        msg.error_msg("PLEASE SELECT A SPECIFIC RESOLUTION")
                        continue

        except RegexMatchError:
            msg.error_msg("A YOUTUBE URL WAS NOT PROVIDED")




