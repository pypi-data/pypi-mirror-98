# -*- coding: utf-8 -*-
"""Init and utils."""
from plone import api
from zope.i18nmessageid import MessageFactory

HAS_PLONE_5 = api.env.plone_version().startswith("5")
_ = MessageFactory("collective.pivot")
