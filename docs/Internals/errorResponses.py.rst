=================
errorResponses.py
=================

=======================================================================================================================
``class waffleweb.errorResponses.HTTPException(mainMessage, subMessage='', description='', traceback='', debug=False)``
=======================================================================================================================

Inherits from ``HTTPResponse``

A class for exception responses. The content of the response is set in the classes initialization. The content is set to either a debug page or a non-debug page.

**Parameters:**
 - **mainMessage** (``str``) - The main message of the exception. It will be shown in the debug page and the non-debug page.
 - **subMessage** (``str``) (optional) - The sub message of the exception. It will be shown in the debug page and the non-debug page.
 - **description** (``str``) (optional) - The description of the exception. It will only be shown in the debug page.
 - **traceback** (``str``) (optional) - The traceback to the exception. It will only be shown in the debug page.
 - **debug** (``bool``) (optional) - If the content should be the debug page or the non-debug page.

--------------------
``debugErrorPage()``
--------------------

This returns a debug error page using all the data from the class.

---------------
``errorPage()``
---------------

This returns a normal error page using some of the data from the class.

===============================================================
``class waffleweb.errorResponses.BadRequest()``
===============================================================

Inherits from ``HTTPException``

A 400 Bad Request response.

==========================================================================
``class waffleweb.errorResponses.PageNotFound(views)``
==========================================================================

Inherits from ``HTTPException``

A 404 Page Not Found Error response.

**Paramters:**
 - **views** (``list``) - The list of all the views to display for debug mode.

=======================================================================================
``class waffleweb.errorResponses.MethodNotAllowed(allowedMethods)``
=======================================================================================

Inherits from ``HTTPException``

A Method Not Allow Response.

**Paramters:**
 - **allowedMethods** (``list``) - The list of all the methods that are allowed.

=======================================================================================
``class waffleweb.errorResponses.InternalServerError(exception)``
=======================================================================================

Inherits from ``HTTPException``

A Internal Server Error response.

**Paramters:**
 - **exception** (``Exception``) - The exception for the debug page.

===============================================================================================================================
``function waffleweb.errorResponses.getErrorHandlerResponse(errorHandlers=None, request=None, response=None, statusCode=None)``
===============================================================================================================================

Looks for a error handler with the response's status code or the ``statusCode`` arg. If it finds an error handler it returns the response from the error handler otherwise it returns the ``response`` arg. You should provide either a response or a statusCode.

**Returns:** ``HTTPResponse``

**Parameters:**
 - **errorHandlers** (optional) (``list[ErrorHandler]``) - The list of ErrorHandler's to find the responses from.
 - **request** (optional) (``Request``) - The request to pass to the error handling functions.
 - **response** (optional) (``HTTPResponse``) - The response to get the status code from to find the handler.
 - **statusCode** (optional) (``int``) - The status code to find the handler.