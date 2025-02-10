from http import HTTPStatus

from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass


User = get_user_model()


class TestRoutes(BaseTestClass):

    def setUp(self):
        urls = (
            self.URL_ADD_NOTE,
            self.URL_DETAIL,
            self.URL_SUCCESS,
            self.URL_DELETE,
            self.NOTES_LIST_URL,
            self.URL_EDIT_NOTE,
        )
        self.redirect_url = {}
        for url in urls:
            self.redirect_url[url] = f'{self.URL_LOGIN}?next={url}'

    def test_pages_availability(self):
        urls = (
            (self.URL_HOME, self.client, HTTPStatus.OK),
            (self.URL_LOGIN, self.client, HTTPStatus.OK),
            (self.URL_LOGOUT, self.client, HTTPStatus.OK),
            (self.URL_SIGN_UP, self.client, HTTPStatus.OK),
            (self.URL_ADD_NOTE, self.auth_client, HTTPStatus.OK),
            (self.URL_SUCCESS, self.auth_client, HTTPStatus.OK),
            (self.NOTES_LIST_URL, self.auth_client, HTTPStatus.OK),
            (self.URL_EDIT_NOTE, self.auth_client, HTTPStatus.OK),
            (self.URL_DELETE, self.auth_client, HTTPStatus.OK),
            (self.URL_EDIT_NOTE, self.auth_client, HTTPStatus.OK),
            (self.URL_EDIT_NOTE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),

        )
        for url, client, status in urls:
            with self.subTest(name=url):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymus_client(self):
        urls = (
            self.URL_ADD_NOTE,
            self.URL_DETAIL,
            self.URL_SUCCESS,
            self.URL_DELETE,
            self.NOTES_LIST_URL,
            self.URL_EDIT_NOTE,
        )
        for url in urls:
            self.assertRedirects(self.client.get(url), self.redirect_url[url])
