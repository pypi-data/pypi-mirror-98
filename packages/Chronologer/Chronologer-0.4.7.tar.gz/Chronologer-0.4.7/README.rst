.. image:: https://badge.fury.io/py/Chronologer.svg
   :target: https://pypi.org/project/Chronologer/
.. image:: https://img.shields.io/docker/image-size/saaj/chronologer
   :target: https://hub.docker.com/r/saaj/chronologer/

===========
Chronologer
===========

.. figure:: https://heptapod.host/saajns/chronologer/raw/f01c4c2e/source/resource/clui/image/logo/logo-alt240.png
   :alt: Chronologer

Chronologer is a counterpart of Python stdlib's logging ``HTTPHandler`` [1]_ and more.
It provides RESTful API for accepting Python logging HTTP POST requests and optional
UI for browsing and searching the logs. The idea is the same as for database backends
of logging software, like ``rsyslog-mysql`` [2]_.

UI features are described in the `frontend`_ branch and released as
``ChronologerUI`` [17]_ package.

.. contents::

Scope
=====
Chronologer is meant for small- and medium-sized logging workloads and audit logging.
Practically it's limited by its backend's write throughput and capacity. In case of
MySQL backend vertical scaling can suffice many types of applications.

Especially it's useful for microservice architecture where file logging is no longer
practical.

Installation
============
Chronologer is available as a Python package [3]_ and as a Docker image [4]_ (includes UI).
The former can be installed like ``pip install chronologer[server,mysql,ui]``. The latter
can be used like in the following ``docker-compose.yml`` for deployment with MySQL database.

.. sourcecode:: yaml

    version: '2.4'
    services:
      web:
        image: saaj/chronologer
        environment:
          CHRONOLOGER_STORAGE_DSN: mysql://chronologer:pass@mysql/chronologer
          CHRONOLOGER_SECRET: some_long_random_string
          CHRONOLOGER_USERNAME: logger
          CHRONOLOGER_PASSWORD: another_long_random_string
        depends_on:
          mysql:
            condition: service_healthy
        ports:
          - 8080:8080

      mysql:
        image: mysql:5.7
        environment:
          MYSQL_DATABASE: chronologer
          MYSQL_USER: chronologer
          MYSQL_PASSWORD: pass
          MYSQL_ROOT_PASSWORD: pass
        healthcheck:
          test: mysqladmin ping --protocol=tcp --password=pass --silent
          interval: 5s
          retries: 4

It can be run like the following. The second line applies database migrations.

.. sourcecode:: bash

    docker-compose up -d
    docker-compose run --rm web python -m chronologer -e production migrate

To open the UI navigate to ``http://localhost:8080/``.

Chronologer's configuration can be fine-tuned with several environment variables
defined in ``envconf`` [5]_. Default ``envconf`` can be overridden completely, see
``python -m chronologer --help``.

For examples of scaling the application server with ``docker-compose`` see
``perftest/stack`` directory [22]_. There are examples for Nginx and Traefik.

Quickstart
==========
Having Chronologer server running as described above, client logging configuration
may look like the following. It requires ``chronologer`` package installed on the
client as well (i.e. ``pip install chronologer``).

.. sourcecode:: python

    import logging.config


    config = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'http' : {
          'class'        : 'chronologer.client.QueueProxyHandler',
          'queue'        : {'()': 'queue.Queue', 'maxsize': 10 ** 4},
          'target'       : 'ext://chronologer.client.BatchJsonHandler',
          'prefix'       : 'appname',
          'capacity'     : 128,
          'host'         : 'chronologer_host:8080',
          'url'          : '/api/v1/record',
          'credentials'  : ('logger', 'another_long_random_string'),
          'flushLevel'   : 'ERROR',
          'flushTimeout' : 30,
        },
      },
      'root' : {
        'handlers' : ['http'],
        'level'    : 'INFO'
      }
    }
    logging.config.dictConfig(config)

The ``http`` handler buffers records for efficiency. It flushes its buffer to
the server when one of the following occurs:

