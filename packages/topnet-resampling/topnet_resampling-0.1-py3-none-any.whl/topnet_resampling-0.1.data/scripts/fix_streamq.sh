#!/bin/bash

usage="$0 streamq_file.nc"

INPUT_FILE=$1
if [ "${INPUT_FILE}" == "" ]; then
  echo "Please provide an input file: ${usage}"
  exit 1
fi

ncatted -O -a bounds,time,d,, "${INPUT_FILE}"

echo "Removed time:bounds from ${INPUT_FILE}"
