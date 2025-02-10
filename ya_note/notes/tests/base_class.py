from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note


User = get_user_model()


class BaseTestClass(TestCase):
    NOTES_LIST_URL = reverse('notes:list', args=None)
    URL_HOME = reverse('notes:home', args=None)
    URL_LOGIN = reverse('users:login', args=None)
    URL_LOGOUT = reverse('users:logout', args=None)
    URL_SIGN_UP = reverse('users:signup', args=None)
    NOTE_SLUG = 'zametka'
    URL_EDIT_NOTE = reverse('notes:edit', args=(NOTE_SLUG,))
    URL_ADD_NOTE = reverse('notes:add', args=None)
    URL_SUCCESS = reverse('notes:success', args=None)
    URL_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
    URL_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Иосиф Сталин')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug=BaseTestClass.NOTE_SLUG,
            author=cls.user,
        )
        cls.form_data = {
            'title': 'Заметки',
            'text': 'Просто текст',
            'slug': 'note-slug',
        }
