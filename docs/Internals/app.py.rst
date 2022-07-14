======
app.py
======

=====================================================
``class waffleweb.WaffleApp(appName, middleware=[])``
=====================================================

The WaffleApp object is what you attach your views and app specific middleware to.

**Parameters:**
 - **appName** (``str``) - The name of your app.
 - **middleware** (``list[str]``) - A list of your app's middleware. All the middleware are strings with the module and middleware class. Example: 'testModule.Middleware' or 'middleware.testModule.Middleware'.

---------------------------------------------------------------------------------------------------------------
``route(path='/', name=None, methods=['GET'])``
---------------------------------------------------------------------------------------------------------------

A decorator to route a function to an URL.

**Parameters:**
 - **path** (``str``) - The path to your view.
 - **name** (``str``) - The name of your view.
 - **methods** (``list[str]``) - The allowed methods for your view.
 
----------------------------
``errorHandler(statusCode)``
----------------------------

A decorator to route a function to a certain error code. Whenever you return a response with a status code a errorHandler will be looked for with that status code. it will return your errorHandler.

**Parameters:**
 - **statusCode** (``int``) - The status code to route the function to.

-----------------------
``request(rawRequest)``
-----------------------

Sends a request to any of the views. It's main use is for the testing of waffleweb. It goes through the normal process that the requests takes when going through the server, except it doesn't go through a server.

**Parameters:**
 - **rawRequest** (``bytes``) - A byte request.
 
**Returns:** Response
 
**Usage:**

.. code-block:: python

	from waffleweb import WaffleApp
	
	app = WaffleApp('appName')
	
	@app.route('/')
	def index(request):
	    return HTTPResponse(request, 'index')
	    
	res = app.request(b'GET /index HTTP/1.1\r\nHeader-Name: value\r\n\r\n')