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
USER = lf('client')


@pytest.mark.parametrize(
    'url, user, status',
    (
        (HOME_URL, USER, HTTPStatus.OK),
        (DETAILS_URL, USER, HTTPStatus.OK),
        (LOGIN_URL, USER, HTTPStatus.OK),
        (LOGOUT_URL, USER, HTTPStatus.OK),
        (SIGNUP_URL, USER, HTTPStatus.OK),
        (EDIT_URL, lf('author_client'), HTTPStatus.OK),
        (DELETE_URL, lf('author_client'), HTTPStatus.OK),
        (EDIT_URL, lf('reader_client'), HTTPStatus.NOT_FOUND),
        (DELETE_URL, lf('reader_client'), HTTPStatus.NOT_FOUND),
    ),
)
def test_available_pages(url, user, status, news):
    response = user.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url, excepted',
    (
        (DELETE_URL, EXCEPTED_URL_DELETE),
        (EDIT_URL, EXCEPTED_URL_EDIT),
    ),
)
def test_redirect_for_anonymus(url, client, excepted):
    assertRedirects(client.get(url), excepted)
