from http import HTTPStatus

from notes.models import Note
from ya_note.notes.tests.base_class import BaseTestClass

from pytils.translit import slugify


class TestNoteCreation(BaseTestClass):

    def test_anonymous_cant_create_note(self):
        self.client.post(self.URL_ADD_NOTE, data=self.form_data)
        new_note = Note.objects.get()
        self.assertEqual(self.note, new_note)

    def test_note_creation_auth_client(self):
        notes_count = Note.objects.count()
        self.auth_client.post(self.URL_ADD_NOTE, data=self.form_data)
        new_notes_count = Note.objects.count()
        self.assertEqual(new_notes_count, notes_count + 1)
        note = Note.objects.latest('id')
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_two_identical_slug(self):
        self.form_data['slug'] = self.note.slug
        self.auth_client.post(self.URL_ADD_NOTE, data=self.form_data)
        new_note = Note.objects.get()
        self.assertEqual(self.note.slug, new_note.slug)
        self.assertEqual(self.note.title, new_note.title)
        self.assertEqual(self.note.slug, new_note.slug)
        self.assertEqual(self.note.author, new_note.author)

    def test_empty_slug(self):
        self.form_data.pop('slug')
        self.auth_client.post(self.URL_ADD_NOTE, data=self.form_data)
        note = Note.objects.latest('id')
        self.assertEqual(note.slug, slugify(self.form_data['title']))
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.user)

    def test_author_delete_note(self):
        notes_count = Note.objects.count()
        response = self.auth_client.delete(self.URL_DELETE)
        self.assertRedirects(response, self.URL_SUCCESS)
        new_notes_count = Note.objects.count()
        self.assertEqual(new_notes_count, notes_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get()
        self.assertEqual(note.author, self.user)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)

    def test_author_edit_note(self):
        response = self.auth_client.post(
            self.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertRedirects(response, self.URL_SUCCESS)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, note.author)
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            self.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get()
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(note.author, note.author)