* the buffer, of 128 records, has been filled,
* a logging record with ``level`` ``ERROR`` or above has been logged,
* while logging a record there's a record in the buffer created earlier
  then 30 seconds ago.

``chronologer.client`` itself doesn't have dependencies but Python standard library.
For working only with standard library ``logging.handlers.HTTPHandler`` read below.

Path of the logging handler
===========================
This section starts with ``logging.handlers.HTTPHandler`` and explains why
``chronologer.client`` builds on it and beyond. The naive imperative logging
configuration looks like:

.. sourcecode:: python

    import logging.handlers

    chrono = logging.handlers.HTTPHandler(
      'localhost:8080', '/api/v1/record', 'POST', credentials = ('logger', ''))
    handlers = [logging.StreamHandler(), chrono]
    logging.basicConfig(level = logging.DEBUG, handlers = handlers)

The same can be expressed declaratively:

.. sourcecode:: python

    import logging.config

    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'logging.handlers.HTTPHandler',
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

This configuration is called naive because the handler is blocking. It may
work in trivial cases but generally it's discouraged because the network is
not reliable [6]_. Instead Python provides logging queueing in stdlib [7]_:

    Along with ``QueueHandler`` class, ``QueueListener`` is used to let
    handlers do their work on a separate thread. This is important for web and
    other applications where threads serving clients need to respond as
    quickly as possible, while any potentially slow, and especially
    complementary operations are done in background.

Here follows imperative configuration with memory queueing.

.. sourcecode:: python

    chrono = logging.handlers.HTTPHandler(
      'localhost:8080', '/api/v1/record', 'POST', credentials = ('logger', ''))
    q = queue.Queue(maxsize = 4096)
    qh = logging.handlers.QueueHandler(q)
    ql = logging.handlers.QueueListener(q, chrono)
    ql.start()
    handlers = [logging.StreamHandler(),  qh]
    logging.basicConfig(level = logging.DEBUG, handlers = handlers)

    # somewhere on shutdown
    ql.stop()

Because the queue listener's shutdown procedure is inconvenient this way and it's
hard to express declaratively, ``QueueProxyHandler`` is suggested.

.. sourcecode:: python

    import logging.handlers
    import logging.config


    class QueueProxyHandler(logging.handlers.QueueHandler):
      '''Queue handler which creates its own ``QueueListener`` to
      proxy log records via provided ``queue`` to ``target`` handler.'''

      _listener = None
      '''Queue listener'''


      def __init__(self, queue, target = logging.handlers.HTTPHandler, **kwargs):
        # user-supplied factory is not converted by default
        if isinstance(queue, logging.config.ConvertingDict):
          queue = queue.configurator.configure_custom(queue)

        super().__init__(queue)
        self._listener = logging.handlers.QueueListener(queue, target(**kwargs))
        self._listener.start()

      def close(self):
        super().close()
        self._listener.stop()

    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'somemodule.QueueProxyHandler',
          'queue'       : {'()': 'queue.Queue', 'maxsize': 4096},
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

.. warning::
   Always set reasonable ``maxsize`` for the underlying queue to avoid
   unbound memory growth. ``logging.handlers.QueueHandler`` uses
   non-blocking ``put_nowait`` to enqueue records and in case the queue
   is full, it raises and the exception is handled by
   ``logging.Handler.handleError``. Alternatively a file-based queue, for
   instance, ``pqueue`` [8]_, can used to allow more capacity in
   memory-restricted environments.

Client
======
For convenience reasons, the above is available as
``chronologer.client.QueueProxyHandler``.

In addition it has logger name prefixing and suffixing capability, and some
edge case resilience. ``prefix`` is passed to ``QueueProxyHandler`` on creation.
It allows many applications logging into the same Chronologer instance to have
separate logger namespaces (e.g. including ``aiohttp`` logging whose namespace
is fixed). ``suffix`` is an extra attribute of ``LogRecord`` which allows to
fine-tune the logger namespace for easier search of the records.

