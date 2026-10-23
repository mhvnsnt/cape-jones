# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import json
from collections import OrderedDict
from typing import Any

from bpy.app.translations import pgettext_iface as iface_
from bpy.types import Context, UILayout

from ..bs_utils.prefs import get_addon_prefs
from ..bs_utils.ui import label_split
from ..generation.cloudrig import is_cloud_metarig
from .bone_info import BoneInfo, ensure_custom_property
from .overlay_painter import no_overlay
from .properties_ui import add_property_to_ui


class CloudUIMixin:
    """Mixin providing UI drawing utilities and rig property helpers for rig components."""

    forced_params = {}

    @no_overlay
    def rig_ui__add_bone_property(
        self,
        prop_bone: BoneInfo,
        prop_id: str,
        *,
        panel_name: str = "Settings",
        label_name="",
        row_name="",
        slider_name="",
        texts: list[str] | str = "",
        ###
        custom_prop_settings: dict | None = None,
        ###
        operator="",
        op_icon='BLANK1',
        op_kwargs: dict | None = None,
        ###
        context_bones: list[str | BoneInfo] | None = None,
    ) -> OrderedDict:
        """Ensure a custom property exists on prop_bone and register it in the rig UI."""
        custom_prop_settings = custom_prop_settings or {}
        op_kwargs = op_kwargs or {}
        context_bones = context_bones or []
        ensure_custom_property(prop_bone, prop_id, **custom_prop_settings)

        op_kwargs.update({'prop_bone': prop_bone.name, 'prop_id': prop_id})

        if not slider_name:
            slider_name = prop_id

        if type(texts) is str:
            if texts.startswith("["):
                texts = json.loads(texts)
            else:
                texts = [t.strip() for t in texts.split(",")]

        return add_property_to_ui(
            obj=self.target_rig,
            owner_path=f'pose.bones["{prop_bone.name}"]',
            prop_name=f'["{prop_id}"]',
            texts=texts,
            panel_name=panel_name,
            label_name=label_name,
            row_name=row_name,
            slider_name=slider_name,
            operator=operator,
            op_icon=op_icon,
            op_kwargs=op_kwargs,
            context_bones=context_bones,
        )

    @staticmethod
    def draw_control_label(layout: UILayout, text=""):
        """Draw a section label with a trailing colon in the given layout."""
        label_split(layout, text=text + ":")

    @staticmethod
    def is_advanced_mode(context: Context) -> bool:
        """Return whether advanced mode is enabled for the active CloudRig."""
        return is_advanced_mode(context)

    @classmethod
    def is_forced_param(cls, prop_name: str) -> bool:
        """Return True if the given parameter is overridden by forced_params."""
        for forced_param_name in cls.forced_params:
            if forced_param_name.endswith(prop_name):
                return True
        return False

    @classmethod
    def draw_prop(
        cls, context: Context, layout: UILayout, prop_owner: Any, prop_name: str, enabled=True, alert=False, **kwargs
    ) -> UILayout | None:
        """Draw a property row, skipping it silently if it is forced (overridden)."""
        is_forced = cls.is_forced_param(prop_name)
        if is_forced:
            return

        if cls.hide_as_default(context, prop_owner, prop_name):
            return

        row = draw_prop(layout, prop_owner, prop_name, enabled=enabled, alert=alert, **kwargs)
        if is_forced:
            row.enabled = False

        return row

    @classmethod
    def draw_prop_search(
        cls,
        context: Context,
        layout: UILayout,
        prop_owner: Any,
        prop_name: str,
        collection: Any,
        coll_prop_name: str,
        alert=False,
        **kwargs,
    ):
        """Draw a property search row, skipping or disabling it if the parameter is forced."""
        is_forced = cls.is_forced_param(prop_name)
        if is_forced and not cls.is_advanced_mode(context):
            return
        if cls.hide_as_default(context, prop_owner, prop_name):
            return

        row = draw_prop_search(layout, prop_owner, prop_name, collection, coll_prop_name, alert, **kwargs)

        if is_forced:
            row.enabled = False

        return row

    @classmethod
    def draw_prop_custom_shape(cls, context: Context, layout: UILayout, prop_owner: Any, prop_name: str):
        """Draw the custom shape selector widget for a given property."""
        prefs = get_addon_prefs(context)
        pgroup = getattr(prop_owner, prop_name)
        row = layout.row(align=True)

        if cls.hide_as_default(context, pgroup, 'name'):
            return

        metarig = context.object
        generator = metarig.cloudrig.generator
        if generator.preserve_shapes_properties and generator.preserve_custom_shapes:
            row.enabled = False

        if pgroup.use_pointer:
            cls.draw_prop(context, row, pgroup, 'custom_shape')
        else:
            cls.draw_prop_search(context, row, pgroup, 'name', prefs, 'widget_names')
            big_enough = prefs.widget_popup_size > 2
            row.template_icon_view(
                pgroup, 'name_enum', show_labels=big_enough, scale=1, scale_popup=prefs.widget_popup_size
            )

        row.prop(pgroup, 'use_pointer', text="", toggle=True, icon='OBJECT_DATA')

    @classmethod
    def hide_as_default(cls, context: Context, prop_owner: Any, prop_name: str) -> bool:
        metarig = context.object
        generator = metarig.cloudrig.generator
        hide_default = generator.show_only_nondefaults and cls.is_advanced_mode(context)
        if hide_default:
            prop_value = getattr(prop_owner, prop_name)
            if prop_value is None:
                return True
            prop = next(
                (prop for prop in prop_owner.bl_rna.properties if prop.identifier == prop_name and prop.is_runtime),
                None,
            )
            if not prop:
                return True
            if prop.type in {'POINTER', 'COLLECTION'}:
                # These have no `default`. A pointer's default is None, which was handled above.
                return False
            default = prop.default
            if prop_value == default:
                return True
        return False


