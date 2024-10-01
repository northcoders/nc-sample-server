import pytest
from unittest.mock import patch
from src.api.helpers import get_db_connection, process_query, DBConnectionException
from data import (
    sample_data,
    sample_headers,
    sample_result,
)


@pytest.fixture
def mock_config():
    env_vars = {
        "DB_HOST": "abc",
        "DB_PORT": "5432",
        "DB_USER": "def",
        "DB_PASSWORD": "password",
        "DB_DB": "db",
    }
    with patch("src.api.helpers.get_config", return_value=env_vars) as mock_config:
        yield mock_config


def db_data(query):
    if query == "test query":
        return sample_data
    return []


def db_data_params(query, **params):
    if query == "test params":
        return sample_data
    return []


@pytest.mark.describe("Helpers")
@pytest.mark.it("Creates DB connection")
@patch("src.api.helpers.Connection", autospec=True)
def test_get_db_connection(mock_conn, mock_config):
    get_db_connection()
    mock_conn.assert_called_with(
        host="abc", user="def", port="5432", password="password", database="db"
    )


@pytest.mark.describe("Helpers")
@pytest.mark.it("Raises DB connection error")
def test_db_error(mock_config):
    with pytest.raises(DBConnectionException):
        get_db_connection()


@pytest.mark.describe("Helpers")
@pytest.mark.it("DB Connection logs successful connection")
def test_db_connection_log():
    pass


@pytest.mark.describe("Helpers")
@pytest.mark.it("Query processor returns correctly formatted dict")
def test_process_query():
    with patch("src.api.helpers.get_db_connection") as mock_conn:
        mock_conn().run.side_effect = db_data
        mock_conn().columns = sample_headers
        result = process_query("test query")
        assert result == sample_result


@pytest.mark.describe("Helpers")
@pytest.mark.it("Query processor uses parameters")
def test_query_parameters(mock_config):
    with patch("src.api.helpers.Connection", autospec=True) as mock_conn:
        mock_conn().columns = sample_headers
        mock_conn().run.side_effect = db_data_params
        result = process_query("test params", param1="x")
        assert result == sample_result
        mock_conn().run.assert_called_once_with("test params", param1="x")
