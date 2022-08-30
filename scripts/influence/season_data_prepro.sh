#!/bin/bash
VAR=$1 # precip, t2max,tsurf

FROM=/work/mh1007/MPI-GE_processed/onepct/
FFILE=${FROM}onepct_1850-1999_ens_1-100.${VAR}.nc

TO=/work/mh0033/m300883/3rdPanel/data/influence/$VAR/
TFILE=${TO}onepct_1850-1999_ens_1-100.${VAR}.nc

# do pre-process
cdo -P 48 -f nc -yearmean -selmonth,1,2,3,4 -selyear,1851/1999 -shifttime,1mo ${FFILE} ${TFILE}