def is_advanced_mode(context: Context) -> bool:
    """Return True if advanced mode is enabled for the active metarig."""
    if not is_cloud_metarig(context.object):
        return False
    return get_addon_prefs(context).advanced_mode


def draw_label_with_linebreak(context: Context, layout: UILayout, text: str, alert=False, align_split=False):
    """Attempt to simulate a proper textbox by only displaying as many
    characters in a single label as fits in the UI.
    This only works well on specific UI zoom levels.
    """

    if text == "":
        return
    text = iface_(text)
    col = layout.column(align=True)
    col.alert = alert
    if align_split:
        split = col.split(factor=0.2)
        split.row()
        col = split.row().column(align=True)
    paragraphs = text.split("\n")

    # Try to determine maximum allowed characters per line, based on pixel width of the area.
    # Not a great metric, but I couldn't find anything better.
    ui_scale = context.preferences.view.ui_scale
    max_line_length = 100
    if context.area:
        max_line_length = context.area.width / 8 / ui_scale
    if align_split:
        max_line_length *= 0.95
    for paragraph in paragraphs:
        if hasattr(col, 'label_multiline'):
            col.label_multiline(text=paragraph)
            continue
        # TODO: Remove these lines when dropping compatibility for Blender 5.x.
        lines = [""]
        for word in paragraph.split(" "):
            if len(lines[-1]) + len(word) + 1 > max_line_length:
                lines.append("")
            lines[-1] += word + " "

        for line in lines:
            col.label(text=line)
    return col


def draw_prop(layout: UILayout, prop_owner: Any, prop_name: str, enabled=True, alert=False, **kwargs) -> UILayout:
    """Draw a property in a row and return that row."""
    row = layout.row(align=True)
    row.alert = alert
    row.prop(prop_owner, prop_name, **kwargs)
    row.enabled = enabled
    return row


def draw_prop_search(
    layout: UILayout, prop_owner: Any, prop_name: str, collection: Any, coll_prop_name: str, alert: bool, **kwargs
) -> UILayout:
    """Draw a property search widget in a row and return that row."""
    row = layout.row()
    row.alert = alert
    if alert:
        kwargs['icon'] = 'ERROR'
    row.prop_search(prop_owner, prop_name, collection, coll_prop_name, **kwargs)
    return row
