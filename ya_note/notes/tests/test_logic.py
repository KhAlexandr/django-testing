from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add', args=None)
        cls.user = User.objects.create(username='Иосиф Сталин')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': 'Заголовок',
            'text': 'Текст',
        }

    def test_create_note(self):
        users = (
            (self.client.post, 0),
            (self.auth_client.post, 1)
        )
        for name, number in users:
            with self.subTest(name=name):
                name(self.url, data=self.form_data)
                notes_count = Note.objects.count()
                self.assertEqual(notes_count, number)
                if number > 0:
                    note = Note.objects.get()
                    self.assertEqual(note.text, 'Текст')
                    self.assertEqual(note.title, 'Заголовок')
                    self.assertEqual(note.author, self.user)

    def test_two_identical_slug(self):
        self.auth_client.post(self.url, data=self.form_data)
        slug = Note.objects.count()
        self.assertEqual(slug, 1)
        self.auth_client.post(self.url, data=self.form_data)
        new_slug = Note.objects.count()
        self.assertEqual(new_slug, 1)

    def test_empty_slug(self):
        self.auth_client.post(self.url, data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(note.slug, 'zagolovok')


class TestNoteEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор комментария')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )
        cls.note_url = reverse('notes:success', args=None)
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'text': 'Текст',
            'title': 'Заголовок'
        }

    def test_author_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.note_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 0)

    def test_user_cant_delete_not_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_edit_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, self.note_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, 'Текст')
        self.assertEqual(self.note.title, 'Заголовок')

    def test_user_cant_edit_note_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, 'Текст')
        self.assertEqual(self.note.title, 'Заголовок')
