import pytest

from datetime import timedelta

from django.conf import settings
from django.test import Client
from django.utils import timezone
from django.urls import reverse


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
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )


@pytest.fixture
def comments(author, news, comment):
    all_comments = []
    for index in range(222):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст комментария {index}'
        )
        comment.created = timezone.now() + timedelta(days=index)
        comment.save()
        all_comments.append(comment)
    return all_comments


@pytest.fixture
def homepage_url():
    return reverse('news:home', args=None)


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
    return reverse('users:login', args=None)


@pytest.fixture
def logout_url():
    return reverse('users:logout', args=None)


@pytest.fixture
def signup_url():
    return reverse('users:signup', args=None)


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def excepted_url_delete(login_url, delete_url):
    return f'{login_url}?next={delete_url}'


@pytest.fixture
def excepted_url_edit(login_url, edit_url):
    return f'{login_url}?next={edit_url}'
