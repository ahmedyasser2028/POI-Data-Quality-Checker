# POI-Data-Quality-Checker
A GIS data quality control tool built with Python and ArcPy to identify common issues in Points of Interest (POI) datasets.

## Features

- Detect missing POI names
- Identify duplicate names
- Generate a QC report table

## Requirements

- ArcGIS Pro
- Python 3.x
- ArcPy

## Workflow

1. The script scans the POI dataset.
2. It identifies missing and duplicated names.
3. Issues are stored in a QC report table.

## Example Issues Detected

| OBJECTID | POI_Name | QC_Issue |
|----------|----------|---------|
| 105 | NULL | Missing name |
| 322 | Cafe Cairo | Duplicate name |

## Usage

Update the input layer and workspace paths:

```python
input_layer = r"path_to_poi_layer"
arcpy.env.workspace = r"path_to_gdb"
