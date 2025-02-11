from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .base_class import BaseTestClass, UrlManager


class TestNoteCreation(BaseTestClass):

    def test_anonymous_cant_create_note(self):
        notes = set(Note.objects.all())
        response = self.client.post(
            UrlManager.URL_ADD_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(notes, set(Note.objects.all()))

    def test_note_creation_auth_client(self):
        notes = set(Note.objects.all())
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.user)

    def test_two_identical_slug(self):
        notes = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        self.assertEqual(notes, set(Note.objects.all()))

    def test_empty_slug(self):
        notes = set(Note.objects.all())
        self.form_data.pop('slug')
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, slugify(self.form_data['title']))
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.author, self.user)

    def test_author_delete_note(self):
        first_count = Note.objects.count()
        response = self.auth_client.delete(UrlManager.URL_DELETE)
        self.assertRedirects(response, UrlManager.URL_SUCCESS)
        final_count = Note.objects.count()
        self.assertEqual(final_count, first_count - 1)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cant_delete_note_of_another_user(self):
        notes = set(Note.objects.all())
        first_count = Note.objects.count()
        response = self.reader_client.delete(UrlManager.URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        final_count = Note.objects.count()
        self.assertEqual(final_count, first_count)
        self.assertEqual(notes, set(Note.objects.all()))
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.author, self.note.author)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)

    def test_author_edit_note(self):
        response = self.auth_client.post(
            UrlManager.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertRedirects(response, UrlManager.URL_SUCCESS)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            UrlManager.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
