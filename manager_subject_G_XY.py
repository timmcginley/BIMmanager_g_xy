from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# This template enables other users (teachers in this case) to run your analysis and generate reports in a standardized way.
# Ideally, this should allow running all manager tools in a single script, by calling each manager subject's run_analysis function one after another.
# Therefore, please do not change the function signature of run_analysis, nor the data classes defined below. 
#
# The function run_analysis should perform the analysis defined by this manager subject,
# using any modules defined by the relevant analyst groups (imported from external.BIManalyst_g_xy etc...).
#
# It is a strict requirement for managers that you provide this interface:
#       def run_analysis(model_path: Path, out_dir: Path, options: Dict[str, Any] = dict()) -> AnalysisResults:
#
# It is the primary entry point for assesment of your work as a manager.
# The function should return an AnalysisResults object containing paths to all relevant output files and errors encountered during analysis
#
# IMPORTANT! All output files must be written to the out_dir directory (or its subdirectories) provided as argument to the function.
# Make sure to use the provided out_dir path for all output file operations (it's your responsibility that analysts also do so).

# If your project for some reason cannot conform to this interface, please contact the course staff and we will find a solution.


# Data classes for structured results - DO NOT EDIT
@dataclass
class ResultItem:
    """
    This class describes a single result item produced by the analysis.
    It can represent a report file, data file, or IFC model output.
    This object contains the file path to the file, not the file content itself.
    """
    file_path: Path # Path to the result file
    description: str # Brief description of the result file
    responsible_group: Optional[str] = None # Name of the analyst group responsible for this result (if applicable)

@dataclass
class AnalysisError:
    responsible_group: str # Name of the analyst group where the error occurred
    failed_action: str # Description of the action that failed
    error_message: str # Description of the error

@dataclass
class AnalysisResults:
    """
    This class encapsulates all results produced by the entire analysis (both manager and analyst results).
    """
    main_report: ResultItem # The main report file (either a markdown or HTML file)
    errors: List[AnalysisError] = [] # List of errors encountered during analysis

    supplementary_reports: List[ResultItem] = [] # List of supplementary report files (e.g., markdown or HTML files)
    data_files: List[ResultItem] = [] # List of data files generated as output (e.g., CSV, JSON)
    ifc_models_output: List[ResultItem] = [] # List of IFC models generated as output


#####################################
##### Edit below this line only #####
#####################################

