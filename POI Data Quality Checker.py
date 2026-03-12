import arcpy


def check_poi_quality(input_layer, name_field, output_table):
    """
    Perform quality control checks on a POI dataset.
    Detects missing names and duplicate names.
    """

    if not arcpy.Exists(input_layer):
        raise Exception(f"Input layer not found: {input_layer}")

    # Delete output table if it exists
    if arcpy.Exists(output_table):
        arcpy.management.Delete(output_table)

    gdb_path = arcpy.env.workspace
    table_name = output_table.split("\\")[-1]

    # Create output table
    arcpy.management.CreateTable(gdb_path, table_name)

    arcpy.management.AddField(output_table, "OBJECTID", "LONG")
    arcpy.management.AddField(output_table, "POI_Name", "TEXT", field_length=255)
    arcpy.management.AddField(output_table, "QC_Issue", "TEXT", field_length=100)

    name_counts = {}
    records = []

    # Read records
    with arcpy.da.SearchCursor(input_layer, ["OBJECTID", name_field]) as cursor:
        for oid, name in cursor:

            val = name or ""

            if val == "":
                records.append((oid, val, "Missing name"))

            name_counts[val] = name_counts.get(val, 0) + 1
            records.append((oid, val, ""))

    # Insert QC results
    with arcpy.da.InsertCursor(
        output_table,
        ["OBJECTID", "POI_Name", "QC_Issue"],
    ) as insert_cursor:

        for oid, name, issue in records:

            if issue:
                insert_cursor.insertRow((oid, name, issue))

            elif name_counts.get(name, 0) > 1:
                insert_cursor.insertRow((oid, name, "Duplicate name"))


def main():

    input_layer = r"path_to_poi_layer"
    name_field = "Primary_Place_Name"

    arcpy.env.workspace = r"path_to_gdb"
    arcpy.env.overwriteOutput = True

    output_table = r"path_to_gdb\POI_QC_Report"

    check_poi_quality(input_layer, name_field, output_table)


if __name__ == "__main__":
    main()
