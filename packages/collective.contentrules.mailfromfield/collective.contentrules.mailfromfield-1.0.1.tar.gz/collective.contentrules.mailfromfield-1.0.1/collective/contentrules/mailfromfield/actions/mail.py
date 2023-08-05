# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_base
from collective.contentrules.mailfromfield import messageFactory as _, logger
from OFS.SimpleItem import SimpleItem
from plone.app.contentrules.actions.mail import MailAddForm
from plone.app.contentrules.actions.mail import MailEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IRuleElementData, IExecutable
from plone.registry.interfaces import IRegistry
from plone.stringinterp.interfaces import IStringInterpolator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from six.moves import filter
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.interface import implementer
from zope.interface import Interface

import six


class IMailFromFieldAction(Interface):
    """Definition of the configuration available for a mail action
    """

    subject = schema.TextLine(
        title=_(u"Subject"),
        description=_(u"Subject of the message"),
        required=True,
    )

    source = schema.TextLine(
        title=_(u"Sender email"),
        description=_(
            u"The email address that sends the email. If no email is "
            u"provided here, it will use the portal from address."
        ),
        required=False,
    )

    fieldName = schema.TextLine(
        title=_(u"Source field"),
        description=_(
            u"Put there the field name from which get the e-mail. "
            u"You can provide an attribute name, a method name, an AT field name or "
            u"ZMI property"
        ),
        required=True,
    )

    target = schema.Choice(
        required=True,
        title=_(u"Target element"),
        description=_(
            "help_target",
            default=(
                u"Choose to get the address info from: the container "
                u"where the rule is activated on, the content who triggered "
                u"the event or the parent of the triggering content."
            ),
        ),
        default="object",
        vocabulary="collective.contentrules.mailfromfield.vocabulary.targetElements",
    )

    message = schema.Text(
        title=_(u"Mail message"),
        description=_(
            "help_message",
            default=u"Type in here the message that you want to mail. You can "
            u"use some dynamic strings that will be replaced with relative "
            "values. See Substitutions table to see all available options.",
        ),
        required=True,
    )


@implementer(IMailFromFieldAction, IRuleElementData)
class MailFromFieldAction(SimpleItem):
    """
    The implementation of the action defined before
    """

    subject = u""
    source = u""
    fieldName = u""
    target = u""
    message = u""

    element = "plone.actions.MailFromField"

    @property
    def summary(self):
        return _(
            "action_summary",
            default=u'Email to users defined in the "${fieldName}" data',
            mapping=dict(fieldName=self.fieldName),
        )


