from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass
from notes.forms import NoteForm


User = get_user_model()


class TestNotesContent(BaseTestClass):

    def test_notes_list(self):
        response = self.auth_client.get(self.NOTES_LIST_URL)
        notes = response.context['note_list']
        self.assertIn(self.note, notes)
        for note in notes:
            self.assertContains(response, note.title)
            self.assertContains(response, note.author)
            self.assertContains(response, note.slug)

    def test_form_on_notes_edit_and_add_pages(self):
        urls = (
            ('notes:edit', self.URL_EDIT_NOTE),
            ('notes:add', self.URL_ADD_NOTE),
        )
        for url, url_name in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url_name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
