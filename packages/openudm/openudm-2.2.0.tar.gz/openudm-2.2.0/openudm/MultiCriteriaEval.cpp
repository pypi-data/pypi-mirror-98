#include "MultiCriteriaEval.h"

void MaskedWeightedSum(bool useBin, 
  										 const std::string& iRasCount, 
  										 const std::string& iRasInputs, 
  										 const std::string& dRasCount, 
  										 const std::string& dRasInputs, 
  										 const std::string& output,	
  										 const std::string& rastHdr, 
  										 const std::string& binConfigPath, 
  										 bool reverse) {
  //new - BEGIN
	std::string swap_path = binConfigPath;
	//new - END

	//cout << "Reading Data..." << endl;

	bool bin_ras = useBin;
	bool rev = reverse;

	//setup single item read string
	std::vector<std::string> singleItemStr(1);

	//variables to store number of input IRasters/DRasters
	int numI, numD;

	//IRasters Setup BEGIN---------------------------------------------------

	//read numI
	ExtractCSV(iRasCount, 1, 0, singleItemStr);
	numI = std::stoi(singleItemStr[0]);
	//cout << "numI = " << numI << endl;

	//variables to store IRaster names and weights
	std::vector<std::string> iRasStr(numI);
	std::vector<std::string> iWgtStr(numI);
	std::vector<double> iWgt(numI);

	//read rasters column from csv
	ExtractCSV(iRasInputs, 4, 1, iRasStr);

	//read weights column from csv
	ExtractCSV(iRasInputs, 4, 2, iWgtStr);

	//convert string data to double
	for (int i = 0; i != numI; ++i) {
		iWgt[i] = std::stod(iWgtStr[i]);
	}

	//setup a vector of IRasters
	std::vector<IRaster> iVec(numI);

	//setup and read rasters
	for (int i = 0; i != numI; ++i) {		

		iVec[i].Setup(rastHdr);

		if (bin_ras){
			iVec[i].FromPGBinary(swap_path + iRasStr[i]);
		}
		else {
			iVec[i].FromCSV(swap_path + iRasStr[i]);
			std::cout << "reading " << swap_path + iRasStr[i] << std::endl;
		}
	}

	//IRasters Setup END-----------------------------------------------------

	//DRasters Setup BEGIN---------------------------------------------------

	//read numD
	ExtractCSV(dRasCount, 1, 0, singleItemStr);
	numD = std::stoi(singleItemStr[0]);
	//cout << "numD = " << numD << endl;

	//variables to store DRaster names and weights
	std::vector<std::string> dRasStr(numD);
	std::vector<std::string> dWgtStr(numD);
	std::vector<double> dWgt(numD);

	//read rasters column from csv
	ExtractCSV(dRasInputs, 4, 1, dRasStr);

	//read weights column from csv
	ExtractCSV(dRasInputs, 4, 2, dWgtStr);

	//convert string data to double
	for (int d = 0; d != numD; ++d) {
		dWgt[d] = std::stod(dWgtStr[d]);
	}

	//setup a vector of DRasters
	std::vector<DRaster> dVec;

	//push back by numD
	for (int d = 0; d != numD; ++d) {
		dVec.push_back(DRaster());
	}

	//setup and read rasters
	for (int d = 0; d != numD; ++d) {

		dVec[d].Setup(rastHdr);

		if (bin_ras) {
			dVec[d].FromPGBinary(swap_path + dRasStr[d]);
		}
		else {
			dVec[d].FromCSV(swap_path + dRasStr[d]);
			std::cout << "reading " << swap_path + dRasStr[d] << std::endl;
		}
	}

	//IRasters Setup END-----------------------------------------------------

	//setup result raster - cells initialised to 0.0 by default
	DRaster result;
	result.Setup(rastHdr);

	//initialise cells to 1.0 when reversing
	if (rev) {
		for (int r = 0; r != result.nrows; ++r) {
			for (int c = 0; c != result.ncols; ++c) {
				result.data[r][c] = 1.0;
			}
		}
	}

	//SUM IRASTERS
	if (!iVec.empty()) {
		for (int i = 0; i != numI; ++i) {
			if (iWgt[i] < 0.0f) {				//-ve weight indicates mask raster - don't include in sum
			}
			else {
				for (int r = 0; r != result.nrows; ++r) {
					for (int c = 0; c != result.ncols; ++c) {

						if (rev) {
							result.data[r][c] -= iVec[i].data[r][c] * iWgt[i];		//weighted summed subtraction from 1.0
						}
						else {
							result.data[r][c] += iVec[i].data[r][c] * iWgt[i];		//weighted summed addition from 0.0
						}
					}
				}
			}
		}
	}

	//SUM DRASTERS
	if (!dVec.empty()) {
		for (int d = 0; d != numD; ++d) {
			for (int r = 0; r != result.nrows; ++r) {
				for (int c = 0; c != result.ncols; ++c) {

					if (rev) {
						result.data[r][c] -= dVec[d].data[r][c] * dWgt[d];		//weighted summed subtraction from 1.0
					}
					else {
						result.data[r][c] += dVec[d].data[r][c] * dWgt[d];		//weighted summed addition from 0.0
					}
				}
			}			
		}
	}

	//APPLY MASK
	for (int i = 0; i != numI; ++i) {
		if (iWgt[i] < 0.0f) {				//-ve weight indicates mask raster - apply mask

			for (int r = 0; r != result.nrows; ++r) {
				for (int c = 0; c != result.ncols; ++c) {

					if (iVec[i].data[r][c] == iVec[i].NODATA_value) {
						result.data[r][c] = result.NODATA_value;		//set result to NODATA_value where mask is NODATA_value
					}
					else {
						result.data[r][c] *= iVec[i].data[r][c];		//otherwise multiply by mask (0 or 1)
					}
				}
			}
		}		
	}

	//write result to file
	if (bin_ras) {
		result.ToPGBinary(binConfigPath, output);
	}
	else {
		result.ToCSV(output);
	}

	//cout << "Writing Data..." << endl;
}