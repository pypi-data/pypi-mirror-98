feincms-button
==============

Displaying a Bootstrap 3 Button_ in text.

This button can be used for navigation, for example at the end of a text block. These buttons can't be used in forms.

Authored by `Basil Shubin <https://github.com/bashu>`_, and some great `contributors <https://github.com/bashu/feincms-button/contributors>`_.

.. image:: https://img.shields.io/pypi/v/feincms-button.svg
    :target: https://pypi.python.org/pypi/feincms-button/

.. image:: https://img.shields.io/pypi/dm/feincms-button.svg
    :target: https://pypi.python.org/pypi/feincms-button/

.. image:: https://img.shields.io/github/license/bashu/feincms-button.svg
    :target: https://pypi.python.org/pypi/feincms-button/

Installation
------------

First make sure the project is configured for feincms_.

Then add the following settings:

.. code-block:: python

    INSTALLED_APPS += (
        'feincms_button',
    )

Now, you can create ``ButtonContent`` content type:

.. code-block:: python

    from feincms.module.page.models import Page
    from feincms_button.contents import ButtonContent

    Page.create_content_type(ButtonContent)


Frontend styling
----------------

The button is rendered with the HTML that Bootstrap prescribes:

.. code-block:: html+django

    <a class="btn btn-default" href="#" role="button">Link</a>

The standard Bootstrap 3 CSS will provide a reasonable styling for this, which can either be overwritten, or replaced in your own CSS files.
The defaults provided by Bootstap 3 is: https://github.com/twbs/bootstrap-sass/blob/master/assets/stylesheets/bootstrap/_buttons.scss

When you use Sass, you can also override the Sass variables.


Configuration
-------------

When desired, the following settings can be overwritten:

.. code-block:: python

    from django.utils.translation import pgettext_lazy

    FEINCMS_BUTTON_STYLES = (
        ('btn-default', pgettext_lazy("button-style", u"Default")),
        ('btn-primary', pgettext_lazy("button-style", u"Primary")),
        ('btn-success', pgettext_lazy("button-style", u"Success")),
        ('btn-info', pgettext_lazy("button-style", u"Info")),
        ('btn-warning', pgettext_lazy("button-style", u"Warning")),
        ('btn-danger', pgettext_lazy("button-style", u"Danger")),
        ('btn-link', pgettext_lazy("button-style", u"Link")),
    )

    FEINCMS_BUTTON_SIZES = (
        ('', pgettext_lazy("button-size", u"Default")),
        ('btn-lg', pgettext_lazy("button-size", u"Large")),
        ('btn-sm', pgettext_lazy("button-size", u"Small")),
        ('btn-xs', pgettext_lazy("button-size", u"Extra Small")),
    )

By default, the standard Bootstrap button classes are used.
These can be redefined when the project uses other classes for the buttons.

Contributing
------------

If you like this module, forked it, or would like to improve it, please let us know!
Pull requests are welcome too. :-)

.. _feincms: https://github.com/feincms/feincms
.. _Button: http://getbootstrap.com/css/#buttons
