from http import HTTPStatus

from notes.models import Note
from .base_class import BaseTestClass, UrlManager

from pytils.translit import slugify


class TestNoteCreation(BaseTestClass):

    def test_anonymous_cant_create_note(self):
        initial_notes = set(Note.objects.all())
        response = self.client.post(
            UrlManager.URL_ADD_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        final_notes = set(Note.objects.all())
        self.assertEqual(initial_notes, final_notes)

    def test_note_creation_auth_client(self):
        initial_notes = set(Note.objects.all())
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        final_notes = set(Note.objects.all())
        new_notes = final_notes - initial_notes
        self.assertTrue(len(new_notes) == 1)
        note = new_notes.pop()
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_two_identical_slug(self):
        initial_notes = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        final_notes = set(Note.objects.all())
        self.assertEqual(initial_notes, final_notes)

    def test_empty_slug(self):
        initial_notes = set(Note.objects.all())
        self.form_data.pop('slug')
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        final_notes = set(Note.objects.all())
        new_notes = final_notes - initial_notes
        self.assertTrue(len(new_notes) + 1)
        note = new_notes.pop()
        self.assertEqual(note.slug, slugify(self.form_data['title']))
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.user)

    def test_author_delete_note(self):
        initial_notes = set(Note.objects.all())
        response = self.auth_client.delete(UrlManager.URL_DELETE)
        self.assertRedirects(response, UrlManager.URL_SUCCESS)
        final_notes = set(Note.objects.all())
        self.assertEqual(len(final_notes), len(initial_notes) - 1)

    def test_user_cant_delete_note_of_another_user(self):
        initial_notes = set(Note.objects.all())
        response = self.reader_client.delete(UrlManager.URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        final_notes = set(Note.objects.all())
        self.assertEqual(initial_notes, final_notes)

    def test_author_edit_note(self):
        response = self.auth_client.post(
            UrlManager.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertRedirects(response, UrlManager.URL_SUCCESS)
        note = set(Note.objects.all()).pop()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            UrlManager.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = set(Note.objects.all()).pop()
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
