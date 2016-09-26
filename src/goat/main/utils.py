import requests

def character_exists(name, server, apikey):
    r = requests.get(
        'https://us.api.battle.net/wow/character/{}/{}?fields=items&locale=en_US&apikey={}'
         .format(server, name, apikey))
    return r.ok


def update_character(char, apikey):
    print("Getting info for: {}".format(char.name))
    try:
        r = requests.get(
            'https://us.api.battle.net/wow/data/character/classes?locale=en_US&apikey={}'
            .format(apikey))
        classes = r.json()['classes']

        r = requests.get('https://us.api.battle.net/wow/character/{}/{}?fields=items&locale=en_US&apikey={}'
                         .format(char.realm, char.name, apikey))
        character = r.json()

        char.level = character['level']
        char.ilvl = character['items']['averageItemLevel']
        portrait_url = "http://render-api-us.worldofwarcraft.com/static-render/us/{}"
        char.portrait = portrait_url.format(character['thumbnail'])
        for class_name in classes:
            if character['class'] == class_name['id']:
                name = class_name['name']
                if name == 'Demon Hunter':
                    name = 'Demon_Hunter'
                if name == 'Death Knight':
                    name = 'Death_Knight'
                char.wowclass = name

        char.save()
    except Exception as e:
        print("There was an error getting!")
        return e
