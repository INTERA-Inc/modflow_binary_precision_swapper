import os
import sys
sys.path.insert(0,"flopy")
import numpy as np
import flopy
print(flopy.__file__)


def swap_ucn_precision_from_double_to_single(org_filename,new_filename):
	assert os.path.exists(org_filename)
	assert org_filename != new_filename
	ucn = flopy.utils.UcnFile("MT3D001.UCN",precision="double")
	org_header_dt = ucn.header_dtype
	new_header_items = [("totim","<f4") if d[0] == "totim" else d for d in org_header_dt.descr]
	header_dt = np.dtype(new_header_items)
	f = open(new_filename,'wb')
	for rec in ucn.recordarray:
		full_arr = ucn.get_data(totim=rec[3])
		print(rec,full_arr.dtype)
		full_arr = full_arr.astype("<f4")
		arr = full_arr[rec[-1]-1,:,:]
		header = np.array(tuple(rec), dtype=header_dt)
		header.tofile(f)
		arr.tofile(f)

	f.close()


def test():
	#swap_ucn_precision_from_double_to_single("MT3D001.UCN", "test.ucn")
	ucn1 = flopy.utils.UcnFile("MT3D001.UCN",precision="double")
	ucn2 = flopy.utils.UcnFile("test.ucn")
	for totim in ucn1.times:
		arr1 = ucn1.get_data(totim=totim)
		arr2 = ucn2.get_data(totim=totim)
		d = np.abs(arr1 - arr2).sum()
		print(totim,d)


if __name__ == "__main__":
	#swap_ucn_precision("MT3D001.UCN","test.ucn")
	test()