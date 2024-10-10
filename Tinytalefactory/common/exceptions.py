class NoAccessToOpenAiException(BaseException):
    def __str__(self):
        return "Can't access recourse"
