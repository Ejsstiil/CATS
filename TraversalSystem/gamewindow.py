import ctypes
import ctypes.wintypes
import time
import threading

from log import Log

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcMonitor", ctypes.wintypes.RECT),
        ("rcWork", ctypes.wintypes.RECT),
        ("dwFlags", ctypes.wintypes.DWORD)
    ]


class GameWindow(threading.Thread):
    window_name=""

    # client area inside its window
    cl_left=0
    cl_top=0
    cl_width=0
    cl_height=0

    # client area's offset within the monitor
    inner_window_left=0
    inner_window_top=0

    # monitor resolution
    screen_w=None
    screen_h=None

    # ratios for windowed game
    ratio_horiz=0.0
    ratio_vert=0.0
    
    _handle=None

    def __init__(self, window_name):
        super().__init__()
        self.previous_window_pos = None
        self.window_name = window_name
        self.get_game_window()
        self.start()

    def run(self):
        while True:
            hwnd = ctypes.windll.user32.FindWindowW(None, self.window_name)
            if hwnd != 0:
                rect = ctypes.wintypes.RECT()
                ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
                current_pos = (rect.left, rect.top)
                if self.previous_window_pos is not None and current_pos != self.previous_window_pos:
                    Log.log("Window moved")
                    self.get_game_window()
                self.previous_window_pos = current_pos
            time.sleep(0.1)

    def get_game_window(self):
        user32 = ctypes.windll.user32
        self._handle = user32.FindWindowW(0, self.window_name)
       
        # get Client-rect - the interior of the window
        rect = ctypes.wintypes.RECT()
        user32.GetClientRect(self._handle, ctypes.byref(rect))

        self.cl_left = rect.left
        self.cl_top = rect.top
        self.cl_width = rect.right - rect.left
        self.cl_height = rect.bottom - rect.top

        # get window position
        window_pos = ctypes.wintypes.POINT()
        window_pos.x = self.cl_left
        window_pos.y = self.cl_top
        user32.ClientToScreen(self._handle, ctypes.byref(window_pos))

        # get monitor size
        monitor_info = MONITORINFO()
        monitor_info.cbSize = ctypes.sizeof(monitor_info)
        user32.GetMonitorInfoW(user32.MonitorFromPoint(window_pos, 2), ctypes.byref(monitor_info))
        monitor_left = monitor_info.rcMonitor.left
        monitor_top = monitor_info.rcMonitor.top
        # - monitor dimensions
        self.screen_w = monitor_info.rcMonitor.right
        self.screen_h = monitor_info.rcMonitor.bottom
        # - get precise position of the inner_area against monitor resolution
        self.inner_window_left = window_pos.x - monitor_left
        self.inner_window_top = window_pos.y - monitor_top

        # downscale ratio for the fixed coordinates (mouse clicks)
        if not self.screen_w == 0:
            self.ratio_horiz = self.cl_width / self.screen_w 
            self.ratio_vert = self.cl_height / self.screen_h
        else:
            print("This will work only on the primary display and windowed or borderless mode!!")
            raise SystemExit(0)

    def activate(self):
        print(self._handle)
        user32 = ctypes.windll.user32
        user32.SetForegroundWindow(self._handle)
        
    def getGameResolution(self):
        return self.cl_width, self.cl_height

    def getGameX(self):
        return self.inner_window_left

    def getGameY(self):
        return self.inner_window_top

    def toString(self):
        return f"w: {self.cl_width}, " \
               f"h: {self.cl_height}, " \
               f"left: {self.inner_window_left}, " \
               f"top: {self.inner_window_top}"


