from django.conf import settings

from news.forms import CommentForm


def test_count_of_news_on_home_page(client, news_count, homepage_url):
    response = client.get(homepage_url)
    news = response.context['object_list']
    assert news.count() == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order_on_homepage(client, news, homepage_url):
    response = client.get(homepage_url)
    news = response.context['object_list']
    all_news_date = [news.date for news in news]
    assert all_news_date == sorted(all_news_date, reverse=True)


def test_comment_order(client, news, comments, detail_url):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert [
        comment.created for comment in all_comments
    ] == sorted([comment.created for comment in all_comments])


def test_anonymous_client_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(reader_client, detail_url):
    assert isinstance(
        reader_client.get(detail_url).context.get('form'), CommentForm
    )
