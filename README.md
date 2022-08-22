# modflow_binary_precision_swapper

Example usage:

import precision_swapper
org_filename = "MT3D001.UCN"
new_filename = "single.ucn"
precision_swapper.swap_precision(org_filename,"double",new_filename,"single")

org_filename = "model.hds" #single  precision
new_filename = "model_double.hds"
precision_swapper.swap_precision(org_filename,"single",new_filename,"double")
