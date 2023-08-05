# -*- coding: utf-8 -*-

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1
    from zope.schema.interfaces import IVocabularyFactory

from zope.interface import implementer
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.contentrules.mailfromfield import messageFactory as _


@implementer(IVocabularyFactory)
class TargetElementsVocabulary(object):
    """Vocabulary factory for possible rule target
    """

    def __call__(self, context):
        return SimpleVocabulary(
            [
                SimpleTerm(u"object", u"object", _(u"From rule's container")),
                SimpleTerm(
                    u"target",
                    u"target",
                    _(u"From content that triggered the event"),
                ),
                SimpleTerm(u"parent", u"parent", _(u"From content's parent")),
            ]
        )


targetElements = TargetElementsVocabulary()
