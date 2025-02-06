from http import HTTPStatus

from pytest_django.asserts import assertRedirects
from pytest_django.asserts import assertRedirects

from django.urls import reverse

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
    client, form_data, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    client.post(url, data=form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author, author_client, news, form_data, news_id_for_args
):
    url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(url, data=form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(author_client, news_id_for_args):
    url = reverse('news:detail', args=news_id_for_args)
    bad_words_data = {'text': f'Начало текста, {BAD_WORDS[0]}, конец текста'}
    response = author_client.post(url, data=bad_words_data)
    assert response.context['form'].errors['text'][0] == WARNING
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(
    author_client, news_id_for_args, comment_id_for_args
):
    url = reverse('news:delete', args=comment_id_for_args)
    news_url = reverse('news:detail', args=news_id_for_args)
    response = author_client.delete(url)
    assertRedirects(response, f'{news_url}#comments')
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_cant_delete_comment_of_another_user(
    reader_client, news_id_for_args, comment_id_for_args
):
    url = reverse('news:delete', args=comment_id_for_args)
    response = reader_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_count = Comment.objects.count()
    assert comment_count == 1


def test_author_can_edit_comment(
    author_client, comment_id_for_args, form_data, news_id_for_args, comment
):
    urls = reverse('news:edit', args=comment_id_for_args)
    news_url = reverse('news:detail', args=news_id_for_args)
    response = author_client.post(urls, data=form_data)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    reader_client, comment_id_for_args, form_data, comment
):
    response = reader_client.delete('news:delete', args=comment_id_for_args)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment.refresh_from_db()
    assert comment.text == 'Текст комментария'
