import sys
import json
import time
import types
import base64
import tempfile
import warnings
import logging.handlers
from urllib.parse import urlencode
from unittest import mock, TestCase
from http.cookies import SimpleCookie
from datetime import datetime, timedelta, timezone

import jwt
import cherrypy.lib
from clor import configure
# CherryPy helper uses nose as runner, emulate for standard runner
sys.modules['nose'] = types.ModuleType('nose')  # noqa: E402
from cherrypy.test.helper import CPWebCase  # noqa: E402

from .. import test, controller, model, envconf, server, __version__  # noqa: E402
from ..controller import toolbox  # noqa: E402
from ..controller.auth import (  # noqa: E402
  PasswordAuthenticator, JwtCookieAuthenticator, User, createRuleset
)


def setUpModule():
  test.warntoexc()
  # cherrypy.wsgiserver.wsgiserver3: reported #1331
  warnings.filterwarnings('ignore', 'unclosed <socket.socket', ResourceWarning)
  # should be addressed by cherrypy upgraded
  warnings.filterwarnings('ignore', category = PendingDeprecationWarning)

def tearDownModule():
  warnings.filterwarnings('default', 'unclosed <socket.socket', ResourceWarning)
  warnings.filterwarnings('default', category = PendingDeprecationWarning)


del CPWebCase.test_gc

class TestController(CPWebCase):

  interactive = False

  maxDiff = None

  port = None
  '''The port that the test server is serving on'''


  def setUp(self):
    # Proxy nose's setup
    self.setup_class()

    self.port = self.PORT

  @classmethod
  def setUpServer(cls):
    test.bootstrap()

  @classmethod
  def setup_server(cls):
    cls.setUpServer()

  def tearDown(self):
    # Proxy nose's teardown
    self.teardown_class()

  def assertJsonBody(self, expected, msg = None):
    self.assertEqual(expected, json.loads(self.body.decode()), msg)


