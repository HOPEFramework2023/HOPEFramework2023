#!/bin/sh
rm -rf m5out_bwaves_dram_test_timing_caches
./build/X86/gem5.fast --outdir=m5out_bwaves_stt_test_timing_caches ./configs/example/fs.py --cpu-clock 3GHz --kernel /home/markus/.cache/gem5/x86-linux-kernel-4.19.83 --disk-image /mnt/hgfs/Fast/spec-2017 --script script_bwaves_stt_test.rcS --mem-size 4GB --cpu-type TimingSimpleCPU --caches --l1d_size=32kB --l1i_size=32kB --l2_size=256kB --mem-type STT_1333_4x16 2>&1 | tee bwaves_stt_test_timing_caches_out.log
mv bwaves_stt_test_timing_caches_out.log m5out_bwaves_stt_test_timing_caches/gem5.log
mkdir m5out_bwaves_stt_test_timing_caches/SPEC2017_out
mv m5out_bwaves_stt_test_timing_caches/CPU2017* m5out_bwaves_stt_test_timing_caches/SPEC2017_out/
python3 cMcPAT/Scripts/GEM5ToMcPAT.py m5out_bwaves_stt_test_timing_caches/stats.txt m5out_bwaves_stt_test_timing_caches/config.json cMcPAT/mcpat/ProcessorDescriptionFiles/x86_TimingSimpleCPU_template.xml -o m5out_bwaves_stt_test_timing_caches/mcpat.in
./cMcPAT/mcpat/mcpat -infile m5out_bwaves_stt_test_timing_caches/mcpat.in -print_level 7 > m5out_bwaves_stt_test_timing_caches/mcpat.out
python3 cMcPAT/Scripts/print_energy.py m5out_bwaves_stt_test_timing_caches/mcpat.out m5out_bwaves_stt_test_timing_caches/stats.txt > m5out_bwaves_stt_test_timing_caches/print_energy.out