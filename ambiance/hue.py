import os
from requests_oauthlib import OAuth2Session
from sanic import Blueprint, response
import aiohttp

# App Specific Codes
app_id = 'ambiance'
client_id = "4ZkvHrATYYgK5XvyvXvtJFkiTgHGZGqJ"
client_secret = "Wk36KI48MitiqyaT"

authorization_base_url = 'https://api.meethue.com/oauth2/auth'
token_url = 'https://api.meethue.com/oauth2/token'
api_url = 'https://api.meethue.com/bridge'
whitelist_url = 'https://api.meethue.com/bridge/0/config'
whitelist_body = {"linkbutton": True}
body_2 = {"devicetype": "huetest"}

bp = Blueprint('oauth_blueprint', url_prefix='/auth')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

whitelist_id = ''
token = None


def headers():
    return {"Authorization": "Bearer " + token['access_token'], "ContentType": "Application/JSON"}


def get_endpoint():
    return '%s/%s/lights' % (api_url, whitelist_id)


def set_endpoint(eid):
    return '%s/%s/lights/%s/state' % (api_url, whitelist_id, eid)


@bp.route("/login")
async def login(request):
    hue = OAuth2Session(client_id)
    authorization_url, state = hue.authorization_url(authorization_base_url, deviceid='ABCDEF', appid=app_id)
    request['session']['oauth_state'] = state
    return response.redirect(authorization_url)


@bp.route("/callback")
async def callback(request):
    global whitelist_id, token
    hue = OAuth2Session(client_id, state=request['session']['oauth_state'])
    token = hue.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    async with aiohttp.ClientSession() as session:
        await session.put(whitelist_url, json=whitelist_body, headers=headers())
        whitelist_resp = await (await session.post(api_url, json=body_2, headers=headers())).json()
        request['session']['whitelist_id'] = whitelist_resp[0]['success']['username']
        whitelist_id = request['session']['whitelist_id']

    return response.redirect('/status')


@bp.route("/logout")
async def login(request):
    global whitelist_url, token
    token = None
    whitelist_url = request['session']['whitelist_id'] = None
    return response.redirect('/status')


class HueAuth:
    def __init__(self, app):
        app.register_blueprint(bp)


async def get_lights():
    async with aiohttp.ClientSession() as session:
        async with session.get(get_endpoint(), headers=headers()) as resp:
            return await resp.json()


async def set_light(eid, hue, sat, bri):
    async with aiohttp.ClientSession() as session:
        payload = {
            'hue': int(hue),
            'sat': int(sat),
            'bri': bri
        }
        resp = await session.put(set_endpoint(eid), json=payload, headers=headers())


async def set_light_ct(eid, ct):
    async with aiohttp.ClientSession() as session:
        payload = {
            'ct': int(ct)
        }
        resp = await session.put(set_endpoint(eid), json=payload, headers=headers())
        print(await resp.json())


async def increment_light(eid, inc):
    # print("Incrementing: " + str(inc))
    async with aiohttp.ClientSession() as session:
        payload = {
            'ct_inc': int(inc)
        }
        resp = await session.put(set_endpoint(eid), json=payload, headers=headers())
        # print(await resp.json())
