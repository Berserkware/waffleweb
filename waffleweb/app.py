import re

class waffleApp():
    '''
    The waffleApp() class is the centre of all the apps for your project.
    It only takes one argument: name, which is the name of your
    application. It is automatically defined when you create an app as so:
    app = waffleApp('yourAppName')
    '''

    def __init__(self, appName: str):
        self.appName = appName
        self.views = []

    @property
    def views(self):
        return self._views

    @views.setter
    def views(self, value):
        self._views = value

    def route(self, path: str, name: str):
        '''
        This is the decorator you put on all your views it gives your view a URL and a name.
        It takes two arguments path and name. The path argument is the reletive URL to your 
        view and the name argument is the name of your view.

        the name argument is used to reference the view in templates and redirects, it looks
        like this: appName:name

        You can add varibles to your url by puting <argumentName:valueType>
        you then add the argumentName to your views arguments, example:

        @app.route('profile/<username:str>', 'profile')
        def profileView(request, username):
            #your view logic goes here

        '''
        
        def decorator(view):
            #regex from https://stackoverflow.com/questions/31430167/regex-check-if-given-string-is-relative-url
            if re.compile(r'^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*').search(path):
                self.views.append({'path': path, 'name': name})

                def wrapper(*args, **kwargs):
                    view(*args, **kwargs)
                return wrapper
            else:
                raise ValueError('Your path has to be a valid relative URL pattern.')
        return decorator 