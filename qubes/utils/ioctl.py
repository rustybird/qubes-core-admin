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
# Derived from MIT licensed code at
# <https://github.com/olavmrk/python-ioctl/blob/1f090606fb5b68cd4cd98a3eb18fd4a571fc931c/ioctl/linux.py>:
#
# Copyright (C) 2016 Olav Morken
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

import platform


# linux/include/uapi/asm-generic/ioctl.h
class _GenericNumbers():
    IOC_NRBITS = 8
    IOC_TYPEBITS = 8
    IOC_SIZEBITS = 14
    IOC_NONE = 0
    IOC_WRITE = 1
    IOC_READ = 2

    @classmethod
    def ioc(cls, req_dir, req_type, req_nr, req_size):
        ioc_nrshift = 0
        ioc_typeshift = ioc_nrshift + cls.IOC_NRBITS
        ioc_sizeshift = ioc_typeshift + cls.IOC_TYPEBITS
        ioc_dirshift = ioc_sizeshift + cls.IOC_SIZEBITS

        return ((req_dir << ioc_dirshift) |
                (req_type << ioc_typeshift) |
                (req_nr << ioc_nrshift) |
                (req_size << ioc_sizeshift))

    @classmethod
    def io(cls, req_type, req_nr):  # pylint: disable=invalid-name
        return cls.ioc(cls.IOC_NONE, req_type, req_nr, 0)

    @classmethod
    def iow(cls, req_type, req_nr, req_size):
        return cls.ioc(cls.IOC_WRITE, req_type, req_nr, req_size)

    @classmethod
    def ior(cls, req_type, req_nr, req_size):
        return cls.ioc(cls.IOC_READ, req_type, req_nr, req_size)

    @classmethod
    def iowr(cls, req_type, req_nr, req_size):
        return cls.ioc(cls.IOC_WRITE | cls.IOC_READ, req_type, req_nr, req_size)

# linux/arch/alpha/include/uapi/asm/ioctl.h
class _AlphaNumbers(_GenericNumbers):
    IOC_SIZEBITS = 13
    IOC_NONE = 1
    IOC_WRITE = 4

# linux/arch/mips/include/uapi/asm/ioctl.h
class _MIPSNumbers(_GenericNumbers):
    IOC_SIZEBITS = 13
    IOC_NONE = 1
    IOC_WRITE = 4

# linux/arch/parisc/include/uapi/asm/ioctl.h
class _PARISCNumbers(_GenericNumbers):
    IOC_WRITE = 2
    IOC_READ = 1

# linux/arch/powerpc/include/uapi/asm/ioctl.h
class _PowerPCNumbers(_GenericNumbers):
    IOC_SIZEBITS = 13
    IOC_NONE = 1
    IOC_WRITE = 4

# linux/arch/sparc/include/uapi/asm/ioctl.h
class _SPARCNumbers(_GenericNumbers):
    IOC_SIZEBITS = 13
    IOC_NONE = 1
    IOC_WRITE = 4

_MACHINE_TO_NUMBERS = {
    'alpha': _AlphaNumbers,
    'mips': _MIPSNumbers,
    'mips64': _MIPSNumbers,
    'parisc': _PARISCNumbers,
    'parisc64': _PARISCNumbers,
    'ppc': _PowerPCNumbers,
    'ppcle': _PowerPCNumbers,
    'ppc64': _PowerPCNumbers,
    'ppc64le': _PowerPCNumbers,
    'sparc': _SPARCNumbers,
    'sparc64': _SPARCNumbers,
}


def get_numbers(machine=platform.machine()):
    return _MACHINE_TO_NUMBERS.get(machine, _GenericNumbers)

MachineNumbers = get_numbers()
