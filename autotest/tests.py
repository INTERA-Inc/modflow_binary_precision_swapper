import os
import sys
import shutil
sys.path.insert(0,"flopy")
import numpy as np
import flopy
print(flopy.__file__)

sys.path.insert(0,os.path.join("..","src"))
import precision_swapper


def test_single():
	fdir = "test_single_files"
	files = os.listdir(fdir)
	for f in files:
		fext = f.split(".")[-1].lower()
		if fext not in ["hds","ucn"]:
			continue
		if fext == "hds":
			fxn = flopy.utils.HeadFile
		else:
			fxn = flopy.utils.UcnFile

		precision_swapper.swap_precision(os.path.join(fdir,f),"single","test_double.{0}".format(fext),"double")
		org_bfile = fxn(os.path.join(fdir,f),precision="single")
		new_bfile = fxn("test_double.{0}".format(fext),precision="double")
		for totim in org_bfile.times:
			arr1 = org_bfile.get_data(totim=totim)
			arr2 = new_bfile.get_data(totim=totim)
			arr1[np.abs(arr1) > 1.e+10] = 0.0
			arr2[np.abs(arr2) > 1.e+10] = 0.0
			d = np.abs(arr1 - arr2).sum()
			print(totim,d)
			assert d < 0.001
		precision_swapper.swap_precision("test_double.{0}".format(fext), "double", "test_single.{0}".format(fext),"single")
		org_bfile = fxn("test_double.{0}".format(fext), precision="double")
		new_bfile = fxn("test_single.{0}".format(fext), precision="single")
		for totim in org_bfile.times:
			arr1 = org_bfile.get_data(totim=totim)
			arr2 = new_bfile.get_data(totim=totim)
			arr1[np.abs(arr1) > 1.e+10] = 0.0
			arr2[np.abs(arr2) > 1.e+10] = 0.0
			d = np.abs(arr1 - arr2).sum()
			print(totim, d)
			assert d < 0.001

def test_double():
	fdir = "test_double_files"
	files = os.listdir(fdir)
	for f in files:
		fext = f.split(".")[-1].lower()
		if fext not in ["hds","ucn"]:
			continue
		if fext == "hds":
			fxn = flopy.utils.HeadFile
		else:
			fxn = flopy.utils.UcnFile

		precision_swapper.swap_precision(os.path.join(fdir,f),"double","test_single.{0}".format(fext),"single",echo=True)
		org_bfile = fxn(os.path.join(fdir,f),precision="double")
		new_bfile = fxn("test_single.{0}".format(fext),precision="single")
		for totim in org_bfile.times:
			arr1 = org_bfile.get_data(totim=totim)
			arr2 = new_bfile.get_data(totim=totim)
			arr1[np.abs(arr1)>1.e+10] = 0.0
			arr2[np.abs(arr2) > 1.e+10] = 0.0
			darr = arr1 - arr2
			d = np.abs(darr).sum()
			print(totim,d)
			assert d < 0.001
		precision_swapper.swap_precision("test_single.{0}".format(fext), "single", "test_double.{0}".format(fext),"double")
		org_bfile = fxn("test_single.{0}".format(fext), precision="single")
		new_bfile = fxn("test_double.{0}".format(fext), precision="double")
		for totim in org_bfile.times:
			arr1 = org_bfile.get_data(totim=totim)
			arr2 = new_bfile.get_data(totim=totim)
			arr1[np.abs(arr1) > 1.e+10] = 0.0
			arr2[np.abs(arr2) > 1.e+10] = 0.0
			d = np.abs(arr1 - arr2).sum()
			print(totim, d)
			assert d < 0.001


if __name__ == "__main__":
	test_double()
	test_single()