# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.app.translations import pgettext_rpt as rpt_

if TYPE_CHECKING:
    from .bone_info import BoneInfo, ConstraintInfo

from .overlay_painter import no_overlay


class CloudConstraintRelinkingMixin:
    """Relinking - Allow users to easily add constraints to the Target Rig to specific bones,
    in cases where user intent can be made clear."""

    # Constraints on the metarig's bones get transferred to bones named with this prefix.
    # Child classes are expected to override this with the prefix of their highest level controls.
    relink_default_prefix = ""

    @no_overlay
    def base__relink(self):
        """Move constraints from original bones to other bones."""
        for org_idx, org_bi in enumerate(self.bones_org):
            for con_info in org_bi.constraint_infos[:]:
                if not con_info.is_from_real:
                    # If this constraint was added by CloudRig code, don't relink it.
                    # We only want to relink constraints that were added by the user.
                    continue

                self.base__relink_single(org_idx, con_info)

    def base__relink_single(self, org_idx: int, con_info: ConstraintInfo):
        """Move a single constraint from its original bone to its relink target."""
        org_bi = self.bones_org[org_idx]
        to_binfo = self.base__relink_get_target(org_idx, con_info)
        if con_info.type == 'ARMATURE' and 'NOHLP' not in con_info.name:
            is_parent_helper = any(child.parent_helper is to_binfo for child in to_binfo.children)
            if not is_parent_helper:
                to_binfo = self.create_parent_bone(to_binfo, self.bones_mch)

        base_name = con_info.name.split("@")[0]
        if to_binfo != org_bi:
            existing_arm = None
            if con_info.type == 'ARMATURE':
                existing_arm = next((con for con in to_binfo.constraint_infos if con.type == 'ARMATURE'), None)
            if existing_arm:
                self.base__relink_replace_armature(org_bi, to_binfo, existing_arm, con_info)
            else:
                to_binfo.constraint_infos.append(con_info)
            org_bi.constraint_infos.remove(con_info)
        elif "-" in base_name and (('KEEP-' not in base_name and 'ORG-' not in base_name) or not org_bi.preserve):
            target_name = con_info.name.rsplit("-", 1)[0] + "-" + org_bi.name
            self.raise_generation_error(
                description=rpt_(
                    'Relinking Failed for constraint "{constraint}".\n'
                    'The dash (-) in the constraint name tells CloudRig to move the constraint to a '
                    'generated bone named "{bone}", but no such bone exists.'
                ).format(constraint=con_info.name, bone=target_name),
                icon='CONSTRAINT_BONE',
                description_short=rpt_('Relinking Failed: {constraint}').format(constraint=con_info.name),
                trouble_bone=org_bi.name,
            )

    def base__relink_replace_armature(
        self, org_bi: BoneInfo, to_binfo: BoneInfo, existing: ConstraintInfo, con_info: ConstraintInfo
    ):
        """Replace an existing Armature constraint with a relinked one, since a bone should never have two."""
        idx = to_binfo.constraint_infos.index(existing)
        to_binfo.constraint_infos[idx] = con_info
        if not existing.is_from_real:
            # Replacing a generated Armature constraint is the intended use case.
            return
        self.add_log(
            rpt_('Armature constraint replaced: {constraint}').format(constraint=con_info.name),
            description=rpt_(
                'Constraint "{constraint}" was moved to "{bone}", replacing the Armature constraint "{existing}", '
                'which was also moved there from the metarig. A bone should not have two Armature constraints.\n'
                'Check the constraints on the metarig bones and remove one of them.'
            ).format(constraint=con_info.name, bone=to_binfo.name, existing=existing.name),
            icon='CONSTRAINT_BONE',
            trouble_bone=org_bi.name,
        )

    def base__relink_get_target(self, org_idx: int, con_info: ConstraintInfo) -> BoneInfo:
        """Return which BoneInfo a given constraint should be moved to.
        Params:
            org_idx: Index of the original bone that has the constraint
            con_info: The constraint itself.
        This function should be overridden by child classes.
        By default, we will return the original bone itself, ie. not moving the constraint anywhere.
        """

        org_name = self.bones_org[org_idx].name

        name_without_target = con_info.name.replace("NOHLP-", "NOHLP_").split("@")[0]
        if "-" in name_without_target:
            prefix, _base_name = name_without_target.rsplit("-", 1)
        else:
            prefix = type(self).relink_default_prefix

        target_name = "-".join([prefix, org_name])
        for bone_info in self.all_bone_infos:
            if bone_info.name == target_name:
                return bone_info

        return self.bones_org[org_idx]
