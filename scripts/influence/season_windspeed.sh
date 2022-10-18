#!/bin/bash
U=u10
V=v10

FROM=/work/mh1007/MPI-GE_processed/onepct/
UFILE=${FROM}onepct_1850-1999_ens_1-100.u10.nc
VFILE=${FROM}onepct_1850-1999_ens_1-100.v10.nc

TO=/work/mh0033/m300883/3rdPanel/data/influence/windspeed/
TFILE=${TO}onepct_1850-1999_ens_1-100.windspeed.nc


TMP=/scratch/m/m300883/

mkdir -p ${TMPU}
mkdir -p ${TMPV}

FTMPU=${TMP}u.nc
FTMPV=${TMP}v.nc


# do select and yearly mean
cdo -P 48 -f nc -r -yearmean -selmonth,1,2,3,4 -selyear,1851/1999 -shifttime,1mo ${UFILE} ${FTMPU}
cdo -P 48 -f nc -r -yearmean -selmonth,1,2,3,4 -selyear,1851/1999 -shifttime,1mo ${VFILE} ${FTMPV}

# do square and square root
cdo -P 48 -f nc -r -sqrt -add -sqr ${FTMPU} -sqr ${FTMPV} ${TFILE}

# do anomaly 
cdo -P 48 -f nc -r -sub ${TFILE} -timmean ${TFILE} ${TFILE:0:-2}ano.nc

rm -f ${TMPU}
rm -f ${TMPV}