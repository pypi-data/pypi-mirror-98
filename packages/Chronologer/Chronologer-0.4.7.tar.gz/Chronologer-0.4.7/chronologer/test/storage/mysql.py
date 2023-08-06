import decimal
import logging
import unittest
from unittest import mock
from urllib.parse import urlparse
from datetime import datetime, timezone, timedelta

import cherrypy

from .. import bootstrap, warntoexc
from ...storage import mysql, StorageQueryError, StorageSizeLimitError
from ...model import Record, createRecord


def setUpModule():
  warntoexc()
  bootstrap()


class TestMysqlStorage(unittest.TestCase):

  all = {
    'level' : logging.DEBUG,
    'date'  : (None, None),
    'name'  : None,
    'query' : None
  }


  def setUp(self):
    cursor = cherrypy.tree.apps['/api/v1/record'].storage._db.cursor()
    cursor.execute("SHOW VARIABLES LIKE 'max_allowed_packet'")
    origMaxPacket = cursor.fetchone()['Value']
    cursor.execute('SET GLOBAL max_allowed_packet=16384')
    self.addCleanup(cursor.execute, 'SET GLOBAL max_allowed_packet={}'.format(origMaxPacket))

    self.testee = mysql.Storage(urlparse(cherrypy.config['storage']['dsn']))

    self.testee._db.cursor().execute('BEGIN')

  def tearDown(self):
    self.testee._db.cursor().execute('ROLLBACK')

  def testRecord(self):
    self.assertEqual(0, self.testee.count(self.all))

    now = datetime.now(timezone.utc)
    expected = Record(
      'some.test', now, logging.INFO, 'The Realm of Shades', {'foo': [{'bar': -1}]})
    actual = self.testee.record([expected])[0]
    self.assertEqual(expected, actual)

    self.assertEqual(1, self.testee.count(self.all))

    actualRangeItem = self.testee.range(0, 0, self.all)[0]
    self.assertGreater(actualRangeItem.id, 0)
    self.assertEqual('some.test', actualRangeItem.name)
    self.assertEqual(logging.INFO, actualRangeItem.level)
    self.assertEqual('The Realm of Shades', actualRangeItem.message)
    self.assertEqual(now, actualRangeItem.ts)

    actualItem = self.testee.get(actualRangeItem.id)
    self.assertEqual(actualRangeItem.id, actualItem.id)
    self.assertEqual('some.test', actualItem.name)
    self.assertEqual(logging.INFO, actualItem.level)
    self.assertEqual(now, actualItem.ts)
    self.assertEqual('The Realm of Shades', actualItem.message)
    self.assertEqual({'foo': [{'bar': -1}]}, actualItem.logrec)

  def testRecordMicroseconds(self):
    now = datetime.now(timezone.utc).replace(microsecond = 123456)
    expected = Record(
      'some.test', now, logging.INFO, 'The Realm of Shades', {'foo': [{'bar': -1}]})
    actual = self.testee.record([expected])[0]
    self.assertEqual(expected, actual)

    actual = self.testee.get(actual.id)
    self.assertEqual(expected, actual)

  def testRecordMultiple(self):
    now = datetime.now(timezone.utc).replace(microsecond = 0)
    records = self.testee.record([
      Record(
        'mutli.test{}'.format(i), now - timedelta(days = i), logging.WARN,
        'Hardcore Will Never Die, But You Will', {'track': 'Rano Pano'})
      for i in range(5)])

    for r in records:
      self.assertEqual(r, self.testee.get(r.id))

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

  def testRecordTooLongName(self):
    record = Record('', datetime.now(timezone.utc), logging.INFO, 'Message', {})
    record.name = 'a' * 128

    with self.assertRaises(StorageSizeLimitError) as ctx:
      self.testee.record([record])

    expected = '(1406, "Data too long for column \'name\' at row 1")'
    self.assertEqual(expected, str(ctx.exception))

  def testRecordTooLongMessage(self):
    record = Record('some.logger', datetime.now(timezone.utc), logging.INFO, '', {})
    record.message = 'a' * 256

    with self.assertRaises(StorageSizeLimitError) as ctx:
      self.testee.record([record])

    expected = '(1406, "Data too long for column \'message\' at row 1")'
    self.assertEqual(expected, str(ctx.exception))

  def testRecordTooLongPacket(self):
    recordDict = self.getLogRecordDict()
    for i in range(1000):
      recordDict[str(i)] = ['Note']
    record = createRecord(recordDict)

    with self.assertRaises(StorageSizeLimitError) as ctx:
      self.testee.record([record])

    expected = '(1153, "Got a packet bigger than \'max_allowed_packet\' bytes")'
    self.assertEqual(expected, str(ctx.exception))

  def testRecordTooLongMysqlSerialisedJson(self):
    recordDict = self.getLogRecordDict()
    for i in range(500):
      recordDict[str(i)] = ['■ 注意事項']
    record = createRecord(recordDict)

    with self.assertRaises(StorageSizeLimitError) as ctx:
      self.testee.record([record])

    expected = (
      "(1301, 'Result of json_binary::serialize() was larger than "
      "max_allowed_packet (16384) - truncated')"
    )
    self.assertEqual(expected, str(ctx.exception))

  def testGet(self):
    now = datetime.now(timezone.utc).replace(microsecond = 0)
    rec = {
      'int': 26,
      'float': 0.1,
      'decimal': decimal.Decimal('0.1'),
      'list': list(range(4)),
      'dict': dict(zip(range(4), range(3, -1, -1))),
      'none': None,
      'object': object()
    }
    id = self.testee.record([Record('some.test', now, logging.INFO, '', rec)])[0].id

    actual = self.testee.get(id).logrec
    self.assertEqual(26, actual['int'])
    self.assertEqual(0.1, actual['float'])
    self.assertEqual('0.1', actual['decimal'])
    self.assertEqual([0, 1, 2, 3], actual['list'])
    self.assertEqual({'0': 3, '1': 2, '2': 1, '3': 0}, actual['dict'])
    self.assertEqual(None, actual['none'])
    self.assertTrue(actual['object'].startswith('<object object at'))

  def testCount(self):
    self.assertEqual(0, self.testee.count(self.all))

    now = datetime.now(timezone.utc).replace(microsecond = 0)
    self.testee.record([
      Record(
        'some.test', now, logging.INFO, 'The Realm of Shades', {'key': [{'a': 1}, {'b': 2}]}),
      Record(
        'something.test', now, logging.WARN, 'The Realm of Shades', {'key': [{'a': 1}]})
    ])

    self.assertEqual(2, self.testee.count(self.all))

    self.assertEqual(0, self.testee.count(dict(self.all, level = logging.ERROR)))
    self.assertEqual(1, self.testee.count(dict(self.all, level = logging.WARN)))
    self.assertEqual(2, self.testee.count(dict(self.all, level = logging.INFO)))

    self.assertEqual(0, self.testee.count(dict(
      self.all, date = (now - timedelta(seconds = 10), now - timedelta(seconds = 5)))))
    self.assertEqual(0, self.testee.count(dict(
      self.all, level = logging.INFO,
      date = (now - timedelta(seconds = 10), now - timedelta(seconds = 5)))))
    self.assertEqual(2, self.testee.count(dict(
      self.all, level = logging.INFO,
      date = (now - timedelta(seconds = 10), now + timedelta(seconds = 5)))))

    self.assertEqual(0, self.testee.count(dict(self.all, name = 'foo')))
    self.assertEqual(1, self.testee.count(dict(self.all, name = 'some.')))
    self.assertEqual(1, self.testee.count(dict(self.all, name = 'something')))
    self.assertEqual(2, self.testee.count(dict(self.all, name = 'some, something')))
    self.assertEqual(2, self.testee.count(dict(self.all, name = 'so')))

    self.assertEqual(2, self.testee.count(dict(self.all, query = "logrec->'$.key[0].a' = 1")))
    self.assertEqual(1, self.testee.count(dict(self.all, query = "logrec->'$.key[1].b' = 2")))

    self.assertEqual(1, self.testee.count(dict(
      self.all,
      query = "logrec->>'$.key[1].b' = 2",
      level = logging.INFO,
      date = (now - timedelta(seconds = 10), now + timedelta(seconds = 5))
    )))

  def testCountQuerySyntaxError(self):
    with self.assertRaises(StorageQueryError):
      self.testee.count(dict(self.all, query = 'logrec->$#!'))

    now = datetime.now(timezone.utc).replace(microsecond = 0)
    rec = Record(
      'some.test', now, logging.INFO, 'The Realm of Shades', {'key': [{'a': 1}, {'b': 2}]})
    self.testee.record([rec])

    with self.assertRaises(StorageQueryError):
      self.testee.count(dict(self.all, query = "logrec->'$#123' = '3e7a'"))

  def testCountNonQuerySyntaxError(self):
    with mock.patch.object(self.testee, '_isSqlSyntaxError', lambda ex: False):
      with self.assertRaises(mysql.connections.ProgrammingError):
        self.testee.count(dict(self.all, query = 'logrec->$#!'))

  def testCountHistogram(self):
    now = datetime(2017, 6, 17, 23, 14, 37, tzinfo = timezone.utc)

    self.testee.record([Record(
      'something.test', now + timedelta(minutes = i * 5, microseconds = i * 50),
      logging.WARN, 'Fela the Congueror', {'a': 1}) for i in range(16)])

    actual = self.testee.count(self.all, group = True)
    self.assertEqual((
      (datetime(2017, 6, 17, 23, 0,  tzinfo = timezone.utc), 1),
      (datetime(2017, 6, 17, 23, 15, tzinfo = timezone.utc), 3),
      (datetime(2017, 6, 17, 23, 30, tzinfo = timezone.utc), 3),
      (datetime(2017, 6, 17, 23, 45, tzinfo = timezone.utc), 3),
      (datetime(2017, 6, 18, 0,  0,  tzinfo = timezone.utc), 3),
      (datetime(2017, 6, 18, 0,  15, tzinfo = timezone.utc), 3),
    ), actual)

    actual = self.testee.count(
      dict(self.all, date = (now + timedelta(minutes = 59), None), query = "logrec->>'$.a' = 1"),
      group = True)
    self.assertEqual((
      (datetime(2017, 6, 18, 0, 0,  tzinfo = timezone.utc), 1),
      (datetime(2017, 6, 18, 0, 15, tzinfo = timezone.utc), 3),
    ), actual)

  def testRange(self):
    now = datetime.now(timezone.utc).replace(microsecond = 0)
    self.testee.record([
      Record(
        'some.test', now, logging.INFO, 'The Realm of Shades', {'key': [{'a': 1}, {'b': 2}]}
      ),
      Record(
        'something.test',
        now + timedelta(seconds = 1),
        logging.WARN,
        'The Realm of Shades',
        {'key': [{'a': 1}]},
      ),
    ])

    actual = tuple(r.asdict() for r in self.testee.range(0, 1, self.all))
    self.assertEqual(2, len(actual))
    self.assertGreater(actual[0]['id'], actual[1]['id'])
    [r.pop('id') for r in actual]
    self.assertEqual((
      {
        'level': 30, 'name': 'something.test', 'ts': now + timedelta(seconds = 1),
        'message': 'The Realm of Shades', 'logrec': {'key': [{'a': 1}]}},
      {
        'level': 20, 'name': 'some.test', 'ts': now,
        'message': 'The Realm of Shades', 'logrec': {'key': [{'a': 1}, {'b': 2}]}}
    ), actual)

    actual = self.testee.range(0, 0, self.all)
    self.assertEqual(1, len(actual))
    self.assertEqual('something.test', actual[0].name)

    actual = self.testee.range(1, 1, self.all)
    self.assertEqual(1, len(actual))
    self.assertEqual('some.test', actual[0].name)

    actual = self.testee.range(1, 0, self.all)
    self.assertEqual([], actual)

    actual = self.testee.range(
      0, 0, dict(
        self.all,
        query = "logrec->>'$.key[1].b' = 2",
        level = logging.INFO,
        date = (now - timedelta(seconds = 10), now + timedelta(seconds = 5))
      )
    )
    self.assertEqual(1, len(actual))
    self.assertEqual('some.test', actual[0].name)

  def testRangeQuerySyntaxError(self):
    with self.assertRaises(StorageQueryError):
      self.testee.range(0, 0, dict(self.all, query = 'logrec->>$#!'))

  def testRangeNonQuerySyntaxError(self):
    with mock.patch.object(self.testee, '_isSqlSyntaxError', lambda ex: False):
      with self.assertRaises(mysql.connections.ProgrammingError):
        self.testee.range(0, 0, dict(self.all, query = 'logrec->>$#!'))

  def testReconnect(self):
    # suicide
    with self.assertRaises(mysql.connections.OperationalError) as ctx:
      self.testee._db.kill(self.testee._db.thread_id())
    self.assertEqual(str(ctx.exception), "(1317, 'Query execution was interrupted')")

    self.testee._db.cursor().execute('BEGIN')

    now = datetime.now(timezone.utc).replace(microsecond = 0)
    self.testee.record([Record('some.test', now, logging.INFO, '')])
    self.assertEqual(1, self.testee.count(self.all))

  def testPurge(self):
    now = datetime.now(timezone.utc).replace(microsecond = 0) - timedelta(days = 10)
    records = self.testee.record([
      Record(
        'purge.test',
        now + timedelta(days = i),
        logging.INFO,
        'Hardcore Will Never Die, But You Will',
        {'track': 'Death Rays'},
      )
      for i in range(11)
    ])
    record_ids = [r.id for r in records]

    cur = self.testee._db.cursor()
    cur.execute('SELECT record_id FROM record')

    purged = self.testee.purge(timedelta(days = 5))
    self.assertEqual(6, purged)
    self.assertEqual(5, self.testee.count(self.all))

    recordsLeft = self.testee.range(0, 10, self.all)
    self.assertEqual(record_ids[6:], [r.id for r in reversed(recordsLeft)])

  def testPurgeOlderFraction(self):
    now = datetime.now(timezone.utc).replace(microsecond = 0) - timedelta(days = 10)
    records = self.testee.record([
      Record(
        'purge.test',
        now + timedelta(days = i),
        logging.INFO,
        'Hardcore Will Never Die, But You Will',
        {'track': 'Death Rays'},
      )
      for i in range(11)
    ])
    record_ids = [r.id for r in records]

    cur = self.testee._db.cursor()
    cur.execute('SELECT record_id FROM record')

    purged = self.testee.purge(timedelta(days = 5.1))
    self.assertEqual(5, purged)
    self.assertEqual(6, self.testee.count(self.all))

    recordsLeft = self.testee.range(0, 10, self.all)
    self.assertEqual(record_ids[5:], [r.id for r in reversed(recordsLeft)])

