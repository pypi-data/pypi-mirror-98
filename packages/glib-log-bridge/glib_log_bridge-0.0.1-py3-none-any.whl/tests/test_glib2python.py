import unittest
import logging
import logging.handlers
import queue
from gi.repository import GLib
import glib_log_bridge.glib2python as g2p
from hypothesis import given, strategies


LOGGER_NAME = 'glibtest'
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(1)
q: queue.Queue = queue.Queue()
qhandler = logging.handlers.QueueHandler(q)


class GLib2PythonWriterTest(unittest.TestCase):

    def setUp(self):
        logger.addHandler(qhandler)

    def tearDown(self):
        was_empty = q.empty()
        while not q.empty():
            q.get(timeout=1)
        self.assertTrue(was_empty)
        logger.removeHandler(qhandler)

    def _register(self, l):
        GLib.log_set_writer_func(l.glibToPythonLogWriterFunc, None)

    def _log(self, logger_name, flags, message, fields=None):
        f = {'MESSAGE': GLib.Variant('s', message)}
        if fields is not None:
            f.update(fields)
        GLib.log_variant(logger_name, flags, GLib.Variant('a{sv}', f))

    @given(strategies.text(alphabet=strategies.characters(
        blacklist_categories=('C'), blacklist_characters='\x00'),
        min_size=1))
    def test_basic(self, msg):
        self._register(g2p.GLibToPythonLogger())
        self._log(LOGGER_NAME, GLib.LogLevelFlags.LEVEL_WARNING, msg)
        record = q.get(timeout=1)
        self.assertEqual(record.message, msg)

    @given(strategies.sampled_from([
        # (GLib.LogLevelFlags.LEVEL_ERROR, logging.ERROR), # fatal, so aborts
        (GLib.LogLevelFlags.LEVEL_CRITICAL, logging.CRITICAL),
        (GLib.LogLevelFlags.LEVEL_WARNING, logging.WARNING),
        (GLib.LogLevelFlags.LEVEL_MESSAGE, logging.INFO),
        (GLib.LogLevelFlags.LEVEL_INFO, logging.INFO),
        (GLib.LogLevelFlags.LEVEL_DEBUG, logging.DEBUG),
    ]))
    def test_loglevels(self, m):
        self._register(g2p.GLibToPythonLogger())
        glib_level, logging_level = m
        self._log(LOGGER_NAME, m[0], "some_message")
        self.assertEqual(m[1], q.get(timeout=1).levelno)

    @given(strategies.sampled_from([
        # (GLib.LogLevelFlags.LEVEL_ERROR, logging.ERROR), # fatal, so aborts
        (GLib.LogLevelFlags.LEVEL_CRITICAL, logging.CRITICAL),
        (GLib.LogLevelFlags.LEVEL_WARNING, logging.WARNING),
        (GLib.LogLevelFlags.LEVEL_MESSAGE, logging.INFO),
        (GLib.LogLevelFlags.LEVEL_INFO, logging.INFO),
        (GLib.LogLevelFlags.LEVEL_DEBUG, logging.DEBUG),
    ]))
    def test_loglevels_priority(self, m):
        self._register(g2p.GLibToPythonLogger(use_priority_field=False))
        self._log(LOGGER_NAME, m[0], "some_message")
        self.assertEqual(m[1], q.get(timeout=1).levelno)

    @given(strategies.lists(strategies.text(
        alphabet=strategies.characters(blacklist_categories=('C'),
                                       blacklist_characters='\x00'),
        min_size=1), min_size=1))
    def test_domain(self, domain):
        self._register(g2p.GLibToPythonLogger())
        level = GLib.LogLevelFlags.LEVEL_INFO
        domain = '-'.join(domain)
        logger = logging.getLogger(LOGGER_NAME + '.'
                                   + domain.replace('-', '.'))
        lq = queue.Queue()
        logger.addHandler(logging.handlers.QueueHandler(lq))
        self._log(LOGGER_NAME + '-' + domain, level, domain)
        self.assertEqual(domain, lq.get(timeout=1).message)
        self.assertTrue(lq.empty())

        while not q.empty():
            q.get(timeout=1)

    @given(strategies.lists(strategies.from_regex('[a-zA-Z][a-zA-Z0-9]*',
                                                  fullmatch=True),
                            min_size=1, max_size=5))
    def test_domain_prefix(self, domain):
        self._register(g2p.GLibToPythonLogger(logger_prefix=LOGGER_NAME + '.'))
        level = GLib.LogLevelFlags.LEVEL_INFO
        domain = '-'.join(domain)
        logger = logging.getLogger(LOGGER_NAME + '.'
                                   + domain.replace('-', '.'))
        lq = queue.Queue()
        handler = logging.handlers.QueueHandler(lq)
        logger.addHandler(handler)
        try:
            self._log(domain, level, domain)
            self.assertEqual(domain, lq.get(timeout=1).message)
            self.assertTrue(lq.empty())
        finally:
            logger.removeHandler(handler)

        while not q.empty():
            q.get(timeout=1)

    def test_invalid_message(self):
        self._register(g2p.GLibToPythonLogger())
        self._log(LOGGER_NAME, GLib.LogLevelFlags.LEVEL_WARNING, '', fields={
            'MESSAGE': GLib.Variant('ay', b'\xFF')  # Not valid UTF-8
        })
        record = q.get(timeout=1)
        self.assertEqual(record.message, '\uFFFD')  # At least still a string
        self.assertTrue(q.empty())


@unittest.skip("No easy access to unstructured logging")
class GLib2PythonHandlerTest(GLib2PythonWriterTest):

    def _log(self, logger_name, flags, message, fields=None):
        f = {'MESSAGE': GLib.Variant('s', message)}
        if fields is not None:
            f.update(fields)
        GLib.log_variant(logger_name, flags, GLib.Variant('a{sv}', f))
        # TODO: Change this to use unstrucuted logging functions

    def _register(self, l):
        GLib.log_set_handler(LOGGER_NAME, GLib.LogLevelFlags.LEVEL_MASK,
                             l.glibToPythonLogFunc, None)


if __name__ == '__main__':
    unittest.main()
