from civomega import Parser, Match
from jinja2 import Environment, PackageLoader
from civomega.registry import REGISTRY
from random import Random
from flask import request

env = Environment(loader=PackageLoader('civomega', 'templates'))

import os
import re
import json
import requests

SIMPLE_PATTERN = re.compile('^\s*is\s(?P<name>(\s?\w+)+)\s(?:a|the)\swerewolf',re.IGNORECASE)

class WerewolfParser(Parser):
    def search(self, s):
        if SIMPLE_PATTERN.match(s):
            d = SIMPLE_PATTERN.match(s).groupdict()
            noun = d['name'].strip()
            if(noun[-1] == '?'):
                noun = noun[0:-1]
            return WerewolfMatch(noun)
        return None

class WerewolfMatch(Match):
    def __init__(self, noun):
        self.name = noun
        r = Random()
        r.seed(request.remote_addr)
        self.is_werewolf = r.choice([True, False])
        self.data = {
          'is_werewolf': self.is_werewolf,
          'name': self.name
        }

    def as_json(self):
        return json.dumps(self.data)

    def as_html(self):
        template = env.get_template('werewolf/werewolf_search.html')
        return template.render(**self.data)

REGISTRY.add_parser('werewolf_search', WerewolfParser)