@implementer(IExecutable)
@adapter(Interface, IMailFromFieldAction, Interface)
class MailActionExecutor(object):
    """The executor for this action.
    """

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event
        self.portal = self.get_portal()
        self.mapping = self.get_mapping()

    def get_portal(self):
        """Get's the portal object
        """
        urltool = getToolByName(aq_inner(self.context), "portal_url")
        return urltool.getPortalObject()

    def get_mapping(self):
        """Return a mapping that will replace markers in the template
        """
        obj_title = safe_unicode(self.event.object.Title())
        event_url = self.event.object.absolute_url()
        section_title = safe_unicode(self.context.Title())
        section_url = self.context.absolute_url()
        return {
            # "url": event_url,
            # "title": obj_title,
            "section_name": section_title,
            "section_url": section_url,
        }

    def expand_markers(self, text):
        """Replace markers in text with the values in the mapping
        """
        for key, value in six.iteritems(self.mapping):
            if not isinstance(value, six.text_type):
                value = value.decode("utf-8")
            text = text.replace("${%s}" % key, value)
        return text

    def get_from(self):
        """Get the from address
        """
        source = self.element.source
        if source:
            return source

        # no source provided, looking for the site wide "from" email address
        from_address = None
        registry = getUtility(IRegistry)
        record = registry.records.get("plone.email_from_address", None)
        if record:
            from_address = record.value

        if not from_address:
            raise ValueError(
                "You must provide a source address for this "
                "action or enter an email in the portal "
                "properties"
            )

        from_name = ""
        record_name = registry.records.get("plone.email_from_name", None)
        if record_name:
            from_name = record_name.value
        source = ("%s <%s>" % (from_name, from_address)).strip()
        return source

    def get_target_obj(self):
        """Get's the target object, i.e. the object that will provide the field
        with the email address
        """
        target = self.element.target
        if target == "object":
            obj = self.context
        elif target == "parent":
            obj = self.event.object.aq_parent
        elif target == "target":
            obj = self.event.object
        else:
            raise ValueError(target)
        return aq_base(aq_inner(obj))

    def get_recipients(self):
        """
        The recipients of this mail
        """
        # Try to load data from the target object
        fieldName = str(self.element.fieldName)
        obj = self.get_target_obj()

        # 1: object attribute
        try:
            attr = obj.__getattribute__(fieldName)
            # 3: object method
            if hasattr(attr, "__call__"):
                recipients = attr()
                logger.debug("getting e-mail from %s method" % fieldName)
            else:
                recipients = attr
                logger.debug("getting e-mail from %s attribute" % fieldName)
        except AttributeError:
            # 2: try with AT field
            # if IBaseContent.providedBy(obj):
            #     field = obj.getField(fieldName)
            #     if field:
            #         recipients = field.get(obj)
            #     else:
            #         recipients = False
            # else:
            #     recipients = False
            # if not recipients:
            #     recipients = obj.getProperty(fieldName, [])
            #     if recipients:
            #         logger.debug('getting e-mail from %s CMF property'
            #                      % fieldName)
            # else:
            #     logger.debug('getting e-mail from %s AT field' % fieldName)
            pass

        # maybe for some reason we could execute this action without any
        # recipients. It can't be that the page breaks due to this kind
        # of problem
        if not recipients:
            return []

        # now transform recipients in a iterator, if needed
        if type(recipients) == str or type(recipients) == six.text_type:
            recipients = [str(recipients)]
        return list(filter(bool, recipients))

    def get_mailhost(self):
        """
        The recipients of this mail
        """
        mailhost = getToolByName(aq_inner(self.context), "MailHost")
        if not mailhost:
            error = "You must have a Mailhost utility to execute this action"
            raise ComponentLookupError(error)
        return mailhost

    def __call__(self):
        """
        Does send the mail
        """
        mailhost = self.get_mailhost()
        source = self.get_from()
        recipients = self.get_recipients()

        obj = self.event.object

        interpolator = IStringInterpolator(obj)

        # No way to use self.context (where rule is fired) in interpolator
        # self.context in interpolator is the obj given
        # And having  two interpolators is strange, because they
        # both adapt fully. Unless you can somehow adapt it to
        # 'firing a rule' event, which isn't available to my knowledge.

        # Section title/urk
        subject = self.expand_markers(self.element.subject)
        message = self.expand_markers(self.element.message)
        # All other stringinterp
        subject = interpolator(self.element.subject).strip()
        message = interpolator(self.element.message).strip()

        email_charset = None
        registry = getUtility(IRegistry)
        record = registry.records.get("plone.email_charset", None)
        if record:
            email_charset = record.value

        for email_recipient in recipients:
            logger.debug("sending to: %s" % email_recipient)
            mailhost.send(
                message,
                mto=email_recipient,
                mfrom=source,
                subject=subject,
                charset=email_charset,
            )
        return True


class MailFromFieldAddForm(MailAddForm):

    schema = IMailFromFieldAction
    Type = MailFromFieldAction


class MailFromFieldAddFormView(ContentRuleFormWrapper):
    form = MailFromFieldAddForm


class MailFromFieldEditForm(MailEditForm):

    schema = IMailFromFieldAction


class MailFromFieldEditFormView(ContentRuleFormWrapper):
    form = MailFromFieldEditForm
