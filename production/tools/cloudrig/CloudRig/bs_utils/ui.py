# SPDX-FileCopyrightText: 2025 Blender Studio Tools Authors
#
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.types import UILayout


def aligned_label(layout: UILayout, *, factor=0.4, alert=False, alignment="LEFT", **kwargs):
    """Draw some text in the single-column-layout style, ie. offset by 60%."""

    text = kwargs.get("text")
    if not text:
        return
    del kwargs['text']
    lines = text.split("\n")
    for line in lines:
        row = layout.split(factor=factor)
        row.separator()
        row.alert = alert
        row.alignment = alignment
        row.label(text=line, **kwargs)
        if 'icon' in kwargs:
            kwargs['icon'] = 'BLANK1'


def label_split(layout: UILayout, *, alert=False, **kwargs) -> UILayout:
    """Return an empty UILayout with a text label to its left in the single-column-layout style."""
    split = layout.split(factor=0.4, align=True)
    split.alert = alert
    row = split.row(align=True)
    row.alignment = "RIGHT"
    row.label(**kwargs)
    return split
