from phonebook_django.settings import LAST_UPDATE


def get_last_update(request):
    last_update = {'last_update': LAST_UPDATE}
    return last_update