.. sourcecode:: python

    import logging.config


    conf = {
      'version'                  : 1,
      'disable_existing_loggers' : False,
      'handlers'                 : {
        'console' : {
          'class' : 'logging.StreamHandler',
        },
        'http' : {
          'class'       : 'chronologer.client.QueueProxyHandler',
          'queue'       : {'()': 'queue.Queue', 'maxsize': 4096},
          'prefix'      : 'appname',
          'host'        : 'localhost:8080',
          'url'         : '/api/v1/record',
          'method'      : 'POST',
          'credentials' : ('logger', ''),
          'secure'      : False
        },
      },
      'root' : {
        'handlers' : ['console', 'http'],
        'level'    : 'DEBUG'
      }
    }
    logging.config.dictConfig(conf)

    logging.getLogger('some').info(
      'Chronologer!', extra = {'suffix': 'important.transfer'})

The ``LogRecord`` corresponding to the last line will have ``name`` equal to
``'appname.some.important.transfer'``. If ``name`` is modified the original is
saved as ``origname``.

But this is unfortunately not it. Looking at ``logging.handlers.HTTPHandler``
carefully we can see a few flaws, including but not limited to:

* it doesn't validate response codes, say ``403 Forbidden``, and will silently
  ignore the error, i.e. not calling ``logging.Handler.handleError``, will
  leads to data loss,
* it doesn't support request retries,
* it doesn't support buffering to improve throughput,
* it doesn't support other serialisation formats but
  ``application/x-www-form-urlencoded``.

``chronologer.client.BatchJsonHandler`` tries to address these issues, see
`Quickstart`_.

JSON input support
==================
Besides ``application/x-www-form-urlencoded`` of  ``HTTPHandler`` Chronologer
supports ``application/json`` of the same structure. It also supports
``application/x-ndjson`` [19]_ for bulk ingestion.

JSON of arbitrary structure can be ingested in the *raw mode*. In the mode
Chronologer will not classify input into logging ``meta``, ``data`` and
``error`` and will not insist on presence of Python ``logging``-specific keys.
For example, a file containing newline separated JSON entries can be sent to
Chronologer like:

.. sourcecode:: bash

  curl -H "content-type: application/x-ndjson" --user logger: \
    --data-binary @/path/to/some/file.ndjson localhost:8080/api/v1/record?raw=1

Record retention
================
When ``CHRONOLOGER_RETENTION_DAYS`` is set, daily, around midnight a background
thread will purge records older than given number of days.

Authentication
==============
Chronologer does not provide (neither intends to) a user management. The intent
is to delegate authentication. The credentials and roles used by the server can
be provided by the following environment variables:

* ``CHRONOLOGER_USERNAME``
* ``CHRONOLOGER_PASSWORD``
* ``CHRONOLOGER_ROLES`` ­– space separated role list (see below)

Alternatively a JSON file located by ``CHRONOLOGER_AUTHFILE`` of the following
structure can be used to authenticate multiple users:

.. sourcecode:: json

    [
      {
        "username": "bob",
        "pbkdf2": "f57ef1e3e8f90cb367dedd44091f251b5b15c9c36ddd7923731fa7ee41cbaa82",
        "hashname": "sha256",
        "salt": "c0139cff",
        "iterations": 32,
        "roles": ["writer"]
      }, {
        "username": "obo",
        "pbkdf2": "ff680a9237549f698da5345119dec1ed314eb4fdefe59837d0724d747c3169089ae45...",
        "hashname": "sha384",
        "salt": "9230dbdd5a13f009",
        "iterations": 4096,
        "roles": ["basic-reader", "query-reader"]
      }
    ]

The value of ``pbkdf2`` and keys ``hashname``, ``salt``, ``iterations`` correspond to
Python ``hashlib.pbkdf2_hmac`` [21]_.

.. warning::
   Note that the auth-scheme is ``Basic`` which means that the password hash is calculated
   per request. Thus ``iterations`` should be a low value (especially for writing
   users). To compensate that it is possible to choose passwords with enough entropy.

Authorisation
=============
Chronologer defines the following roles:

