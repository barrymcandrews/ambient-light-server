#!/usr/bin/env python3.7
from signal import signal, SIGINT

from sanic import Sanic
from ambiance.web import bp
from ambiance import mqtt
import uvloop
import asyncio
import os
import ambiance.configuration as config

app = Sanic(__name__)


def main():
    app.config.LOGO = config.GeneralOptions.logo
    app.blueprint(bp)
    server = app.create_server(host=config.WebOptions.hostname,
                               port=config.WebOptions.port,
                               debug=config.WebOptions.debug)

    asyncio.set_event_loop(uvloop.new_event_loop())
    loop = asyncio.get_event_loop()

    web_task = asyncio.ensure_future(server)
    mqtt_task = asyncio.ensure_future(mqtt.start_client())

    signal(SIGINT, lambda s, f: loop.stop())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        os._exit(0)


if __name__ == '__main__':
    main()
