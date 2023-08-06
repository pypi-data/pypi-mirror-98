class ProgramStautsException(BaseException):
    pass


class QuitException(ProgramStautsException):
    pass


class UserNeedQuitException(QuitException):
    pass


class ProgramNeedQuitException(QuitException):
    pass
