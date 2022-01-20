from time import gmtime, strftime
import simple_chalk as color

import sys
# from classes.Alert import Alert_sounds
# sys.path.insert(1, '/classes/Alert.py')




def get_time():
    stick = color.chalk
    current_time = strftime("%H:%M:%S", gmtime())
    open_msg = stick.magentaBright(f"[{current_time}]")
    return open_msg
class Messages:
    @staticmethod
    def yt_menu(msg):
        stick = color.chalk

        open_msg = get_time() + stick.yellowBright.dim(f" {msg}")
        print(open_msg)

    @staticmethod
    def info_msg(msg):
        stick = color.chalk

        open_msg = get_time()+stick.green.cyan(f" {msg}...")
        print(open_msg)

    @staticmethod
    def success_msg(msg):
        stick = color.chalk

        open_msg =get_time()+ stick.green(f" {msg}.....")
        print(open_msg)

    @staticmethod
    def error_msg(msg):
        stick = color.chalk

        open_msg = get_time() + stick.redBright.bold(f" {msg}.....")
        print(open_msg)
    @staticmethod
    def try_app_open_msg():
        stick=color.chalk

        open_msg=get_time()+stick.green.cyan(f" Trying to open Facebook...")
        print(open_msg)

    @staticmethod
    def unable_to_locate_UiObject(object_name):
        stick = color.chalk

        open_msg =get_time()+ stick.green.black(f" Unable to locate {object_name} Icon/Field")
        print(open_msg)
        # Alert_sounds.beep()

    @staticmethod
    def not_loggedIn():
        stick = color.chalk

        open_msg = get_time()+stick.green.redBright(f" PLEASE LOGIN TO CONTINUE")
        print(open_msg)

    @staticmethod
    def app_opened_msg():
        stick = color.chalk

        open_msg = get_time()+stick.green.bold(f" Facebook is opened")
        print(open_msg)



    @staticmethod
    def sleep_msg(secs):
        stick=color.chalk
        sleep_msg=get_time()+stick.yellow(f" Sleeping  for {secs} second(s) before proceeding.... ")
        print(sleep_msg)
    @staticmethod
    def already_logged_in():
        stick = color.chalk
        sleep_msg =get_time()+ stick.green(f" Already logged in...Proceeding ")
        print(sleep_msg)

    @staticmethod
    def welcome_msg():
        stick=color.chalk
        d3v=stick.magenta("****KvngThr!v3****")
        time_and_date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        current_date_time=stick.black.bold.underline(time_and_date)
        right_half=stick.blue('<=====]')
        left_half=stick.blue('[=====>')


        print(stick.blue(f"""Welcome To YT DL v1.0 {left_half}{current_date_time}{right_half} 
Script Written By {d3v}
"""))



