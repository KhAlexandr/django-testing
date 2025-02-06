from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_count_of_news_on_hompage(client, news_count):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order_on_homepage(client, news):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_news_date = [news.date for news in object_list]
    assert all_news_date == sorted(all_news_date, reverse=True)


def test_comment_order(client, news, comments, news_id_for_args):
    response = client.get(reverse('news:detail', args=(news_id_for_args)))
    assert 'news' in response.context
    sorted_date = sorted([comment.created for comment in comments])
    assert [comment.created for comment in comments] == sorted_date


def test_anonymous_client_has_no_form(client, news_id_for_args):
    url = reverse('news:detail', args=(news_id_for_args))
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(reader_client, news_id_for_args):
    url = reverse('news:detail', args=(news_id_for_args))
    response = reader_client.get(url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
