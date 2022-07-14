=========
static.py
=========

============================================================================================================================================
``function waffleweb.static.findStatic(path, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)``
============================================================================================================================================
Finds a static file, takes all the same arguments as ``open()``. This is to separate the static finder from the static opener so you can provide your own static finder.

**Returns:** a file object

============================================================================================================================================
``function waffleweb.static.openStatic(file, mode='rb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)``
============================================================================================================================================

Opens a static file. takes all the same arguments as ``open()``. Its basically just ``open`` but it adds your static directory to the start of the path.

**Returns:** a file object

=======================================================================
``function waffleweb.static.getStaticFileResponse(request, root, ext)``
=======================================================================

Finds a static file and puts it into a ``FileResponse``. If can't find file it raises HTTP404.

**Parameters:**
 - **request** (``Request``) - The request for the response.
 - **root** (``str``) - The path to the file.
 - **ext** (``str``) - The file extension.
 
**Returns:** ``FileResponse``