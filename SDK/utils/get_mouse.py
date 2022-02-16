import win32api

def get_mouse(button: int):
    state = win32api.GetKeyState(button)
    return state == -127 or state == -128
