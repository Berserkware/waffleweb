from logging import exception
import os

from urllib.parse import urlparse

from waffleweb.response import HTTP404, FileResponse, HTTPResponse, JSONResponse
from waffleweb.static import StaticHandler

class Request():
    def __init__(self, requestHeaders, clientIP):
        self.headers = {}
        self.clientIP = clientIP
        self.requestHeaders = requestHeaders

        #Splits the request into it's seporate headers and adds it to a dictionary.
        splitHeaders = requestHeaders.split('\n')
        for line in splitHeaders:
                splitLine = line.strip().split(' ')
                self.headers[str(splitLine[0][:(len(splitLine[0]) - 1)])] = ' '.join(splitLine[1:])

    @property
    def path(self):
        return self.requestHeaders.split('\n')[0].split()[1]

    @property
    def method(self):
        return self.requestHeaders.split('\n')[0].split()[0]

    @property
    def HTTPVersion(self):
        return self.requestHeaders.split('\n')[0].split()[2]

    @property
    def host(self):
        return self.headers['Host']

    @property
    def userAgent(self):
        return self.headers['User-Agent']

    @property
    def accept(self):
        return self.headers['Accept']

    @property
    def acceptLanguage(self):
        return self.headers['Accept-Language']

    @property
    def acceptEncoding(self):
        return self.headers['Accept-Encoding']

    @property
    def connection(self):
        return self.headers['Connection']

    @property
    def cookie(self):
        return self.headers['Cookie']

class RequestHandler:
    '''Handles a requests, Returns response'''
    def __init__(self, request: Request, apps: list):
        self.request = request
        self.apps = apps

    def _405MethodNotAllowed(self, view) -> HTTPResponse:
        '''Returns a 405 response'''
        methods = ', '.join(view["allowedMethods"])
        return HTTPResponse(status=405, headers=f'Allow: {methods}') 

    def _getArg(self, index, part) -> tuple:
        '''
        Gets the kwargs and converts them to their type.
        returns a tuple with the name and type
        '''
        kwargName = ''
        kwargValue = None

        if part[1] == 'int':
            kwargName = str(part[0])
            kwargValue = int(self.splitRoot[index])
        elif part[1] == 'float':
            kwargName = str(part[0])
            kwargValue = float(self.splitRoot[index])
        else:
            kwargName = str(part[0])
            kwargValue = str(self.splitRoot[index])

        return (kwargName, kwargValue)

    def _splitURL(self) -> tuple:
        reqPath = urlparse(self.request.path).path

        #gets the root and file extenstion
        root, ext = os.path.splitext(reqPath)
        root = root.strip('/')
        splitRoot = root.split('/')

        return (root, splitRoot, ext)

    def _getView(self):
        '''Finds a view matching the request url, Returns view and the views kwargs.'''

        #Searches through all the apps to match the url
        for app in self.apps:
            app = app['app']
            for view in app.views:
                urlMatches = True
                viewKwargs = {}
                if view['path'] == self.root:
                    return (view, {})

                #checks if length of the view's split path is equal to the length of the split request request path
                if len(view['splitPath']) == len(self.splitRoot) and view['splitPath'] != ['']:
                    for index, part in enumerate(view['splitPath']):
                        #checks if path part is equal to the split request path part at the same index
                        if part != self.splitRoot[index] and type(part) == str:
                            urlMatches = False
                            break
                        
                        #adds args to view kwargs if part is list
                        if type(part) == list:
                            kwarg = self._getArg(index, part)
                            viewKwargs[kwarg[0]] = kwarg[1]

                    if urlMatches:
                        return (view, viewKwargs)
        
        raise HTTP404

    def _handleHead(self, view, kwargs):
        if 'HEAD' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view)

        newView = view['view'](self.request, **kwargs)

        if type(newView) == HTTPResponse:
            newView.content = None
        elif newView == JSONResponse:
            newView.json = None
        elif newView == FileResponse:
            newView.fileObj = None

        return newView

    def _handleGet(self, view, kwargs):
        if 'GET' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view)

        return view['view'](self.request, **kwargs)

    def _handlePost(self, view, kwargs):
        if 'POST' not in view['allowedMethods']:
            #Returns 405 response if request method is not in the view's allowed methods
            return self._405MethodNotAllowed(view)

        return view['view'](self.request, **kwargs)

    def getResponse(self):
        '''Gets a response to a request, retuerns Response.'''

        self.root, self.splitRoot, self.ext = self._splitURL()
        if self.ext == '':
            view, kwargs = self._getView()
            try:
                #Gets methods and runs it handle function
                if self.request.method == 'GET':
                    return self._handleGet(view, kwargs)
                elif self.request.method == 'HEAD':
                    return self._handleHead(view, kwargs)
                else:
                    return HTTPResponse('Not Implemented Error', status=501) 
            except HTTP404:
                return HTTPResponse('The requested page could not be found', status=404)
        else:
            try:
                handler = StaticHandler(self.root, self.splitRoot, self.ext)
                return handler.findFile()
            except HTTP404:
                return HTTPResponse('The requested file could not be found', status=404)