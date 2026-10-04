#!/bin/bash
# usage: make_case_figs.sh <scan> <case_dir> <package_dir> <label> <returns_dir>   -> viz/out/<scan>_{wall,cpr_cfd,profile}.png (nice -n 10)
S=$1; C=$2; PK=$3; LB=$4; RD=$5; V=/home/azan/paper6_t6_work/viz; mkdir -p $V/out
MASK=/mnt/e/Paper6-T6/cfd_local_only/archive/paper6_t6_cfd_2026-09_bulk_moved/imagecas_x_raw/extracted/ImageCAS-X_dataset/segmentations/$S.coronary.nii.gz
nice -n 10 python3 $V/viz_imaging.py wall $C $PK $V/out/${S}_wall.png 2>&1 | grep -E "wrote|rror"
nice -n 10 python3 $V/viz_imaging.py cpr $PK $MASK $V/out/${S}_cpr_cfd.png $C 2>&1 | grep -E "wrote|rror"
nice -n 10 python3 $V/viz_p5_profile.py $V/out/${S}_profile.png "$LB: pressure along the lesion vessel (resistance mode)" $RD/M1_probes_${S}_resistance.csv 2>&1 | grep -E "wrote|rror"
