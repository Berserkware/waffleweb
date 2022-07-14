=============
middleware.py
=============

=======================================================================
``class waffleweb.middleware.MiddlewareHandler(middleware, apps=None)``
=======================================================================

A handler of middleware. Middleware gets ran on the request before your view receives it and on the response before it is sent.

**Parameters:**
 - **middleware** (``list[str]``) - A list of all your middleware. You need to format the middleware strings as so: 'module.MiddlewareClass'.
 - **apps** (``list``) - If you want to add your own apps instead of using waffleweb.defaults.APPS.
 
------------------------------
``loadMiddleware(middleware)``
------------------------------

Loads all the middleware into a list of dictionaries. The dictionaries include the module and the class of the middleware: ``{'module': middleware module, 'middleware': middlwareClass,}``.

**Parameters:**
 - **middleware** (``list[str]``) - A list of all the middleware needed to be loaded. You need to format the middleware strings as so: 'module.MiddlewareClass'.
 
**Returns:** ``list[dict]``

--------------------------------------
``runRequestMiddleware(request, app)``
--------------------------------------

Runs all the middleware on the request and then returns the request. It calls the ``before(request)`` method on the middleware classes.

**Parameters:**
 - **request** (``Request``) - The request to run the middleware on.
 - **app** (``WaffleApp``) - The app of the route matching the URL (for app specific middleware).
 
**Returns:** ``Request``

----------------------------------------
``runResponseMiddleware(response, app)``
----------------------------------------

Runs all the middleware on the response and then returns the response. It calls the ``after(response)`` method on the middleware classes.

**Parameters:**
 - **request** (``HTTPResponse``) - The response to run the middleware on.
 - **app** (``WaffleApp``) - The app of the route matching the URL (for app specific middleware).
 
**Returns:** ``HTTPResponse``