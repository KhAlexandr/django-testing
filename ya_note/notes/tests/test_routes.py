from http import HTTPStatus

from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass


User = get_user_model()


class TestRoutes(BaseTestClass):

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
            (self.URL_EDIT_NOTE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_LOGIN, self.reader_client, HTTPStatus.OK),
            (self.URL_LOGOUT, self.reader_client, HTTPStatus.OK),
            (self.URL_SIGN_UP, self.reader_client, HTTPStatus.OK),
            (self.URL_LOGIN, self.auth_client, HTTPStatus.OK),
            (self.URL_LOGOUT, self.auth_client, HTTPStatus.OK),
            (self.URL_SIGN_UP, self.auth_client, HTTPStatus.OK),

        )
        for url, client, status in urls:
            with self.subTest(name=url, client=client, status=status):
                self.assertEqual(client.get(url).status_code, status)

    def test_redirect_for_anonymus_client(self):
        urls = (
            (self.URL_ADD_NOTE, f'{self.URL_LOGIN}?next={self.URL_ADD_NOTE}'),
            (self.URL_DETAIL, f'{self.URL_LOGIN}?next={self.URL_DETAIL}'),
            (self.URL_SUCCESS, f'{self.URL_LOGIN}?next={self.URL_SUCCESS}'),
            (self.URL_DELETE, f'{self.URL_LOGIN}?next={self.URL_DELETE}'),
            (self.NOTES_LIST_URL,
             f'{self.URL_LOGIN}?next={self.NOTES_LIST_URL}'),
            (self.URL_EDIT_NOTE,
             f'{self.URL_LOGIN}?next={self.URL_EDIT_NOTE}'),
        )
        for url, redirect in urls:
            with self.subTest(name=url):
                self.assertRedirects(self.client.get(url), redirect)
