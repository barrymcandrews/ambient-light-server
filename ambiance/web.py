import asyncio
from sanic import Blueprint, response
from sanic.response import html
from jinja2 import Environment, PackageLoader, select_autoescape
from ambiance import mqtt
from ambiance import hue
from ambiance import algorithm

bp = Blueprint(__name__)
bp.static('/static', './ambiance/static')
env = Environment(loader=PackageLoader('ambiance', 'templates'), autoescape=select_autoescape(['html', 'xml']))


@bp.route('/')
def root(request):
    template = env.get_template('index.j2')
    content = template.render(data=algorithm.last_measurement, data_exists=(algorithm.last_measurement is not None))
    return html(content)


@bp.post('/data')
def data(request):
    return response.redirect('/')


@bp.route('/lights')
async def lights_ep(request):
    template = env.get_template('lights.j2')
    lights_status = (await hue.get_lights()) if hue.token is not None else {}
    content = template.render(lights=lights_status)
    return html(content)


@bp.route('/sensors')
def sensors(request):
    template = env.get_template('sensors.j2')

    content = template.render(sensors=enumerate(mqtt.devices))
    return html(content)


@bp.route('/status')
def status(request):
    template = env.get_template('status.j2')

    hue_connected = 'whitelist_id' in request['session']
    content = template.render(mqtt_connected=mqtt.connected,
                              hue_connected=hue_connected)
    return html(content)


@bp.post('/demo')
async def demo(request):
    asyncio.ensure_future(algorithm.demo())
    return response.redirect('/')
