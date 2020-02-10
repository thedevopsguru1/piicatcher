import logging
from argparse import Namespace

from click.testing import CliRunner
from pytest_mock import mocker

from piicatcher.command_line import cli


def test_db(tmp_path, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    config_file = tmp_path / "db_host.ini"
    config_file.write_text("""
[db]
host="localhost"
database="db"
port="6032"
user="user"
password="password"
scan_type="deep"
list_all=True
output_format="json"
schema=["schema1", "schema2"]
exclude_schema=["schema1", "schema2"]
table=["table1", "table2"]
exclude_table=["table1", "table2"]
"""
                           )

    logging.info("Config File: %s" % config_file)
    rel = mocker.patch("piicatcher.explorer.databases.RelDbExplorer")
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_file), "db"])
    assert result.exception is None
    assert "" == result.stdout
    assert 0 == result.exit_code

    ns = Namespace(connection_type='mysql',
                   database='db',
                   host='localhost',
                   list_all=True,
                   password="password",
                   port=6032,
                   scan_type='deep',
                   user='user',
                   include_schema=("schema1", "schema2"),
                   exclude_schema=("schema1", "schema2"),
                   include_table=("table1", "table2"),
                   exclude_table=("table1", "table2"),
                   catalog={
                       'host': None,
                       'port': None,
                       'user': None,
                       'password': None,
                       'format': 'json',
                       'file': None
                   })

    rel.dispatch.assert_called_once_with(ns)


def test_sqlite(tmp_path, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    config_file = tmp_path / "db_host.ini"
    config_file.write_text("""
[sqlite]
path="sqlite.db"
scan_type="deep"
list_all=True
output_format="json"
schema=["schema1", "schema2"]
exclude_schema=["schema1", "schema2"]
table=["table1", "table2"]
exclude_table=["table1", "table2"]
"""
                           )

    logging.info("Config File: %s" % config_file)
    explorer = mocker.patch("piicatcher.explorer.sqlite.SqliteExplorer")
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_file), "sqlite"])
    assert result.exception is None
    assert "" == result.stdout
    assert 0 == result.exit_code
    explorer.dispatch.assert_called_once_with(Namespace(path='sqlite.db',
                                                        list_all=True,
                                                        scan_type='deep',
                                                        include_schema=("schema1", "schema2"),
                                                        exclude_schema=("schema1", "schema2"),
                                                        include_table=("table1", "table2"),
                                                        exclude_table=("table1", "table2"),
                                                        catalog={'host': None, 'port': None,
                                                                 'user': None, 'password': None,
                                                                 'format': 'json', 'file': None}))


def test_files(tmp_path, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    config_file = tmp_path / "db_host.ini"
    config_file.write_text("""
[files]
path="file path"
output_format="json"
"""
                           )

    logging.info("Config File: %s" % config_file)
    explorer = mocker.patch("piicatcher.explorer.files.FileExplorer")
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_file), "files"])
    assert result.exception is None
    assert "" == result.stdout
    assert 0 == result.exit_code
    explorer.dispatch.assert_called_once_with(Namespace(path='file path',
                                                        catalog={
                                                            'host': None,
                                                            'port': None,
                                                            'user': None,
                                                            'password': None,
                                                            'format': 'json',
                                                            'file': None
                                                        }))


def test_aws(tmp_path, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    config_file = tmp_path / "db_host.ini"
    config_file.write_text("""
[aws]
access_key='AAAA'
list_all=True
output_format='json'
region='us-east'
scan_type='deep'
secret_key='SSSS'
staging_dir='s3://dir'
schema=["schema1", "schema2"]
exclude_schema=["schema1", "schema2"]
table=["table1", "table2"]
exclude_table=["table1", "table2"]
""")

    logging.info("Config File: %s" % config_file)
    explorer = mocker.patch("piicatcher.explorer.aws.AthenaExplorer")
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_file), "aws"])
    assert result.exception is None
    assert "" == result.stdout
    assert 0 == result.exit_code
    explorer.dispatch.assert_called_once_with(Namespace(
        access_key='AAAA',
        list_all=True,
        region='us-east',
        scan_type='deep',
        secret_key='SSSS',
        staging_dir='s3://dir',
        include_schema=("schema1", "schema2"),
        exclude_schema=("schema1", "schema2"),
        include_table=("table1", "table2"),
        exclude_table=("table1", "table2"),
        catalog={
            'host': None,
            'port': None,
            'user': None,
            'password': None,
            'format': 'json',
            'file': None
        }))


def test_catalog(tmp_path, mocker, caplog):
    caplog.set_level(logging.DEBUG)
    config_file = tmp_path / "db_host.ini"
    config_file.write_text("""
catalog_host='host'
catalog_port='port'
catalog_user='user'
catalog_password='password'
catalog_format='db'

[aws]
access_key='AAAA'
list_all=True
region='us-east'
scan_type='deep'
secret_key='SSSS'
staging_dir='s3://dir'
schema=["schema1", "schema2"]
exclude_schema=["schema1", "schema2"]
table=["table1", "table2"]
exclude_table=["table1", "table2"]
""")

    logging.info("Config File: %s" % config_file)
    explorer = mocker.patch("piicatcher.explorer.aws.AthenaExplorer")
    runner = CliRunner()
    result = runner.invoke(cli, ["--config", str(config_file), "aws"])
    assert "" == result.stdout
    assert result.exception is None
    assert 0 == result.exit_code
    explorer.dispatch.assert_called_once_with(Namespace(
        access_key='AAAA',
        list_all=True,
        region='us-east',
        scan_type='deep',
        secret_key='SSSS',
        staging_dir='s3://dir',
        include_schema=("schema1", "schema2"),
        exclude_schema=("schema1", "schema2"),
        include_table=("table1", "table2"),
        exclude_table=("table1", "table2"),
        catalog={
            'host': 'host',
            'port': 'port',
            'user': 'user',
            'password': 'password',
            'format': 'db',
            'file': None
        }))