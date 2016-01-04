#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import print_function
import discord, random, os, sys, time, json

def m(client, message, what):
    client.send_message(message.channel, message.author.mention() + ' ' + what)

man_meme = "es por ej: 'nombre url', como 'genial meme http://www.google.com' o 'xd http://xd.com' donde el ultimo elemento separado por espacios es el meme"
login_file = "login.json"
memes_file = "memes.json"
masters_file = "masters.json"

def loadmemes():
    global memes
    memes = {}
    with open(memes_file) as f:
        memes = json.loads(f.read())

def setmeme(name, val):
    global memes

    memes[name] = val
    rewrite_memes()

    return True

def delmeme(name):
    global memes
    if name in memes:
        memes.pop(name)
        rewrite_memes()

def rewrite_memes():
    global memes
    with open(memes_file, "w") as f:
        f.write(json.dumps(memes))
    f.close()


# Crear archivo de sesión si no existe
if not os.path.isfile(login_file):
    f = open(login_file, 'w+')
    f.write('{"email":"","password":""}')
    f.close()

# Crear archivo de memes si no existe
if not os.path.isfile(memes_file):
    f = open(memes_file, 'w+')
    f.write("{}")
    f.close()

# Crear archivo de masters si no existe
if not os.path.isfile(masters_file):
    f = open(masters_file, 'w+')
    f.write("[]")
    f.close()

# memes
memes = {}
loadmemes()

# Archivos
tig = ""
with open("this_is_gospel.txt") as f:
    tig = f.read()

my_masters = []
with open(masters_file) as f:
    my_masters = json.loads(f.read())

xd = []
with open("xd.txt") as f:
    xd = f.readlines()

login = {}
with open(login_file) as f:
    login = json.loads(f.read())

if 'email' not in login or 'password' not in login:
    print("Configurar el archivo de sesión correctamente.")
    exit()
if login['email'] == "" or login['password'] == "":
    print("Completar la configuración de sesión.")
    exit()

print("iniciando...")

client = discord.Client()
client.login(login['email'], login.password)

tig_last = time.time() - 10
tig_timeout = 10

@client.event
def on_message(message):
    global tig_timeout, tig_last
    aid = message.author.id
    msg = message.content.strip()
    is_channel = isinstance(message.channel, discord.Channel)
    is_everyone = False
    is_master = aid in my_masters

    if is_channel:
        roles = message.author.roles;
        if len(roles) == 1 and roles[0].is_everyone():
            is_everyone = True


    if aid == client.user.id or is_everyone:
        return

    # COMANDOS PARA PROS
    if is_master:

        if msg == '!reiniciate':
            print(message.author.name + " ha solicitado reiniciar")
            client.send_message(message.channel, 'voy y vuelvo... si me conecto es porque volvi xd')
            os.execv(__file__, sys.argv)

        if msg == '!chaoctm':
            print(message.author.name + " ha solicitado apagar")
            client.send_message(message.channel, 'me boi u.u... chao cauroh')
            exit()

        if msg.startswith('!tigtimeout '):
            asd = msg.split(" ")
            try:
                if len(asd) < 2:
                    raise Exception()

                new_to = int(asd[1])
                if new_to > 0 and new_to <= 100:
                    tig_timeout = new_to
                    m(client, message, 'ahora puedo cantar This Is Gospel después de ' + str(new_to) + (' segundo' if new_to == 1 else ' segundos'))
                elif new_to <= 0:
                    m(client, message, 'no pos men pone un número entre 1 y 100')
                else:
                    m(client, message, 'no poh aweonaito pone algo entre 1 y 100')
            except:
                m(client, message, 'que mal meme viejo escribe bein la wea (!tigtimeout [1-100])')

        if msg.startswith('+meme ') or msg.startswith('++meme '):
            force = msg.startswith('++meme ')
            line = msg.split(" ")[1:]

            if len(line) < 2:
                m(client, message, 'escribe bien la wea po: ' + man_meme)
                return

            name = " ".join(line[:-1])
            val = line[-1]

            if not force and name in memes:
                m(client, message, 'ya existe el meme, usa ++meme para cambiarlo')
                return

            setmeme(name, val)
            m(client, message, 'meme agregado: "'+ name + '"')


        if msg.startswith('-meme '):
            name = " ".join(msg.split(" ")[1:])

            if name not in memes:
                m(client, message, 'no tengo ese meme wn aonde la vistes')
                return

            delmeme(name)
            m(client, message, 'meme borrado: "'+ name + '" u.u')

        if msg == "~meme":
            m(client, message, 'recargando memes...')
            loadmemes()
            m(client, message, 'memes recargados')

        if msg == "!memes":
            if len(memes) == 0:
                m(client, message, 'no tengo memes')
                return

            ms = "'" + "', '".join(list(memes.keys())) + "'"
            client.send_message(message.channel, 'tengo ' + str(len(memes)) + (' memes' if len(memes) != 1 else ' meme') + ': ' + ms)


    if msg == '!miid':
        if not is_channel:
            m(client, message, 'tu id es ' + aid)
        else:
            m(client, message, 'pídelo por privado')

    # COMANDOS PARA TODOS sólo por canal
    if is_channel or (not is_channel and is_master):

        if msg == '!moneda':
            moneda = random.random()
            if moneda < 0.02:
                m(client, message, 'canto')
            elif moneda >= 0.02 and moneda < 0.52:
                m(client, message, 'cara')
            else:
                m(client, message, 'sello')

        if msg == '!quiensoy':
            m(client, message, 'pa k kieres saber eso jaja saludos')

        if msg == '!quieneres':
            m(client, message, 'soy el guason XD')

        if msg == '!thisisgospel':
            rem_dif = int(tig_timeout - (time.time() - tig_last))
            if rem_dif <= 0:
                client.send_message(message.channel, tig)
                tig_last = time.time()
            else:
                m(client, message, 'intenta de nuevo en unos ' + str(rem_dif) + ' seg y te la canto de nuevo')

        if msg == '!xd':
            m(client, message, random.choice(xd))

        if msg == 'que buen bot':
            m(client, message, 'gracias bro a tu servisio jeje')

        if msg == '!memes' and not is_master:
            client.send_message(message.channel, 'tengo ' + str(len(memes)) + (' memes' if len(memes) != 1 else ' meme'))

        if msg.startswith("!meme ") or msg == "!meme":
            if len(memes) == 0:
                m(client, message, 'no hay stock de memes ahora')
                return

            meme = ""
            if len(msg.split(" ")) == 1:
                k = random.choice(list(memes.keys()))
                meme = k
            else:
                meme = " ".join(msg.split(" ")[1:])

            if meme in memes:
                client.send_message(message.channel, memes[meme].strip())
            else:
                m(client, message, 'sorry m4n no tengo ese miim')

@client.event
def on_ready():
    print('Logged in as ' + client.user.name + ', id: ' + client.user.id)
    print('------')

    #for channel in client.get_all_channels():
    #    client.send_message(channel, "wena cauros volvi")

client.run()
