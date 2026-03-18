import tkinter as tk
import sys
import json
import os

## settings
TIMER_FONT = (
    ("Consolas", 64, "bold")
    if sys.platform == "win32"
    else ("DejaVu Sans Mono", 64, "bold")
)


SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {"work_minutes": 50, "break_minutes": 5}


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()


def save_settings(work_min, break_min):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"work_minutes": work_min, "break_minutes": break_min}, f)


# --- COLOR PALETTE ---
BG_MAIN = "#1e1e2e"  # Main window background
BG_FRAME = "#181825"  # Slightly darker background for frames/settings window
BG_INPUT = "#11111b"  # Very dark background for tk.Entry fields

BTN_BG = "#313244"  # Normal button background
BTN_ACTIVE = "#45475a"  # Button color when clicked

TEXT_MAIN = "#cdd6f4"  # Main timer text and standard text
TEXT_SUB = "#bac2de"  # Smaller labels (like "Work Time" in settings)

ACCENT_WORK = "#a6e3a1"  # Soft Green (Work mode label)
ACCENT_BREAK = "#f38ba8"  # Soft Red/Pink (Break mode label, Break Window text)
ACCENT_WARN = "#fab387"  # Peach/Orange (Snooze button)
# ---------------------
settings = load_settings()
root = tk.Tk()
root.geometry("600x400")
root.title("Timer")
root.configure(bg="#1e1e2e")


# Main Background: #1e1e2e (Dark Navy)
# Timer Text: #cdd6f4 (Soft White)
# "Work" Text: #a6e3a1 (Soft Green)
# "Break" Text: #f38ba8 (Soft Red/Pink)
# Button Background: #313244
# Button Text: #cdd6f4

workMin = settings["work_minutes"]
breakMin = settings["break_minutes"]
## vars
isRunning = False
SecondsRemaing = workMin * 60


time_var = tk.StringVar(value=str(workMin))
trackId = None
settingsWin = None


def OpenSettings():
    global settingsWin
    settingsWin = tk.Toplevel(root)
    settingsWin.geometry("600x400")
    settingsWin.title("settings")
    settingsWin.configure(bg="#1e1e2e")

    settingsWin.grab_set()
    workFrame = tk.Frame(settingsWin, bg="#1e1e2e")
    breakFrame = tk.Frame(settingsWin, bg="#1e1e2e")
    workTime = tk.Entry(
        workFrame, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN
    )
    breakTime = tk.Entry(
        breakFrame, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN
    )
    workTime.insert(0, str(workMin))
    breakTime.insert(0, str(breakMin))
    workL = tk.Label(workFrame, text="Work Time", bg=BG_FRAME, fg=TEXT_SUB)
    breakL = tk.Label(breakFrame, text="Break Time", bg=BG_FRAME, fg=TEXT_SUB)

    def SaveBTN():
        global workMin, breakMin
        try:
            workMin = int(workTime.get())
            breakMin = int(breakTime.get())
        except ValueError:
            print("error")
            return
        save_settings(workMin, breakMin)
        Rest()

        settingsWin.destroy()

    def RestSettings():
        global workMin, breakMin
        workMin = DEFAULT_SETTINGS["work_minutes"]
        breakMin = DEFAULT_SETTINGS["break_minutes"]

        workTime.delete(0, tk.END)
        breakTime.delete(0, tk.END)

        workTime.insert(0, str(workMin))
        breakTime.insert(0, str(breakMin))
        save_settings(workMin, breakMin)

    saveB = tk.Button(
        settingsWin,
        text="save",
        command=SaveBTN,
        bg=BTN_BG,
        activebackground=BTN_ACTIVE,
        fg=buttonText,
        width=12,
        borderwidth=0,
    )
    restB = tk.Button(
        settingsWin,
        text="Rest",
        command=RestSettings,
        bg=BTN_BG,
        activebackground=BTN_ACTIVE,
        fg=buttonText,
        width=12,
        borderwidth=0,
    )

    workFrame.pack(pady=5)
    breakFrame.pack(pady=5)
    workL.pack(side=tk.LEFT, padx=5)
    workTime.pack(side=tk.LEFT, padx=5)
    breakL.pack(side=tk.LEFT, padx=5)
    breakTime.pack(side=tk.LEFT, padx=5)
    saveB.pack(pady=50)
    restB.pack(pady=10)


def StartTimer():
    global isRunning
    if not isRunning and SecondsRemaing > 0:
        isRunning = True
        Tick()


def StopTimer():
    global isRunning

    isRunning = False
    if trackId != None:
        root.after_cancel(trackId)


def Rest():
    global SecondsRemaing
    SecondsRemaing = workMin * 60
    StopTimer()
    FormatTime()


def FormatTime():
    minutes, seconds = divmod(SecondsRemaing, 60)
    hours, minutes = divmod(minutes, 60)
    time_var.set("{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds)))


def Tick():

    global SecondsRemaing
    global trackId
    global isRunning
    # Do some math here
    if SecondsRemaing <= 0:
        isRunning = False

    if isRunning:
        trackId = root.after(1000, Tick)
        SecondsRemaing = SecondsRemaing - 1
        FormatTime()


buttonBG = "#313244"
buttonText = "#cdd6f4"

buttonsFram = tk.Frame(root, bg="#1e1e2e")


startButton = tk.Button(
    buttonsFram,
    text="Start",
    fg=buttonText,
    bg=buttonBG,
    width=20,
    borderwidth=0.49,
    command=StartTimer,
)
stopButton = tk.Button(
    buttonsFram,
    text="Stop",
    fg=buttonText,
    bg=buttonBG,
    width=12,
    borderwidth=0,
    command=StopTimer,
)
restButton = tk.Button(
    buttonsFram,
    text="Restart",
    fg=buttonText,
    bg=buttonBG,
    width=12,
    borderwidth=0,
    command=Rest,
)
settingsButton = tk.Button(
    root,
    text="settings",
    fg=buttonText,
    bg=buttonBG,
    width=12,
    borderwidth=0,
    command=OpenSettings,
)

timer_label = tk.Label(
    root, textvariable=time_var, bg="#1e1e2e", fg="#a6e3a1", font=TIMER_FONT
)


mode_label = tk.Label(
    root,
    text="work",
    bg="#1e1e2e",
    fg="#abe9a5",
    font=("Arial", 20, "bold"),
)
# ---------main pack -----------
timer_label.pack(pady=20)
mode_label.pack(pady=20)
buttonsFram.pack(pady=30)
restButton.pack(side=tk.LEFT, padx=5)
startButton.pack(side=tk.LEFT, padx=0)
stopButton.pack(side=tk.LEFT, padx=5)
settingsButton.pack(pady=20)


root.mainloop()
