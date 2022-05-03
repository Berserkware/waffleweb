from requests import head
import waffleweb
import json

from datetime import datetime
from pytz import timezone
from http.client import responses

from waffleweb.cookie import Cookies

class HTTP404(Exception):
    pass

class ResponseHeaders(dict):
    def __init__(self, data: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #splits data into the seporate headers
        if data:
            for header in data.split('\n'):
                splitHeader = header.strip().split(' ')
                self[splitHeader[0][:(len(splitHeader[0]) - 1)]] = ' '.join(splitHeader[1:])

class HTTPResponseBase():
    '''Handles the HTTP responses only.'''
    
    statusCode = 200

    def __init__(
        self, headers=None, contentType=None, charset=None, status=None, reason=None
    ):
        self.headers = ResponseHeaders(headers)
        self._charset = charset
        self.cookies = Cookies()

        if str(self.cookies) != '':
            self.headers['Set-Cookie'] = str(self.cookies)

        #Checks if content type is in headers if it isn't adds one
        if 'Content-Type' not in self.headers:
            if contentType is None:
                contentType = f'text/html; charset={self.charset}'
            self.headers['Content-Type'] = contentType
        elif contentType:
            raise ValueError(
                'You cannot have a contentType provided if you have a Content-Type in your headers.'
            )

        if 'Date' not in self.headers:
            now = datetime.now(timezone('GMT'))
            dateTime = now.strftime("%a, %d %b %Y %X %Z")

            self.headers['Date'] = dateTime

        #Checks if status code is valid.
        if status is not None:
            try:
                self.statusCode = int(status)
            except(ValueError, TypeError):
                raise TypeError('HTTP status code has to be an integer.')

            if 100 > status or status > 599:
                raise ValueError('HTTP status code must be a integer from 100 to 599.')
        self._reasonPhrase = reason

    @property
    def reasonPhrase(self):
        if self._reasonPhrase is not None:
            return self._reasonPhrase
        return responses.get(self.statusCode, "Unknown status code.")
        
    @reasonPhrase.setter
    def reasonPhrase(self, value):
        self._reasonPhrase = value

    @property
    def charset(self):
        '''Gets charset if charset is None, gets defualt charset.'''
        if self._charset is not None:
            return self._charset

        return waffleweb.defaults.DEFAULT_CHARSET

    @charset.setter
    def charset(self, value):
        self._charset = value 

    def setCookie(self, name, value):
        '''Sets a cookie to a value, takes two arguments: name and value'''
        self.cookies.setCookie(name, value)   
        #self.headers['Set-Cookie'] = str(self.cookies)    

    def deleteCookie(self, name):
        '''Deletes a cookie if exists, takes one argument: name.'''
        self.cookies.removeCookie(name)
        #if str(self.cookies) != '':
        #    self.headers['Set-Cookie'] = str(self.cookies)
        #else:
        #    del self.headers['Set-Cookie']

    def serializeHeaders(self):
        '''This gets just the headers in a binary string.'''
        headers = b'\r\n'.join([
            key.encode(self.charset) + b': ' + value.encode(self.charset)
            for key, value in self.headers.items()
        ])
        setCookies = (b'' if str(self.cookies) == '' else 
            b'\r\n' + b'\r\n'.join([
                b'Set-Cookie' + b': ' + f'{key}={value}'.encode(self.charset)
                for key, value in self.cookies.items()
                ]))

        return headers + setCookies

    __bytes__ = serializeHeaders    

    def serialize(self, content):
        '''This gets the fully binary string including headers and the content.'''
        return b'HTTP/1.1 ' + self.convertBytes(self.statusCode) + b' ' + self.convertBytes(self.reasonPhrase) + b'\r\n' + self.serializeHeaders() + b'\r\n\r\n' + content

    def convertBytes(self, value):
        '''Encodes value and converts it to bytes.'''
        if isinstance(value, str):
            return bytes(value, encoding=self.charset)

        return bytes(str(value), encoding=self.charset)

class HTTPResponse(HTTPResponseBase):
    '''Handles the HTTP responses and content.'''

    def __init__(self, content=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.content = content 
        self.headers['Content-Length'] = str(len(str(self.content)))

    def __bytes__(self):
        content = (self.content if self.content != b'None' else b'')
        return self.serialize(content)

    @property
    def content(self):
        return b"".join(self._content)

    @content.setter
    def content(self, value):
        self._content = [self.convertBytes(value)]

class JSONResponse(HTTPResponseBase):
    '''Handles the HTTP responses and json.'''

    def __init__(self, jsonContent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.json = jsonContent
        self.headers['Content-Length'] = str(len(json.dumps(jsonContent)))
        self.headers['Content-Type'] = f'application/json; charset={self.charset}'

    def __bytes__(self):
        json = (self.json if self.json != b'None' else b'')
        return self.serialize(json)

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = bytes(json.dumps(value), encoding=self.charset)

class FileResponse(HTTPResponseBase):
    '''Handles the HTTP responses and file.'''

    def __init__(self, fileObj=None, mimeType=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mimeType = mimeType
        self.fileObj = fileObj

        #add mimetype to content-type
        if mimeType is not None:
            self.headers['Content-Type'] = f'{mimeType}; charset={self.charset}'

    def __bytes__(self):
        fileObj = (self.fileObj if self.fileObj != b'None' else b'')
        return self.serialize(fileObj)

    @property
    def fileObj(self):
        return self._fileObj

    @fileObj.setter
    def fileObj(self, value):
        self._fileObj = value.read()
