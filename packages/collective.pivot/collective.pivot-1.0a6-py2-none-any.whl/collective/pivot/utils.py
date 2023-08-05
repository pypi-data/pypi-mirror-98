# -*- coding: utf-8 -*-
from plone import api
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain


def _(msgid, context, domain="collective.pivot", mapping=None):
    translation_domain = queryUtility(ITranslationDomain, domain)
    return translation_domain.translate(msgid, context=context.REQUEST, mapping=mapping)


def add_family(context, family_id, title):
    """Add a family in the configuration folder"""
    Family = api.content.create(
        container=context, type="collective.pivot.Family", family=family_id, title=title
    )
    return Family
