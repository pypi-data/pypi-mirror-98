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

"""PyAMS_zmi.table module

This module provides bases classes for tables management.
"""

import json

from pyramid.decorator import reify
from zope.component import queryAdapter, queryMultiAdapter
from zope.interface import implementer
from zope.location import ILocation
from zope.schema.fieldproperty import FieldProperty

from pyams_table.column import Column, GetAttrColumn
from pyams_table.table import Table as BaseTable
from pyams_template.template import get_view_template
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.data import ObjectDataManagerMixin
from pyams_utils.date import SH_DATE_FORMAT, format_datetime
from pyams_utils.factory import get_object_factory, is_interface
from pyams_utils.interfaces import ICacheKeyValue
from pyams_utils.interfaces.data import IObjectData
from pyams_utils.list import boolean_iter
from pyams_utils.url import absolute_url
from pyams_zmi.interfaces.table import IInnerTable, ITableAdminView, ITableElementEditor, \
    ITableElementName
from pyams_zmi.view import InnerAdminView


__docformat__ = 'restructuredtext'

from pyams_zmi import _  # pylint: disable=ungrouped-imports


def get_table_id(table, context=None):
    """Table ID getter"""
    if context is None:
        context = table.context
    return '{}_{}'.format(table.prefix, ICacheKeyValue(context))


def get_column_sort(column, ignored=None):  # pylint: disable=unused-argument
    """Get column sortable attribute"""
    return getattr(column, 'sortable', None)


def get_column_type(column, ignored=None):  # pylint: disable=unused-argument
    """Get column sort type attribute"""
    return getattr(column, 'sort_type', None)


def get_row_id(table, element, context=None):
    """Row ID getter"""
    return '{}::{}'.format(get_table_id(table, context), ICacheKeyValue(element))


def get_row_name(element):
    """Row name getter"""
    return getattr(element, '__name__', None)


def get_row_editor(table, element):
    """Row editor getter"""
    return queryMultiAdapter((element, table.request, table), ITableElementEditor)


def check_attribute(attribute, source, column=None):
    """Check attribute value"""
    if callable(attribute):
        return attribute(source, column)
    return str(attribute)


def get_attributes(table, element, source, column=None):
    """Get table data attributes"""
    result = ''
    attrs = getattr(table, 'data_attributes', {}).get(element, {})
    for key, value in attrs.items():
        checked_value = check_attribute(value, source, column)
        if checked_value is not None:
            result += " {}='{}'".format(key, checked_value)
    return result


def get_data_attributes(element):
    """Get object data attributes"""
    data = IObjectData(element, None)
    if data is not None:
        return ' '.join(("data-{}='{}'".format(k, v if isinstance(v, str) else json.dumps(v))
                         for k, v in data.object_data.items()))
    return ''


class Table(ObjectDataManagerMixin, BaseTable):
    """Extended table class"""

    @reify
    def id(self):  # pylint: disable=invalid-name
        """Table ID getter"""
        return get_table_id(self, self.context)

    css_classes = {
        'table': 'table table-striped table-hover table-sm datatable'
    }

    object_data = {
        'responsive': True,
        'auto-width': False
    }

    @property
    def data_attributes(self):
        """Table data attributes getter

        These attributes are to be use with DataTables plug-in, and can be overridden in
        subclasses.
        """
        result = {
            'table': {
                'id': self.id,
                'data-ams-location': absolute_url(self.context, self.request)
            },
            'tr': {
                'id': lambda row, col: get_row_id(self, row),
                'data-ams-element-name': lambda row, col: get_row_name(row),
                'data-ams-url': lambda row, col: getattr(get_row_editor(self, row), 'href', None),
                'data-toggle':
                    lambda row, col: 'modal' if getattr(get_row_editor(self, row),
                                                        'modal_target', None)
                    else None
            },
            'th': {
                'data-ams-column-name': lambda row, col: row.__name__,
                'data-ams-sortable': get_column_sort,
                'data-ams-type': get_column_type
            }
        }
        return result

    def get_selected_row_class(self, row, css_class=None):
        """Get selected row class"""
        klass = self.css_classes.get('tr.selected')
        if callable(klass):
            klass = klass(*row)
        if klass and css_class:
            klass = '{} {}'.format(klass, css_class)
        else:
            klass = css_class or ''
        return klass

    def render_table(self):
        return super(Table, self).render_table() \
            .replace('<table', '<table {}'.format(get_attributes(self, 'table', self))) \
            .replace('<table', '<table {}'.format(get_data_attributes(self)))

    def render_row(self, row, css_class=None):
        css_class = self.get_selected_row_class(row[0], css_class)
        return super(Table, self).render_row(row, css_class) \
            .replace('<tr', '<tr {}'.format(get_attributes(self, 'tr', row[0][0])))

    def render_head_cell(self, column):
        return super(Table, self).render_head_cell(column) \
            .replace('<th', '<th {}'.format(get_attributes(self, 'th', column))) \
            .replace('<th', '<th {}'.format(get_data_attributes(column)))

    def render_cell(self, item, column, colspan=0):
        return super(Table, self).render_cell(item, column, colspan) \
            .replace('<td', '<td {}'.format(get_attributes(self, 'td', item, column)))


class InnerTableMixin:
    """Inner table mixin class"""

    table_class = Table
    table_label = FieldProperty(ITableAdminView['table_label'])

    empty_template = get_view_template(name='empty')

    def __init__(self, context, request, *args, **kwargs):
        super().__init__(context, request, *args, **kwargs)
        factory = get_object_factory(self.table_class) if is_interface(self.table_class) \
            else self.table_class
        self.table = factory(context, request)

    def update(self):
        """Admin view updater"""
        super().update()  # pylint: disable=no-member
        self.table.update()

    def render(self):
        """Admin view renderer"""
        has_values, values = boolean_iter(self.table.values)  # pylint: disable=no-member,unused-variable
        if not has_values:
            return self.empty_template()
        return super().render()  # pylint: disable=no-member