class TestRecordApi(TestController):

  def tearDown(self):
    super().tearDown()

    cherrypy.tree.apps['/api/v1/record'].storage._db.cursor().execute('TRUNCATE record')

  def getLogRecordDict(self):
    return {
      'lineno'          : 10,
      'thread'          : 140550102431488,
      'levelno'         : 20,
      'msecs'           : 63.5066032409668,
      'levelname'       : 'INFO',
      'lisfor'          : 'lightfullness',
      'nested'          : [{1: 2}, ('123', '234')],
      'stack_info'      : None,
      'threadName'      : 'MainThread',
      'filename'        : 'log.py',
      'exc_text'        : None,
      'module'          : 'log',
      'relativeCreated' : 11.342048645019531,
      'msg'             : 'Band – %d, %s',
      'processName'     : 'MainProcess',
      'created'         : 1497106862.0635066,
      'funcName'        : 'info',
      'args'            : (8, 'arg2'),
      'asctime'         : '2017-06-10 17:01:02,063',
      'exc_info'        : None,
      'message'         : 'Band – 8, arg2',
      'foo'             : 'bar',
      'process'         : 29799,
      'pathname'        : 'log.py',
      'name'            : 'test'
    }

  def testPostInfoUrlencoded(self):
    body = urlencode(self.getLogRecordDict())
    headers = [
      ('content-type',   'application/x-www-form-urlencoded'),
      ('content-length', str(len(body)))
    ]

    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    bodyPost = json.loads(self.body.decode())

    self.getPage('/api/v1/record/{}'.format(bodyPost['id']))
    self.assertStatus(200)
    self.assertHeader('Cache-Control', 'max-age=2600000')
    bodyGet = json.loads(self.body.decode())
    self.assertEqual(bodyPost, bodyGet)

    self.assertEqual({
      'level'   :  20,
      'ts'      : '2017-06-10 15:01:02.063507+00:00',
      'name'    : 'test',
      'message' : 'Band – 8, arg2',
      'id'      : bodyPost['id'],
      'logrec'  : {
        'meta' : {
          'lineno'          : 10,
          'msecs'           : 63.5066032409668,
          'processName'     : 'MainProcess',
          'relativeCreated' : 11.342048645019531,
          'thread'          : 140550102431488,
          'filename'        : 'log.py',
          'msg'             : 'Band – %d, %s',
          'threadName'      : 'MainThread',
          'args'            : [8, 'arg2'],
          'module'          : 'log',
          'process'         : 29799,
          'funcName'        : 'info',
          'pathname'        : 'log.py',
          'stack_info'      : None
        },
        'data' : {
          'foo'    : 'bar',
          'lisfor' : 'lightfullness',
          'nested' : [{'1': 2}, ['123', '234']],
        }
      }
    }, bodyGet)

  def testPostErrorUrlencoded(self):
    logrec = {
      'lineno'          : '16',
      'thread'          : '140550102431488',
      'levelno'         : '40',
      'msecs'           : '97.8283882141113',
      'levelname'       : 'ERROR',
      'pathname'        : 'log.py',
      'stack_info'      : 'None',
      'threadName'      : 'MainThread',
      'filename'        : 'log.py',
      'module'          : 'log',
      'relativeCreated' : '45.66383361816406',
      'msg'             : 'Failure %s',
      'processName'     : 'MainProcess',
      'created'         : '1497106862.0978284',
      'funcName'        : 'error',
      'args'            : '(123,)',
      'asctime'         : '2017-06-10 17:01:02,097',
      'message'         : 'Failure 123',
      'process'         : '29799',
      'name'            : 'test',
      'exc_text'        :
        'Traceback (most recent call last):\n'
        '  File "log.py", line 72, in <module>\n    1 / 0\n'
        'ZeroDivisionError: division by zero',
      'exc_info' :
        "(<class 'ZeroDivisionError'>, "
        "ZeroDivisionError('division by zero',), <traceback object at 0x7fd45c98b248>)",
    }
    body = urlencode(logrec)
    headers = [
      ('content-type',   'application/x-www-form-urlencoded'),
      ('content-length', str(len(body)))
    ]

    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    bodyPost = json.loads(self.body.decode())

    self.getPage('/api/v1/record/{}'.format(bodyPost['id']))
    self.assertStatus(200)
    bodyGet = json.loads(self.body.decode())
    self.assertEqual(bodyPost, bodyGet)

    self.assertEqual({
      'level'   : 40,
      'name'    : 'test',
      'id'      : bodyGet['id'],
      'message' : 'Failure 123',
      'ts'      : '2017-06-10 15:01:02.097828+00:00',
      'logrec'  : {
        'meta' : {
          'thread'          : 140550102431488,
          'process'         : 29799,
          'processName'     : 'MainProcess',
          'args'            : [123],
          'funcName'        : 'error',
          'lineno'          : 16,
          'filename'        : 'log.py',
          'threadName'      : 'MainThread',
          'msecs'           : 97.8283882141113,
          'module'          : 'log',
          'msg'             : 'Failure %s',
          'relativeCreated' : 45.66383361816406,
          'pathname'        : 'log.py',
          'stack_info'      : None,
        },
        'error' : {
          'exc_text' :
            'Traceback (most recent call last):\n  '
            'File "log.py", line 72, in <module>\n    1 / 0\nZeroDivisionError: division by zero',
          'exc_info' :
            "(<class 'ZeroDivisionError'>, ZeroDivisionError('division by zero',), "
            "<traceback object at 0x7fd45c98b248>)",
        }
      },
    }, bodyGet)

  def testPostUnsupportedMediaType(self):
    body = 'The Lung'
    headers = [
      ('content-type',   'text/plain'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(415)

  def testPostInfoJson(self):
    body = json.dumps(self.getLogRecordDict())
    headers = [
      ('content-type',   'application/json'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    bodyPost = json.loads(self.body.decode())

    self.getPage('/api/v1/record/{}'.format(bodyPost['id']))
    self.assertStatus(200)
    self.assertHeader('Cache-Control', 'max-age=2600000')
    bodyGet = json.loads(self.body.decode())
    self.assertEqual(bodyPost, bodyGet)

    self.assertEqual({
      'level'   :  20,
      'ts'      : '2017-06-10 15:01:02.063507+00:00',
      'name'    : 'test',
      'message' : 'Band – 8, arg2',
      'id'      : bodyPost['id'],
      'logrec'  : {
        'meta' : {
          'lineno'          : 10,
          'msecs'           : 63.5066032409668,
          'processName'     : 'MainProcess',
          'relativeCreated' : 11.342048645019531,
          'thread'          : 140550102431488,
          'filename'        : 'log.py',
          'msg'             : 'Band – %d, %s',
          'threadName'      : 'MainThread',
          'args'            : [8, 'arg2'],
          'module'          : 'log',
          'process'         : 29799,
          'funcName'        : 'info',
          'pathname'        : 'log.py',
          'stack_info'      : None
        },
        'data' : {
          'foo'    : 'bar',
          'lisfor' : 'lightfullness',
          'nested' : [{'1': 2}, ['123', '234']],
        }
      }
    }, bodyGet)

  def testPostInfoJsonNameMessageTrim(self):
    recordDict = self.getLogRecordDict()
    recordDict['name'] = 'n' * 256
    recordDict['message'] = 'm' * 256

    body = json.dumps(recordDict)
    headers = [
      ('content-type',   'application/json'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    bodyPost = json.loads(self.body.decode())
    self.assertEqual(recordDict['name'][:127], bodyPost['name'])
    self.assertEqual(recordDict['message'][:255], bodyPost['message'])

    self.getPage('/api/v1/record/{}'.format(bodyPost['id']))
    self.assertStatus(200)
    bodyGet = json.loads(self.body.decode())
    self.assertEqual(recordDict['name'][:127], bodyGet['name'])
    self.assertEqual(recordDict['message'][:255], bodyGet['message'])

  def testPostInfoJsonTooLong(self):
    cursor = cherrypy.tree.apps['/api/v1/record'].storage._db.cursor()
    cursor.execute("SHOW VARIABLES LIKE 'max_allowed_packet'")
    origMaxPacket = cursor.fetchone()['Value']
    cursor.execute('SET GLOBAL max_allowed_packet=16384')
    self.addCleanup(cursor.execute, 'SET GLOBAL max_allowed_packet={}'.format(origMaxPacket))

    recordDict = self.getLogRecordDict()
    for i in range(500):
      recordDict[str(i)] = ['■ 注意事項']

    body = json.dumps(recordDict)
    headers = [
      ('content-type',   'application/json'),
      ('content-length', str(len(body)))
    ]
    with self.assertLogs('cherrypy.error', 'ERROR'):
      self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(413)
    bodyPost = json.loads(self.body.decode())
    self.assertEqual({
      'error': {
        'message': (
          "(1301, 'Result of json_binary::serialize() was larger than "
          "max_allowed_packet (16384) - truncated')"
        ),
        'type': 'StorageSizeLimitError',
      }
    }, bodyPost)

  def testPostRawJson(self):
    body = json.dumps({'a': 1, 'b': [2], 'c': '3'})
    headers = [
      ('content-type',   'application/json'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record?raw=1', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    bodyPost = json.loads(self.body.decode())

    self.getPage('/api/v1/record/{}'.format(bodyPost['id']))
    self.assertStatus(200)
    self.assertHeader('Cache-Control', 'max-age=2600000')
    bodyGet = json.loads(self.body.decode())
    self.assertEqual(bodyPost, bodyGet)

    self.assertEqual({
      'level'   :  20,
      'ts'      : bodyPost['ts'],
      'name'    : '',
      'message' : '',
      'id'      : bodyPost['id'],
      'logrec'  : {'a': 1, 'b': [2], 'c': '3'},
    }, bodyGet)

  def testPostIncompleteLogRecord(self):
    body = json.dumps({})
    headers = [
      ('content-type',   'application/json'),
      ('content-length', str(len(body)))
    ]
    with self.assertLogs('cherrypy.error', 'ERROR'):
      self.getPage('/api/v1/record?raw=0', method = 'POST', body = body, headers = headers)
    self.assertStatus(400)
    actual = json.loads(self.body.decode())
    self.assertEqual(
      {'error': {'message': 'Key "name" is missing', 'type': 'ModelError'}}, actual)

  def testPostInfoMultilineJson(self):
    logdict = self.getLogRecordDict()
    del logdict['args'], logdict['nested']

    logdicts = [logdict] * 2
    body = '\n'.join(map(json.dumps, logdicts))
    headers = [
      ('content-type',   'application/x-ndjson'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    actual = json.loads(self.body.decode())
    self.assertEqual(2, len(actual))

    for i, id in enumerate(actual):
      self.getPage('/api/v1/record/{}'.format(id))
      actual = model.Record(**json.loads(self.body.decode()))
      actual.ts = controller.parse8601(actual.ts.replace(' ', 'T').replace('+00:00', 'Z'))
      expected = model.createRecord(logdicts[i].copy())
      expected.id = id
      self.assertEqual(dict(expected.asdict()), dict(actual.asdict()))

  def testPostInfoMultilineMalformedJson(self):
    logdict = self.getLogRecordDict()
    logdicts = [logdict] * 2
    body = '\n'.join(map(json.dumps, logdicts)) + '\n!@#'
    headers = [
      ('content-type',   'application/x-ndjson'),
      ('content-length', str(len(body)))
    ]
    with self.assertLogs('chronologer.controller', 'ERROR'):
      self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(400)
    actual = json.loads(self.body.decode())
    self.assertEqual(
      {'error': {'type': 'HTTPError', 'message': 'Invalid JSON document on line 3'}}, actual)

    self.getPage('/api/v1/record', method = 'HEAD')
    self.assertStatus(200)
    self.assertEqual(0, int(dict(self.headers)['X-Record-Count']))

  def testPostInfoMultilineMultistatusJson(self):
    logdict = self.getLogRecordDict()
    chunkSize = cherrypy.config['ingestion']['chunk_size']
    logdicts = [logdict] * chunkSize
    body = '\n'.join(map(json.dumps, logdicts)) + '\n!@#'
    headers = [
      ('content-type',   'application/x-ndjson'),
      ('content-length', str(len(body)))
    ]
    with self.assertLogs('chronologer.controller', 'ERROR'):
      self.getPage('/api/v1/record', method = 'POST', body = body, headers = headers)
    self.assertStatus(207)
    actual = json.loads(self.body.decode())
    self.assertEqual(
      {'multistatus': [
        {
          'status' : 201,
          'body'   : list(range(1, chunkSize + 1))},
        {
          'status' : 400,
          'body'   : {
            'error': {
              'message' : 'Invalid JSON document on line {}'.format(chunkSize + 1),
              'type'    : 'ValueError'
            }
          }
        },
      ]}, actual)

    self.getPage('/api/v1/record', method = 'HEAD')
    self.assertStatus(200)
    self.assertEqual(chunkSize, int(dict(self.headers)['X-Record-Count']))

  def testPostRawMultilineJson(self):
    logdict = self.getLogRecordDict()
    del logdict['args'], logdict['nested']

    logdicts = [logdict] * 2
    body = '\n'.join(map(json.dumps, logdicts))
    headers = [
      ('content-type',   'application/x-ndjson'),
      ('content-length', str(len(body)))
    ]
    self.getPage('/api/v1/record?raw=1', method = 'POST', body = body, headers = headers)
    self.assertStatus(201)
    actual = json.loads(self.body.decode())
    self.assertEqual(2, len(actual))

    for i, id in enumerate(actual):
      self.getPage('/api/v1/record/{}'.format(id))
      self.assertEqual(logdicts[i], json.loads(self.body.decode())['logrec'])

  def testHttpHandler(self):
    logger = logging.getLogger('{}.testHttpHandler'.format(__name__))
    logger.propagate = False
    logger.level = logging.INFO
    logger.addHandler(logging.handlers.HTTPHandler(
      host   = 'localhost:{}'.format(self.port),
      url    = '/api/v1/record',
      method = 'POST'
    ))

    now = datetime.now(timezone.utc).replace(microsecond = 0)

    logger.info('Test', extra = {'lisfor': 'lighty'})

    self.getPage('/api/v1/record', method = 'HEAD')
    self.assertStatus(200)
    self.assertEqual(1, int(dict(self.headers)['X-Record-Count']))
    self.assertHeader('Cache-Control', 'no-cache')

    try:
      1 / 0
    except Exception:
      logger.exception('Failure', extra = {'lisfor': 'twiggy'})

    self.getPage('/api/v1/record', method = 'HEAD')
    self.assertStatus(200)
    self.assertEqual(2, int(dict(self.headers)['X-Record-Count']))

    self.getPage('/api/v1/record?level=30&name=chronologer', method = 'HEAD')
    self.assertStatus(200)
    self.assertEqual(1, int(dict(self.headers)['X-Record-Count']))

    self.getPage('/api/v1/record?left=0&right=1')
    self.assertStatus(200)
    actual = json.loads(self.body.decode())

    for item in actual:
      self.assertAlmostEqual(
        now,
        datetime.strptime(
          item.pop('ts').rsplit('+', 1)[0], '%Y-%m-%d %H:%M:%S.%f').replace(tzinfo = timezone.utc),
        delta = timedelta(seconds = 2))

      list(map(
        item['logrec']['meta'].pop, ('lineno', 'msecs', 'process', 'relativeCreated', 'thread')))

      self.assertTrue(
        item['logrec']['meta'].pop('pathname').endswith('chronologer/test/controller.py'))

    expected = [{
      'name'    : 'chronologer.test.controller.testHttpHandler',
      'id'      : 2,
      'level'   : logging.ERROR,
      'message' : 'Failure',
      'logrec'  : {
        'data': {'lisfor': 'twiggy'},
        'meta': {
          'args': [],
          'filename': 'controller.py',
          'funcName': 'testHttpHandler',
          'module': 'controller',
          'msg': 'Failure',
          'processName': 'MainProcess',
          'stack_info': None,
          'threadName': 'MainThread'
        }
      },
    }, {
      'name'    : 'chronologer.test.controller.testHttpHandler',
      'id'      : 1,
      'level'   : logging.INFO,
      'message' : 'Test',
      'logrec'  : {
        'data': {'lisfor': 'lighty'},
        'meta': {
          'args': [],
          'filename': 'controller.py',
          'funcName': 'testHttpHandler',
          'module': 'controller',
          'msg': 'Test',
          'processName': 'MainProcess',
          'stack_info': None,
          'threadName': 'MainThread'
        }
      },
    }]
    self.assertEqual(expected, actual)

    params = {
      'left'   : 0,
      'right'  : 0,
      'after'  : (now.replace(tzinfo = None) - timedelta(seconds = 5)).isoformat() + 'Z',
      'before' : (now.replace(tzinfo = None) + timedelta(seconds = 5)).isoformat() + 'Z',
      'name'   : 'chronologer',
      'level'  : logging.ERROR,
      'query'  : "logrec->>'$.data.lisfor' = 'twiggy'",
    }
    self.getPage('/api/v1/record?' + urlencode(params))
    self.assertStatus(200)
    self.assertHeader('Cache-Control', 'no-cache')
    actual = json.loads(self.body.decode())
    self.assertAlmostEqual(
      now,
      datetime
        .strptime(actual[0].pop('ts').rsplit('+', 1)[0], '%Y-%m-%d %H:%M:%S.%f')
        .replace(tzinfo = timezone.utc),
      delta = timedelta(seconds = 2))
    list(map(
      actual[0]['logrec']['meta'].pop,
      ('lineno', 'msecs', 'process', 'relativeCreated', 'thread')))
    self.assertTrue(
      actual[0]['logrec']['meta'].pop('pathname').endswith('chronologer/test/controller.py'))
    self.assertEqual(expected[:1], actual)

  def testCountHistorgram(self):
    logger = logging.getLogger('{}.testCountHistorgram'.format(__name__))
    logger.propagate = False
    logger.level = logging.INFO
    logger.addHandler(logging.handlers.HTTPHandler(
      host   = 'localhost:{}'.format(self.port),
      url    = '/api/v1/record',
      method = 'POST'
    ))

    now = datetime(2017, 6, 17, 23, 14, 37, tzinfo = timezone.utc)
    for i in range(4):
      with mock.patch('time.time', lambda: (now - timedelta(hours = i)).timestamp()):
        logger.info('Test', extra = {'i': i})

    qs = urlencode({'group': 'hour', 'timezone': 'Europe/Amsterdam'})
    self.getPage('/api/v1/record?' + qs, method = 'HEAD')
    self.assertStatus(200)
    self.assertHeader('X-Record-Count', '1,1,1,1')
    self.assertHeader('X-Record-Group', ','.join([
      '1497729600', '1497733200', '1497736800', '1497740400']))

    qs = urlencode({'group': 'day', 'timezone': 'Europe/Amsterdam'})
    self.getPage('/api/v1/record?' + qs, method = 'HEAD')
    self.assertStatus(200)
    self.assertHeader('X-Record-Count', '2,2')
    self.assertHeader('X-Record-Group', ','.join(['1497650400', '1497736800']))

    qs = urlencode({'group': 'hour', 'timezone': 'Europe/Amsterdam', 'level': logging.ERROR})
    self.getPage('/api/v1/record?' + qs, method = 'HEAD')
    self.assertStatus(200)
    self.assertHeader('X-Record-Count', '')
    self.assertHeader('X-Record-Group', '')

  def testRecordCountError(self):
    with self.assertLogs('cherrypy.error', 'ERROR') as ctx:
      self.getPage('/api/v1/record?' + urlencode({'query': '123#'}), method = 'HEAD')
    self.assertStatus(400)
    self.assertBody(b'')
    self.assertHeader('X-Error-Type', 'StorageQueryError')
    self.assertHeader('X-Error-Message', 'Make sure the query filter is a valid WHERE expression')
    self.assertHeader('Content-Type', 'text/html')

    self.assertEqual(1, len(ctx.output))
    self.assertTrue(ctx.output[0].endswith(
      'chronologer.storage.StorageQueryError: '
      'Make sure the query filter is a valid WHERE expression'))

    params = {'after': '2019--14 18:49:-- Z'}
    with self.assertLogs('cherrypy.error', 'ERROR') as ctx:
      self.getPage('/api/v1/record?' + urlencode(params), method = 'HEAD')
    self.assertStatus(400)
    self.assertBody(b'')
    self.assertHeader('X-Error-Type', 'ValueError')
    self.assertHeader('X-Error-Message', "time data '{}' is not supported".format(params['after']))
    self.assertHeader('Content-Type', 'text/html')

  def testRecordRangeError(self):
    with self.assertLogs('cherrypy.error', 'ERROR') as ctx:
      self.getPage('/api/v1/record?' + urlencode({'query': '123#', 'left': 0, 'right': 127}))
    self.assertStatus(400)
    self.assertHeader('Content-Type', 'application/json')
    self.assertEqual({'error': {
      'message' : 'Make sure the query filter is a valid WHERE expression',
      'type'    : 'StorageQueryError'
    }}, json.loads(self.body.decode()))

    self.assertEqual(1, len(ctx.output))
    self.assertTrue(ctx.output[0].endswith(
      'chronologer.storage.StorageQueryError: '
      'Make sure the query filter is a valid WHERE expression'))

  def testRecordNotFound(self):
    self.getPage('/api/v1/record/-1')
    self.assertStatus(404)
    self.assertHeader('Content-Type', 'application/json')
    self.assertEqual({'error': {
      'message' : 'Nothing matches the given URI',
      'type'    : 'HTTPError'
    }}, json.loads(self.body.decode()))


class TestRecordApiAuthorisation(TestController):

  authHeaders = None


  def setUp(self):
    super().setUp()

    credpair = '{}:{}'.format(
      cherrypy.config['auth']['username'], cherrypy.config['auth']['password']
    ).encode()
    credentials = base64.b64encode(credpair).decode()
    self.authHeaders = [('Authorization', 'Basic {}'.format(credentials))]

    m = mock.patch.object(controller.RecordApi, '_cp_config', {
      'chronotools.authenticate.on'            : True,
      'chronotools.authenticate.basic_realm'   : 'Test',
      'chronotools.authenticate.basic_handler' : PasswordAuthenticator(cherrypy.config['auth']),
      'chronotools.authorise.on'               : True,
      'chronotools.authorise.rulsetfactory'    : createRuleset,
    }, create = True)
    m.start()
    self.addCleanup(m.stop)

  def testHead(self):
    with mock.patch.dict(cherrypy.config['auth'], {'roles': []}):
      self.getPage('/api/v1/record', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(403)
      self.getPage('/api/v1/record?query=1', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['writer']}):
      self.getPage('/api/v1/record', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(403)
      self.getPage('/api/v1/record?query=1', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader']}):
      self.getPage('/api/v1/record', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(200)
      self.getPage('/api/v1/record?query=1', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader', 'query-reader']}):
      self.getPage('/api/v1/record', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(200)
      self.getPage('/api/v1/record?query=1', method = 'HEAD', headers = self.authHeaders.copy())
      self.assertStatus(200)

  def testGet(self):
    with mock.patch.dict(cherrypy.config['auth'], {'roles': []}):
      self.getPage('/api/v1/record/1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(403)
      self.getPage('/api/v1/record/1?query=1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['writer']}):
      self.getPage('/api/v1/record/1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(403)
      self.getPage('/api/v1/record/1?query=1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader']}):
      self.getPage('/api/v1/record/1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(404)
      self.getPage('/api/v1/record/1?query=1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader', 'query-reader']}):
      self.getPage('/api/v1/record/1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(404)
      self.getPage('/api/v1/record/1?query=1', method = 'GET', headers = self.authHeaders.copy())
      self.assertStatus(404)

  def testPost(self):
    with mock.patch.dict(cherrypy.config['auth'], {'roles': []}):
      self.getPage('/api/v1/record', method = 'POST', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['writer']}):
      with self.assertLogs('cherrypy.error', 'ERROR'):
        self.getPage('/api/v1/record', method = 'POST', headers = self.authHeaders.copy())
      self.assertStatus(400)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader']}):
      self.getPage('/api/v1/record', method = 'POST', headers = self.authHeaders.copy())
      self.assertStatus(403)

    with mock.patch.dict(cherrypy.config['auth'], {'roles': ['basic-reader', 'query-reader']}):
      self.getPage('/api/v1/record', method = 'POST', headers = self.authHeaders.copy())
      self.assertStatus(403)


class TestRecordApiCompression(TestController):

  def setUp(self):
    super().setUp()

    m = mock.patch.object(controller.RecordApi, '_cp_config', {
      'tools.gzip.on'                 : True,
      'tools.gzip.mime_types'         : ['application/json', 'application/javascript'],
      'chronotools.brotli.on'         : True,
      'chronotools.brotli.mime_types' : ['application/json', 'application/javascript'],
    }, create = True)
    m.start()
    self.addCleanup(m.stop)

  def testIdentity(self):
    headerList = [
      {},
      {'Accept-Encoding': 'identity'},
      {'Accept-Encoding': 'identity, gzip'},
      {'Accept-Encoding': 'identity, br'},
      {'Accept-Encoding': 'identity, gzip, br'},
    ]
    for requestHeaders in headerList:
      self.getPage('/api/v1/record/1', headers = list(requestHeaders.items()))
      self.assertStatus(404)
      self.assertEqual(
        {'error': {'message': 'Nothing matches the given URI', 'type': 'HTTPError'}},
        json.loads(self.body.decode()))

      responseHeaders = dict(self.headers)
      self.assertNotIn('Content-Encoding', responseHeaders)
      self.assertEqual(513, int(responseHeaders['Content-Length']))
      self.assertEqual('Accept-Encoding', responseHeaders['Vary'])
      self.assertEqual('application/json', responseHeaders['Content-Type'])

  def testGzip(self):
    self.getPage('/api/v1/record/1', headers = [('Accept-Encoding', 'gzip')])
    self.assertStatus(404)
    self.assertEqual(
        {'error': {'message': 'Nothing matches the given URI', 'type': 'HTTPError'}},
        json.loads(cherrypy.lib.encoding.decompress(self.body).decode()))

    responseHeaders = dict(self.headers)
    self.assertEqual(93, int(responseHeaders['Content-Length']))
    self.assertEqual('gzip', responseHeaders['Content-Encoding'])
    self.assertEqual('Accept-Encoding', responseHeaders['Vary'])
    self.assertEqual('application/json', responseHeaders['Content-Type'])

  def testBrotli(self):
    import brotli

    headerList = [{'Accept-Encoding': 'br'}, {'Accept-Encoding': 'gzip, br'}]
    for requestHeaders in headerList:
      self.getPage('/api/v1/record/1', headers = list(requestHeaders.items()))
      self.assertStatus(404)
      self.assertEqual(
          {'error': {'message': 'Nothing matches the given URI', 'type': 'HTTPError'}},
          json.loads(brotli.decompress(self.body).decode()))

      responseHeaders = dict(self.headers)
      self.assertTrue(74 <= int(responseHeaders['Content-Length']) <= 79)
      self.assertEqual('br', responseHeaders['Content-Encoding'])
      self.assertEqual('Accept-Encoding', responseHeaders['Vary'])
      self.assertEqual('application/json', responseHeaders['Content-Type'])


class TestRecordPurgePlugin(TestCase):

  setUpClass = test.bootstrap

  def testNoRetentionDays(self):
    self.assertIsNone(cherrypy.config['retention']['days'])
    testee = controller.RecordPurgePlugin(cherrypy.engine, mock.Mock())
    testee.start()
    try:
      self.assertIsNone(testee.thread)
    finally:
      testee.stop()

  def testRetentionDaysDefined(self):
    cherrypy.config['retention']['days'] = 1
    storage = mock.Mock()
    testee = controller.RecordPurgePlugin(cherrypy.engine, storage)
    nextRun = testee._schedule.next_run
    testee.frequency = 0.1
    with mock.patch('schedule.datetime') as m:
      m.datetime.now.return_value = nextRun + timedelta(seconds = 1)
      testee.start()
      try:
        time.sleep(0.11)
        storage.purge.assert_called_once_with(timedelta(days = 1))
        self.assertIsNotNone(testee.thread)
      finally:
        testee.stop()


class TestPasswordAuthenticator(TestCase):

  def testUserdict(self):
    userdict = {'username': 'tosin', 'password': 'totanh', 'roles': ['guitar', 'manufacturer']}
    testee = PasswordAuthenticator(userdict)

    result, roles = testee.verify('tosin', 'tocos')
    self.assertFalse(result)
    self.assertIsNone(roles)

    result, roles = testee.verify('tosin', 'totanh')
    self.assertTrue(result)
    self.assertEqual(roles, userdict['roles'])

  def testAuthfileFilename(self):
    userdata = [
      {
        'username': 'david',
        'pbkdf2': 'f1d19a11d3d6d4694907d1538a20bff5a3e4e1057b5bc9a0c3acdb082140e165',
        'hashname': 'sha256',
        'salt': 'salty caramel',
        'iterations': 1024,
        'roles': ['writer']
      }, {
        'username': 'danny',
        'pbkdf2': 'dbe40d2f05026ea82c37e2c05125c6ad56fad460',
        'hashname': 'sha1',
        'salt': 'pepper',
        'iterations': 1,
        'roles': ['basic-reader', 'query-reader']
      }
    ]
    userdict = {'username': 'tosin', 'password': 'totanh', 'roles': ['guitar', 'manufacturer']}
    with tempfile.NamedTemporaryFile('w') as f:
      f.write(json.dumps(userdata))
      f.flush()
      testee = PasswordAuthenticator(userdict = userdict, authfile = f.name)

    result, roles = testee.verify('tosin', 'tocos')
    self.assertFalse(result)
    self.assertIsNone(roles)

    result, roles = testee.verify('david', '123')
    self.assertFalse(result)
    self.assertIsNone(roles)

    # "userdict" is not used when "authfile" is provided
    result, roles = testee.verify('tosin', 'totanh')
    self.assertFalse(result)
    self.assertIsNone(roles)

    result, roles = testee.verify('david', 'bodenos8')
    self.assertTrue(result)
    self.assertEqual(roles, userdata[0]['roles'])

    result, roles = testee.verify('danny', '6.5/8')
    self.assertTrue(result)
    self.assertEqual(roles, userdata[1]['roles'])

  def testAuthfileList(self):
    userdata = [
      {
        'username': 'david',
        'pbkdf2': 'f1d19a11d3d6d4694907d1538a20bff5a3e4e1057b5bc9a0c3acdb082140e165',
        'hashname': 'sha256',
        'salt': 'salty caramel',
        'iterations': 1024,
        'roles': ['writer']
      }, {
        'username': 'danny',
        'pbkdf2': 'dbe40d2f05026ea82c37e2c05125c6ad56fad460',
        'hashname': 'sha1',
        'salt': 'pepper',
        'iterations': 1,
        'roles': ['basic-reader', 'query-reader']
      }
    ]
    userdict = {'username': 'tosin', 'password': 'totanh', 'roles': ['guitar', 'manufacturer']}
    testee = PasswordAuthenticator(userdict = userdict, authfile = userdata)

    result, roles = testee.verify('tosin', 'tocos')
    self.assertFalse(result)
    self.assertIsNone(roles)

    result, roles = testee.verify('david', '123')
    self.assertFalse(result)
    self.assertIsNone(roles)

    # "userdict" is not used when "authfile" is provided
    result, roles = testee.verify('tosin', 'totanh')
    self.assertFalse(result)
    self.assertIsNone(roles)

    result, roles = testee.verify('david', 'bodenos8')
    self.assertTrue(result)
    self.assertEqual(roles, userdata[0]['roles'])

    result, roles = testee.verify('danny', '6.5/8')
    self.assertTrue(result)
    self.assertEqual(roles, userdata[1]['roles'])

  def testAuthfileInvalid(self):
    with self.assertRaises(ValueError) as ctx:
      PasswordAuthenticator(authfile = {'a': 'b'})
    self.assertEqual(
      'authfile has to be either filename or list of dictionaries', str(ctx.exception))

  def testNoAuthSource(self):
    with self.assertRaises(ValueError):
      PasswordAuthenticator()


class TestJwtCookieAuthenticator(TestCase):

  testee = None


  def setUp(self):
    self.testee = JwtCookieAuthenticator('secret very secret')

  def testHasCookie(self):
    cookies = SimpleCookie()

    cookies['foo'] = 'foo'
    self.assertFalse(self.testee.hasCookie(cookies))

    cookies[self.testee.cookieName] = 'bar'
    self.assertTrue(self.testee.hasCookie(cookies))

  def testCreateJwtMorsel(self):
    user = User('xavier', ['rhythm', 'signaturee'])
    morsel = self.testee.createJwtMorsel(user, secret = self.testee._secret)
    self.assertTrue(morsel['httponly'])
    self.assertEqual('/', morsel['path'])
    self.assertEqual('strict', morsel['samesite'])

    payload = jwt.decode(morsel.value, self.testee._secret, algorithms = ['HS256'])
    self.assertAlmostEqual(time.time(), payload['iat'], delta = 2)  # iat is int
    self.assertEqual(user.username, payload['username'])
    self.assertEqual(user.roles, payload['roles'])

  def testVerify(self):
    user = User('xavier', ['rhythm', 'signaturee'])
    morsel = self.testee.createJwtMorsel(user, self.testee._secret)

    cookies = SimpleCookie()
    cookies[morsel.key] = morsel
    username, roles = self.testee.verify(cookies)
    self.assertEqual(user.username,  username)
    self.assertEqual(user.roles, roles)

    cookies = SimpleCookie()
    username, roles = self.testee.verify(cookies)
    self.assertIsNone(username)
    self.assertIsNone(roles)

    cookies = SimpleCookie()
    cookies[morsel.key] = 'foobar'
    username, roles = self.testee.verify(cookies)
    self.assertIsNone(username)
    self.assertIsNone(roles)


class TestServerBootstrap(TestCase):

  def testMissingSecret(self):
    config = configure(*getattr(envconf, 'test_suite'))
    config['auth']['secret'] = ''
    with self.assertRaises(ValueError) as ctx:
      server.bootstrap(config)
    self.assertEqual(
      'UI authentication requires CHRONOLOGER_SECRET to be defined', str(ctx.exception)
    )


class TestAuthenticateTool(TestCase):

  def testNoHandlerForbidden(self):
    with self.assertRaises(cherrypy.HTTPError) as ctx:
      toolbox.authenticateTool()
    self.assertEqual(403, ctx.exception.code)

  def testBasicHandlerMissingArguments(self):
    with self.assertRaises(ValueError) as ctx:
      toolbox.authenticateBasic(handler = None, realm = None, negotiate = None)
    self.assertEqual('Realm is required for basic authentication', str(ctx.exception))

    with self.assertRaises(ValueError) as ctx:
      toolbox.authenticateBasic(handler = None, realm = 'Project "borderland"', negotiate = None)
    self.assertEqual('Realm cannot contain quotes', str(ctx.exception))


class TestProductionEnv(TestController):

  passwordHandler = None


  @classmethod
  def setUpServer(cls):
    cls.passwordHandler = PasswordAuthenticator(
      {'username': 'jo', 'password': 'burns', 'roles': ['basic-reader']})

    test.bootstrap(extraConfig = {
      'authenticator' : {
        **envconf.production[1]['authenticator'],
        'password' : cls.passwordHandler,
      },
      'app' : envconf.production[1]['app']
    })

  def getBasicAuthnHeaderList(self, username, password):
    credentials = base64.b64encode('{}:{}'.format(username, password).encode()).decode()
    return [('Authorization', 'Basic {}'.format(credentials))]

  def testApiBasicAuthFixed(self):
    userdict = {'username': 'bob', 'password': 'obb', 'roles': ['basic-reader']}
    with mock.patch.object(self.passwordHandler, '_userdict', userdict):
      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('bob', 'foo'))
      self.assertStatus(403)

      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('bob', 'obb'))
      self.assertStatus(200)

  def testApiBasicAuthFile(self):
    authfile = {r['username']: r for r in [
      {
        'username': 'bob',
        'pbkdf2': 'f57ef1e3e8f90cb367dedd44091f251b5b15c9c36ddd7923731fa7ee41cbaa82',
        'hashname': 'sha256',
        'salt': 'c0139cff',
        'iterations': 32,
        'roles': ['basic-reader']
      }, {
        'username': 'obo',
        'pbkdf2': (
          'ff680a9237549f698da5345119dec1ed314eb4fdefe59837d0724d747c3169'
          '089ae45215ec98b7c84b7b8b3ac1589139'),
        'hashname': 'sha384',
        'salt': '9230dbdd5a13f009',
        'iterations': 4096,
        'roles': ['basic-reader']
      },
    ]}
    with mock.patch.object(self.passwordHandler, '_authfile', authfile):
      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('alice', ''))
      self.assertStatus(403)

      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('bob', ''))
      self.assertStatus(403)

      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('bob', 'obo'))
      self.assertStatus(200)

      self.getPage(
        '/api/v1/record', method = 'HEAD', headers = self.getBasicAuthnHeaderList('obo', 'bob'))
      self.assertStatus(200)

  def testApiNoNegotation(self):
      self.getPage('/api/v1/record')
      self.assertStatus(403)

  def testRootRedirect(self):
    self.getPage('/')
    self.assertStatus(303)

    expectedUrl = 'http://127.0.0.1:{}/ui/authn'.format(self.port)
    self.assertHeader('Location', expectedUrl)
    self.assertEqual(
      'This resource can be found at <a href="{0}">{0}</a>.'.format(expectedUrl),
      self.body.decode())

  def testUiTrailingSlashRedirect(self):
    self.getPage('/ui/authn', headers = self.getBasicAuthnHeaderList('jo', 'burns'))
    self.assertStatus(303)

    self.getPage('/ui', headers = self.cookies)
    self.assertStatus(301)

    expectedUrl = 'http://127.0.0.1:{}/ui/'.format(self.port)
    self.assertHeader('Location', expectedUrl)
    self.assertEqual(
      'This resource has permanently moved to <a href="{0}">{0}</a>.'.format(expectedUrl),
      self.body.decode())

  def testUiAuthn(self):
    self.getPage('/ui/authn')
    self.assertStatus(401)
    self.assertJsonBody({
      'error': {'message': 'You are not authorised to access that resource', 'type': 'HTTPError'}})

    self.getPage('/ui/authn', headers = self.getBasicAuthnHeaderList('jo', 'burns'))
    self.assertStatus(303)

    expectedUrl = 'http://127.0.0.1:{}/ui/'.format(self.port)
    self.assertHeader('Location', expectedUrl)
    self.assertEqual(
      'This resource can be found at <a href="{0}">{0}</a>.'.format(expectedUrl),
      self.body.decode())

    cookies = SimpleCookie(self.cookies[0][1])
    morsel = cookies['Jwt']
    self.assertTrue(morsel['httponly'])
    self.assertEqual('/', morsel['path'])
    self.assertEqual('strict', morsel['samesite'])

    payload = jwt.decode(morsel.value, cherrypy.config['auth']['secret'], algorithms = ['HS256'])
    self.assertAlmostEqual(time.time(), payload['iat'], delta = 1)
    self.assertEqual(self.passwordHandler._userdict['username'], payload['username'])
    self.assertEqual(self.passwordHandler._userdict['roles'], payload['roles'])

    self.getPage(expectedUrl, headers = self.cookies)
    self.assertStatus(200)

  def testUiAuthnForbiddenRedirect(self):
    self.getPage('/ui/', headers = [('Cookie', 'Jwt=EtudeNo12; Path=/')])
    self.assertStatus(303)

    self.assertHeader('Location', 'http://127.0.0.1:{}/ui/authn'.format(self.port))
    self.assertHeader('Content-Type', 'application/json')
    self.assertJsonBody({
      'error': {
        'message' : 'Request forbidden -- authorization will not help',
        'type'    : 'HTTPError'
      }
    })

  def testUiAuthnStatus(self):
    self.getPage('/ui/authn', headers = self.getBasicAuthnHeaderList('jo', 'burns'))
    self.assertStatus(303)

    self.getPage('/ui/authn', method = 'HEAD', headers = self.cookies)
    self.assertStatus(200)
    self.assertHeader('X-Username', self.passwordHandler._userdict['username'])
    self.assertHeader('X-Version', __version__)

  def testUiAuthnSignout(self):
    self.getPage('/ui/authn', headers = self.getBasicAuthnHeaderList('jo', 'burns'))
    self.assertStatus(303)
    self.getPage('/ui/authn', method = 'DELETE', headers = self.cookies)
    self.assertStatus(401)

  def testHealthCkeck(self):
    self.getPage('/health')
    self.assertStatus(200)
    self.assertBody(b'OK')

