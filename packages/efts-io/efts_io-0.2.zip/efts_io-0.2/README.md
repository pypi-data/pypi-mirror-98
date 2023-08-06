# efts_io documentation

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/csiro-hydroinformatics/efts-python/blob/master/LICENSE.txt) ![status](https://img.shields.io/badge/status-alpha-orange.svg) 

<!-- master: [![Build status - master](https://ci.appveyor.com/api/projects/status/vmwq7xarxxj8s564/branch/master?svg=true)](https://ci.appveyor.com/project/jmp75/efts-python/branch/master) testing: [![Build status - devel](https://ci.appveyor.com/api/projects/status/vmwq7xarxxj8s564/branch/testing?svg=true)](https://ci.appveyor.com/project/jmp75/efts-python/branch/testing) -->

<!-- ![Reference counted native handles](./img/efts_io-principles.png "Reference counted native handles") -->

Plain text files are not well suited to storing the large volumes of data generated for and by ensemble streamflow forecasts with numerical weather prediction models. netCDF is a binary file format developed primarily for climate, ocean and meteorological data. netCDF has traditionally been used to store time slices of gridded data, rather than complete time series of point data. **efts** is for handling the latter. 

**efts** is designed to handle netCDF data following the [NetCDF for Water Forecasting Conventions v2.0](https://github.com/csiro-hydroinformatics/efts/blob/master/docs/netcdf_for_water_forecasting.md)

## License

MIT (see [License.txt](https://github.com/csiro-hydroinformatics/efts-python/blob/master/LICENSE.txt))

## Source code

The code repository is on [GitHub](https://github.com/csiro-hydroinformatics/efts-python).

## Installation

```sh
pip install efts_io
```

From source:

```sh
pip install -r requirements.txt
python setup.py install
```

## Sample use

Placeholder