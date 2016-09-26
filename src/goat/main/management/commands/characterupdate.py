import requests
from django.core.management.base import BaseCommand, CommandError
from main.models import *

base_url = 'http://render-api-us.worldofwarcraft.com/static-render/us/'

def character_exists(name, server):
    r = requests.get('https://us.api.battle.net/wow/character/{}/{}?fields=items&locale=en_US&apikey=zpwrz24xqd8yhmhk2uv8b4qr5gv6ecef'.format(server, name))
    return r.ok


def update_character(char):
    print("Getting info for: {}".format(char.name))
    try:
        r = requests.get('https://us.api.battle.net/wow/data/character/classes?locale=en_US&apikey=zpwrz24xqd8yhmhk2uv8b4qr5gv6ecef')
        classes = r.json()['classes']

        r = requests.get('https://us.api.battle.net/wow/character/{}/{}?fields=items&locale=en_US&apikey=zpwrz24xqd8yhmhk2uv8b4qr5gv6ecef'.format(char.realm, char.name))
        character = r.json()

        #char.level = character['level']
        char.portrait = base_url + character['thumbnail']
        char.ilvl = character['items']['averageItemLevel']
        for class_name in classes:
            if character['class'] == class_name['id']:
                name = class_name['name']
                name = name.replace(' ', '_')
                char.wowclass = name

        char.save()
    except Exception as e:
        print("There was an error getting!")
        print(e)
        return e

class Command(BaseCommand):
    help = 'A test'

    def handle(self, *args, **options):
        self.stdout.write('Beginning character update...')
        for char in Character.objects.all():
            update_character(char)

