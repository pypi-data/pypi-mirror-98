import argparse
import xarray as xr


all_variables_for_sum = ["aprecip", "drainge", "soilevp", "potevap", "canevap", "snowevp"]
all_variables_for_mean = ["river_flow_rate_mod", "soilh2o"]
suffix_output = {'1D': 'Daily', '1M': 'Monthly', '7D': "Weekly"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_nc", type=str, help="Input file (TopNet streamq file)")
    parser.add_argument("--resampling_interval", choices=["1D","1M", "7D"], default="1D", 
                        help="Choose the resampling interval: 1D (daily), 1M (monthly) or 7D (weekly)")
    parser.add_argument("--variables", nargs="+", default=["river_flow_rate_mod", "aprecip"],
                        help="Space separated list of the variables to resample. Currently accepting "
                                 + ", ".join(all_variables_for_sum + all_variables_for_mean))
    return parser.parse_args()


def main():
    args = parse_args()
    input_nc = args.input_nc
    resampling_interval = args.resampling_interval
    variables = args.variables

    print("Inputs: ", input_nc, resampling_interval, variables)
    DS = xr.open_dataset(input_nc)

    variables_for_mean = []
    variables_for_sum = []
    output_file_name = input_nc.split(".")[0]+ "-" + suffix_output[resampling_interval] + ".nc"
        
    print("Will create the output file: ", output_file_name)

    for variable in variables:
        if variable in all_variables_for_sum:
            variables_for_sum.append(variable)
        elif variable in all_variables_for_mean:
            variables_for_mean.append(variable)
        else:
            print("Variable {} is not on the allowed variables for mean: {} or for sum: {}. Ignoring".format(
                        variable, all_variables_for_mean, all_variables_for_sum))

    if len(variables_for_mean) > 0:
        print("Resampling variables (mean)", variables_for_mean)
        DS_variables_mean = DS[variables_for_mean]
        DS_variables_mean_resampled = DS_variables_mean.resample(time=resampling_interval).mean()
    
    if len(variables_for_sum) > 0:
        print("Resampling variables (sum)", variables_for_sum)
        DS_variables_sum = DS[variables_for_sum]
        DS_variables_sum_resampled = DS_variables_sum.resample(time=resampling_interval).sum()

    if len(variables_for_mean) > 0 and len(variables_for_sum) > 0:
        DS_resampled = xr.merge([DS_variables_mean_resampled, DS_variables_sum_resampled])
    elif len(variables_for_mean) == 0:
        DS_resampled = DS_variables_sum_resampled
    else:
        DS_resampled = DS_variables_mean_resampled 

    # Adding the reaches
    DS_resampled["rchid"] = DS["rchid"]

    # Editing the time attributes
    # This does not do anything, here just as an example
    # time = DS_resampled.time.to_index()
    # time_utc = time.tz_localize(pytz.UTC)
    # local_series = time_utc.to_series(keep_tz=True)
    # local_da = xr.DataArray.from_series(local_series)
    # DS_resampled['time'] = local_da

    DS_resampled.time.attrs["_FillValue"] = -9999
    DS_resampled.time.attrs["axis"] = "T"
    DS_resampled.time.attrs["standard_name"] = "time"

    # Editing the global attributes
    DS_resampled.attrs["source"] = "Averaged values for {} from streamq {}".format(
                                        variables_for_mean + variables_for_sum,
                                        input_nc)
    DS_resampled.attrs["institute"] = "NIWA"
    DS_resampled.attrs["title"] = "Averaged streamq values from TopNet"


    DS_resampled.to_netcdf(output_file_name)


if __name__ == "__main__":
    main()


