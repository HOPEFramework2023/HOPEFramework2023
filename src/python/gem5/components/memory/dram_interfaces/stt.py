# Copyright (c) 2012-2021 Arm Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2013 Amin Farmahini-Farahani
# Copyright (c) 2015 University of Kaiserslautern
# Copyright (c) 2015 The University of Bologna
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Interfaces for DDR4 memories

These memory "interfaces" contain the timing,energy,etc parameters for each
memory type and are usually based on datasheets for the memory devices.

You can use these interfaces in the MemCtrl object as the `dram` timing
interface.
"""

from m5.objects import STTDDR4Interface

class STT_1333_4x16(STTDDR4Interface):
    """
    EMD4E001G16G2 1Gbit x16, 8-banks (2-banks per Bank Group). 1333 MHz
    Datasheet EMD4E001G16G2 Rev. 1.2 used for this configuration.
    """

    write_buffer_size = 128
    read_buffer_size = 64

    # size of device in bytes
    device_size = "128MiB" #166

    # 4x16 configuration, 4 devices each with an 16-bit interface
    device_bus_width = 16 #166

    # DDR4 is a BL8 device
    burst_length = 8 # 1, optionally Burst-Chop 4 (BC4) and On-the-fly (OTF) availabel

    # Each device has a page (row buffer) size of 2 Kbyte (2K columns x8)
    # Page size is per bank, calculated as follows: Page size = 2^COLBITS x ORG, where COLBITS = the number
    # of column address bits and ORG = the number of DQ bits.
    # COLBITS = 7, DQ = 16
    # 2^7 * 16 = 2048 bits, 256 Bytes
    device_rowbuffer_size = "256B" # 21

    # 4x16 configuration, so 4 devices
    devices_per_rank = 4

    # Use dual rank
    ranks_per_channel = 2

    # DDR4 has 2 (x16) or 4 (x4 and x8) bank groups
    # Set to 2 for x16 case
    # bank_groups_per_rank = 2

    # DDR4 has 16 banks(x4,x8) and 8 banks(x16) (4 bank groups in all
    # configurations). Currently we do not capture the additional
    # constraints incurred by the bank groups
    banks_per_rank = 8

    # 667 MHz
    tCK = "1.5ns" # 32

    # 8 beats across an x64 interface translates to 4 clocks @ 667 MHz
    tBURST = "6ns"

    # Greater of 4 CK or 7.5 ns
    tWTR = "9ns" # 15

    # Default same rank rd-to-wr bus turnaround to 2 CK, @800 MHz = 2.5 ns
    tRTW = "9ns" # not in datasheet 

    # rank bus delay
    tCS = "0ns" # not in datasheet

    # DDR4-1333
    tRCD = "135ns" # 54
    tCL = "15ns" # 32 CL = 10tCK
    tRP = "7.5ns" # 13
    tRAS = "143ns" # 13
    tRRD = "10ns" # 54
    tRRD_L = "10ns" # 54
    tXAW = "240ns" # 13
    activation_limit = 4
    tRFC = "380ns" # 32 & 57
    tST = "380ns" # 32

    tWR = "15ns" # 55

    # Greater of 4 CK or 7.5 ns
    tWTR = "9ns" # 15
    tWTR_L = "9ns" # 15    

    # Default same rank rd-to-wr bus turnaround to 2 CK, @800 MHz = 2.5 ns
    tRTW = "9ns" # not in datasheet 

    # Greater of 4 CK or 7.5 ns
    tRTP = "7.5ns" # 55

    tREFI = "0us" # 57

    # active powerdown and precharge powerdown exit time
    tXP = "6ns" # 58

    # self refresh exit time
    tXS = "10ns" # 57

    # Same bank group CAS to CAS delay
    tCCD_L = "7.5ns" # 75 Must be higher than tBURST

    # Current values from datasheet Die Rev E,J
    IDD0 = "437mA" # 33
    IDD2N = "90mA" # 33
    IDD3N = "95mA" # 33
    IDD4W = "230mA" # 33
    IDD4R = "180mA" # 33
    IDD3P1 = "15mA" # 33
    IDD2P1 = "15mA" # 33
    IDD6 = "15mA" # 33
    VDD = "1.2V" # 28

