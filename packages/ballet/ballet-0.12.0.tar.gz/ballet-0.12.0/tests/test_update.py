import logging
from unittest.mock import Mock, patch

import git
import pytest

import ballet
import ballet.util.log
from ballet.update import (
    _check_for_updated_ballet, _extract_latest_from_search_triple,
    _get_latest_ballet_version_string, _log_recommended_reinstall,
    _make_template_branch_merge_commit_message, _query_pip_search_ballet,
    _safe_delete_remote, _warn_of_updated_ballet,)


@pytest.mark.skip(
    reason='Disabled due to https://status.python.org/incidents/grk0k7sz6zkp'
)
def test_query_pip_search_ballet():
    # nothing better to do that just call the function...
    # actually hits PyPI but difficult to mock because uses subprocess >:(
    result = _query_pip_search_ballet()
    assert 'ballet' in result


def test_extract_latest_from_search_triple():
    triple = (
        'ballet (x.y.z)  - some description',
        '  INSTALLED: x.y.z',
        '  LATEST:    u.v.w',
    )
    result = _extract_latest_from_search_triple(triple)
    assert result == 'u.v.w'


def test_extract_latest_from_search_triple_not_found():
    triple = (
        'something',
        'that does not',
        'match the expected format'
    )
    result = _extract_latest_from_search_triple(triple)
    assert result is None


@patch('funcy.partition')
@patch('ballet.update._extract_latest_from_search_triple')
@patch('ballet.update._query_pip_search_ballet')
def test_get_latest_ballet_version_string(
    mock_query, mock_extract, mock_partition
):
    mock_partition.return_value = ['some', 'iterable']
    expected = 'x.y.z'
    mock_extract.return_value = expected

    actual = _get_latest_ballet_version_string()

    assert actual == expected


@patch('ballet.update._get_latest_ballet_version_string')
def test_check_for_updated_ballet(mock_latest):
    # obviously this will represent an update from whatever the current
    # version is
    latest = '99999999999.0.0'
    mock_latest.return_value = latest
    expected = latest
    actual = _check_for_updated_ballet()
    assert actual == expected


@patch('ballet.update._get_latest_ballet_version_string')
def test_check_for_updated_ballet_no_updates(mock_latest):
    mock_latest.return_value = ballet.__version__
    expected = None  # no updates available
    actual = _check_for_updated_ballet()
    assert actual == expected


def test_warn_of_updated_ballet(caplog):
    caplog.set_level(logging.DEBUG, ballet.util.log.logger.name)
    latest = 'x.y.z'
    _warn_of_updated_ballet(latest)
    assert latest in caplog.text


def test_make_template_branch_merge_commit_message():
    result = _make_template_branch_merge_commit_message()
    assert ballet.__version__ in result


def test_safe_delete_remote():
    repo = Mock(spec=git.Repo)
    name = 'name'
    _safe_delete_remote(repo, name)
    repo.delete_remote.assert_called_once_with(name)


def test_log_recommended_reinstall(caplog):
    caplog.set_level(logging.DEBUG, ballet.util.log.logger.name)
    _log_recommended_reinstall()
    assert caplog.text
