from http import HTTPStatus

from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass, UrlManager

User = get_user_model()

OK = HTTPStatus.OK


class TestRoutes(BaseTestClass):

    def test_pages_availability(self):
        anon = self.client
        author = self.auth_client
        reader = self.reader_client
        urls = (
            (UrlManager.URL_HOME, anon, OK),
            (UrlManager.URL_LOGIN, anon, OK),
            (UrlManager.URL_LOGOUT, anon, OK),
            (UrlManager.URL_SIGN_UP, anon, OK),
            (UrlManager.URL_ADD_NOTE, author, OK),
            (UrlManager.URL_SUCCESS, author, OK),
            (UrlManager.NOTES_LIST_URL, author, OK),
            (UrlManager.URL_EDIT_NOTE, author, OK),
            (UrlManager.URL_DELETE, author, OK),
            (UrlManager.URL_EDIT_NOTE, reader, HTTPStatus.NOT_FOUND),
            (UrlManager.URL_DELETE, reader, HTTPStatus.NOT_FOUND),
            (UrlManager.URL_DETAIL, reader, HTTPStatus.NOT_FOUND),
            (UrlManager.URL_LOGIN, reader, OK),
            (UrlManager.URL_LOGOUT, reader, OK),
            (UrlManager.URL_SIGN_UP, reader, OK),
            (UrlManager.URL_LOGIN, author, OK),
            (UrlManager.URL_LOGOUT, author, OK),
            (UrlManager.URL_SIGN_UP, author, OK),
            (UrlManager.URL_ADD_NOTE, anon, HTTPStatus.FOUND),
            (UrlManager.URL_DETAIL, anon, HTTPStatus.FOUND),
            (UrlManager.URL_SUCCESS, anon, HTTPStatus.FOUND),
            (UrlManager.URL_DELETE, anon, HTTPStatus.FOUND),
            (UrlManager.URL_EDIT_NOTE, anon, HTTPStatus.FOUND),
            (UrlManager.NOTES_LIST_URL, anon, HTTPStatus.FOUND)
        )
        for url, client, status in urls:
            with self.subTest(name=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymus_client(self):
        urls = (
            (UrlManager.URL_ADD_NOTE, UrlManager.REDIRECT_URL_ADD_NOTE),
            (UrlManager.URL_DETAIL, UrlManager.REDIRECT_URL_DETAIL),
            (UrlManager.URL_SUCCESS, UrlManager.REDIRECT_URL_SUCCESS),
            (UrlManager.URL_DELETE, UrlManager.REDIRECT_URL_DELETE),
            (UrlManager.NOTES_LIST_URL, UrlManager.REDIRECT_URL_NOTES_LIST),
            (UrlManager.URL_EDIT_NOTE, UrlManager.REDIRECT_URL_EDIT),
        )
        for url, redirect in urls:
            with self.subTest(name=url):
                self.assertRedirects(self.client.get(url), redirect)
