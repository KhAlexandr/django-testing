from http import HTTPStatus

from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


FORM_DATA = {
    'text': 'Новый текст',
}
BAD_WORDS_DATA = [
    {'text': f'Начало текста, {BAD_WORD}, конец текста'}
    for BAD_WORD in BAD_WORDS
]


def test_anonymous_user_cant_create_comment(
    client, detail_url
):
    client.post(detail_url, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author_client, news, detail_url, comment_url, author
):
    assertRedirects(
        author_client.post(detail_url, data=FORM_DATA), comment_url
    )
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    for bad_word_data in BAD_WORDS_DATA:
        response = author_client.post(detail_url, data=bad_word_data)
        assert response.context['form'].errors['text'][0] == WARNING
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client, comment_url, comment_delete_url
):
    assertRedirects(author_client.delete(comment_delete_url), comment_url)
    comment_count = Comment.objects.count()
    assert comment_count == 0


def test_user_cant_delete_comment_of_another_user(
    reader_client, comment_delete_url, news, comment, author
, comments):
    comments = set(Comment.objects.all())
    assert reader_client.delete(
        comment_delete_url
    ).status_code == HTTPStatus.NOT_FOUND
    assert comments == set(Comment.objects.all())
    comments = Comment.objects.get(id=comment.id)
    assert comments.author == comment.author
    assert comments.news == comments.news
    assert comments.text == comment.text


def test_author_can_edit_comment(
    author_client, edit_url, comment, comment_url
):
    assertRedirects(author_client.post(edit_url, data=FORM_DATA), comment_url)
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
    reader_client, edit_url, comment
):
    reader_client.post(edit_url, data=FORM_DATA)
    new_comment = Comment.objects.get(id=comment.id)
    assert new_comment.text == comment.text
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author
