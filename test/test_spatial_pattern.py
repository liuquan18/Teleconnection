
import xarray as xr

import src.Teleconnection.spatial_pattern as ssp
import src.Teleconnection.tools as tools

ex = xr.open_dataset("/work/mh0033/m300883/3rdPanel/data/sample.nc")

data = ex.isel(hlayers = 0).var156
data = tools.stack_ens(data,withdim = 'time')

eof,pc,fra = ssp.doeof(data,nmode = 2)

# do eof
def test_doeof():
    assert fra >0

# project field
ppc = ssp.project_field(data,eof)

