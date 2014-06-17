import json

from django.test import TestCase
from mock import Mock

from silk.model_factory import RequestModelFactory

DJANGO_META_CONTENT_TYPE = 'CONTENT_TYPE'


class TestEncodingForRequests(TestCase):
    """
    Check that the RequestModelFactory deals with encodings correctly via charset
    """

    def test_utf_plain(self):
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'text/plain; charset=UTF-8'}
        mock_request.body = u'语'
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertFalse(body)
        self.assertEqual(raw_body, mock_request.body)

    def test_plain(self):
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'text/plain'}
        mock_request.body = 'sdfsdf'
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertFalse(body)
        self.assertEqual(raw_body, mock_request.body)

    def test_utf_json_not_encoded(self):
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'application/json; charset=UTF-8'}
        d = {'x': u'语'}
        mock_request.body = json.dumps(d)
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertDictEqual(json.loads(body), d)
        self.assertEqual(raw_body, mock_request.body)

    def test_utf_json_encoded(self):
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'application/json; charset=UTF-8'}
        d = {'x': u'语'}
        mock_request.body = json.dumps(d).encode('UTF-8')
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertDictEqual(json.loads(body), d)
        self.assertEqual(raw_body, mock_request.body.decode('UTF-8'))

    def test_utf_json_encoded_no_charset(self):
        """default to UTF-8"""
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'application/json'}
        d = {'x': u'语'}
        mock_request.body = json.dumps(d).encode('UTF-8')
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertDictEqual(json.loads(body), d)
        self.assertEqual(raw_body, mock_request.body.decode('UTF-8'))

    def test_invalid_encoding_json(self):
        mock_request = Mock()
        mock_request.META = {DJANGO_META_CONTENT_TYPE: 'application/json; charset=asdas-8'}
        d = {'x': u'语'}
        mock_request.body = json.dumps(d).encode('UTF-8')
        mock_request.get = mock_request.META.get
        factory = RequestModelFactory(mock_request)
        body, raw_body = factory.body()
        self.assertFalse(body)
        self.assertFalse(raw_body)