#!/bin/bash
# activate environment
conda activate thirdPanel

# go to 
cd /work/mh0033/m300883/3rdPanel/docs

# upload
swift upload 3rdPanel build
