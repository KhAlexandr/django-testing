from django.contrib.auth import get_user_model

from .base_class import BaseTestClass, UrlManager
from notes.forms import NoteForm


User = get_user_model()


class TestNotesContent(BaseTestClass):

    def test_notes_list(self):
        response = self.auth_client.get(UrlManager.NOTES_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(UrlManager.NOTES_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_on_notes_edit_and_add_pages(self):
        urls = (UrlManager.URL_EDIT_NOTE, UrlManager.URL_ADD_NOTE)
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
