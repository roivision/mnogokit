from mock import patch, call
from unittest import TestCase
from backup import parse
from click.testing import CliRunner


@patch('backup.mongodump')
class TestDump(TestCase):

    def test_parser(self, mongodump):
        runner = CliRunner()
        result = runner.invoke(
                parse,
                ['-d', 'database', '--collections', 'c1,c2', '-o', '/tmp/'])
        mongodump.assert_called_with(
                '--collection', u'c2', '-o', u'/tmp/', '-d', 'database')
        result = runner.invoke(
                parse,
                ['-d', 'database', '-o', '/tmp/'])
        mongodump.assert_called_with(
                '-o', u'/tmp/', '-d', 'database')



