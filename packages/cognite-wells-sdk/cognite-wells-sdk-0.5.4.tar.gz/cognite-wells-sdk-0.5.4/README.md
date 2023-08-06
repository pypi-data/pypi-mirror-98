# well-model


Python scripts for ingestion and query of wells in CDF. 
Also some notebook examples on how to use are available in the examples folder.

## Running locally

### Install poetry

If you don't yet have poetry installed and configured to use artifactory, follow the steps in
[Cognite's Python guide](https://github.com/cognitedata/python-developer-hub)

### Install dependencies

In the root folder of the project, use poetry to install dependencies:
```bash
poetry install
```

### Add pre-commit

Pre-commit will allow you to test your changes in the linting and formatting tools before commiting them, to avoid
failing the Jenkins build. It is installed as a dev dependency in the project, so yu just have to initialize by running:
```bash
pre-commit install
```

### Environment variables

```bash
export COGNITE_API_KEY="<use an api key for subsurface-test. If you don't have one, ask a member of the team>"
export COGNITE_PROJECT="subsurface-test"
```

### Run tests
```bash
poetry run pytest
```

## Model files generated from openapi

We use
[datamodel-code-generator](https://pydantic-docs.helpmanual.io/datamodel_code_generator/)
to generated pydantic model files based on the openapi.yaml file. To update it, run
```sh
poetry run make generate-pydantic
```
Or if you want to copy the openapi.yaml file from `../well-service` first, run
```sh
poetry run make pydantic
```

## **Consuming**

### Optionally set your env variables (must be valid for both cdf and geospatial API)

```bash
COGNITE_WELLS_PROJECT=<project-tenant>
COGNITE_WELLS_CREDENTIALS=<your-api-key>
```

Project and key can then be accessed without exposing them in the code. Alternatively, the client can be initialised like:
```python
wells_client = CogniteWellsClient(project="your-project", api_key="your-api-key")
```
```

### Set up client with Api-Key

```python
import os

from cognite.well_model import CogniteWellsClient

wells_client = CogniteWellsClient(project=os.getenv("COGNITE_WELLS_PROJECT"), api_key=os.getenv("COGNITE_WELLS_CREDENTIALS"))
```

### **Well queries**

#### _Get well by id:_

```python
well = wells_client.wells.get_by_id(8456650753594878)
```

#### _List wells:_

```python
wells = wells_client.wells.list()
```

#### _Filter wells by wkt polygon:_

```python
from cognite.well_model.models import PolygonFilter

polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(polygon=PolygonFilter(geometry=polygon, crs="epsg:4326"))
```

#### _Filter wells by wkt polygon, name/description and specify desired outputCrs_

```python
polygon = 'POLYGON ((0.0 0.0, 0.0 80.0, 80.0 80.0, 80.0 0.0, 0.0 0.0))'
wells = wells_client.wells.filter(
    polygon=PolygonFilter(geometry=polygon, crs="epsg:4326", geometry_type="WKT"),
    string_matching="16/",
    output_crs="EPSG:23031"
)
```

#### _Get wells that have a trajectory_

```python
from cognite.well_model.models import TrajectoryFilter

wells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(), limit=None)
```

#### _Get wells that have a trajectory with data between certain depths_

```python
wells = wells_client.wells.filter(has_trajectory=TrajectoryFilter(min_depth=1400.0, max_depth=1500.0), limit=None)
```

#### _Get wells that has the right set of measurement types_

```python
from cognite.well_model.models import MeasurementFilter, MeasurementFilters, MeasurementType

gammarayFilter = MeasurementFilter(measurement_type=MeasurementType.gamma_ray)
densityFilter = MeasurementFilter(measurement_type=MeasurementType.density)

# Get wells with all measurements
measurements_filter = MeasurementFilters(contains_all=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)

# Or get wells with any of the measurements
measurements_filter = MeasurementFilters(contains_any=[gammarayFilter, densityFilter])
wells = wells_client.wells.filter(has_measurements=measurements_filter, limit=None)
```

#### _Get wellbores for a well id:_

```python
wellbores = wells_client.wellbores.get_from_well(well.id)
```

or

```python
well = wells_client.wells.get_by_id(519497487848)
wellbores = well.wellbores()
```

#### _Get wellbores from multiple well ids:_

```python
wellbores = wells_client.wellbores.get_from_wells([17257290836510, 8990585729991697])
```

#### _Filter - list all labels:_

```python
blocks = wells_client.wells.blocks()
fields = wells_client.wells.fields()
operators = wells_client.wells.operators()
quadrants = wells_client.wells.quadrants()
sources = wells_client.wells.sources()
measurementTypes = wells_client.wells.measurements()
```

### **Wellbore queries**

#### _Get wellbore by id:_

```jupyterpython
wellbore = wells_client.wellbores.get_by_id(2360682364100853)
```

#### _Get wellbore measurement for measurementType: 'GammaRay':_

```python
measurements = wells_client.wellbores.get_measurement(wellbore_id=2360682364100853, measurement_type=MeasurementType.gamma_ray)
```

#### _Get trajectory for a wellbore:_

```python
wellbore = wells_client.wellbores.get_by_id(2360682364100853)
trajectory = wellbore.trajectory()
```

Or get it directly from a wellbore id

```python
trajectory = wells_client.surveys.get_trajectory(2360682364100853)
```

### **Survey queries**

#### _Get data from a survey, from start and end rows:_

```python
trajectory_data = wells_client.surveys.get_data(17257290836510, start=0, end=100000, columns=["MD", "AZIMUTH"])
```

#### Get all data from a survey object
```python
trajectory = wells_client.surveys.get_trajectory(2360682364100853)
trajectory_data = trajectory.data()
```

## Ingestion

### Ingest wells
```python
import os
from datetime import date

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleWithUnit, WellDatum, Wellhead, WellIngestion

wells_client = CogniteWellsClient(project=os.getenv("COGNITE_PROJECT"), api_key=os.getenv("COGNITE_API_KEY"))
source_asset_id = 102948135620745 # Id of the well source asset in cdf

well_to_create = WellIngestion(
    asset_id=source_asset_id,
    well_name="well-name",
    description="Optional description for the well",
    country="Norway",
    quadrant="25",
    block="25/5",
    field="Example",
    operator="Operator1",
    spud_date=date(2021, 3, 17),
    water_depth=0.0,
    water_depth_unit="meters",
    wellhead=Wellhead(
        x = 21.0,
        y = 42.0,
        crs = "EPSG:4236" # Must be a EPSG code
    ),
    datum=WellDatum(
        elevation = DoubleWithUnit(value=1.0, unit="meters"),
        reference = "well-datum-reference",
        name = "well-datum-name"
    ),
    source="Source System Name"
)

wells_client.ingestion.ingest_wells([well_to_create]) # Can add multiple WellIngestion objects at once
```

### Ingest wellbores with optional well and/or trajectory
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleArrayWithUnit, TrajectoryIngestion, WellIngestion, WellboreIngestion, ParentType

wells_client = CogniteWellsClient(project=os.getenv("COGNITE_PROJECT"), api_key=os.getenv("COGNITE_API_KEY"))
source_asset_id = 102948135620745 # Id of the wellbore source asset in cdf
source_trajectory_ext_id = "some sequence ext id" # Id of the source sequence in cdf

well_to_create = WellIngestion(...)
trajectory_to_create = TrajectoryIngestion(
    source_sequence_ext_id=source_trajectory_ext_id,
    measured_depths = DoubleArrayWithUnit(values=[0.0, 1.0, 2.0], unit="meters"),
    inclinations = DoubleArrayWithUnit(values=[10.0, 1.0, 22.0], unit="degrees"),
    azimuths = DoubleArrayWithUnit(values=[80.0, 81.0, 82.0], unit="degrees")
)

wellbore_to_create = WellboreIngestion(
    asset_id = source_asset_id,
    wellbore_name = "wellbore name",
    parent_name = "name of parent well or wellbore",
    parent_type = ParentType.well, # or ParentType.wellbore
    source = "Source System Name",
    trajectory_ingestion = trajectory_to_create,
    well_ingestion = well_to_create # if not ingesting a well, then one must already exist
)

wells_client.ingestion.ingest_wells([wellbore_to_create]) # Can add multiple WellboreIngestion objects at once
```

### Ingest wellbores with optional well and/or trajectory
```python
import os

from cognite.well_model import CogniteWellsClient
from cognite.well_model.models import DoubleArrayWithUnit, CasingIngestion

wells_client = CogniteWellsClient(project=os.getenv("COGNITE_PROJECT"), api_key=os.getenv("COGNITE_API_KEY"))
source_casing_id = 102948135620745 # Id of the casing source sequence in cdf


casing_to_ingest = CasingIngestion(
    source_casing_id = source_casing_id,
    wellbore_name = "wellbore name",
    casing_name = "Surface Casing",
    body_inside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),
    body_outside_diameter = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="mm"),
    md_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"),
    md_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m"),
    tvd_top = DoubleArrayWithUnit(values=[100.0, 120.0, 130.0], unit="m"), # TVD measurements are optional
    tvd_base = DoubleArrayWithUnit(values=[120.0, 150.0, 190.0], unit="m") # TVD measurements are optional
)

wells_client.ingestion.ingest_casings([casing_to_ingest]) # Can add multiple CasingIngestion objects at once
```