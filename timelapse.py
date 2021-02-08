import time
import datetime
import os
import subprocess
import tkinter
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

capture_count = 0
paused = False
start_time = time.time()
scheduler = BackgroundScheduler()

def start_camera():
    os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")

def switch_ultrawide():
    os.system("adb shell input tap 420 1600")

def take_a_picture():
    os.system("adb shell input keyevent 27")

def switch_108M():
    os.system("adb shell input tap 760 1800")

def return_home():
    os.system("adb shell input keyevent 3")
    os.system("adb shell input tap 320 2280")
    os.system("adb shell input tap 530 2000")

def power_button():
    os.system("adb shell input keyevent 26")

def power_control():
    subprocess.Popen(["adb", "shell", "input", "keyevent", "26"])

def get_pic_name():
    myfilename = os.popen("adb shell ls -t /sdcard/DCIM/Camera/ | head -n 1 | tr -d '\n'").read()
    print(myfilename)
    return myfilename

def save_file(type, filename):
    if filename[-1] == 'g' and filename[-2] == 'p' and filename[-3] == 'j':
        os.system("adb pull /sdcard/DCIM/Camera/" + filename + " ./" + type + "/" + filename)
    else:
        print("error, not jpg")

def capture():
    global capture_count
    print("capture action at %s"% format(time.ctime()))
    power_button()
    start_camera()
    time.sleep(5)
    switch_ultrawide()
    time.sleep(5)
    take_a_picture()
    time.sleep(5)
    ultrawide = get_pic_name()
    capture_count += 1
    switch_108M()
    time.sleep(5)
    take_a_picture()
    time.sleep(5)
    wide108 = get_pic_name()
    capture_count += 1
    return_home()
    power_button()
    save_file("ULTRAWIDE", ultrawide)
    save_file("108MP", wide108)
    print("action complete")

def update_status():
    current_time = time.time()
    formated_time = time.asctime(time.localtime(current_time))
    delta = int(current_time - start_time)
    t_sec = delta % 60
    t_min = (delta // 60) % 60
    t_hour = (delta // 3600) % 24
    t_day = (delta // (3600 * 24))
    clock_display.set("Current time is %s" % (formated_time))
    count_display.set("%d pictures captured." % capture_count)
    lapse_display.set("This script has been running for %d day(s) %d hour(s) %d min(s) %d sec(s)." % (t_day, t_hour, t_min, t_sec))

def init():
    Trigger_0 = IntervalTrigger(seconds=1)
    Trigger_1 = IntervalTrigger(seconds=60)
    Trigger_2 = CronTrigger(hour="6-18", minute="*/15", second="0")
    scheduler.add_job(update_status, Trigger_0, id="status")
    scheduler.add_job(capture, Trigger_2, id="capture")
    scheduler.start()
    start_time = time.time()
    formated_time = time.asctime(time.localtime(start_time))
    print("successfully added task at %s" % formated_time)

def pause():
    global paused
    if paused == False:
        print("pause")
        scheduler.pause_job("capture")
        paused = True
        button_p_display.set("resume")
    else:
        print("resume")
        scheduler.resume_job("capture")
        paused = False
        button_p_display.set("pause")

def list_jobs():
    scheduler.print_jobs()

if __name__ == "__main__":
    init()
    window = tkinter.Tk()
    window.title("timelapse control center")
    window.geometry("480x160")
    
    clock_display = tkinter.StringVar()
    count_display = tkinter.StringVar()
    lapse_display = tkinter.StringVar()
    label_clock = tkinter.Label(window, textvariable=clock_display)
    label_count = tkinter.Label(window, textvariable=count_display)
    label_lapse = tkinter.Label(window, textvariable=lapse_display)
    button_p_display = tkinter.StringVar()
    button_p_display.set("pause")
    button_pause = tkinter.Button(window, textvariable=button_p_display, command=pause, width=10)
    button_print = tkinter.Button(window, text="print jobs", command=list_jobs, width=10)
    button_power = tkinter.Button(window, text="power button", command=power_control, width=10)

    button_pause.pack()
    button_print.pack()
    button_power.pack()
    label_clock.pack()
    label_lapse.pack()
    label_count.pack()

    window.mainloop()