# -*- coding: utf-8 -*-

import sys

from model.ascii import ASCII
from model.base_64 import Base64
from model.date_time import DateTime
from model.html import Html
from model.javascript import Javascript
from model.md5 import MD5
from model.number import Number
from model.sha import SHA
from model.string import String
from model.the_uuid import TheUUID
from model.ip_addr import IPAddr
from workflow import Workflow, ICON_INFO

__version__ = "1.2.7"


class Hasher:
    def __init__(self, wf):
        self.wf = wf
        if self.wf.update_available:
            wf.add_item('New version available',
                        'Action this item to install the update',
                        autocomplete='workflow:update',
                        icon=ICON_INFO)

        self.models = [
            DateTime(),
            MD5(),
            Base64(),
            Html(),
            Javascript(),
            SHA(),
            Number(),
            ASCII(),
            TheUUID(),
            String(),
            IPAddr(),
        ]
        self.modelDict = dict()
        self.max_age = 60 * 60 * 24 * 365
        for m in self.models:
            self.modelDict[m.name] = m

    def convert(self, query):
        result = []
        result += self.autocomplete(query)
        result += self.sort_items(self.convert_by_type(query))
        result += self.sort_items(self.convert_all(query))

        self.add_to_wf(result)
        self.wf.send_feedback()

    def convert_all(self, query):
        result = []

        if not query:
            return result

        for m in self.models:
            result += m.convert(query)

        return result

    def convert_by_type(self, query):
        query = str(query).strip()
        if " " not in query:
            if query in self.modelDict:
                return self.modelDict[query].convert("")
        else:
            group = query.split(' ', 1)
            type_value = group[0]
            input_value = group[1]

            if type_value in self.modelDict:
                return self.modelDict[type_value].convert(input_value)

    def autocomplete(self, query):
        result = []

        if query.find(' ') >= 0:
            return result

        for m in self.models:
            result += m.autocomplete(query)

        return result

    def sort_items(self, items):
        if not items:
            return []

        def sort_by_usage(item):
            key = item.arg.split(":", 1)[0]
            count = self.wf.cached_data(key, max_age=self.max_age)
            if not count:
                return 0
            return count

        return sorted(items, reverse=True, key=sort_by_usage)

    def add_to_wf(self, items):
        for item in items:
            self.wf.add_item(
                title=item.title,
                subtitle=item.subtitle,
                modifier_subtitles=item.modifier_subtitles,
                arg=item.arg,
                autocomplete=item.autocomplete,
                valid=item.valid,
                uid=item.uid,
                icon=item.icon,
                icontype=item.icontype,
                type=item.type,
                largetext=item.largetext,
                copytext=item.copytext
            )


def main(wf):
    query = None

    if len(wf.args):
        query = wf.args[0]

    hasher = Hasher(wf)
    hasher.convert(query)


if __name__ == u"__main__":
    wf = Workflow(update_settings={
        'github_slug': 'dozer47528/alfred2-hasher',
        'version': __version__,
        'frequency': 1})

    sys.exit(wf.run(main))
