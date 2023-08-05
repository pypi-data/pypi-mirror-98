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

"""PyAMS_skin.interfaces.metas module

This module defines interfaces used to provide metas-headers.
"""

from zope.interface import Interface

__docformat__ = 'restructuredtext'


class IMetaHeader(Interface):
    """Meta HTML header"""

    def render(self):
        """Render META header"""


class IHTMLContentMetas(Interface):
    """Get list of metas headers associated with given context"""

    def get_metas(self):
        """Get content metas"""
