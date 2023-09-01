#!/usr/bin/env python

import os
import stat

bechmarks = [
"600.perlbench_s",
"602.gcc_s",
"605.mcf_s",
"620.omnetpp_s",
"623.xalancbmk_s",
"625.x264_s",
"631.deepsjeng_s",
"641.leela_s",
"648.exchange2_s",
"657.xz_s",
"603.bwaves_s",
"607.cactuBSSN_s",
"619.lbm_s",
"621.wrf_s",
"627.cam4_s",
"628.pop2_s",
"638.imagick_s",
"644.nab_s",
"649.fotonik3d_s",
"654.roms_s"
]

cpus = {"TimingSimpleCPU": {"caches": True, "name": "timing", "mcPatTemplate": "x86_TimingSimpleCPU_template.xml"},
        #"AtomicSimpleCPU": {"caches": False, "name": "atomic", "mcPatTemplate": "x86_AtomicSimpleCPU_template.xml"}
}
        
memories = {"dram": "DDR4_2400_8x8", "stt": "STT_1333_4x16"}

CACHES_ARGS = "--caches --l1d_size=32kB --l1i_size=32kB --l2_size=256kB"

RUN_TEMPLATE = """#!/bin/sh
rm -rf m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}
./build/X86/gem5.fast --outdir=m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME} ./configs/example/fs.py --cpu-clock 3GHz --kernel /home/markus/.cache/gem5/x86-linux-kernel-4.19.83 --disk-image /mnt/hgfs/Fast/spec-2017 --script script_{BENCH_NAME}_dram_test.rcS --mem-size 4GB --cpu-type {CPU} {CACHE} --mem-type {MEM_DEVICE} 2>&1 | tee {BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}_out.log
mv {BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}_out.log m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/gem5.log
mkdir m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/SPEC2017_out
mv m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/CPU2017* m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/SPEC2017_out/
python3 cMcPAT/Scripts/GEM5ToMcPAT.py m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/stats.txt m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/config.json cMcPAT/mcpat/ProcessorDescriptionFiles/{MCPAT_TEMPLATE} -o m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/mcpat.in
./cMcPAT/mcpat/mcpat -infile m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/mcpat.in -print_level 7 > m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/mcpat.out
python3 cMcPAT/Scripts/print_energy.py m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/mcpat.out m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/stats.txt > m5out_{BENCH_NAME}_{MEM}_test_{CPU_NAME}{CACHE_NAME}/print_energy.out"""

SCRIPT_TEMPLATE = "{BENCH} test ."


def main():
    for benchmark in bechmarks:
        benchname = benchmark.split(".")[1][:-2]
        with open("script_" + benchname + "_dram_test.rcS", "w") as script_file:
            script_file.write(SCRIPT_TEMPLATE.format(BENCH = benchmark))
        for cpu in cpus:
            for mem in memories:
                run_file_name = "run_" + benchname + "_" + mem + "_test_" + cpus[cpu]["name"]
                if cpus[cpu]["caches"]:
                    run_file_name = run_file_name + "_caches"
                run_file_name = run_file_name + ".sh"
                with open(run_file_name, "w") as run_file:
                    if cpus[cpu]["caches"]:
                        run_file.write(RUN_TEMPLATE.format(BENCH_NAME = benchname, CPU_NAME = cpus[cpu]["name"], CACHE_NAME = "_caches", CPU = cpu, CACHE = CACHES_ARGS, MCPAT_TEMPLATE = cpus[cpu]["mcPatTemplate"], MEM = mem, MEM_DEVICE = memories[mem] ))
                    else:
                        run_file.write(RUN_TEMPLATE.format(BENCH_NAME = benchname, CPU_NAME = cpus[cpu]["name"], CACHE_NAME = "", CPU = cpu, CACHE = "", MCPAT_TEMPLATE = cpus[cpu]["mcPatTemplate"], MEM = mem, MEM_DEVICE = memories[mem] ))
                os.chmod(run_file_name, stat.S_IRWXU)


if __name__ == '__main__':
    main()
