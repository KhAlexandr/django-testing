import pytest

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.test import Client

from news.models import News, Comment


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader):
    client = Client()
    client.force_login(reader)
    return client


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )


@pytest.fixture
def news_count(author):
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=timezone.now() + timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    return News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comments(author, news):
    return [
        Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария{index}',
            created=timezone.now() + timedelta(days=index)
        )
        for index in range(222)
    ]


@pytest.fixture
def homepage_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_url(detail_url):
    return f'{detail_url}#comments'


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def excepted_url(login_url, delete_url, edit_url):
    excepted_url = {}
    for url in [delete_url, edit_url]:
        excepted_url[url] = f'{login_url}?next={url}'
    return excepted_url
