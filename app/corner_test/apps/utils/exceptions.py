class BaseException(Exception):
    def __init__(self, msg):
        self.message = msg


class SlackUserListException(BaseException):
    pass


class SlackChannelListException(BaseException):
    pass


class EmployeeDoesNotExistException(BaseException):
    pass


class SlaskUserInfoException(BaseException):
    pass


class SlackErrorException(BaseException):
    pass


class SlackGetMessageException(BaseException):
    pass


class SlackGetChannelException(BaseException):
    pass


class SlackSendMessageException(BaseException):
    pass
