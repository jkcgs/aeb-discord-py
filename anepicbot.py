#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import print_function
import discord, random, os, sys, time, json, subprocess, traceback
from urllib2 import urlopen

def m(client, message, what):
    client.send_message(message.channel, message.author.mention() + ' ' + what)

# último error
gf_last_error = False

# USD https://currency-api.appspot.com/api/usd/clp.json
usd_conv = False
try:
     res = urlopen("https://currency-api.appspot.com/api/usd/clp.json")
     usd_conv = json.loads(res.read())
except OSError as e:
    print("error al cargar datos de conversión de divisas")

man_meme = "es por ej: 'nombre url', como 'genial meme http://www.google.com' o 'xd http://xd.com' donde el ultimo elemento separado por espacios es el meme"
config_file = "config.json"
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

fb_loading = False
def fb_get_posts(pid):
    global fb_loading
    fb_loading = True
    res = urlopen("https://graph.facebook.com/v2.5/" + pid + "/posts?fields=link,message&access_token=" + config['fb_token'])
    cont = json.loads(res.read())
    fb_loading = False
    return cont["data"]

# Crear archivo de sesión si no existe
if not os.path.isfile(config_file):
    f = open(config_file, 'w+')
    f.write('{"email":"","password":"","fb_token:""}')
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

config = {}
with open(config_file) as f:
    config = json.loads(f.read())


if 'email' not in config or 'password' not in config:
    print("Configurar el archivo de sesión correctamente.")
    exit()
if config['email'] == "" or config['password'] == "":
    print("Completar la configuración de sesión.")
    exit()

if not config['fb_token']:
    print('Conexión con facebook no activada')
elif config["fb_token"] == '':
    print('Completar token de facebook')
    exit()

print("iniciando...")

client = discord.Client()
client.login(config['email'], config['password'])

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
    try:
        if is_master:

            if msg == '!reiniciate':
                print(message.author.name + " ha solicitado reiniciar")
                print("revisando si el archivo es compilable...")

                process = subprocess.Popen(["python", "-m", "py_compile", __file__], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                process.wait()
                out,_ = process.communicate()

                if process.returncode != 0:
                    print('')
                    client.send_message(message.channel, 'el programa tiene errores en el código, revísalo antes de reiniciar')
                    client.send_message(message.channel, 'puedes ver el último error con !lasterror')
                    last_error = out.decode("utf-8")
                    return

                print("código ok, reiniciando...")
                client.send_message(message.channel, 'voy y vuelvo... si me conecto es porque volvi xd')
                os.execv(__file__, sys.argv)

            if msg == "!lasterror":
                if gf_last_error:
                    m(client, message, gf_last_error)
                else:
                    m(client, message, 'no ha habido errores por el momento')

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
                linej = " ".join(line)

                if len(line) < 2:
                    m(client, message, 'escribe bien la wea po: ' + man_meme)
                    return

                quot = linej.find('"')
                if linej[(quot-1)] == " " and quot-1 != len(linej)-1 and linej[-1] == '"':
                    name = linej[0:(quot-1)]
                    val = linej[(quot+1):-1]
                else:
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

            elif msg == '!quiensoy':
                m(client, message, 'pa k kieres saber eso jaja saludos')

            elif msg == '!quieneres':
                m(client, message, 'soy el guason XD')

            elif msg == '!thisisgospel':
                rem_dif = int(tig_timeout - (time.time() - tig_last))
                if rem_dif <= 0:
                    client.send_message(message.channel, tig)
                    tig_last = time.time()
                else:
                    m(client, message, 'intenta de nuevo en unos ' + str(rem_dif) + ' seg y te la canto de nuevo')

            elif (msg.startswith("!usd ") or msg == "!usd") and usd_conv:
                rate = 1
                if msg != "!usd":
                    try: rate = float(msg.split(" ")[1])
                    except: pass

                client.send_message(message.channel, str(rate) + " usd = " + str(int(usd_conv["rate"] * rate)))

            elif msg == '!xd':
                m(client, message, random.choice(xd))

            elif msg == "!mysterion":
                if not fb_loading:
                    post = fb_get_posts("899097090126531")[0]
                    cont = u'último post de mr ion:\n' + post["message"] + '\nlink: ' + post["link"]
                    client.send_message(message.channel, cont.encode("utf-8"))

            elif msg == 'que buen bot':
                m(client, message, 'gracias bro a tu servisio jeje')

            elif msg == '!memes' and not is_master:
                client.send_message(message.channel, 'tengo ' + str(len(memes)) + (' memes' if len(memes) != 1 else ' meme'))

            elif msg.startswith("!meme ") or msg == "!meme":
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
            elif msg.startswith("!") and msg[1:] in memes:
                client.send_message(message.channel, memes[msg[1:]].strip())

    except Exception as e:
        client.send_message(message.channel, "ocurrió un error al ejecutar el último comando")
        client.send_message(message.channel, e)
        out = u'ocurrió un error al executar el comando \'' + msg + '\''
        print(out.encode("utf-8"))
        traceback.print_exc()
        last_error = e

@client.event
def on_ready():
    print('Logged in as ' + client.user.name + ', id: ' + client.user.id)
    print('------')

    #for channel in client.get_all_channels():
    #    client.send_message(channel, "wena cauros volvi")

try:
    client.run()
except KeyboardInterrupt:
    print("\ncerrado jeje aios")
