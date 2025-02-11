from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note


User = get_user_model()

NOTE_SLUG = 'zametka'


class UrlManager:
    NOTES_LIST_URL = reverse('notes:list')
    URL_HOME = reverse('notes:home')
    URL_LOGIN = reverse('users:login')
    URL_LOGOUT = reverse('users:logout')
    URL_SIGN_UP = reverse('users:signup')
    URL_EDIT_NOTE = reverse('notes:edit', args=(NOTE_SLUG,))
    URL_ADD_NOTE = reverse('notes:add')
    URL_SUCCESS = reverse('notes:success')
    URL_DELETE = reverse('notes:delete', args=(NOTE_SLUG,))
    URL_DETAIL = reverse('notes:detail', args=(NOTE_SLUG,))
    REDIRECT_URL_ADD_NOTE = f'{URL_LOGIN}?next={URL_ADD_NOTE}'
    REDIRECT_URL_DETAIL = f'{URL_LOGIN}?next={URL_DETAIL}'
    REDIRECT_URL_SUCCESS = f'{URL_LOGIN}?next={URL_SUCCESS}'
    REDIRECT_URL_DELETE = f'{URL_LOGIN}?next={URL_DELETE}'
    REDIRECT_URL_NOTES_LIST = f'{URL_LOGIN}?next={NOTES_LIST_URL}'
    REDIRECT_URL_EDIT = f'{URL_LOGIN}?next={URL_EDIT_NOTE}'


class BaseTestClass(TestCase):

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
            slug=NOTE_SLUG,
            author=cls.user,
        )
        cls.form_data = {
            'title': 'Заметки',
            'text': 'Просто текст',
            'slug': 'note-slug',
        }
