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

"""PyAMS_security_views.zmi.plugin base module

This module defines classes which are used by all security plug-ins management views.
"""

from pyramid.events import subscriber
from zope.interface import Interface, Invalid

from pyams_form.browser.checkbox import SingleCheckBoxFieldWidget
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_security.interfaces import IPlugin, ISecurityManager, IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security_views.zmi import SecurityPluginsTable
from pyams_skin.viewlet.menu import MenuItem
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility
from pyams_utils.url import absolute_url
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor, ITableElementName
from pyams_zmi.table import TableElementEditor


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


class SecurityPluginAddMenu(MenuItem):
    """Security manager plug-in add form"""

    modal_target = True

    def get_href(self):
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        return absolute_url(sm, self.request, self.href)


class SecurityPluginAddForm(AdminModalAddForm):
    """Security plug-in add form"""

    title = _("Security manager")
    content_factory = IPlugin

    object_data = {
        'ams-warn-on-change': False
    }

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(self.content_factory).omit('__parent__', '__name__')
        fields['enabled'].widget_factory = SingleCheckBoxFieldWidget
        return fields

    def add(self, obj):
        sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
        sm[obj.prefix] = obj

    def next_url(self):
        return absolute_url(self.request.root, self.request, 'admin#security-plugins.html')


@subscriber(IDataExtractedEvent, form_selector=SecurityPluginAddForm)
def extract_plugin_add_form_data(event):
    """Security plug-in add form data extraction"""
    data = event.data
    sm = get_utility(ISecurityManager)  # pylint: disable=invalid-name
    if data.get('prefix') in sm:
        event.form.widgets.errors += (Invalid(_("Specified prefix is already used!")),)


@adapter_config(required=(ISecurityManager, IAdminLayer, SecurityPluginAddForm),
                provides=IAJAXFormRenderer)
class SecurityPluginAddFormRenderer(ContextRequestViewAdapter):
    """Security plug-in add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if changes is None:  # WARNING: creating an empty container will return a "false" value!
            return None
        return {
            'status': 'redirect',
            'location': self.view.next_url()
        }


@adapter_config(required=IPlugin,
                provides=ITableElementName)
def security_plugin_name(context):
    """Security plug-in name adapter"""
    return context.title


@adapter_config(required=(IPlugin, IAdminLayer, Interface),
                provides=ITableElementEditor)
class SecurityPluginEditor(TableElementEditor):
    """Security plug-in editor adapter"""


@adapter_config(required=IPlugin, provides=IViewContextPermissionChecker)
class SecurityManagerPluginPermissionChecker(ContextAdapter):
    """Security manager plug-in permission checker"""

    edit_permission = MANAGE_SECURITY_PERMISSION


class SecurityPluginPropertiesEditForm(AdminModalEditForm):
    """Security plug-in properties editor adapter"""

    legend = _("Properties")
    plugin_interface = IPlugin

    @property
    def fields(self):
        """Form fields getter"""
        fields = Fields(self.plugin_interface).omit('__parent__', '__name__')
        fields['enabled'].widget_factory = SingleCheckBoxFieldWidget
        return fields

    def update_widgets(self, prefix=None):
        super(SecurityPluginPropertiesEditForm, self).update_widgets(prefix)
        if 'prefix' in self.widgets:
            self.widgets['prefix'].mode = DISPLAY_MODE


@adapter_config(required=(IPlugin, IAdminLayer, SecurityPluginPropertiesEditForm),
                provides=IAJAXFormRenderer)
class SecurityPluginPropertiesAJAXRenderer(ContextRequestViewAdapter):
    """Security plugin properties AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return get_json_table_row_refresh_callback(self.request.root, self.request,
                                                   SecurityPluginsTable, self.context)
