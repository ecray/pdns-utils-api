import os
import logging
import requests
import sys

from flask import abort, request, Flask
from instance.config import app_config

logger = logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("pdns-fetch")
handler = logging.StreamHandler()
formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


try:
    API_KEY = os.getenv('PDNS_API_KEY')
except LookupError:
    logger.debug(f"Missing API_KEY from environment")

URI = 'https://pdns-api.marqeta.com/api/v1/servers/localhost/zones'
HEADERS = {'X-API-Key': API_KEY}


def pdns_utils(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    @app.route('/fetch/')
    def query_next_ip(response=None):
        """ Query for next available IP in zone """
        if request.query_string:
            ra = request.args.to_dict()
        else:
            ra = dict()
        # Verify we got zone and origin
        if all(x in ra.keys() for x in ['zone', 'origin']):
            origin, zone, get_all = ra['origin'], \
                                    ra['zone'], \
                                    ra.get('all', None)
        else:
            abort(422)

        r = requests.get(URI + '/' + zone + '.', headers=HEADERS)

        logger.debug(f"Request Time For {r.url} - {r.elapsed.total_seconds()}")
        if r.status_code == 200:
            content = None
            data = r.json()['rrsets']
            content = [v['records'][0]['content'] for v in data
                       if v['type'] in 'A']
        elif r.status_code == 401:
            abort(401)
        else:
            abort(404)

        if content:
            """ collect and sort based on subnet """
            subnets = {}
            for i in content:
                net = '.'.join(i.split('.')[:3])
                ip = int(i.split('.')[3])
                if subnets.get(net, False):
                    subnets[net].append(ip)
                else:
                    subnets[net] = [ip]

            if subnets.get(origin, False):
                subnets[origin].sort()
            else:
                abort(404)

            """ find gaps in ips available in zone """
            ips = _find_gaps(subnets[origin])
            if get_all:
                response = []
                for ip in ips:
                    response.append(f"{origin}.{ip}")
            else:
                response = f"{origin}.{str(ips[0])}"

        return str(response)

    def _find_gaps(ips):
        # keeping ranges away from network device ranges
        start, end = 11, 250
        return list(set(range(start, end + 1)).difference(ips))

    return app
