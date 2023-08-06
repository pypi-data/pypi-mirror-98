#
# Copyright (c) 2015-2019 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS Alchemy.include module

This module is used for Pyramid integration
"""

from pyams_alchemy.interfaces import MANAGE_SQL_ENGINES_PERMISSIONS, SQL_MANAGER_ROLE
from pyams_security.interfaces import ADMIN_USER_ID, SYSTEM_ADMIN_ROLE
from pyams_security.interfaces.base import ROLE_ID


__docformat__ = 'restructuredtext'

from pyams_alchemy import _


def include_package(config):
    """Pyramid package include"""

    # add translations
    config.add_translation_dirs('pyams_alchemy:locales')

    # add SQLAlchemy management permissions
    config.register_permission({
        'id': MANAGE_SQL_ENGINES_PERMISSIONS,
        'title': _("Manage SQL engines properties")
    })

    # upgrade system manager roles
    config.upgrade_role(SYSTEM_ADMIN_ROLE,
                        permissions={
                            MANAGE_SQL_ENGINES_PERMISSIONS
                        })

    # register new roles
    config.register_role({
        'id': SQL_MANAGER_ROLE,
        'title': _("SQL engines manager (role)"),
        'permissions': {
            MANAGE_SQL_ENGINES_PERMISSIONS
        },
        'managers': {
            ADMIN_USER_ID,
            ROLE_ID.format(SYSTEM_ADMIN_ROLE)
        }
    })

    # package scan
    ignored = []
    try:
        import pyams_zmi  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:
        ignored.append('pyams_alchemy.zmi')
        ignored.append('pyams_alchemy.task.zmi')

    try:
        import pyams_scheduler  # pylint: disable=import-outside-toplevel,unused-import
    except ImportError:
        ignored.append('pyams_alchemy.task')

    config.scan(ignore=ignored)