@implementer(ITableAdminView)
class TableAdminView(InnerTableMixin, InnerAdminView):
    """Table admin view

    This class is a wrapper for an admin view based on an inner table.
    """


@implementer(IInnerTable)
class InnerTableAdminView(InnerTableMixin):
    """Inner table admin view"""


class I18nColumnMixin:
    """Column mixin with I18n header"""

    i18n_header = None

    @property
    def header(self):
        """Column header getter translation"""
        return self.request.localizer.translate(self.i18n_header)


@adapter_config(required=ILocation, provides=ITableElementName)
def location_element_name(context):
    """Basic location name factory"""
    return context.__name__


class NameColumn(I18nColumnMixin, GetAttrColumn):
    """Common name column"""

    i18n_header = _("Name")
    weight = 10

    def get_value(self, obj):
        adapter = queryMultiAdapter((obj, self.request, self.table),
                                    ITableElementName)
        if adapter is None:
            adapter = queryAdapter(obj, ITableElementName)
        return adapter


class IconColumn(Column):
    """Base icon column"""

    header = ''
    css_classes = {
        'th': 'action'
    }
    sortable = 'false'

    icon_class = ''
    hint = ''

    permission = None
    checker = None

    def render_cell(self, item):
        """Column cell renderer based on permission and checker"""
        if not self.has_permission(item):
            return ''
        if self.checker:
            if callable(self.checker):
                checked = self.checker(item)  # pylint: disable=not-callable
            else:
                checked = self.checker
            if not checked:
                return ''
        return self.get_icon(item)

    def has_permission(self, item):
        """Column permission test"""
        if not self.permission:
            return True
        return self.request.has_permission(self.permission, item)

    def get_icon(self, item):
        """Column icon getter"""
        hint = self.get_icon_hint(item)
        return '<i class="fa-fw {} {}" data-original-title="{}"></i>'.format(
            self.get_icon_class(item), 'hint' if hint else '', hint)

    def get_icon_class(self, item):  # pylint: disable=unused-argument
        """Column class getter"""
        return self.icon_class

    def get_icon_hint(self, item):  # pylint: disable=unused-argument
        """Column hint getter"""
        return self.request.localizer.translate(self.hint)


class BaseActionColumn(IconColumn):
    """Base action column"""

    status = 'primary'
    href = None
    target = None
    modal_target = True

    permission = None

    css_classes = {
        'th': 'action',
        'td': 'action'
    }

    def is_visible(self, item):
        """Action visibility checker"""
        if not self.has_permission(item):
            return False
        if self.checker:
            if callable(self.checker):
                checked = self.checker(item)  # pylint: disable=not-callable
            else:
                checked = self.checker
            if not checked:
                return False
        return True

    def get_url(self, item):
        """Action URL getter"""
        return absolute_url(item, self.request, self.href)


class ActionColumn(BaseActionColumn):
    """Base action column"""

    def render_cell(self, item):
        """Column cell renderer"""
        if not self.is_visible(item):
            return ''
        return '<a href="{}" ' \
               '   data-ams-stop-propagation="true" ' \
               '   {} {} {}>{}</a>'.format(
                self.get_url(item),
                'data-ams-target="{}"'.format(self.target) if self.target else '',
                'data-toggle="modal"' if self.modal_target else '',
                'data-ams-modules="modal"' if self.modal_target else '',
                self.get_icon(item))


class ButtonColumn(BaseActionColumn):
    """Button action column"""

    label = None

    css_classes = {
        'th': 'action',
        'td': 'action py-1'
    }

    def render_cell(self, item):
        """Column cell renderer"""
        if not self.is_visible(item):
            return ''
        return '<a class="btn btn-sm btn-{} text-nowrap" ' \
               '   href="{}" ' \
               '   data-ams-stop-propagation="true" ' \
               '   {} {} {}>{}</a>'.format(
                self.status,
                self.get_url(item),
                'data-ams-target="{0}"'.format(self.target) if self.target else '',
                'data-toggle="modal"' if self.modal_target else '',
                'data-ams-modules="modal"' if self.modal_target else '',
                self.request.localizer.translate(self.label))


class JsActionColumn(ActionColumn):
    """Javascript action column"""

    def get_url(self, item):
        """Action URL getter"""
        return self.href


class TrashColumn(ObjectDataManagerMixin, JsActionColumn):
    """Trash column"""

    hint = _("Delete element")
    icon_class = 'fa fa-trash-alt'

    href = 'MyAMS.container.deleteElement'
    modal_target = False

    object_data = {
        'ams-modules': 'container'
    }

    weight = 999


class DateColumn(GetAttrColumn):
    """Date or datetime column"""

    formatter = SH_DATE_FORMAT

    def get_value(self, obj):
        """Date column value getter"""
        value = super(DateColumn, self).get_value(obj)
        if not value:
            return '--'
        return format_datetime(value, self.formatter, self.request)


@implementer(ITableElementEditor)
class TableElementEditor(ContextRequestViewAdapter):
    """Base table element editor"""

    view_name = FieldProperty(ITableElementEditor['view_name'])
    modal_target = FieldProperty(ITableElementEditor['modal_target'])

    @property
    def href(self):
        """Table element editor getter"""
        return absolute_url(self.context, self.request, self.view_name)
