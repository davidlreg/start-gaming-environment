import os
import time
import subprocess

import pyautogui
import win32con
import win32gui

# =====================================================================
# CONFIG
# =====================================================================

#: Path to Chrome executable
CHROME_PATH = r"C:\Users\david\AppData\Local\Google\Chrome\Application\chrome.exe"

#: Single monitor resolution
MON_WIDTH = 2560
MON_HEIGHT = 1440

#: Frame / titlebar offsets for tight window borders
BORDER_X = 8
TITLEBAR_Y = 32

#: Left monitor (positioned left of main monitor)
LEFT_MON_X = -MON_WIDTH

#: Predefined areas on the left monitor (currently not used directly)
YOUTUBE_AREA = {
    "x": LEFT_MON_X + MON_WIDTH // 2 - BORDER_X,
    "y": 0,
    "w": MON_WIDTH // 2 + BORDER_X,
    "h": MON_HEIGHT + TITLEBAR_Y,
}

YTMUSIC_AREA = {
    "x": LEFT_MON_X,
    "y": 0,
    "w": MON_WIDTH // 2 + BORDER_X,
    "h": MON_HEIGHT // 2 + TITLEBAR_Y // 2,
}

DISCORD_AREA = {
    "x": LEFT_MON_X,
    "y": MON_HEIGHT // 2 + 10,
    "w": MON_WIDTH // 2,
    "h": MON_HEIGHT // 2 - 10,
}

#: Layout for small windows (Steam, EA, etc.) on main monitor
SMALL_W = 1200
SMALL_H = 800

SMALL_POSITIONS = [
    (100, 100),
    (950, 100),
    (1800, 100),
    (100, 750),
]

# =====================================================================
# WINDOW HELPERS
# =====================================================================

def find_windows_by_title_substring(substring: str) -> list[int]:
    """
    Return all visible window handles whose title contains the substring.
    """
    substring = substring.lower()
    handles: list[int] = []

    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if substring in title.lower():
                handles.append(hwnd)

    win32gui.EnumWindows(enum_handler, None)
    return handles


def move_and_resize(hwnd: int, x: int, y: int, width: int, height: int) -> None:
    """
    Move and resize a window to the given rectangle.
    """
    win32gui.MoveWindow(hwnd, x, y, width, height, True)


def focus_window(hwnd: int) -> None:
    """
    Restore and bring a window to the foreground.
    """
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.3)


def move_to_left_monitor_full(hwnd: int) -> None:
    """
    Place a window full-size on the left monitor once.
    """
    move_and_resize(hwnd, LEFT_MON_X, 0, MON_WIDTH, MON_HEIGHT)
    time.sleep(0.2)


def snap_top_left_on_current_monitor(hwnd: int) -> None:
    """
    Snap a window to top-left on its current monitor using Win hotkeys.
    """
    focus_window(hwnd)
    pyautogui.hotkey("win", "left")
    time.sleep(0.2)
    pyautogui.hotkey("win", "up")
    time.sleep(0.2)


def snap_bottom_left_on_current_monitor(hwnd: int) -> None:
    """
    Snap a window to bottom-left on its current monitor using Win hotkeys.
    """
    focus_window(hwnd)
    pyautogui.hotkey("win", "left")
    time.sleep(0.2)
    pyautogui.hotkey("win", "down")
    time.sleep(0.2)


def snap_right_on_current_monitor(hwnd: int) -> None:
    """
    Snap a window to the right half of its current monitor.
    """
    focus_window(hwnd)
    pyautogui.hotkey("win", "right")
    time.sleep(0.2)


# =====================================================================
# APP LAUNCH HELPERS
# =====================================================================

def open_chrome_window(url: str) -> None:
    """
    Open a new Chrome window with the given URL.
    """
    subprocess.Popen([CHROME_PATH, "--new-window", url])


def open_discord() -> None:
    """
    Launch Discord via start menu shortcut.
    """
    os.startfile(
        r"C:\Users\david\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"
    )


# =====================================================================
# MAIN: GAMING SETUP
# =====================================================================

def start_gaming_setup() -> None:
    # 1. Open apps / websites
    open_chrome_window("https://www.youtube.com/")
    time.sleep(1)
    open_chrome_window("https://music.youtube.com/")
    time.sleep(1)
    open_discord()

    os.startfile(r"C:\Program Files (x86)\Steam\steam.exe")
    os.startfile(r"C:\Program Files\Electronic Arts\EA Desktop\EA Desktop\EALauncher.exe")

    # Xbox app
    os.startfile(r"shell:AppsFolder\Microsoft.GamingApp_8wekyb3d8bbwe!Microsoft.Xbox.App")

    os.startfile(r"C:\Program Files\NVIDIA Corporation\NVIDIA App\CEF\NVIDIA App.exe")

    # 2. Wait for all windows to spawn
    print("Warte 8 Sekunden, bis alle Fenster vollständig geladen sind...")
    time.sleep(8)

    # 3. Arrange Chrome windows

    # YouTube → right side on left monitor
    for hwnd in find_windows_by_title_substring("YouTube - Google Chrome"):
        move_to_left_monitor_full(hwnd)
        snap_right_on_current_monitor(hwnd)

    # YouTube Music → top-left on left monitor
    for hwnd in find_windows_by_title_substring("YouTube Music - Google Chrome"):
        move_to_left_monitor_full(hwnd)
        snap_top_left_on_current_monitor(hwnd)

    print("Chrome wurde angeordnet – warte kurz, bevor Discord gesetzt wird...")
    time.sleep(1.2)

    # 4. Discord → bottom-left on left monitor
    for hwnd in find_windows_by_title_substring("Discord"):
        move_to_left_monitor_full(hwnd)
        snap_bottom_left_on_current_monitor(hwnd)

    # 5. Optional: place small windows (Steam, EA, Xbox, Nvidia)
    small_titles = [
        "Steam",
        "EA app",
        "Xbox",
        "NVIDIA GeForce Experience",
    ]

    idx = 0
    for title in small_titles:
        handles = find_windows_by_title_substring(title)
        for hwnd in handles:
            if idx < len(SMALL_POSITIONS):
                x, y = SMALL_POSITIONS[idx]
                move_and_resize(hwnd, x, y, SMALL_W, SMALL_H)
                idx += 1


# =====================================================================
# ENTRY POINT
# =====================================================================

if __name__ == "__main__":
    start_gaming_setup()
