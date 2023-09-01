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

from m5.objects.MemCtrl import MemCtrl
from m5.objects.MemInterface import *

# Enum for the page policy, either open, open_adaptive, close, or
# close_adaptive.
class PageManage(Enum): vals = ['open', 'open_adaptive', 'close',
                                'close_adaptive']

class STTDDR4Interface(MemInterface):
    type = 'STTDDR4Interface'
    cxx_header = "mem/sttddr4_interface.hh"
    cxx_class = 'gem5::memory::STTDDR4Interface'

    # scheduler page policy
    page_policy = Param.PageManage('open_adaptive', "Page management policy")

    # enforce a limit on the number of accesses per row
    max_accesses_per_row = Param.Unsigned(16, "Max accesses per row before "
                                          "closing");

    # default to 0 bank groups per rank, indicating bank group architecture
    # is not used
    # update per memory class when bank group architecture is supported
    bank_groups_per_rank = Param.Unsigned(0, "Number of bank groups per rank")

    # Enable STTDDR4 powerdown states if True. This is False by default due to
    # performance being lower when enabled
    enable_dram_powerdown = Param.Bool(False, "Enable powerdown states")

    # For power modelling we need to know if the STTDDR4 has a DLL or not
    dll = Param.Bool(True, "STTDDR4 has DLL or not")

    # STTDDR4Power provides in addition to the core power, the possibility to
    # include RD/WR termination and IO power. This calculation assumes some
    # default values. The integration of STTDDR4Power with gem5 does not include
    # IO and RD/WR termination power by default. This might be added as an
    # additional feature in the future.

    # timing behaviour and constraints - all in nanoseconds

    # the amount of time in nanoseconds from issuing an activate command
    # to the data being available in the row buffer for a read
    tRCD = Param.Latency("RAS to Read CAS delay")

    # the amount of time in nanoseconds from issuing an activate command
    # to the data being available in the row buffer for a write
    tRCD_WR = Param.Latency(Self.tRCD, "RAS to Write CAS delay")

    # the time from issuing a read command to seeing the actual data
    tCL = Param.Latency("Read CAS latency")

    # the time from issuing a write command to seeing the actual data
    tCWL = Param.Latency(Self.tCL, "Write CAS latency")

    # minimum time between a precharge and subsequent activate
    tRP = Param.Latency("Row precharge time")

    # minimum time between an activate and a precharge to the same row
    tRAS = Param.Latency("ACT to PRE delay")

    # minimum time between a write data transfer and a precharge
    tWR = Param.Latency("Write recovery time")

    # minimum time between a read and precharge command
    tRTP = Param.Latency("Read to precharge")

    # tBURST_MAX is the column array cycle delay required before next access,
    # which could be greater than tBURST when the memory access time is greater
    # than tBURST
    tBURST_MAX = Param.Latency(Self.tBURST, "Column access delay")

    # tBURST_MIN is the minimum delay between bursts, which could be less than
    # tBURST when interleaving is supported
    tBURST_MIN = Param.Latency(Self.tBURST, "Minimim delay between bursts")

    # CAS-to-CAS delay for bursts to the same bank group
    # only utilized with bank group architectures; set to 0 for default case
    # tBURST is equivalent to tCCD_S; no explicit parameter required
    # for CAS-to-CAS delay for bursts to different bank groups
    tCCD_L = Param.Latency("0ns", "Same bank group CAS to CAS delay")

    # Write-to-Write delay for bursts to the same bank group
    # only utilized with bank group architectures; set to 0 for default case
    # This will be used to enable different same bank group delays
    # for writes versus reads
    tCCD_L_WR = Param.Latency(Self.tCCD_L,
      "Same bank group Write to Write delay")

    # time taken to complete one refresh cycle (N rows in all banks)
    tRFC = Param.Latency("Refresh cycle time")

    # time to store data in the persistant memory array
    tST = Param.Latency("Store operation period")

    # refresh command interval, how often a "ref" command needs
    # to be sent. It is 7.8 us for a 64ms refresh requirement
    tREFI = Param.Latency("Refresh command interval")

    # write-to-read, same rank turnaround penalty for same bank group
    tWTR_L = Param.Latency(Self.tWTR, "Write to read, same rank switching "
                           "time, same bank group")

    # minimum precharge to precharge delay time
    tPPD = Param.Latency("0ns", "PRE to PRE delay")

    # maximum delay between two-cycle ACT command phases
    tAAD = Param.Latency(Self.tCK,
                         "Maximum delay between two-cycle ACT commands")

    two_cycle_activate = Param.Bool(False,
                         "Two cycles required to send activate")

    # minimum row activate to row activate delay time
    tRRD = Param.Latency("ACT to ACT delay")

    # only utilized with bank group architectures; set to 0 for default case
    tRRD_L = Param.Latency("0ns", "Same bank group ACT to ACT delay")

    # time window in which a maximum number of activates are allowed
    # to take place, set to 0 to disable
    tXAW = Param.Latency("X activation window")
    activation_limit = Param.Unsigned("Max number of activates in window")

    # time to exit power-down mode
    # Exit power-down to next valid command delay
    tXP = Param.Latency("0ns", "Power-up Delay")

    # Exit Powerdown to commands requiring a locked DLL
    tXPDLL = Param.Latency("0ns", "Power-up Delay with locked DLL")

    # time to exit self-refresh mode
    tXS = Param.Latency("0ns", "Self-refresh exit latency")

    # time to exit self-refresh mode with locked DLL
    tXSDLL = Param.Latency("0ns", "Self-refresh exit latency DLL")

    # number of data beats per clock. with DDR, default is 2, one per edge
    # used in drampower.cc
    beats_per_clock = Param.Unsigned(2, "Data beats per clock")

    data_clock_sync = Param.Bool(False, "Synchronization commands required")

    # Currently rolled into other params
    ######################################################################

    # tRC  - assumed to be tRAS + tRP

    # Power Behaviour and Constraints
    # STTDDR4s like LPDDR and WideIO have 2 external voltage domains. These are
    # defined as VDD and VDD2. Each current is defined for each voltage domain
    # separately. For example, current IDD0 is active-precharge current for
    # voltage domain VDD and current IDD02 is active-precharge current for
    # voltage domain VDD2.
    # By default all currents are set to 0mA. Users who are only interested in
    # the performance of STTDDR4s can leave them at 0.

    # Operating 1 Bank Active-Precharge current
    IDD0 = Param.Current("0mA", "Active precharge current")

    # Operating 1 Bank Active-Precharge current multiple voltage Range
    IDD02 = Param.Current("0mA", "Active precharge current VDD2")

    # Precharge Power-down Current: Slow exit
    IDD2P0 = Param.Current("0mA", "Precharge Powerdown slow")

    # Precharge Power-down Current: Slow exit multiple voltage Range
    IDD2P02 = Param.Current("0mA", "Precharge Powerdown slow VDD2")

    # Precharge Power-down Current: Fast exit
    IDD2P1 = Param.Current("0mA", "Precharge Powerdown fast")

    # Precharge Power-down Current: Fast exit multiple voltage Range
    IDD2P12 = Param.Current("0mA", "Precharge Powerdown fast VDD2")

    # Precharge Standby current
    IDD2N = Param.Current("0mA", "Precharge Standby current")

    # Precharge Standby current multiple voltage range
    IDD2N2 = Param.Current("0mA", "Precharge Standby current VDD2")

    # Active Power-down current: slow exit
    IDD3P0 = Param.Current("0mA", "Active Powerdown slow")

    # Active Power-down current: slow exit multiple voltage range
    IDD3P02 = Param.Current("0mA", "Active Powerdown slow VDD2")

    # Active Power-down current : fast exit
    IDD3P1 = Param.Current("0mA", "Active Powerdown fast")

    # Active Power-down current : fast exit multiple voltage range
    IDD3P12 = Param.Current("0mA", "Active Powerdown fast VDD2")

    # Active Standby current
    IDD3N = Param.Current("0mA", "Active Standby current")

    # Active Standby current multiple voltage range
    IDD3N2 = Param.Current("0mA", "Active Standby current VDD2")

    # Burst Read Operating Current
    IDD4R = Param.Current("0mA", "READ current")

    # Burst Read Operating Current multiple voltage range
    IDD4R2 = Param.Current("0mA", "READ current VDD2")

    # Burst Write Operating Current
    IDD4W = Param.Current("0mA", "WRITE current")

    # Burst Write Operating Current multiple voltage range
    IDD4W2 = Param.Current("0mA", "WRITE current VDD2")

    # Refresh Current
    IDD5 = Param.Current("0mA", "Refresh current")

    # Refresh Current multiple voltage range
    IDD52 = Param.Current("0mA", "Refresh current VDD2")

    # Self-Refresh Current
    IDD6 = Param.Current("0mA", "Self-refresh Current")

    # Self-Refresh Current multiple voltage range
    IDD62 = Param.Current("0mA", "Self-refresh Current VDD2")

    # Main voltage range of the STTDDR4
    VDD = Param.Voltage("0V", "Main Voltage Range")

    # Second voltage range defined by some STTDDR4s
    VDD2 = Param.Voltage("0V", "2nd Voltage Range")

    def controller(self):
        """
        Instantiate the memory controller and bind it to
        the current interface.
        """
        controller = MemCtrl()
        controller.dram = self
        return controller

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

