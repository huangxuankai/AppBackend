#!/usr/bin/python

class ChannelException(Exception):
    def __init__(self, error_msg, error_code):
        self.error_msg = error_msg
        self.error_code = error_code

    def getLastErrorCode(self):
        return self.error_code

    def getLastErrorMsg(self):
        return self.error_msg
