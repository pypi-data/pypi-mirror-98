=======================================
django-ok-language-tools |PyPI version|
=======================================

|Upload Python Package| |Code Health| |Python Versions| |PyPI downloads| |license| |Project Status|

Some language tools for Django.

Installation
============

Install with pip:

.. code:: shell

    $ pip install django-ok-language-tools

Update INSTALLED_APPS:

.. code:: python

    INSTALLED_APPS = [
        ...
        'ok_language_tools',
        ...
    ]


Available settings
==================

``LANGUAGE_TOOLS_REDIRECT_TO_QUERY_PARAMETER`` - Query parameter to get next url for '`set_language`' view.

``LANGUAGE_TOOLS_LANGUAGE_QUERY_PARAMETER`` - Query parameter to get languge to translate next url for '`set_language`' view.

``LANGUAGE_TOOLS_REDIRECT_EXCLUDE_PREFIXES`` - Tuple of prefixes to skip redirect for '`language_redirect_middleware`'.

For example:

.. code:: python

    LANGUAGE_TOOLS_REDIRECT_EXCLUDE_PREFIXES = (
        '/api/v1/',
        '/uploads/',
        '/static/',
    )


``LANGUAGE_TOOLS_DEFAULT_REDIRECT_LANGUAGE`` - Language code to redirect for a first user visit.

``LANGUAGE_TOOLS_VISITED_SESSION_KEY`` - Key to store visited state in session.


Quickstart
==========

- Add '`language_redirect_middleware`' to the MIDDLEWARE configuration to redirect users to default language during a first visit:

.. code:: python

    MIDDLEWARE = [
        ...
        'ok_language_tools.middleware.language_redirect_middleware'
    ]


- To enable '`set_language`' view, add next URL patterns: 

.. code:: python

    urlpatterns = [
        ...
        path('', include('ok_language_tools.urls')),
    ]
    
    language_url = reverse('ok-language-tools:set-language')
    catalog_url = '/catalog/'
    language = 'uk'
    set_language_url = f'{language_url}?redirect_to={catalog_url}&language={language}'
    
    # or using HTTP_REFERER
    set_language_url = f'{language_url}?language={language}'
	

.. |PyPI version| image:: https://badge.fury.io/py/django-ok-language-tools.svg
   :target: https://badge.fury.io/py/django-ok-language-tools
.. |Upload Python Package| image:: https://github.com/LowerDeez/ok-language-tools/workflows/Upload%20Python%20Package/badge.svg
   :target: https://github.com/LowerDeez/ok-language-tools/
   :alt: Build status
.. |Code Health| image:: https://api.codacy.com/project/badge/Grade/e5078569e40d428283d17efa0ebf9d19
   :target: https://www.codacy.com/app/LowerDeez/ok-language-tools
   :alt: Code health
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/django-ok-language-tools.svg
   :target: https://pypi.org/project/django-ok-language-tools/
   :alt: Python versions
.. |license| image:: https://img.shields.io/pypi/l/django-ok-language-tools.svg
   :alt: Software license
   :target: https://github.com/LowerDeez/ok-language-tools/blob/master/LICENSE
.. |PyPI downloads| image:: https://img.shields.io/pypi/dm/django-ok-language-tools.svg
   :alt: PyPI downloads
.. |Project Status| image:: https://img.shields.io/pypi/status/django-ok-language-tools.svg
   :target: https://pypi.org/project/django-ok-language-tools/  
   :alt: Project Status
