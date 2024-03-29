==================
How-To: Templating
==================

Templating is useful for when you want have complex pages with variables and simple logic. By default Waffleweb uses `Jinja2 <https://palletsprojects.com/p/jinja/>`__ for templating. You can change the template renderer. we will get into that later. In this How-To guide you will learn the basics of creating Jinja templates and how to render them with Waffleweb.

Rendering Templates
...................

You can render templates with one of two ways: The ``renderTemplate()`` function or using the ``render()`` response. ``renderTemplate()`` renders the template and returns the rendered template whereas ``render()`` renders the template and returns an ``HTTPResponse``.

By default Waffleweb looks in the "template" directory for templates but your can change it by creating a file called "settings.py" and add a variable called "TEMPLATE_DIR".

.. code-block:: python

	TEMPLATE_DIR = 'static/html'
	
``renderTemplate()``
--------------------

This finds a template and renders with the context.

``renderTemplate`` takes two arguments:
 - ``filePath`` (``str``) - The path to the template.
 - ``context`` (``dict``) - These are the variables for the template.
 
.. code-block:: python

	from waffleweb.template import renderTemplate
	from waffleweb.response import HTTPResponse

	@app.route('/template', methods=['GET'])
	def template(request):
	    page = renderTemplate('page.html', {'var1': 'value'})
	    return HTTPResponse(request, page)
 
``render()``
------------

This calls ``renderTemplate`` with the ``filePath`` and ``context`` and puts it in a ``HTTPResponse`` then returns the response.

``render`` takes 6 arguments:
 - ``request`` (``Request``) - The request passed into the routed function.
 - ``filePath`` (``str``) - The path to the template.
 - ``context`` (``dict``) - These are the variables for the template.
 - The other arguments can be found in the `template.py <../Reference/template.py.html>`_ page.
 
.. code-block:: python

	from waffleweb.response import render

	@app.route('/template', methods=['GET'])
	def template(request):
	    return render(request, 'page.html', {'var1': 'value'})
	    
Creating templates
..................

This is the basics of how to create templates for Jinja2.

Variables In Templates
----------------------

You can add variables to your template with the context argument of the template rendering function. To access your variables in your template all you need to do is surround them with two sets of curly brackets.

.. code-block:: Jinja

	<h1>{{ var1 }}</h1>
	<p>{{ var2 }}</p>
	
Logic In Templates
------------------

You can add simple logic to your template by surrounding the logic with a set of curly brackets and percentage signs. Logic in template is similar to python but it has it's limitations. You can add if statements and for loops.

If Statment:

.. code-block:: Jinja

	{% if var1 is 'on' %}
	    <h1>on</h1>
	{% elif var1 is 'off' %}
	    <h1>on</h1>
	{% else %}
	    <h1>N/A</h1>
	{% endif %}
	
For Loop:

.. code-block:: Jinja
	
	{% for var in dictVar %}
	    <p>{{ var }}</p>
	{% endfor %}

To learn more about creating template you can go the the Jinja `Docs <https://jinja.palletsprojects.com/en/3.1.x/templates/>`_.

Functions in templates
----------------------

Waffleweb has one built in template function: `getRelativeUrl() <../Reference/template.py.html>`_.

.. code-block:: Jinja

	<h1>{{ getRelativeUrl('news:article', id=1234, name='Something happend!') }}</h1>

You can add your own custom template functions by adding a value named "TEMPLATE_RENDERER" to your apps settings.

.. code-block:: python

    yourApp.settings['TEMPLATE_FUNCTIONS'] = {'func1': func1, 'func2': func2}
	
This only work when using the default rendering functions.

Adding Your Own Template Renderer
.................................

Adding your own template renderer is easy. All you need to do is add a value named "TEMPLATE_RENDERER" to your apps settings.

.. code-block:: python

	yourApp.settings['TEMPLATE_RENDERER'] = yourRenderingFunction
	
Your template renderer must take a file path and the context (variables) for the template. It must return a string of the rendered template.

If you have a TEMPLATE_RENDER supplied it will be called by ``renderTemplate()``. So out of the box it will automatically work with ``render()``.

Changing the Jinja Enviroment
.............................

You can change the enviroment that Jinja uses by add a item to your app settings dictionary called "JINJA_ENVIROMENT". You can set the variable to a ``Enviroment`` object.

.. code-block:: python

    from jinja2 import Enviroment

    JINJA_ENVIROMENT = Enviroment(...)