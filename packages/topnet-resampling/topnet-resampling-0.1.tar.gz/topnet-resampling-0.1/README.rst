Resampling of streamq files
-------------------------------------

This script will average the streamq file to daily, monthly or weekly.

- Python Requirements: xarray netcdf4
- Other Requirements: ncatted needs to be avialable (part of NCO)
- prerequisite: run the fix_streamq.sh script on the streamq file. This will remove the time:bounds attribute on the target netcdf file.
- `resample_streamq streamq.nc {1D,1M,7D} --variables [list of variables to resample]`


Currently we have the following available variables:

- Resample by sum: aprecip, drainge, soilevp, potevap, canevap, snowevp
- Resample by averaging: river_flow_rate_mod



