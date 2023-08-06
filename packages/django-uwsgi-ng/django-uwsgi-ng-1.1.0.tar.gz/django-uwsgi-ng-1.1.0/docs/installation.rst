Installation
============

django-uwsgi is easy installable via pip:

.. code-block:: sh

   pip install django-uwsgi-ng


or clone it from `EduGit <https://edugit.org/AlekSIS/libs/django-uwsgi-ng>`_:


.. code-block:: sh

   git clone https://edugit.org/AlekSIS/libs/django-uwsgi-ng.git
   cd django-uwsgi-ng
   pip install .

   # or for development
   pip install -e .


By default ``django-uwsgi-ng`` doesn’t installed with uWSGI as requirement.
And here are a few known reasons why:

* Django project installed into virtualenv and running in `Emperor <http://uwsgi-docs.readthedocs.org/en/latest/Emperor.html>`_ mode. In this case uWSGI is installed system-wide or into some other virtualenv.
* Some devs love to use system package managers like apt and prefer to install uwsgi other way.
* you need to build uWSGI with custom profile ex: ``UWSGI_PROFILE=gevent pip install uwsgi``

You can install django-uwsgi with uWSGI by appending [uwsgi] to the install command:

.. code-block:: sh

   pip install django-uwsgi-ng[uwsgi]
