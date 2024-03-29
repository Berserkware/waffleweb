==========================
How-To: Custom Error Pages
==========================

If you want nice looking error pages rather than plain black and white ones you can use the ``errorHandler()`` decorator. The ``errorHandler()`` makes it easy to create custom error pages for HTTP status codes.

Error handlers work a lot like normal routes except they only get called when the status code in their arguments get returned. Your error handlers should take a argument for the request. The error handler should return a response.

This handler gets called when a 404 page is needed:

.. code-block:: python

	from waffleweb.response import render

	@app.errorHandler(404)
	def pageNotFound(request):
	    return render(request, '404.html', {'path': request.path}, status=404)

This handler gets called when an internal server error occurs:

.. code-block:: python

	from waffleweb.response import render

	@app.errorHandler(500)
	def serverError(request):
	    return render(request, '500.html', status=500)

This handler gets called when the client sends a method that is not allowed:

.. code-block:: python

	from waffleweb.response import render

	@app.errorHandler(405)
	def methodNotAllowed(request):
	    return render(request, '405.html', {'method': request.method}, status=405)
	    
Remember to set the status of the response to the status of the handler, because if you don't the status will the 200 OK.