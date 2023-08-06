# -*- coding: utf-8 -*-

from pip_services3_expressions.io.StringPushbackReader import StringPushbackReader
from test.io.PushbackReaderFixture import PushbackReaderFixture


class TestStringPushbackReader:
    content: str
    reader: StringPushbackReader
    fixture: PushbackReaderFixture

    def setup_method(self):
        self.content = 'Test String'
        self.reader = StringPushbackReader(self.content)
        self.fixture = PushbackReaderFixture(self.reader, self.content)

    def test_operations(self):
        self.fixture.test_operations()

    def test_pushback(self):
        self.fixture.test_pushback()
