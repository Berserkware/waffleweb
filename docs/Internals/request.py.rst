==========
request.py
==========

===============================================================
``class waffleweb.request.Request(rawRequest, IP, wsgi=False)``
===============================================================

A object for storing all the request data.

**Parameters:**
 - **rawRequest** (``bytes``) - The raw request.
 - **IP** (``str``) - The IP of the client sending the request.
 - **wsgi** (``bool``) - If the request is wsgi or not.
 
**Important attributes:**
 - **FILES** (``dict``) -  The uploaded files of the request.
 - **META** (``dict``) - The headers of the request.
 - **POST** (``dict``) - The POST data of the request.
 - **URL_PARAMS** (``dict``) - The URL parameters of the request.
 - **body** (``bytes``) - The body of the request.
 - **COOKIES** (``Cookies``) - All the request`s cookies.
 
------------------
``_getPostData()``
------------------

Parses and gets all the post and file data and adds them to the POST and FILES attributes.

**Returns:** ``None``

-------------------
``_getURLParams()``
-------------------

Gets all the URL parameters and adds them to the URL_PARAMS attribute.

**Returns:** ``None``

--------------
``_getBody()``
--------------

Parses and gets the body then returns it.

**Returns:** ``str``

-------------------
``property path()``
-------------------

Returns the URL of the request.

**Returns:** ``str``

---------------------
``property method()``
---------------------

Returns the HTTP method of the request.

**Returns:** ``str``

--------------------------
``property HTTPVersion()``
--------------------------

Returns the HTTP version of the request.

**Returns:** ``str``

===========================================================================
``class waffleweb.request.RequestHandler(request, debug=False, apps=None)``
===========================================================================

A handler for requests to find the views and responses.

**Parameters:**
 - **request** (``Request``) - The Request to use to find the response.
 - **debug** (``bool``) - If debug mode is on.
 - **apps** (``list``) - If you want to add your own apps instead of using waffleweb.defaults.APPS.
 
------------------------
``_getArg(index, part)``
------------------------

Converts the URL variable to it's type. Returns a ``tuple`` with the name of the variable and the value: ('name', 'value').

**Parameters:**
 - **index** (``int``) - The section in the URL to convert.
 - **part** (``list``) - The part in the view's URL to know what the type to convert is and the name of the argument.

**Returns:** ``tuple``

---------------
``_splitURL()``
---------------

Splits the request's URL into the different parts. Returns a ``tuple`` with the root, split root and extention: (root, splitRoot, ext).

**Returns:** ``tuple``

-------------
``getView()``
-------------

Gets the view function matching the URL and the URL variables in a dictionary, If a view matching the URL can't be found a ``HTTP404`` will be raised. Returns (``viewFunc``, {view arguments}).

**Returns:** ``tuple``

----------------------------
``_handleGet(view, kwargs)``
----------------------------

Handles GET request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends

-----------------------------
``_handleHead(view, kwargs)``
-----------------------------

Handles HEAD request by running the view functions with the kwargs and requests given then stripping the content. Returns what the matched view returns without the content.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
-----------------------------
``_handlePost(view, kwargs)``
-----------------------------

Handles POST request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
----------------------------
``_handlePut(view, kwargs)``
----------------------------

Handles PUT request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends

-------------------------------
``_handleDelete(view, kwargs)``
-------------------------------

Handles DELETE request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Returns:** Depends

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.
 
--------------------------------
``_handleConnect(view, kwargs)``
--------------------------------

Handles CONNECT request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
--------------------------------
``_handleOptions(view, kwargs)``
--------------------------------

Handles OPTIONS request by basically ignores the view function and returning a response with all the allowed methods.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends

------------------------------
``_handleTrace(view, kwargs)``
------------------------------

Handles TRACE request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
------------------------------
``_handlePatch(view, kwargs)``
------------------------------

Handles PATCH request by running the view functions with the kwargs and requests given. Returns what the matched view returns.

**Parameters:**
 - **view** (``func``) - The view function.
 - **kwargs** (``dict``) - The URL variables for the function.

**Returns:** Depends
 
---------------------------------------------------
``getErrorHandler(response=None, statusCode=None)``
---------------------------------------------------

Looks for a error handler with the response's status code or the ``statusCode`` arg. If it finds an error handler it returns the response from the error handler otherwise it returns the ``response`` arg. You should provide either a response or a statusCode.

**Returns:** ``HTTPResponse``

**Parameters:**
 - **response** (optional) (``HTTPResponse``) - The response to get the status code from to find the handler.
 - **statusCode** (optional) (``int``) - The status code to find the handler.
 
--------------------
``_handle404View()``
--------------------

If a ``HTTP404`` is raised this function will get called. If debug is on it will return a default 404 error page. If debug is off then it will try to get a error handler, but if one cannot be found it will return a plain 404 page.

**Returns:** ``HTTPResponse``

----------------------------------------
``_405MethodNotAllowed(allowedMethods)``
----------------------------------------
If the view found does not allow the request's method then this will be called. If debug is on it will return a default 405 error page. If debug is off then it will try to get a error handler, but if one cannot be found it will return a plain 405 page.

**Returns:** ``HTTPResponse``

-----------------------------
``_501NotImplementedError()``
-----------------------------

This will be called when the request's method is unknown this will be called. If debug is on it will return a default 501 error page. If debug is off then it will try to get a error handler, but if one cannot be found it will return a plain 501 page.

**Returns:** ``HTTPResponse``

-----------------
``getResponse()``
-----------------

Gets a response.

**Returns:** ``HTTPResponse``