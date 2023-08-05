Changelog
=========

1.0.1 (2021-03-10)
------------------

- Allow to get to the end of the action execution if no mail is provided.
  You don't want the page to break if the email is missing. 
  For the anonymous user this wold be a bad UX
  [lucabel]


1.0.0 (2020-11-23)
------------------

- Migrate code to Plone 5/python 3.
  [lucabel]
- Add support for plone.stringinterp.
  [cekk]

0.4.0 (2015-03-13)
------------------

Dropped Plone 3 compatibility

- Fixed some label that were not i18n compatible
  [keul]
- Fixed wrong documentation mess introduced on version 0.3:
  the new "parent" option was wrongly descripted
  [keul]
- Updated documentation to reflect changes done in version 0.3
  [keul]

0.3.0 (2014-05-06)
------------------

- Fix unicode error while replacing strings [nicolasenno]
- Do not fail if a rule is activated on a non-AT content [keul]
- Do not try to send mail to empty string recipients [keul]
- Refactoring [alert]
- Added parent option in the target vocabulary [alert]

0.2.0 (2013-05-02)
------------------

* lowered logging level to debug
  [keul]
* fixed ruleAction factory
  [cekk]

0.1.0 (2011-10-21)
------------------

* Initial release
