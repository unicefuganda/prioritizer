from unittest import TestCase
from mock import patch, Mock
from models.encoder import Encoder


def md5_mock(args):
    md5 = Mock()
    md5.hexdigest = Mock(return_value='encrypted_value')
    return md5

class TestEncoder(TestCase):
    @patch('hashlib.md5', md5_mock)
    def test_that_encode_text_using_md5(self):
        text = "important text"
        encoder = Encoder()
        encoded_text = encoder.encode(text)
        self.assertEquals(encoded_text, 'encrypted_value')