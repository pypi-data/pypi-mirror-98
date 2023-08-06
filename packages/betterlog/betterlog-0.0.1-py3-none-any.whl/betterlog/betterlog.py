from colorama import init
init()


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    INFO = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    modes = {
        'regular': f"",
        'bold': f"\033[1m",
        'underline': f"\033[4m"
    }


class log(colors):

    def __init__(self, message, mode='regular'):
        self.mode = mode
        self.message = message

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self, data):
        if data in self.modes:
            self.__mode = self.modes[data]
        else:
            self.__mode = self.modes['regular']

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, data):
        self.__message = f"{data}{self.END}"

    def __repr__(self):
        return self.message

    def __output(self, color):
        print(f"{self.mode}{color}{self.message}")

    def header(self):
        self.__output(self.HEADER)

    def ok(self):
        self.__output(self.BLUE)

    def info(self):
        self.__output(self.INFO)

    def success(self):
        self.__output(self.GREEN)

    def warning(self):
        self.__output(self.WARNING)

    def error(self):
        self.__output(self.FAIL)
