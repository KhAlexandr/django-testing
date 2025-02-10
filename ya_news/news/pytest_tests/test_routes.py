from pytest_lazy_fixtures import lf
import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects


HOME_URL = lf('homepage_url')
DETAILS_URL = lf('detail_url')
LOGIN_URL = lf('login_url')
LOGOUT_URL = lf('logout_url')
SIGNUP_URL = lf('signup_url')
EDIT_URL = lf('edit_url')
DELETE_URL = lf('delete_url')


@pytest.mark.parametrize(
    'url, user, status',
    (
        (HOME_URL, lf('client'), HTTPStatus.OK),
        (DETAILS_URL, lf('client'), HTTPStatus.OK),
        (LOGIN_URL, lf('client'), HTTPStatus.OK),
        (LOGOUT_URL, lf('client'), HTTPStatus.OK),
        (SIGNUP_URL, lf('client'), HTTPStatus.OK),
        (EDIT_URL, lf('author_client'), HTTPStatus.OK),
        (DELETE_URL, lf('author_client'), HTTPStatus.OK),
        (EDIT_URL, lf('reader_client'), HTTPStatus.NOT_FOUND),
        (DELETE_URL, lf('reader_client'), HTTPStatus.NOT_FOUND),

    ),
)
def test_available_pages(url, status, news, user):
    assert user.get(url).status_code == status


@pytest.mark.parametrize(
    'url',
    (DELETE_URL, EDIT_URL)
)
def test_redirect_for_anonymus(url, client, excepted_url):
    assertRedirects(client.get(url), excepted_url[url])
