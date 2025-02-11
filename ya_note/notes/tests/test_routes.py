from http import HTTPStatus

from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass, UrlManager

User = get_user_model()


class TestRoutes(BaseTestClass):

    def test_pages_availability(self):
        urls = (
            (UrlManager.URL_HOME, self.client, HTTPStatus.OK),
            (UrlManager.URL_LOGIN, self.client, HTTPStatus.OK),
            (UrlManager.URL_LOGOUT, self.client, HTTPStatus.OK),
            (UrlManager.URL_SIGN_UP, self.client, HTTPStatus.OK),
            (UrlManager.URL_ADD_NOTE, self.auth_client, HTTPStatus.OK),
            (UrlManager.URL_SUCCESS, self.auth_client, HTTPStatus.OK),
            (UrlManager.NOTES_LIST_URL, self.auth_client, HTTPStatus.OK),
            (UrlManager.URL_EDIT_NOTE, self.auth_client, HTTPStatus.OK),
            (UrlManager.URL_DELETE, self.auth_client, HTTPStatus.OK),
            (
                UrlManager.URL_EDIT_NOTE,
                self.reader_client,
                HTTPStatus.NOT_FOUND
            ),
            (UrlManager.URL_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (UrlManager.URL_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (UrlManager.URL_LOGIN, self.reader_client, HTTPStatus.OK),
            (UrlManager.URL_LOGOUT, self.reader_client, HTTPStatus.OK),
            (UrlManager.URL_SIGN_UP, self.reader_client, HTTPStatus.OK),
            (UrlManager.URL_LOGIN, self.auth_client, HTTPStatus.OK),
            (UrlManager.URL_LOGOUT, self.auth_client, HTTPStatus.OK),
            (UrlManager.URL_SIGN_UP, self.auth_client, HTTPStatus.OK),
            (
                UrlManager.REDIRECT_URL_ADD_NOTE,
                self.client,
                HTTPStatus.OK
            ),
            (
                UrlManager.REDIRECT_URL_DETAIL,
                self.client,
                HTTPStatus.OK
            ),
            (
                UrlManager.REDIRECT_URL_SUCCESS,
                self.client,
                HTTPStatus.OK
            ),
            (
                UrlManager.REDIRECT_URL_DELETE,
                self.client,
                HTTPStatus.OK
            ),
            (
                UrlManager.REDIRECT_URL_EDIT,
                self.client,
                HTTPStatus.OK
            ),
            (
                UrlManager.REDIRECT_URL_NOTES_LIST,
                self.client,
                HTTPStatus.OK
            )
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
