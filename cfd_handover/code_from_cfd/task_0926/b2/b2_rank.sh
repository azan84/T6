#!/bin/bash
# per-rank binding wrapper of the B2 runs (OpenMPI 4.1.2 ignores a taskset applied to mpirun and rebinds every job to the first cores; --cpu-set/--cpu-list fail silently on this host):
# rank r of a job whose cpu base is B2_CPU_BASE runs on the two logical CPUs of ONE physical core: cpus B+2r and B+2r+1 (SMT siblings on this host: cpu 2k and 2k+1 are core k).
# usage (inside mpirun --bind-to none): b2_rank.sh <command> [args]     env: B2_CPU_BASE (0 for L16 and job A, 16 for job B)
r=${OMPI_COMM_WORLD_LOCAL_RANK:?OMPI_COMM_WORLD_LOCAL_RANK not set (run under mpirun)}; a=$(( ${B2_CPU_BASE:?B2_CPU_BASE not set} + 2 * r ))
exec taskset -c "$a,$((a + 1))" "$@"