* ``basic-reader`` allows ``HEAD`` and ``GET`` to ``/api/v1/record``
* ``query-reader`` in combination with ``basic-reader`` allows the use
  ``query``, SQL expression, to (further) filter the records
* ``writer`` allows ``POST`` to ``/api/v1/record``

The UI (in case ``chronologerui`` is installed) is available to every
authenticated user.

API
===
By default Chronologer listens port 8080 and is protected by HTTP Basic
Authentication, username "logger" without password (see environment
variables to override these).

Chronologer provides *Record* resource.

Create record
-------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``POST``
------------------------ -----------------------------------------------
Request content-type     ``application/x-www-form-urlencoded``,
                         ``application/json``, ``application/x-ndjson``
------------------------ -----------------------------------------------
Request body             Representation of ``logging.LogRecord``
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            Representation of created ``model.Record``,
                         except for ``application/x-ndjson`` input
                         where only a list of insert record identifiers
                         is returned
------------------------ -----------------------------------------------
Successful response code ``201 Created``
======================== ===============================================

Optional *raw* mode, accepting arbitrary JSON documents, is supported by
passing ``raw=1`` into the query string.

``application/x-ndjson`` request body can produce ``207 Multi-Status``
response when a successful chunk is followed by a failed chunk,
say that contained malformed a JSON line. Multi-status body looks like:

.. sourcecode:: json

  {
    "multistatus": [
      {"status": 201, "body": [1, 2, "..."]},
      {"status": 400, "body": "Invalid JSON document on line 2012"},
    ]
  }

Retrieve record count
---------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``HEAD``
------------------------ -----------------------------------------------
Query string             Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response headers         * ``X-Record-Count: 42``
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record timeline
------------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``HEAD``
------------------------ -----------------------------------------------
Query string             Required fields:

                         * ``group`` – "day" or "hour"
                         * ``timezone`` – ``pytz``-compatible one

                         Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response headers         * ``X-Record-Count: 90,236``
                         * ``X-Record-Group: 1360450800,1360537200``
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record range
---------------------
======================== ===============================================
URL                      ``/api/v1/record``
------------------------ -----------------------------------------------
Method                   ``GET``
------------------------ -----------------------------------------------
Query string             Required fields:

                         * ``left`` – left offset in the result set
                         * ``right`` – right offset in the result set

                         Optional filtering fields (see details below):

                         * ``after`` – ISO8601 timestamp
                         * ``before`` – ISO8601 timestamp
                         * ``level`` – integer logging level
                         * ``name`` – logging record prefix(es)
                         * ``query`` – storage-specific expression
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            .. sourcecode:: json

                           [
                             {
                               "name": "some.module",
                               "ts": "2018-05-10 16:36:53.377493+00:00",
                               "message": "Et quoniam eadem...",
                               "id": 177260,
                               "level": 20
                             },
                             "..."
                           ]
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Retrieve record
---------------
======================== ===============================================
URL                      ``/api/v1/record/{id}``
------------------------ -----------------------------------------------
Method                   ``GET``
------------------------ -----------------------------------------------
Response content-type    ``application/json``
------------------------ -----------------------------------------------
Response body            .. sourcecode:: json

                           {
                             "name": "some.module",
                             "logrec": {
                               "data": {
                                 "foo": 387
                               },
                               "meta": {
                                 "process": 29406,
                                 "module": "some.module",
                                 "relativeCreated": 103.23762893676758,
                                 "msecs": 376.4379024505615,
                                 "pathname": "logtest.py",
                                 "msg": "Et quoniam eadem...",
                                 "stack_info": null,
                                 "processName": "MainProcess",
                                 "filename": "logtest.py",
                                 "thread": 140312867051264,
                                 "threadName": "MainThread",
                                 "lineno": 20,
                                 "funcName": "main",
                                 "args": null
                               }
                             },
                             "id": 177260,
                             "level": 20,
                             "message": "Et quoniam eadem...",
                             "ts": "2018-05-10 16:36:53.377493+00:00"
                           }

                         ``logrec`` has two nested dictionaries.
                         ``data`` has what was passed to ``extra`` [16]_
                         and ``meta`` has internal fields of
                         ``logging.LogRecord``.
