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

"""PyAMS_skin.interfaces module

This module provides general skin-related interfaces.
"""

from zope.interface import Attribute, Interface, Invalid, implementer, invariant
from zope.interface.interfaces import IObjectEvent, ObjectEvent
from zope.schema import Bool, Choice

from pyams_file.schema import FileField


__docformat__ = 'restructuredtext'

from pyams_skin import _


class ISkinChangedEvent(IObjectEvent):
    """Skin changed event"""


@implementer(ISkinChangedEvent)
class SkinChangedEvent(ObjectEvent):
    """Request skin changed event"""


class ISkinnable(Interface):
    """Skinnable content interface"""

    can_inherit_skin = Attribute("Check if skin can be inherited")

    inherit_skin = Bool(title=_("Inherit parent skin?"),
                        description=_("Should we reuse parent skin?"),
                        required=True,
                        default=False)

    no_inherit_skin = Bool(title=_("Don't inherit parent skin?"),
                           description=_("Should we override parent skin?"),
                           required=True,
                           default=True)

    skin_parent = Attribute("Skin parent (local or inherited)")

    skin = Choice(title=_("Custom graphic theme"),
                  description=_("This theme will be used to handle graphic design (colors and "
                                "images)"),
                  vocabulary='PyAMS user skins',
                  required=False)

    @invariant
    def check_skin(self):
        """Force skin selection when not inheriting from parent"""
        if self.no_inherit_skin and not self.skin:
            raise Invalid(_("You must select a custom skin or inherit from parent!"))

    def get_skin(self, request=None):
        """Get skin matching this content"""

    custom_stylesheet = FileField(title=_("Custom stylesheet"),
                                  description=_("This custom stylesheet will be used to override "
                                                "selected theme styles"),
                                  required=False)

    editor_stylesheet = FileField(title=_("Editor stylesheet"),
                                  description=_("Styles defined into this stylesheet will be "
                                                "available into HTML editor"),
                                  required=False)

    custom_script = FileField(title=_("Custom script"),
                              description=_("This custom javascript file will be used to add "
                                            "dynamic features to selected theme"),
                              required=False)


class IUserSkinnable(ISkinnable):
    """User skinnable content interface"""


BOOTSTRAP_STATUS = ('primary', 'secondary', 'success', 'danger',
                    'warning', 'info', 'light', 'dark')
"""Bootstrap status list"""
