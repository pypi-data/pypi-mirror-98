#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_alchemy.zmi.engine module

This module defines SQL engines management components.
"""

from pyramid.events import subscriber
from zope.copy import copy
from zope.interface import Interface, Invalid, implementer
from zope.intid import IIntIds

from pyams_alchemy.interfaces import IAlchemyEngineUtility, IAlchemyManager, \
    MANAGE_SQL_ENGINES_PERMISSIONS
from pyams_alchemy.zmi import AlchemyManagerEnginesView, AlchemyManagerTable
from pyams_form.ajax import ajax_form_config
from pyams_form.field import Fields
from pyams_form.interfaces import DISPLAY_MODE
from pyams_form.interfaces.form import IAJAXFormRenderer, IAddForm, IDataExtractedEvent
from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.viewlet.actions import ContextAction
from pyams_table.interfaces import IColumn
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.registry import get_utility, query_utility
from pyams_viewlet.viewlet import viewlet_config
from pyams_zmi.form import AdminModalAddForm, AdminModalEditForm
from pyams_zmi.helper.event import get_json_table_row_refresh_callback
from pyams_zmi.interfaces import IAdminLayer
from pyams_zmi.interfaces.table import ITableElementEditor, ITableElementName
from pyams_zmi.interfaces.viewlet import IToolbarViewletManager
from pyams_zmi.table import ActionColumn, TableElementEditor


__docformat__ = 'restructuredtext'

from pyams_alchemy import _  # pylint: disable=ungrouped-imports


class IAlchemyEngineAddForm(IAddForm):
    """SQLAlchemy engine add form interface"""


@subscriber(IDataExtractedEvent, form_selector=IAlchemyEngineAddForm)
def handle_new_engine_data_extraction(event):
    """Handle new engine data"""
    name = event.data['name'] or ''
    engine = query_utility(IAlchemyEngineUtility, name=name)
    if engine is not None:
        event.form.widgets.errors += (Invalid(_("An SQLAlchemy engine is already "
                                                "registered with this name!")),)


@viewlet_config(name='add-sql-engine.menu',
                context=IAlchemyManager, layer=IAdminLayer, view=AlchemyManagerEnginesView,
                manager=IToolbarViewletManager, weight=10,
                permission=MANAGE_SQL_ENGINES_PERMISSIONS)
class AlchemyEngineAddMenu(ContextAction):
    """Alchemy engine add menu"""

    status = 'success'
    icon_class = 'fas fa-plus'
    label = _("Add SQL engine")

    href = 'add-sql-engine.html'
    modal_target = True


@ajax_form_config(name='add-sql-engine.html', context=IAlchemyManager, layer=IPyAMSLayer,
                  permission=MANAGE_SQL_ENGINES_PERMISSIONS)
@implementer(IAlchemyEngineAddForm)
class AlchemyEngineAddForm(AdminModalAddForm):  # pylint: disable=abstract-method
    """SQLAlchemy engine add form"""

    title = _("Add new SQL engine")
    legend = _("New engine properties")

    fields = Fields(IAlchemyEngineUtility)
    content_factory = IAlchemyEngineUtility

    def add(self, obj):
        intids = get_utility(IIntIds)
        self.context[hex(intids.register(obj))[2:]] = obj


@adapter_config(required=IAlchemyEngineUtility,
                provides=ITableElementName)
def alchemy_engine_name_factory(context):
    """SQLAlchemy engine table element name factory"""
    return context.name


@adapter_config(required=(IAlchemyEngineUtility, IAdminLayer, Interface),
                provides=ITableElementEditor)
class AlchemyEngineElementEditor(TableElementEditor):
    """SQLAlchemy engines table element editor"""


@ajax_form_config(name='properties.html', context=IAlchemyEngineUtility, layer=IPyAMSLayer,
                  permission=MANAGE_SQL_ENGINES_PERMISSIONS)
class AlchemyEngineEditForm(AdminModalEditForm):
    """SQLAlchemy engine properties edit form"""

    @property
    def title(self):
        """Title getter"""
        return self.context.name

    legend = _("SQL engine properties")

    fields = Fields(IAlchemyEngineUtility)

    def update_widgets(self, prefix=None):
        super().update_widgets(prefix)
        name = self.widgets.get('name')
        if name is not None:
            name.mode = DISPLAY_MODE


@adapter_config(required=(IAlchemyEngineUtility, IAdminLayer, AlchemyEngineEditForm),
                provides=IAJAXFormRenderer)
class AlchemyEngineEditFormAJAXRenderer(ContextRequestViewAdapter):
    """SQLAlchemy engine edit form AJAX renderer"""

    def render(self, changes):
        """AJAX result renderer"""
        if not changes:
            return None
        engine = self.view.context
        return {
            'callbacks': [
                get_json_table_row_refresh_callback(engine.__parent__, self.request,
                                                    AlchemyManagerTable, engine)
            ]
        }


#
# Engine clone column
#

@adapter_config(name='clone',
                required=(IAlchemyManager, IAdminLayer, AlchemyManagerTable),
                provides=IColumn)
class AlchemyEngineCloneColumn(ActionColumn):
    """SQLAlchemy engine clone column"""

    hint = _("Clone SQL engine")
    icon_class = 'far fa-clone'

    href = 'clone-sql-engine.html'

    weight = 100


@ajax_form_config(name='clone-sql-engine.html', context=IAlchemyEngineUtility,
                  layer=IPyAMSLayer, permission=MANAGE_SQL_ENGINES_PERMISSIONS)
@implementer(IAlchemyEngineAddForm)
class AlchemyEngineCloneForm(AdminModalAddForm):
    """SQLAlchemy engine clone form"""

    @property
    def title(self):
        """Title getter"""
        return self.context.name

    legend = _("Clone SQL connection")

    fields = Fields(IAlchemyEngineUtility).select('name')

    def create(self, data):
        return copy(self.context)

    def add(self, obj):
        intids = get_utility(IIntIds)
        self.context.__parent__[hex(intids.register(obj))[2:]] = obj
