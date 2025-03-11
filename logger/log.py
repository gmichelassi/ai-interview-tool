import inspect
import os
from datetime import datetime
from typing import Literal

from colorama import Fore, Style
from dotenv import load_dotenv

load_dotenv()


OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'output')


class Log:
    def __init__(self, verbose: bool = True, output_mode: Literal['console', 'file'] = 'console'):
        self.use_color = os.getenv('ENV') != 'prod'
        self.verbose = verbose
        self.output_mode = output_mode

    def __now(self) -> str:
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        if self.use_color:
            return f"[{Fore.CYAN}{current_time}{Style.RESET_ALL}]"

        return f"[{current_time}]"

    def __instance(self, value: str) -> str:
        if self.use_color:
            return f"[{Fore.MAGENTA}{value}{Style.RESET_ALL}]"

        return f"[{value}]"

    def __method(self, value: str) -> str:
        if self.use_color:
            return f"({Fore.LIGHTMAGENTA_EX}{value}{Style.RESET_ALL})"

        return f"({value})"

    def __message(self, value: str) -> str:
        if not self.verbose:
            return value

        frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(frame)[2]
        method_name: str = outer_frame.function

        try:
            instance = outer_frame.frame.f_locals['self']
            class_name: str = instance.__class__.__name__
        except KeyError:
            class_name: str = "global"

        datetime = self.__now()
        instance = self.__instance(class_name)
        method = self.__method(method_name)

        return f"{datetime} {instance} {method} | {value}"

    def __message_level(self, level: Literal['info', 'error', 'warning', 'debug'] = 'info') -> str:
        if not self.use_color:
            return f"[{level.upper()}]"

        if level == 'info':
            return f"[{Fore.GREEN}{level.upper()}{Style.RESET_ALL}]"

        if level == 'error':
            return f"[{Fore.RED}{level.upper()}{Style.RESET_ALL}]"

        if level == 'warning':
            return f"[{Fore.YELLOW}{level.upper()}{Style.RESET_ALL}]"

        return f"[{Fore.LIGHTBLACK_EX}{level.upper()}{Style.RESET_ALL}]"

    def __output_message(self, message: str) -> None:
        if self.output_mode == 'console':
            print(" ".join(message.split()))
        else:
            log_path = f'{OUTPUT_DIR}/log.txt'

            if not os.path.exists(OUTPUT_DIR):
                os.mkdir(OUTPUT_DIR)

            with open(f'{log_path}', 'a', encoding="utf-8") as f:
                f.write(message)

    def info(self, value: str) -> None:
        return self.__output_message(f"{self.__message_level('info')} {self.__message(value)}")

    def error(self, value: str) -> None:
        return self.__output_message(f"{self.__message_level('error')} {self.__message(value)}")

    def warning(self, value: str) -> None:
        return self.__output_message(f"{self.__message_level('warning')} {self.__message(value)}")

    def debug(self, value: str) -> None:
        return self.__output_message(f"{self.__message_level('debug')} {self.__message(value)}")
