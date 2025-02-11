from pytest_lazy_fixtures import lf
import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects


HOME_URL = lf('homepage_url')
LOGIN_URL = lf('login_url')
LOGOUT_URL = lf('logout_url')
SIGNUP_URL = lf('signup_url')
DETAILS_URL = lf('detail_url')
EDIT_URL = lf('edit_url')
DELETE_URL = lf('delete_url')
EXCEPTED_URL_DELETE = lf('excepted_url_delete')
EXCEPTED_URL_EDIT = lf('excepted_url_edit')
CLIENT = lf('client')
AUTHOR = lf('author_client')
READER = lf('reader_client')


@pytest.mark.parametrize(
    'url, user, status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (DETAILS_URL, CLIENT, HTTPStatus.OK),
        (LOGIN_URL, CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (EDIT_URL, AUTHOR, HTTPStatus.OK),
        (DELETE_URL, AUTHOR, HTTPStatus.OK),
        (EDIT_URL, READER, HTTPStatus.NOT_FOUND),
        (DELETE_URL, READER, HTTPStatus.NOT_FOUND),
        (DELETE_URL, CLIENT, HTTPStatus.FOUND),
        (EDIT_URL, CLIENT, HTTPStatus.FOUND),
    ),
)
def test_available_pages(url, user, status, news):
    assert user.get(url).status_code == status


@pytest.mark.parametrize(
    'url, excepted',
    (
        (DELETE_URL, EXCEPTED_URL_DELETE),
        (EDIT_URL, EXCEPTED_URL_EDIT),
    ),
)
def test_redirect_for_anonymus(url, client, excepted):
    assertRedirects(client.get(url), excepted)