------------------------ -----------------------------------------------
Successful response code ``200 OK``
======================== ===============================================

Error representation
--------------------
Errors for HTTP method requests that allow a response body are represented like:

.. sourcecode:: json

  {
    "error" : {
      "type"    : "HTTPError",
      "message" : "Nothing matches the given URI"
    }
  }

Errors for HTTP method requests that don't allow a response body are represented in the headers:

* ``X-Error-Type: StorageQueryError``
* ``X-Error-Message: Make sure the query filter is a valid WHERE expression``

Response encoding
-----------------
Chronologer supports Gzip and Brotli response body encoding. The latter takes precedence because
it provides significant improvement for verbose logging records.

.. note::
   Modern browsers don't advertise, via ``Accept-Encoding``, Brotli support on non-HTTPS
   connections (due to broken intermediary software concerns). In Firefox it can be forced
   by appending ``br`` to ``network.http.accept-encoding`` in ``about:config``.

Filtering
=========
Filter fields have the following semantics:

* ``after`` – ISO8601 timestamp.
  The predicate is true for a record which was created after given timestamp.
* ``before`` – ISO8601 timestamp.
  The predicate is true for a record which was created before given timestamp.
* ``level`` – integer logging level.
  The predicate is true for a record whose severity level is greater or equal to given level.
* ``name`` – logging record prefix. Optionally can be a comma-separated list of prefixes.
  The predicate is true for a record whose logger name starts with any of given prefixes.
* ``query`` – storage-specific expression.
  Requires the user to have ``query-reader`` role. See JSON path description below.

.. warning::
   Each user who has access to Chronologer with ``query-reader`` role (default user
   does not have it) effectively has full access to its database, because ``query``
   expressions are put into the SQL queries directly as there's no intent to
   abstract native database search features.

MySQL
=====
Chronologer relies on a compressed InnoDB table which provides good compromise
between reliability, data modelling, search features, performance and size of
logged data. The data of logging records are written into ``logrec`` JSON
field (see the initial migration [9]_ and examples above).

It is a good idea to have dedicated MySQL instance for Chronologer. Then, for
instance, it is possible to fine-tune MySQL's ACID guarantees, namely
``innodb_flush_log_at_trx_commit = 0`` allow MySQL to write 1-second batches
[10]_. Disabling performance schema [11]_ by setting ``performance_schema = 0``
is also recommended, because it has significant overhead. Basic InnoDB settings
should be reasonably configured:

* ``innodb_buffer_pool_size`` [12]_
* ``innodb_log_buffer_size`` [13]_
* ``innodb_log_file_size`` [14]_

JSON path query
---------------
``query`` passes a storage-specific expression. Particularly, it's useful
to write post-filtering conditions for ``logrec`` JSON field using
JSONPath expressions and ``->`` operator [15]_. It may look like the following,
though arbitrary ``WHERE`` clause expressions are possible.

* ``"logrec->'$.data.foo' = 387 AND logrec->'$.meta.lineno' = 20"``
* ``"logrec->'$.meta.threadName' != 'MainThread'"``

Note that connection to MySQL works in ``ANSI_QUOTES`` mode [18]_, so ``"``
cannot be used to form string literals. ``'`` must be used instead.

Compression tuning
------------------
Initial migration [9]_ sets ``KEY_BLOCK_SIZE = 4``. It may be sub-optimal for
the shape of your log records. MySQL provides guidelines for choosing
``KEY_BLOCK_SIZE`` [23]_ and monitoring "compression failures"
at runtime [24]_.

If you want to change ``KEY_BLOCK_SIZE`` for ``record`` table, you can provide
your own database migration. Chronologer uses yoyo-migrations [25]_ for
database migrations. For example, to switch to ``KEY_BLOCK_SIZE = 8``
migration file, named ``20190803T1404_key_size.py``, will look like:

.. sourcecode:: python

    from yoyo import step

    step('ALTER TABLE record KEY_BLOCK_SIZE = 8')

It can be mounted into the migration directory of Chonologer's container
in your ``docker-compose.yml`` like:

