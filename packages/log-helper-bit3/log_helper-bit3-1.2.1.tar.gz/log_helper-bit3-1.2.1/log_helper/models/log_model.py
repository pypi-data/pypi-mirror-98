from datetime import datetime


class LogModel:
    def __init__(self):
        self.__creationDate: datetime = datetime.now()
        self.__log_level: str = None
        self.__filename: str = None
        self.__function: str = None
        self.__line: int = None
        self.__message: str = None

    @property
    def creation_date(self) -> datetime:
        return self.__creationDate

    @creation_date.setter
    def creation_date(self, value: datetime):
        self.__creationDate = value

    @property
    def log_level(self) -> str:
        return self.__log_level

    @log_level.setter
    def log_level(self, value: str):
        self.__log_level = value

    @property
    def filename(self) -> str:
        return self.__filename

    @filename.setter
    def filename(self, value: str):
        self.__filename = value

    @property
    def function(self) -> str:
        return self.__function

    @function.setter
    def function(self, value: str):
        self.__function = value

    @property
    def line_number(self) -> int:
        return self.__line

    @line_number.setter
    def line_number(self, value: int):
        self.__line = value

    @property
    def message(self) -> str:
        return self.__message

    @message.setter
    def message(self, value: str):
        self.__message = value

    def to_dict(self) -> dict:
        return {
            "creation_date": self.creation_date,
            "log_level": self.log_level,
            "filename": self.filename,
            "function": self.function,
            "line_number": self.line_number,
            "message": self.message,
        }
