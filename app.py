from flask import Flask, render_template, Markup
from flask.globals import request
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
temp = dotenv_values(".env")
authone = "12886028"
authtwo = "thais1805"


auth = HTTPBasicAuth(authone, authtwo)


def timestamp_to_datetime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


app = Flask(__name__, static_folder='static')
app.jinja_env.filters['timestamp_to_datetime'] = timestamp_to_datetime
app.jinja_env.globals['Markup'] = Markup


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/', methods=['GET', 'POST'])
def get_player_data():
    nome = request.form['nome']
    url = f"https://medivia.online/api/public/player/{nome}"
    username = authone
    password = authtwo

    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        charinfo = response.json()

        playername = charinfo['player']['name']
        playervoc = charinfo['player']['vocation']
        currentexp = charinfo['player']['experience']
        currentexp_formatted = "{:,}".format(currentexp)
        level = charinfo['player']['level']
        next_level = level + 1
        exp_next_level = (50 * (next_level - 1) ** 3 - 150 * (next_level - 1) ** 2 + 400 * (next_level - 1)) // 3
        dif = exp_next_level - currentexp
        dif_formatted = "{:,}".format(dif)
        currentlevelexp = (50 * (level - 1) ** 3 - 150 * (level - 1) ** 2 + 400 * (level - 1)) // 3
        porcentagem = ((currentexp - currentlevelexp) / (exp_next_level - currentlevelexp)) * 100
        porcentagem_rounded = round(porcentagem, 2)
        porcentagem_formatted = "{:.2f}%".format(porcentagem_rounded)

        ########MainFactions################
        imperial = "Lightbringer Heroes"

        demonic = "Dreadlord"
        archini = "Ancient Watchers"
        grim = "Dark Grims"
        aividem = "Ritualist"
        bishop = "Icons of Light"
        has_imperial = imperial in response.text
        has_demonic = demonic in response.text
        has_grim = grim in response.text
        has_bishop = bishop in response.text
        has_aividem = aividem in response.text
        has_archini = archini in response.text
        ####################################
        ##########SHORTCUTS################
        lbcamp = "Cyclops Warriors"
        abomahell = "Abominations"
        ##minerva being checked with if##
        awacess = "Saequr"
        bnwacess = "Shadow Guards"
        fdraft = "Frost Drakes"
        has_bnwacess = bnwacess in response.text
        has_lbcamp = lbcamp in response.text
        has_abomahell = abomahell in response.text
        has_awacess = awacess in response.text
        has_fdraft = fdraft in response.text







        ####################################


        #########subs############
        mino = "General Manos"
        dwarf = "Corrupted Watchers"
        elf = "Hadrian the Crusher"
        orc = "Elf Swordmasters"
        honou = "Honou"
        rose = "Azure Mercenaries"

        has_mino = mino in response.text
        has_dwarf = dwarf in response.text
        has_elf = elf in response.text
        has_orc = orc in response.text
        has_honou = honou in response.text
        has_rose = rose in response.text
        ###########################

        if 'deaths' in charinfo['player']:
            deaths = charinfo['player']['deaths']
        else:
            deaths = None

        if 'kills' in charinfo['player']:
            kills = charinfo['player']['kills']
        else:
            kills = None

        if 'guild' in charinfo['player']:
            guild = charinfo['player']['guild']
            has_guild = guild['name']
            guild_id = guild['id']
        else:
            guild = ""
            has_guild = ""
            guild_id = ""

        if 'Undead Dragons' in response.text and 'Shadow Drakes' in response.text:
            lightbringer = "True"
        else:
            lightbringer = "False"

        if rose in response.text and abomahell in response.text:
            minerva = "True"
        else:
            minerva = "False"



        return render_template(
            "index.html",
            level=level,
            playername=playername,
            percentage=porcentagem_formatted,
            rawpercentage=porcentagem,
            currentexp=currentexp_formatted,
            playervoc=playervoc,
            dif=dif_formatted,
            has_honou=has_honou,
            has_bishop=has_bishop,
            deaths=deaths,
            kills=kills,
            has_aividem=has_aividem,
            has_archini=has_archini,
            guild=has_guild,
            guild_id=guild_id,
            has_mino=has_mino,
            has_dwarf=has_dwarf,
            has_elf=has_elf,
            has_orc=has_orc,
            has_demonic=has_demonic,
            has_grim=has_grim,
            has_imperial=has_imperial,
            has_lightbringer=lightbringer,
            has_rose=has_rose,
            minerva=minerva,
            has_lbcamp=has_lbcamp,
            has_abomahell=has_abomahell,
            has_bnwacess=has_bnwacess,
            has_awacess=has_awacess,
            has_fdraft=has_fdraft
        )
    else:
        return {'error': 'Erro ao acessar a API'}, response.status_code


if __name__ == "__main__":
    app.run(debug=True)
