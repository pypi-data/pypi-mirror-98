class RequestNotSetException(Exception):
    def __str__(self):
        return "No request set on this hook."


class RequestDataNotStoredException(Exception):
    def __str__(self):
        return "No data stored on this request."
