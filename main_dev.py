"""
This file is for development and testing of your code.
It's only intended for your use during development, and will not be assessed.

It contains example to demonstrate how to use modules defined by analyst groups,
and how to run the report generation function defined in manager_subject_G_XY.py.

You can run this file directly to test your code during development.
"""

# Simple example to demonstrate usage of rules defined in external.BIManalyst_g_xy
def simple_example():
    import ifcopenshell

    from external.BIManalyst_g_xy.rules import windowRule
    from external.BIManalyst_g_xy.rules import doorRule

    model = ifcopenshell.open("path/to/ifcfile.ifc")

    windowResult = windowRule.checkRule(model)
    doorResult = doorRule.checkRule(model)

    print("Window result:", windowResult)
    print("Door result:", doorResult)


# Example on how to run the report generation function defined in manager_subject_G_XY.py
# This demonstrates how other users would call your code to generate reports.
def run_report_generation():
    from pathlib import Path
    import manager_subject_G_XY
    ifc_model_path = Path("path/to/ifcfile.ifc")
    output_directory = Path("path/to/output/dir")

    # Run the analysis and generate reports
    results = manager_subject_G_XY.run_analysis(ifc_model_path,
                                                output_directory,
                                                options={
                                                    "consider_x": True,
                                                    "data_input_xyz": "path/to/datafile.xyz"
                                                })
    
    # Print overview of generated reports, data files, and errors
    print("Analysis completed. Results:")
    print(f"Main report: {results.main_report.file_path} - {results.main_report.description}")
    for data_file in results.data_files:
        print(f"Data file: {data_file.file_path} - {data_file.description}")
    for ifc_model in results.ifc_models_output:
        print(f"IFC model: {ifc_model.file_path} - {ifc_model.description}")
    for error in results.errors:
        print(f"Error: {error}")
    for report in results.supplementary_reports:
        print(f"Supplementary report: {report.file_path} - {report.description}")


# Program entry point for development testing
if __name__ == "__main__":
    # Comment/uncomment which function to run
    simple_example()
    # run_report_generation()
