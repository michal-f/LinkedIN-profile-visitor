# -*- coding: utf-8 -*-


class ExceptionWithFormat(Exception):
    def __init__(self,  *args, **kwargs):
        super(ExceptionWithFormat, self).__init__(*args, **kwargs)

    def __repr__(self):
        if self and type(self) is str:
            return unicode(self) + self.__class__.__name__
        return super(ExceptionWithFormat, self).__repr__()

    def __str__(self):
        return self.__repr__()


class RequestError(ExceptionWithFormat):
    """
    Request Failed! an Error occured!
    """


class NextPageNotFound(ExceptionWithFormat):
    """
    Next page number not found!
    Next page dont exists or parsing error!
    """

class CredentialsError(ExceptionWithFormat):
    """
    Credentials not found or local_settings.py dont exists!
    """


class NoUrlsToParse(ExceptionWithFormat):
    """
    No urls to parse found error!
    """


class ListPageNumberNotFound(ExceptionWithFormat):
    """
    List page number not found in passed url!
    """


class ConnectionErrorException(ExceptionWithFormat):
    """
    A Connection Error occurred can't continue. exit!
    """


class InvalidResponseStatus(ExceptionWithFormat):
    """
    response status code != 200 -> exiting run!
    """


# DBQUERY EXCEPTIONS:
class CreateProfileException(ExceptionWithFormat):
    """
    Error creating new ProfilePage!
    """


class CreateListPageException(ExceptionWithFormat):
    """
    Error creating new ListPage!
    """


class CreateRequestException(ExceptionWithFormat):
    """
    Error in creating new request exception object!
    """


class UpdateProfileFailed(ExceptionWithFormat):
    """
    Error in updating profile requesting status
    """
