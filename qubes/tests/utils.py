#
# The Qubes OS Project, https://www.qubes-os.org
#
# Copyright (C) 2021 Rusty Bird <rustybird@net-c.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, see <https://www.gnu.org/licenses/>.
#

import platform

import qubes.utils
import qubes.utils.ioctl
import qubes.tests


class TC_10_Utils(qubes.tests.QubesTestCase):
    def test_100_ioctl_machine(self):
        self.assertIs(
            qubes.utils.ioctl.MachineNumbers,
            qubes.utils.ioctl.get_numbers(platform.machine())
        )

    def test_101_ioctl_ficlone(self):
        sizeof_int = 4
        FICLONE = 0x94, 9, sizeof_int  # pylint disable=invalid-name

        self.assertEqual(
            qubes.utils.ioctl.get_numbers('x86_64').iow(*FICLONE),
            1074041865
        )

        self.assertEqual(
            qubes.utils.ioctl.get_numbers('ppc64le').iow(*FICLONE),
            2147783689
        )
