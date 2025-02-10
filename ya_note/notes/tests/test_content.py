from django.contrib.auth import get_user_model

from ya_note.notes.tests.base_class import BaseTestClass
from notes.forms import NoteForm


User = get_user_model()


class TestNotesContent(BaseTestClass):

    def test_notes_list(self):
        response = self.auth_client.get(self.NOTES_LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        note = notes[0]
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)

    def test_note_not_in_list_for_another_user(self):
        response = self.reader_client.get(self.NOTES_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_form_on_notes_edit_and_add_pages(self):
        urls = (self.URL_EDIT_NOTE, self.URL_ADD_NOTE)
        for url in urls:
            with self.subTest(url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
