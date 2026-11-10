# SPDX-License-Identifier: GPL-3.0-or-later

from . import (
    actions_component,
    cloud_generator,
    cloudrig,
    generate_test_animation,
    naming,
    troubleshooting,
)

modules = [
    cloudrig,
    troubleshooting,  # Registers LogEntry for the Generator.
    actions_component,  # Registers ActionConstraintSetup before cloud_generator uses it.
    cloud_generator,
    naming,
    generate_test_animation,
]
