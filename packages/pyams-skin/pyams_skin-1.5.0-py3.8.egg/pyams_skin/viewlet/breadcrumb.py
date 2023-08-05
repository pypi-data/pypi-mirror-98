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

"""PyAMS_skin.viewlet.breadcrumb module

This module defines base adapters for breadcrumbs management.
"""

__docformat__ = 'restructuredtext'

from pyramid.location import lineage
from zope.component import queryMultiAdapter
from zope.interface import Interface, implementer
from zope.location import ILocation
from zope.schema.fieldproperty import FieldProperty

from pyams_layer.interfaces import IPyAMSLayer
from pyams_skin.interfaces.viewlet import IBreadcrumbItem
from pyams_template.template import template_config
from pyams_utils.adapter import ContextRequestViewAdapter, adapter_config
from pyams_utils.url import absolute_url
from pyams_viewlet.viewlet import ViewContentProvider, contentprovider_config


@implementer(IBreadcrumbItem)
class BreadcrumbItem(ContextRequestViewAdapter):
    """Breadcrumb item"""

    label = FieldProperty(IBreadcrumbItem['label'])
    css_class = FieldProperty(IBreadcrumbItem['css_class'])
    view_name = FieldProperty(IBreadcrumbItem['view_name'])

    def get_href(self):
        """Breadcrumb URL getter"""
        return absolute_url(self.context, self.request, self.view_name)


@adapter_config(required=(ILocation, IPyAMSLayer, Interface),
                provides=IBreadcrumbItem)
class PyAMSBreadcrumbItem(BreadcrumbItem):
    """Default breadcrumb item adapter"""

    @property
    def label(self):
        """Breadcrumb item label getter"""
        return self.context.__name__

    css_class = 'breadcrumb-item persistent'
    view_name = None


@contentprovider_config(name='pyams.breadcrumbs',
                        context=ILocation, layer=IPyAMSLayer, view=Interface)
@template_config(template='templates/breadcrumbs.pt', layer=IPyAMSLayer)
class BreadcrumbsAdapter(ViewContentProvider):
    """Generic breadcrumbs adapter"""

    @property
    def items(self):
        """Breadcrumbs items getter"""
        for context in reversed(tuple(lineage(self.context))):
            item = queryMultiAdapter((context, self.request, self.view),
                                     IBreadcrumbItem)
            if (item is not None) and item.label:
                yield item
