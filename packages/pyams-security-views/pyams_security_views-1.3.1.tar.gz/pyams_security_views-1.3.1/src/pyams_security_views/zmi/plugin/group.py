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

"""PyAMS_security_views.zmi.plugin.group module

Internal groups management views and content providers.
"""

from pyramid.events import subscriber
from pyramid.view import view_config
from zope.interface import Interface, Invalid

from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces.form import IAJAXFormRenderer, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_pagelet.pagelet import pagelet_config
from pyams_security.interfaces import IGroupsFolderPlugin, ILocalGroup, ISecurityManager, \
    IViewContextPermissionChecker
from pyams_security.interfaces.base import MANAGE_SECURITY_PERMISSION
from pyams_security_views.zmi import ISecurityManagerView
from pyams_security_views.zmi.plugin import SecurityPluginAddForm, SecurityPluginAddMenu, \
    SecurityPluginPropertiesEditForm
from pyams_site.interfaces import ISiteRoot
from pyams_skin.viewlet.actions import ContextAction
from pyams_table.column import GetAttrColumn
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import ContextAdapter, ContextRequestViewAdapter, adapter_config
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.container import delete_container_element
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor
from pyams_zmi.interfaces.viewlet import IContextAddingsViewletManager, IToolbarViewletManager
from pyams_zmi.table import I18nColumnMixin, Table, TableAdminView, TableElementEditor, \
    TrashColumn


__docformat__ = 'restructuredtext'

from pyams_security_views import _  # pylint: disable=ungrouped-imports


@viewlet_config(name='add-groups-folder-plugin.menu',
                context=ISiteRoot, layer=IAdminLayer, view=ISecurityManagerView,
                manager=IContextAddingsViewletManager, weight=50,
                permission=MANAGE_SECURITY_PERMISSION)
class GroupsFolderPluginAddMenu(SecurityPluginAddMenu):
    """Groups folder plug-in add menu"""

    label = _("Add groups folder...")
    href = 'add-groups-folder-plugin.html'


@ajax_form_config(name='add-groups-folder-plugin.html',
                  context=ISecurityManager, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class GroupsFolderPluginAddForm(SecurityPluginAddForm):
    """Groups folder plug-in add form"""

    legend = _("Add groups folder plug-in")
    content_factory = IGroupsFolderPlugin


@ajax_form_config(name='properties.html', context=IGroupsFolderPlugin, layer=IPyAMSLayer)
class GroupsFolderPropertiesEditForm(SecurityPluginPropertiesEditForm):
    """Groups folder plug-in properties edit form"""

    title = _("Groups folder plug-in")
    plugin_interface = IGroupsFolderPlugin


#
# Groups folder table view
#

class GroupsFolderGroupsTable(Table):
    """Groups folders table"""


@adapter_config(name='title',
                required=(IGroupsFolderPlugin, IAdminLayer, GroupsFolderGroupsTable),
                provides=IColumn)
class GroupsFolderGroupsTitleColumn(I18nColumnMixin, GetAttrColumn):
    """Groups folder groups title column"""

    i18n_header = _("Title")
    attr_name = 'title'

    weight = 10


@adapter_config(name='trash',
                required=(IGroupsFolderPlugin, IAdminLayer, GroupsFolderGroupsTable),
                provides=IColumn)
class GroupsFolderGroupsTrashColumn(TrashColumn):
    """Groups folder trash column"""

    permission = MANAGE_SECURITY_PERMISSION


@pagelet_config(name='search.html', context=IGroupsFolderPlugin, layer=IPyAMSLayer,
                permission=MANAGE_SECURITY_PERMISSION)
class GroupsFolderGroupsView(TableAdminView):
    """Groups folders view"""

    # pylint: disable=no-member

    @property
    def title(self):
        """View title getter"""
        return self.context.title

    @property
    def back_url(self):
        """View back URL getter"""
        return absolute_url(self.request.root, self.request, 'security-plugins.html')

    table_class = GroupsFolderGroupsTable
    table_label = _("List of folder groups")


@view_config(name='delete-element.json', context=IGroupsFolderPlugin, request_type=IPyAMSLayer,
             permission=MANAGE_SECURITY_PERMISSION, renderer='json', xhr=True)
def delete_group(request):
    """Delete local group"""
    return delete_container_element(request)


@adapter_config(required=(ILocalGroup, IAdminLayer, Interface),
                provides=ITableElementEditor)
class GroupElementEditor(TableElementEditor):
    """Security manager table element editor"""


@adapter_config(required=ILocalGroup, provides=IViewContextPermissionChecker)
class LocalGroupPermissionChecker(ContextAdapter):
    """Local group permission checker"""

    edit_permission = MANAGE_SECURITY_PERMISSION


#
# Local groups views
#

@viewlet_config(name='add-group.action', context=IGroupsFolderPlugin, layer=IAdminLayer,
                view=GroupsFolderGroupsView, manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_SECURITY_PERMISSION)
class LocalGroupAddAction(ContextAction):
    """Local group add action"""

    label = _("Add group")
    status = 'success'
    icon_class = 'fas fa-plus'

    href = 'add-group.html'
    modal_target = True


@ajax_form_config(name='add-group.html', context=IGroupsFolderPlugin, layer=IPyAMSLayer,
                  permission=MANAGE_SECURITY_PERMISSION)
class LocalGroupAddForm(AdminModalAddForm):
    """Local group add form"""

    @property
    def title(self):
        """Form title getter"""
        return self.context.title

    legend = _("Add local group")

    fields = Fields(ILocalGroup).omit('__parent__', '__name__')
    content_factory = ILocalGroup

    def update_content(self, obj, data):
        obj.group_id = data.get(self, {}).get('group_id')
        return super(LocalGroupAddForm, self).update_content(obj, data)

    def add(self, obj):
        self.context[obj.group_id] = obj

    def next_url(self):
        return absolute_url(self.context, self.request, 'search.html')


@subscriber(IDataExtractedEvent, form_selector=LocalGroupAddForm)
def extract_local_group_add_form_data(event):
    """Check new local group form data"""
    data = event.data
    folder = event.form.context
    if data.get('group_id') in folder:
        event.form.widgets.errors += (Invalid(_("Specified login is already used.")),)


@adapter_config(required=(IGroupsFolderPlugin, IAdminLayer, LocalGroupAddForm),
                provides=IAJAXFormRenderer)
class LocalGroupAddFormRenderer(ContextRequestViewAdapter):
    """Local group add form AJAX renderer"""

    def render(self, changes):
        """AJAX form renderer"""
        if not changes:
            return None
        return {
            'status': 'reload',
            'location': self.view.next_url()
        }


@ajax_form_config(name='properties.html', context=ILocalGroup, layer=IPyAMSLayer)
class LocalGroupEditForm(AdminModalEditForm):
    """Local group edit form"""

    @property
    def title(self):
        """Form title getter"""
        return self.context.title

    legend = _("Group properties")

    fields = Fields(ILocalGroup).omit('__parent__', '__name__')
