#
# Copyright (c) 2015-2020 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_zmi.interfaces.configuration module

This module defines interfaces of ZMI configuration.
"""

from collections import OrderedDict

from zope.interface import Attribute, Interface
from zope.schema import Bool, Choice, TextLine
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from myams_js import myams_core_svg_bundle, myams_full_bundle, myams_mini_svg_bundle
from pyams_file.schema import FileField, ImageField
from pyams_i18n.schema import I18nTextLineField


__docformat__ = 'restructuredtext'

from pyams_zmi import _


MYAMS_BUNDLES = OrderedDict((
    ('full', (myams_full_bundle, _("MyAMS full bundle"))),
    ('mini+svg', (myams_mini_svg_bundle, _("MyAMS mini bundle (with SVG icons)"))),
    ('core+svg', (myams_core_svg_bundle, _("MyAMS core bundle (with SVG icons)")))
))

MYAMS_BUNDLES_VOCABULARY = SimpleVocabulary(
    [SimpleTerm(k, title=v[1]) for k, v in MYAMS_BUNDLES.items()])


class IZMIConfiguration(Interface):
    """Static management configuration interface"""

    site_name = TextLine(title=_("Site name"),
                         default='PyAMS website',
                         required=False)

    application_name = TextLine(title=_("Application name"),
                                default='PyAMS',
                                required=False)

    application_package = TextLine(title=_("Application package"),
                                   description=_("Name of the main package used to get "
                                                 "application version"),
                                   default='pyams_zmi',
                                   required=False)

    inner_package_name = TextLine(title=_("Secondary name"),
                                  required=False)

    inner_package = TextLine(title=_("Secondary package"),
                             description=_("Name of the secondary package used to complete "
                                           "application version"),
                             required=False)

    version = Attribute("Application version")

    myams_bundle = Choice(title=_("MyAMS bundle"),
                          description=_("MyAMS bundle used by the application"),
                          vocabulary=MYAMS_BUNDLES_VOCABULARY,
                          default='full')

    favicon = ImageField(title=_("Icon"),
                         description=_("Favorites icon"),
                         required=False)

    include_header = Bool(title=_("Include header"),
                          required=False,
                          default=True)

    fixed_header = Bool(title=_("Fixed header"),
                        description=_("If selected, the header will not scroll but will stay "
                                      "fixed at the top of the screen"),
                        required=False,
                        default=True)

    logo = ImageField(title=_("Logo image"),
                      description=_("SVG or bitmap image used as logo"),
                      required=False)

    include_site_search = Bool(title=_("Include site search"),
                               description=_("Include a global site search access link "
                                             "in page header"),
                               required=False,
                               default=False)

    site_search_placeholder = I18nTextLineField(title=_("Site search placeholder"),
                                                required=False)

    site_search_handler = TextLine(title=_("Site search handler"),
                                   required=False,
                                   default='#search.html')

    include_menus = Bool(title=_("Include navigation menus"),
                         required=False,
                         default=True)

    include_minify_button = Bool(title=_("Include minify buttons"),
                                 description=_("If selected, this will provide features to "
                                               "reduce or hide navigation menus"),
                                 required=True,
                                 default=True)

    fixed_navigation = Bool(title=_("Fixed menus"),
                            required=True,
                            default=False)

    accordion_menus = Bool(title=_("Accordion menus"),
                           description=_("If selected, only one navigation menu can be opened "
                                         "at a given time"),
                           required=True,
                           default=True)

    include_ribbon = Bool(title=_("Include ribbon"),
                          description=_("Display breadcrumbs ribbon?"),
                          required=False,
                          default=True)

    fixed_ribbon = Bool(title=_("Fixed ribon"),
                        description=_("If selected, the ribbon will not scroll but will stay "
                                      "fixed at the top of the page"),
                        required=True,
                        default=True)

    base_body_css_class = TextLine(title=_("Base body CSS class"),
                                   required=False)

    body_css_class = Attribute("HTML body CSS class")

    custom_stylesheet = FileField(title=_("Custom stylesheet"),
                                  description=_("Custom stylesheet used to override or extend "
                                                "default MyAMS management skin"),
                                  required=False)

    custom_script = FileField(title=_("Custom script"),
                              description=_("Custom javascript used to override or extend "
                                            "default MyAMS modules"),
                              required=False)