.. sourcecode:: yaml

    volumes:
      - ./20190803T1404_key_size.py:/opt/chronologer/chronologer/migration/mysql/20190803T1404_key_size.py

Then re-apply migrations with ``migrate`` or run ``serve`` with ``-m`` command
line flag.

Size limit
----------
Chronologer's MySQL schema has the following size limits.

* logger name – 127 characters
* text message – 255 characters

The structured part of a log record, ``logrec`` column, as a JSON column in
general, has a limit.

    It is important to keep in mind that the size of any JSON document stored
    in a JSON column is limited to the value of the ``max_allowed_packet``
    system variable.

Also note that if a query with a JSON value fits ``max_allowed_packet`` bytes,
it doesn't necessary mean the JSON value fits ``max_allowed_packet`` bytes
in its MySQL serialised representation [26]_.

SQLite
======
SQLite is supported for very simple, one-off or evaluation cases. Also it doesn't
support compression. ``JSON1`` extension [20]_ is required for JSON Path queries.

* ``"json_extract(logrec, '$.data.foo') = 387 AND json_extract(logrec, '$.meta.lineno') = 20"``
* ``"json_extract(logrec, '$.meta.threadName') = 'MainThread'"``

A one-off Chronologer container with SQLite storage can be run on port 8080 like::

  docker run --rm -it -p 8080:8080 -v /tmp/db \
    -e CHRONOLOGER_STORAGE_DSN=sqlite:////tmp/db/chrono.sqlite \
    -e CHRONOLOGER_SECRET=some_long_random_string \
    saaj/chronologer \
    python3.7 -m chronologer -e production serve -u www-data -g www-data -m

Two things to note:

1. ``-m`` to ``serve`` runs migrations before starting the server,
2. SQLite needs permissions to the directory where a database file
   resides, to write its temporary files.

R&D roadmap
===========
See the `roadmap`_ issue.

Credits
=======
Logo is contributed by `lightypaints`_.

____

.. _frontend: https://heptapod.host/saajns/chronologer/tree/branch/frontend
.. _roadmap: https://heptapod.host/saajns/chronologer/issues/1
.. _lightypaints: https://www.behance.net/lightypaints
.. [1]  https://docs.python.org/3/library/logging.handlers.html#httphandler
.. [2]  https://packages.debian.org/sid/rsyslog-mysql
.. [3]  https://pypi.org/project/Chronologer/
.. [4]  https://hub.docker.com/r/saaj/chronologer/
.. [5]  https://heptapod.host/saajns/chronologer/blob/branch/backend/chronologer/envconf.py
.. [6]  https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing
.. [7]  https://docs.python.org/3/library/logging.handlers.html#queuelistener
.. [8]  https://pypi.org/project/pqueue/
.. [9]  https://heptapod.host/saajns/chronologer/blob/bc862715/chronologer/migration/mysql/20171026T1428_initial.py
.. [10] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_flush_log_at_trx_commit
.. [11] https://dev.mysql.com/doc/refman/5.7/en/performance-schema.html
.. [12] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_buffer_pool_size
.. [13] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_log_buffer_size
.. [14] https://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_log_file_size
.. [15] https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#operator_json-column-path
.. [16] https://docs.python.org/3/library/logging.html#logging.debug
.. [17] https://pypi.org/project/ChronologerUI/
.. [18] https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html#sqlmode_ansi_quotes
.. [19] https://github.com/ndjson/ndjson-spec
.. [20] https://www.sqlite.org/json1.html
.. [21] https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac
.. [22] https://heptapod.host/saajns/chronologer/tree/branch/backend/perftest
.. [23] https://dev.mysql.com/doc/refman/5.7/en/innodb-compression-tuning.html
.. [24] https://dev.mysql.com/doc/refman/5.7/en/innodb-compression-tuning-monitoring.html
.. [25] https://pypi.python.org/pypi/yoyo-migrations
.. [26] https://dev.mysql.com/doc/refman/5.7/en/storage-requirements.html#data-types-storage-reqs-json
