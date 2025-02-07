from pytest_lazy_fixtures import lf
import pytest
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:detail', lf('news_id_for_args')),
    ),
)
def test_available_pages_for_anonimus(client, name, args, news):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lf('author_client'), HTTPStatus.OK),
        (lf('reader_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete')
)
def test_available_delete_and_edit_comment_for_different_users(
    parametrized_client, expected_status, name, comment
):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', lf('comment_id_for_args')),
        ('news:edit', lf('comment_id_for_args')),
    )
)
def test_redirect_for_anonymus(name, client, args):
    login_url = reverse('users:login')
    url = reverse(name, args=args)
    excepted_url = (f'{login_url}?next={url}')
    response = client.get(url)
    assertRedirects(response, excepted_url)
