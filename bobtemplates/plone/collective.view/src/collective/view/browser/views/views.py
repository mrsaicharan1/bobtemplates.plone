# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView


class DemoView(BrowserView):
    def the_title(self):
        return u'A list of talks:'
