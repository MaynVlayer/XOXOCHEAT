import struct
import psutil
import win32process
import logging
from ctypes import *
from win32gui import FindWindow

from SDK.process.Structures import SetLastError, WPM, RPM
from SDK.utils.time import now, diff

class Process():

    def __init__(self, proc_name):
        start = now()
        self.name = proc_name
        self.pid = self.get_pid(self.name)
        SetLastError(0)


        # Game
        self.proc_handler = windll.kernel32.OpenProcess(0x1F0FFF, 0, self.pid)

        self.window_handle = FindWindow(None, 'Counter-Strike: Global Offensive - Direct3D 9')
        
        # Modules
        self.modules = self.get_modules()

        self.parser_memory = {}
        self.parser_converter = {
            c_byte 	: 'c',
            c_int	: 'i',
            c_float	: 'f',
            c_bool	: '?'
        }

        logging.info(
            f'Process {self.name} found with PID -> {self.pid} | {len(self.modules)} modules loaded | {round(diff(start), 2)}ms')

    @staticmethod
    def get_pid(targetName):
        if targetName[::-1][0:4] == "exe.":
            targetName = targetName[0:-4]
        for proc in psutil.process_iter():
            try:
                name = proc.name()
            except Exception as e:
                print(e)
            if name == f"{targetName}.exe":
                return proc.pid
        raise Exception(f'Process "{targetName}.exe" not found.')

    @staticmethod
    def Pack(st):
        buffer = create_string_buffer(sizeof(st))
        memmove(buffer, addressof(st), sizeof(st))
        return buffer.raw

    def window_active(self):
        return windll.user32.GetForegroundWindow() ==self.window_handle

    def parse_struct(self, data):

        # Stores the parsed data
        # This is used to avoid parsing the same data multiple times as it is very slow
        if data in self.parser_memory:
            return self.parser_memory[data]

        if issubclass(data, Structure):
            string = ""
            for attribute in data._fields_:
                # <class 'Process.dataures.c_byte_Array_16'>
                if("c_byte_Array" in str(attribute[1])):
                    string += f"{sizeof(attribute[1])}s"
                    continue
                string += self.parser_converter[attribute[1]]
            self.parser_memory[data] = string
            return string

        return self.parser_converter[data]

    def get_modules(self):
        modules = {}
        for hModule in win32process.EnumProcessModulesEx(self.proc_handler, win32process.LIST_MODULES_ALL):
            modulepath = win32process.GetModuleFileNameEx(
                self.proc_handler, hModule)
            modules[modulepath.split('\\')[-1]] = hModule
        return modules

    def read(self, address, data_type):
        start = now()
        size = sizeof(data_type)
        read = c_ulonglong(0)
        buffer = (c_byte * size)()

        RPM(self.proc_handler, address, buffer, size, byref(read))

        data = list(struct.unpack(self.parse_struct(data_type), buffer))

        result = data[0]
        data_size = len(data)
        if data_size > 1:
            for index in range(data_size):
                fragment = data[index]
                if type(fragment) == bytes:
                    data[index] = (c_byte * len(fragment))(*fragment)
            result = data_type(*data)

        if (spent := diff(start)) > 5.0:
            logging.debug(f'took {spent}ms to read {size} bytes of data')

        return result

    def write(self, address, data, data_type):
        start = now()
        
        try:
            buffer = Process.Pack(data)
        except TypeError:
            buffer = Process.Pack(data_type(data))

        WPM(self.proc_handler, address, buffer,
            sizeof(data_type), byref(c_ulonglong(0)))

        if (spent := diff(start)) > 5.0:
            logging.debug(
                f'took {spent}ms to write {sizeof(data_type)} bytes of data')
