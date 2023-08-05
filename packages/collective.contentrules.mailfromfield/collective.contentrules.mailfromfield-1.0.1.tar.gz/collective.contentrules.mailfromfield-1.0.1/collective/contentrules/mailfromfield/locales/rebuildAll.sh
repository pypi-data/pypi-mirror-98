#!/bin/sh

DOMAIN='collective.contentrules.mailfromfield'

i18ndude rebuild-pot --pot ${DOMAIN}.pot --create ${DOMAIN} ..
i18ndude sync --pot ${DOMAIN}.pot ./*/LC_MESSAGES/${DOMAIN}.po

i18ndude rebuild-pot --pot plone.pot
i18ndude merge --pot plone.pot --merge plone-manual.pot
i18ndude sync --pot plone.pot ./*/LC_MESSAGES/plone.po

