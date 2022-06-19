import waffleweb
import importlib

try:
    settings = importlib.import_module('settings')
except ModuleNotFoundError:
    settings = None
    
from waffleweb.exceptions import AppNotFoundError, ViewNotFoundError
from jinja2 import Environment, FileSystemLoader, ModuleLoader, select_autoescape

def getRelativeUrl(viewStr: str, **kwargs):
    if len(viewStr.split(':')) != 2:
        raise ValueError('Your viewStr has to include an app and the view name, example: appName:viewName.')

    appName, viewName = viewStr.split(':')
    apps = waffleweb.defaults.APPS
    
    for app in apps:
        app = app['app']
        
        if app.appName == appName:
            for view in app.views:
                if view.name == viewName:
                    if view.hasPathHasArgs() == False:
                        return f'/{view.path}/'
                    else:
                        finalPath = []
                        
                        for part in view.splitPath:
                            if type(part) == list:
                                argName = part[0]
                                try:
                                    finalPath.append(kwargs[argName])
                                except KeyError:
                                    raise KeyError(f'Value for arg \"{argName}\" not found in kwargs.')
                            else:
                                finalPath.append(part)
                                
                        return f'/{"/".join(finalPath)}/'
                                
            #if cant find view, raise error
            raise ViewNotFoundError(f'View {viewName} could not be found.')
    #if cant find app, raise error
    raise AppNotFoundError(f'App {appName} could not be found.')

def _getEnvironmentFile() -> Environment:
    '''Gets a jinja Enviroment with the loader being FileSystemLoader.'''

    #Gets the template directory
    templateDir = waffleweb.defaults.DEFUALT_TEMPLATE_DIR
    if hasattr(settings, 'TEMPLATE_DIR'):
        templateDir = getattr(settings, 'TEMPLATE_DIR')

    env = Environment(
        loader=FileSystemLoader(searchpath=templateDir),
        autoescape=select_autoescape,
    )

    if hasattr(settings, 'TEMPLATE_FUNCTIONS'):
        templateFunctions = getattr(settings, 'TEMPLATE_FUNCTIONS')
    
        #Adds user supplied template functions
        for key, value in templateFunctions:
            env.globals[key] = value

    env.globals['getRelativeUrl'] = getRelativeUrl
    return env

def renderTemplate(filePath: str, context: dict={}) -> str:
    '''
    renders a template using jinja2, takes three arguments:
     - filepath - required - the file path to the template
     - context - the variables for the template
    '''

    if hasattr(settings, 'TEMPLATE_RENDERER'):
        renderer = getattr(settings, 'TEMPLATE_RENDERER')

        return renderer(filePath, context)
    else:
        #gets the enviroment
        env = _getEnvironmentFile()

        #gets the template render
        template = env.get_template(filePath)
        templateRender = template.render(**context)

        return templateRender
    
def renderErrorPage(mainMessage: str, subMessage: str=None, traceback: str=None) -> str:
    '''
    Renders an error page for debug, it takes 3 arguments:
     - mainMessage
     - subMessage - optional
     - traceback - optional
    '''

    return '''
        <!DOCTYPE html>
        <html>
            <head>
                <title>{mainMessage}</title>
            </head>
            
            <body style="font-family: Arial, Helvetica, sans-serif; margin:0px; padding:0;">
                <h1 style="background-color: #f6c486; display: block; margin:0px; padding:15px;">{mainMessage}</h1>
                {subMessage}
                {traceback}
            </body>
        </html>
    '''.format(
        mainMessage=mainMessage,
        subMessage=(f'<h2 style="color: #7a7a7a; display: block; margin:15px; padding:0px;">{subMessage}</h2>' if subMessage is not None else ''),
        traceback=(f'''
                <fieldset style="display: block; margin:15px; padding:0px;">
                    <legend style="margin-left:15px; margin-top:0px margin-bottom:0px padding:0px;"><h2 style="margin:0; padding:0px;">Traceback</h2></legend>
                    <h3 style="margin-left:15px; margin-top:5px; margin-bottom:10px; padding:0px;">{traceback}</h3>
                </fieldset>
                ''' if traceback is not None else ''),
        )