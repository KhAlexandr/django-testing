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
        initial_notes = set(Note.objects.all())
        self.form_data['slug'] = self.note.slug
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        self.assertEqual(initial_notes, set(Note.objects.all()))

    def test_empty_slug(self):
        initial_notes = set(Note.objects.all())
        self.form_data.pop('slug')
        self.auth_client.post(UrlManager.URL_ADD_NOTE, data=self.form_data)
        final_notes = set(Note.objects.all())
        new_notes = final_notes - initial_notes
        self.assertEqual(len(new_notes), 1)
        note = new_notes.pop()
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
        self.assertFalse(Note.objects.filter(
            slug=self.note.slug,
            text=self.note.text,
            title=self.note.title,
            author=self.note.author,
        ).exists())

    def test_user_cant_delete_note_of_another_user(self):
        first_count = Note.objects.count()
        response = self.reader_client.delete(UrlManager.URL_DELETE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        final_count = Note.objects.count()
        self.assertEqual(final_count, first_count)
        self.assertTrue(Note.objects.filter(
            slug=self.note.slug,
            text=self.note.text,
            title=self.note.title,
            author=self.note.author,
        ).exists())
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
        note = set(Note.objects.filter(id=self.note.id)).pop()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(
            UrlManager.URL_EDIT_NOTE, data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note = set(Note.objects.filter(id=self.note.id)).pop()
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.slug, note.slug)