def run_analysis(model_path: Path, out_dir: Path, options: Dict[str, Any] = dict()) -> AnalysisResults: # Do not edit this line itself!
    # Below is a docstring describing this function.
    # Edit the text as needed to describe the analysis performed by this function.
    # If the options argument is used, describe the options here as well, and if they are optional or required.
    """
    Brief description of what analysis this manager subject performs, and what kind of output is expected.

    Args:
        model_path (Path): Path to the input IFC model.
        out_dir (Path): Directory where output files should be saved.
        options (Dict[str, Any], optional): Additional options for the analysis.
    
    options can include:
        consider_x (bool): Whether to consider X in the analysis. Default is True.
        data_input_xyz (Path): Path to an additional data input file for the analysis.
    """

    # Please note that below is just example code to demonstrate how to join file paths,
    # write report files, log analyst errors, and return the AnalysisResults object.
    # You should replace the example code with your actual analysis code.
    # It's recommended to structure your code in separate modules and functions, keeping
    # this function as a high-level orchestrator of the analysis steps and report creation, thus
    # keeping this function minimal, concise and readable.

    # Below is NOT a good example of how to structure your code for a real analysis.
    # It's only intended to demonstrate the required interface and data structures.
    # The right structure of your code will depend on the specific analysis you are performing,
    # and the modules defined by the relevant analyst groups.
    # This code will not run as is, since it depends on fictional modules and functions for demonstration purposes only.

    errors = list()

    import ifcopenshell
    from external.BIManalyst_g_xy.rules import windowRule
    from external.BIManalyst_g_xy.rules import doorRule

    model = ifcopenshell.open(str(model_path))

    # Run analyst rules
    window_result = windowRule.checkRule(model)
    door_result = doorRule.checkRule(model)


    # Create dummy supplementary report files
    supplementary_reports = list()

    window_report_path = out_dir / "window_report.md"
    window_report_path.write_text(f"Window report content here {window_result}.", encoding="utf-8")
    supplementary_reports.append(ResultItem(window_report_path, "Report on windows"))

    door_report_path = out_dir / "door_report.md"
    door_report_path.write_text(f"Door report content here {door_result}.", encoding="utf-8")
    supplementary_reports.append(ResultItem(door_report_path, "Report on doors"))


    # Specify generated data files and IFC models
    data_files = list()

    people_data_path = generate_dummy_data(out_dir)
    data_files.append(ResultItem(people_data_path, "CSV file with people data"))


    # Output IFC models (if any)
    ifc_models_output = list()

    # Let's presume an analyst group modifies the model and saves a new IFC file
    from external.BIManalyst_g_xy.some_module import remove_windows_from_model
    windowless_model = remove_windows_from_model(ifcopenshell.open(str(model_path)))
    windowless_model_path = out_dir / "original_filename_no_windows.ifc"
    windowless_model.write(str(windowless_model_path))
    ifc_models_output.append(ResultItem(windowless_model_path, "IFC model with windows removed "))


    # Below step depends on another analyst group's work, the windowless model just above.
    # Let's assume that this step doesn't have any other parts of the report that depend on it.
    # Hence, if this step fails, we can still create the remaining of the report.
    # Therefore we wrap it in a try-except block and log any errors.
    # In contrast, we didn't wrap the "create windowless model" step above, because if that fails,
    # we cannot proceed with this step at all. Therefore it's easier to make the entire analysis fail in that case.
    try:
        from external.BIManalyst_g_xy.another_module import some_report_generator
        should_consider_x = options.get("consider_x", True) # Example of passing an option
        some_data_input_xyz = options.get("data_input_xyz", None) # Example of passing an option

        additional_report = some_report_generator.create_report(windowless_model,
                                                                out_dir,
                                                                should_consider_x,
                                                                some_data_input_xyz # This is a file path, the module reads it internally
                                                                ) # Writes its own report file and returns path of report
        supplementary_reports.append(ResultItem(additional_report, "Description of what this report is about"))
    except Exception as e:
        # In case of error, log it but continue with the rest of the analysis
        errors.append(AnalysisError(
            responsible_group="Analyst Group_XY", # Name of the group responsible for the part that failed
            failed_action="Generating additional report", # Description of the action that failed
            error_message=str(e)
        ))


    # Generate the main report content and write to file in out_dir
    markdown_content = generate_main_report(window_result, door_result)
    main_report_path = out_dir / "Main_report_G_XY.md"
    main_report_path.write_text(markdown_content, encoding="utf-8")
    main_report = ResultItem(main_report_path, "Main report for manager group xy some subject")


    # Return the analysis results
    return AnalysisResults(
        main_report=main_report,
        errors=errors,
        supplementary_reports=supplementary_reports,
        data_files=data_files,
        ifc_models_output=ifc_models_output
    )


# Some dummy code to create a quick markdown report. Do it howhever you like.
def generate_main_report(window_result: Any, door_result: Any) -> str:
    content = "# Analysis Report G_XY\n\n"
    content += "## Window Rule Result\n"
    content += f"{window_result}\n\n"
    content += "## Door Rule Result\n"
    content += f"{door_result}\n"
    return content

# Generate dummy data file
def generate_dummy_data(out_dir: Path) -> Path:
    import pandas as pd
    
    data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["Copenhagen", "Aarhus", "Odense"]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Define output file path
    file_path = out_dir / "data/people.csv"

    # Ensure the directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write DataFrame to CSV (overwrite if exists)
    df.to_csv(file_path, index=False)

    return file_path
