================
Django Imbue Tag
================

Extension for Django template syntax. Adds tag that can inject template fragments into other template

Quick start
-----------

Module is compatible (was tested) with following Django versions:

- 3.1
- 3.0
- 2.2
- 2.1
- 2.0

1. Install module from PyPI::

    pip install django-imbue-tag

2. Add ``django_imbue_tag`` to your INSTALLED_APPS setting::

    INSTALLED_APPS = [
        ...
        'django_imbue_tag'
    ]


Basic usage
-----------

Templates that are going to be *imbued* with template fragments must be prepared first. In order to do so we must place
special ``{% slot %}`` tag somewhere in template. The template tag does nothing by itself, its only function is to
designate place in with new template will be injected:

``menu.html``::

    {% load imbue_tag %}

    <div>
        <p>Menu</p>
        <div>
            {% slot %}
        </div>
    </div>

Now we can use above snippet in other template and inject desired content into ``{% slot %}`` place:

``main.html``::

    {% load imbue_tag %}

    {% imbue 'menu.html' %}
        <a href="{% url 'forms' %}">Forms</a>
    {% endimbue %}

The rendered output should look like this::

    <div>
        <p>Menu</p>
        <div>
            <a href="/forms">Forms</a>
        </div>
    </div>

**Note**:
    You are allowed to use **any** Django template syntax inside ``{% imbue %}`` tag.

Context
~~~~~~~

Template *imbued* by ``{% imbue %}`` has its own context separate from the context in with ``{% imbue %}`` is called. If
you want to use any variable form *current* context inside injected template, you must explicitly pass it as a
``{% imbue %}`` parameter:

``main.html``::

    {% load imbue_tag %}

    {% imbue 'menu.html' label=label %}
        <a href="{% url 'forms' %}">{{ label }}</a>
    {% endimbue %}

It is also allowed to pass constant value::

    {% imbue 'menu.html' label='Forms' %}
        ...

**Note**:
    In regard to context ``{% imbue %}`` behaves similarly to ``{% include %}`` and similarly to ``{% include %}`` it
    also automatically passes ``csrf_token``

Multiple slots
~~~~~~~~~~~~~~

You are not limited in number of ``{% slot %}`` that you can have in *imbued* template. Every single one will simply
receive exactly the same template that resides inside ``{% imbue %}`` tag:

``warning.html``::

    {% load imbue_tag %}

    <div>
        <div>{% slot %}</div>
        <p>{{ txt }}</p>
        <div>{% slot %}</div>
    </div>

``main.html``::

    {% load imbue_tag %}

    {% imbue 'menu.html' txt='Dont do that!' %}
        {% for i in txt %}!{% endfor %}
    {% endimbue %}

Above example should result into following HTML::

    <div>
        <div>!!!!!!!!!!!!!</div>
        <p>Dont do that!</p>
        <div>!!!!!!!!!!!!!</div>
    </div>


Named slots
-----------

Repeating single template multiple times may be useful but what if you want to place **different** templates in certain
places of *imbued* template? That's what **named slots** are exactly for:

``article.html``::

    {% load imbue_tag %}

    <div>
        {% slot 'content' %}
    </div>

    <footer>
        <p>Author: {% slot 'author' %}</p>
    </footer>

To use named slot you simply need to add parameter containing its name. Similarly to normal slots its allowed to define
multiple named slots with same name.

Using template with named slots differs from using template with normal slots:

``main.html``::

    {% load imbue_tag %}

    {% imbue 'article.html' %}
        {% template_for_slot 'content' %}
            Hello World!
        {% end_template_for_slot %}

        {% template_for_slot 'author' %}
            Mr. Tom
        {% end_template_for_slot %}
    {% endimbue %}

As you can see ``{% imbue %}`` must be now called in a specific manner:

- content that is meant to be placed in slots must now reside inside ``{% template_for_slot %}`` tag. Each tag has a
  slot name as a parameter that marks its content as template for slot with exactly the same name
- no other content can be placed inside ``{% imbue %}`` when ``{% template_for_slot %}`` tags are used

After rendering we should receive HTML similar to this::

    <div>
        Hello World!
    </div>

    <footer>
        <p>Author: Mr. Tom</p>
    </footer>

**Note**:
    ``{% template_for_slot %}`` can also contain any Django compatible template syntax the same as *pure* ``{% imbue %}``
