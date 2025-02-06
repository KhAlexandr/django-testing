from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note


User = get_user_model()


class TestNotesList(TestCase):
    NOTES_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        all_notes = [
            Note(
                title=f'Заметка{index}',
                text='Просто текст.',
                author=cls.author,
                slug=f'note-{index}'
            )
            for index in range(5)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(object_list[0], object_list)

    def test_reader_and_author_in_context_list(self):
        users = (
            (self.reader, 0),
            (self.author, 5),
        )
        for name, number in users:
            with self.subTest(name=name):
                self.client.force_login(name)
                response = self.client.get(self.NOTES_LIST_URL)
                object_list = response.context['object_list']
                self.assertEqual(len(object_list), number)


class TestAddandEditNotes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Николай Некрасов')
        cls.notes = Note.objects.create(
            title='Заметка',
            text='Случайный текст',
            author=cls.author
        )

    def test_form(self):
        self.client.force_login(self.author)
        urls = (
            ('notes:edit', (self.notes.slug,)),
            ('notes:add', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)