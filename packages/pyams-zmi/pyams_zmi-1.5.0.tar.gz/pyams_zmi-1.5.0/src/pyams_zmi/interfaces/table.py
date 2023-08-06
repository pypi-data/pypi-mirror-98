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

"""PyAMS_zmi.interfaces.table module

This modules defines public interfaces of table views.
"""

__docformat__ = 'restructuredtext'

from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Attribute, Interface
from zope.schema import Bool, TextLine

from pyams_template.template import template_config
from pyams_zmi.interfaces import IInnerAdminView


@template_config(template='templates/table.pt')
@template_config(template='templates/table-empty.pt', name='empty')
class ITableAdminView(IInnerAdminView):
    """Admin table view interface"""

    table_class = Attribute("Inner table class")

    table_label = TextLine(title="Inner table label")


@template_config(template='templates/inner-table.pt')
@template_config(template='templates/inner-table-empty.pt', name='empty')
class IInnerTable(IContentProvider):
    """Inner admin table view interface"""

    table_class = Attribute("Inner table class")

    table_label = TextLine(title="Inner table label")


class ITableElementName(Interface):
    """Table element name interface"""


class ITableWithActions(Interface):
    """Marker interface for table with inner actions menu"""


class ITableElementEditor(Interface):
    """Table row element editor marker interface"""

    view_name = TextLine(title="Editor view name",
                         default='properties.html')

    href = TextLine(title="Editor URL")

    modal_target = Bool(title="Modal target?",
                        required=True,
                        default=True)
