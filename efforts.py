import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

# Define effort keys and their default values
effort_keys = [
    "BusinessProcesses",
    "SourceSystemAnalysis",
    "BusinessRules",
    "ConceptualDataModel",
    "LogicalDataModel",
    "Sources",
    "Read",
    "DQ",
    "Queries",
    "Write",
    "Integrations",
    "Roles",
    "Load",
    "Pipelines",
    "Views",
    "Repos",
    "Environment Setup",
]
process_mappings = {
    "Data Discovery": {
        "Business Discovery": "BusinessProcesses",
        "Source System Analysis": "SourceSystemAnalysis",
        "DQ Assessment": "BusinessRules"
    },
    "Data Model": {
        "Conceptual Model": "ConceptualDataModel",
        "Logical Model": "LogicalDataModel",
    },
    "Bronze Layer": {
        "Extract": "Sources",
        "Assemble": "Load",
        "Pipelines": "Pipelines",
    },
    "Silver Layer": {
        "Read": "Read",
        "DQ": "DQ",
        "Transform": "Queries",
        "Write": "Write",
        "Pipelines": "Pipelines",
    },
    "Match & Merge Layer": {"Match & Merge": "Integrations", "Pipelines": "Pipelines"},
    "Gold Layer": {
        "Read": "Read",
        "Transform": "Queries",
        "Write": "Write",
        "Pipelines": "Pipelines",
        "Security": "Roles",
        "Copy": "Load",
        "Views": "Views",
    },
}

sdlc_phases = ["Discovery", "Design", "Develop", "Test", "Deploy"]
default_percentages = {
    "Discovery": 10,
    "Design": 20,
    "Develop": 40,
    "Test": 20,
    "Deploy": 10,
}

# Mode selection: import JSON or start new
mode = st.sidebar.radio("Configuration Mode", ["Import JSON", "Start New"])

# Initialize default values in session state if they don't exist
if mode == "Start New" or "effort_values" not in st.session_state:
    st.session_state.effort_values = {
        key: {"S": 1, "M": 2, "L": 3} for key in effort_keys
    }
    st.session_state.estimate_values = {
        process: {}
        for process in [
            "Data Model",
            "Bronze Layer",
            "Silver Layer",
            "Match & Merge Layer",
            "Gold Layer",
        ]
    }
    if "selected_technology" not in st.session_state:
        st.session_state["selected_technology"] = "Snowflake"  # Default technology
    if "selected_project_type" not in st.session_state:
        st.session_state["selected_project_type"] = "New"  # Default project type
# Sidebar for project type and technology selection
st.sidebar.header("Project Configuration")
technologies = ["Snowflake", "Databricks", "MDP", "Powered By Excel(EV2)"]
project_types = ["New", "Upgrade"]
# Sidebar for project type and technology selection, reflecting session state values
selected_technology = st.sidebar.selectbox(
    "Select Technology",
    technologies,
    index=technologies.index(st.session_state["selected_technology"])
)
selected_project_type = st.sidebar.selectbox(
    "Project Type",
    project_types,
    index=project_types.index(st.session_state["selected_project_type"])
)

if "selected_technology" not in st.session_state:
    st.session_state["selected_technology"] = "Snowflake"  # or any default technology
else:
    st.session_state["selected_technology"]=selected_technology
if "selected_project_type" not in st.session_state:
    st.session_state["selected_project_type"] = "New"  # or any default project type
else:
    st.session_state["selected_project_type"]=selected_project_type
# Mapping of processes and inputs to effort keys
if "effort_breakdown" not in st.session_state:
    st.session_state.effort_breakdown = default_percentages

# Default configurations for each tech and project type
default_effort_values = {
    "New": {
        "Snowflake": 
        {
            "BusinessProcesses": {"S": 3, "M": 5, "L": 9},
            "SourceSystemAnalysis": {"S": 3, "M": 5, "L": 9},
            "BusinessRules": {"S": 3, "M": 5, "L": 9},
            "ConceptualDataModel": {"S": 3, "M": 5, "L": 9},
            "LogicalDataModel": {"S": 3, "M": 5, "L": 9},
            "Sources": {"S": 3, "M": 5, "L": 9},
            "Read": {"S": 3, "M": 5, "L": 9},
            "DQ": {"S": 3, "M": 5, "L": 9},
            "Queries": {"S": 3, "M": 5, "L": 9},
            "Write": {"S": 3, "M": 5, "L": 9},
            "Integrations": {"S": 3, "M": 5, "L": 9},
            "Roles": {"S": 3, "M": 5, "L": 9},
            "Load": {"S": 3, "M": 5, "L": 9},
            "Pipelines": {"S": 3, "M": 5, "L": 9},
            "Views": {"S": 3, "M": 5, "L": 9},
            "Repos": {"S": 3, "M": 5, "L": 9},
            "Environment Setup": {"S": 3, "M": 5, "L": 9}
        },
        "MDP": 
        {
            "BusinessProcesses": {"S": 13, "M": 5, "L": 9},
            "SourceSystemAnalysis": {"S": 13, "M": 5, "L": 9},
            "BusinessRules": {"S": 3, "M": 15, "L": 9},
            "ConceptualDataModel": {"S": 13, "M": 5, "L": 9},
            "LogicalDataModel": {"S": 13, "M": 5, "L": 9},
            "Sources": {"S": 13, "M": 15, "L": 9},
            "Read": {"S": 13, "M": 15, "L": 9},
            "DQ": {"S": 13, "M": 5, "L": 9},
            "Queries": {"S": 13, "M": 5, "L": 9},
            "Write": {"S": 13, "M": 5, "L": 9},
            "Integrations": {"S": 13, "M": 5, "L": 9},
            "Roles": {"S": 13, "M": 5, "L": 9},
            "Load": {"S": 13, "M": 5, "L": 9},
            "Pipelines": {"S": 13, "M": 5, "L": 9},
            "Views": {"S": 13, "M": 5, "L": 9},
            "Repos": {"S": 13, "M": 5, "L": 9},
            "Environment Setup": {"S": 13, "M": 5, "L": 9}
        },
        "Databricks": 
        {
            "BusinessProcesses": {"S": 23, "M": 5, "L": 9},
            "SourceSystemAnalysis": {"S": 23, "M": 5, "L": 9},
            "BusinessRules": {"S": 3, "M": 15, "L": 9},
            "ConceptualDataModel": {"S": 23, "M": 5, "L": 9},
            "LogicalDataModel": {"S": 23, "M": 5, "L": 9},
            "Sources": {"S": 23, "M": 15, "L": 9},
            "Read": {"S": 23, "M": 15, "L": 9},
            "DQ": {"S": 23, "M": 5, "L": 9},
            "Queries": {"S": 23, "M": 5, "L": 9},
            "Write": {"S": 23, "M": 5, "L": 9},
            "Integrations": {"S": 23, "M": 5, "L": 9},
            "Roles": {"S": 23, "M": 5, "L": 9},
            "Load": {"S": 23, "M": 5, "L": 9},
            "Pipelines": {"S": 23, "M": 5, "L": 9},
            "Views": {"S": 23, "M": 5, "L": 9},
            "Repos": {"S": 23, "M": 5, "L": 9},
            "Environment Setup": {"S": 23, "M": 5, "L": 9}
        },
        "Powered By Excel(EV2)": 
        {
            "BusinessProcesses": {"S": 23, "M": 5, "L": 9},
            "SourceSystemAnalysis": {"S": 23, "M": 5, "L": 9},
            "BusinessRules": {"S": 3, "M": 15, "L": 9},
            "ConceptualDataModel": {"S": 23, "M": 5, "L": 9},
            "LogicalDataModel": {"S": 23, "M": 5, "L": 9},
            "Sources": {"S": 23, "M": 15, "L": 9},
            "Read": {"S": 23, "M": 15, "L": 9},
            "DQ": {"S": 23, "M": 5, "L": 9},
            "Queries": {"S": 23, "M": 5, "L": 9},
            "Write": {"S": 23, "M": 5, "L": 9},
            "Integrations": {"S": 23, "M": 5, "L": 9},
            "Roles": {"S": 23, "M": 5, "L": 9},
            "Load": {"S": 23, "M": 5, "L": 9},
            "Pipelines": {"S": 23, "M": 5, "L": 9},
            "Views": {"S": 23, "M": 5, "L": 9},
            "Repos": {"S": 23, "M": 5, "L": 9},
            "Environment Setup": {"S": 23, "M": 5, "L": 9}
        },
    },
    "Upgrade": {
        "Snowflake": {
            "Sources": {"S": 2, "M": 4, "L": 8},
            "Queries": {"S": 2, "M": 5, "L": 8},
        },
        "MDP": {
            "Sources": {"S": 3, "M": 5, "L": 9},
            "Queries": {"S": 2, "M": 5, "L": 9},
        },
        "Databricks": {
            "Sources": {"S": 3, "M": 5, "L": 8},
            "Queries": {"S": 2, "M": 4, "L": 6},
        },
        "Powered By Excel(EV2)": {
            "Sources": {"S": 3, "M": 5, "L": 8},
            "Queries": {"S": 2, "M": 4, "L": 6},
        },
    },
}
# Load default effort values based on selection
if mode == "Start New":
    st.session_state.effort_values.update(
        default_effort_values[st.session_state["selected_project_type"]][st.session_state["selected_technology"]]
    )
def import_from_json(uploaded_file):
    try:
        data = json.load(uploaded_file)
        st.session_state["selected_technology"] = data.get("Technology", st.session_state["selected_technology"])
        st.session_state["selected_project_type"] = data.get("ProjectType", st.session_state["selected_project_type"])
        
        st.session_state.effort_values = data.get("EffortInputs", st.session_state.effort_values)
        st.session_state.estimate_values = data.get("Estimates", st.session_state.estimate_values)
        
        st.success("JSON configuration imported successfully!")
    except json.JSONDecodeError:
        st.error("The uploaded file is not a valid JSON.")
    return st.session_state.effort_values, st.session_state.estimate_values


# File uploader for JSON import if mode is "Import JSON"
if mode == "Import JSON":
    uploaded_file = st.sidebar.file_uploader("Upload Configuration JSON", type=["json"])
    if uploaded_file is not None:
        effort_values, estimate_values = import_from_json(uploaded_file)

# Export JSON function
def export_to_json():
    data = {
        "Technology": selected_technology,
        "ProjectType": selected_project_type,
        "EffortInputs": st.session_state.effort_values,
        "Estimates": st.session_state.estimate_values,
    }
    json_data = json.dumps(data, indent=4)
    st.download_button(
        "Download Configuration as JSON",
        json_data,
        file_name="configuration.json",
        mime="application/json",
    )



# Tabs for Effort Inputs and Estimates
tab1, tab2, tab3 = st.tabs(["Estimates", "Effort Inputs", "Parameters"])

with tab1:
    st.header("Estimates")
    total_estimate = {}
    for process, inputs in process_mappings.items():
        with st.expander(f"{process}"):
            process_total = 0
            for input_name, effort_key in inputs.items():
                st.subheader(input_name)
                default_total_count = (
                    st.session_state.estimate_values.get(process, {})
                    .get(input_name, {})
                    .get("Total Count", 0)
                )
                default_s_percentage = (
                    st.session_state.estimate_values.get(process, {})
                    .get(input_name, {})
                    .get("S%", 40)
                )
                default_m_percentage = (
                    st.session_state.estimate_values.get(process, {})
                    .get(input_name, {})
                    .get("M%", 30)
                )
                default_l_percentage = (
                    st.session_state.estimate_values.get(process, {})
                    .get(input_name, {})
                    .get("L%", 30)
                )

                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                total_count = col1.number_input(
                    f"Total",
                    min_value=0,
                    step=1,
                    value=default_total_count,
                    key=f"{process}_{input_name}_count",
                )
                s_percentage = col2.number_input(
                    f"S%",
                    min_value=0,
                    max_value=100,
                    value=default_s_percentage,
                    key=f"{process}_{input_name}_s",
                )
                m_percentage = col3.number_input(
                    f"M%",
                    min_value=0,
                    max_value=100,
                    value=default_m_percentage,
                    key=f"{process}_{input_name}_m",
                )
                l_percentage = col4.number_input(
                    f"L%",
                    min_value=0,
                    max_value=100,
                    value=default_l_percentage,
                    key=f"{process}_{input_name}_l",
                )

                if s_percentage + m_percentage + l_percentage == 100:
                    s_count = total_count * (s_percentage / 100)
                    m_count = total_count * (m_percentage / 100)
                    l_count = total_count * (l_percentage / 100)

                    effort = (
                        s_count * st.session_state.effort_values[effort_key]["S"]
                        + m_count * st.session_state.effort_values[effort_key]["M"]
                        + l_count * st.session_state.effort_values[effort_key]["L"]
                    )

                    st.write(f"Estimated Effort for {input_name}: {effort:.2f} hours")
                    # Add a Comments textbox
                    comments = st.text_area(f"Comments for {input_name}", key=f"{process}_{input_name}_comments")
                
                    process_total += effort

                    if process not in st.session_state.estimate_values:
                        st.session_state.estimate_values[process] = {}
                    st.session_state.estimate_values[process][input_name] = {
                        "Total Count": total_count,
                        "S%": s_percentage,
                        "M%": m_percentage,
                        "L%": l_percentage,
                        "Effort": effort,
                        "Comments": comments,
                    }
                else:
                    st.error("The percentages must add up to 100.")
            total_estimate[process] = process_total
            st.write(f"Total Estimated Effort for {process}: {process_total:.2f} hours")

    st.write("### Summary of Estimated Efforts by Process")
    summary_df = pd.DataFrame(
        list(total_estimate.items()), columns=["Process", "Most Likely Estimate"]
    )
    total_effort = summary_df["Most Likely Estimate"].sum()
    total_row = pd.DataFrame(
        [{"Process": "Total", "Most Likely Estimate": total_effort}]
    )
    summary_df = pd.concat([summary_df, total_row], ignore_index=True)
    summary_df["Optimistic Estimate"] = summary_df["Most Likely Estimate"] * 0.9
    summary_df["Pessimistic Estimate"] = summary_df["Most Likely Estimate"] * 1.15
    summary_df["PERT Estimate"] = (
        summary_df["Optimistic Estimate"]
        + 4 * summary_df["Most Likely Estimate"]
        + summary_df["Pessimistic Estimate"]
    ) / 6
    phase_summary_df = summary_df[["Process", "PERT Estimate"]]
    total_allocation = phase_summary_df["PERT Estimate"] / (
        st.session_state.effort_breakdown["Develop"] / 100
    )
    for phase in sdlc_phases:
        phase_summary_df[f"{phase}"] = total_allocation * (
            st.session_state.effort_breakdown[phase] / 100
        )
    phase_summary_df["Total Effort"] = total_allocation

    st.table(summary_df)
    st.table(phase_summary_df)


    st.write("### Waterfall Chart of Efforts by Process")
    fig = go.Figure(
        go.Waterfall(
            x=summary_df["Process"],
            y=summary_df["PERT Estimate"],
            measure=["relative"] * (len(summary_df) - 1) + ["total"],
            name="Effort Breakdown",
            text=summary_df["PERT Estimate"].apply(lambda x: f"{x:.2f}"),
        )
    )
    fig.update_layout(
        title="Effort Waterfall Chart", yaxis_title="Effort (hours)", showlegend=False
    )
    st.plotly_chart(fig)

with tab2:
    st.header("Configure Effort Multipliers (hours per unit)")
    st.subheader(
        f"Effort Multipliers for {selected_project_type} Project on {selected_technology}"
    )
    for category, sizes in st.session_state.effort_values.items():
        with st.container():
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
            col1.write(category.capitalize())
            st.session_state.effort_values[category] = {
                "S": col2.number_input(
                    f"Small ({category.capitalize()})",
                    min_value=0,
                    value=sizes["S"],
                    step=1,
                ),
                "M": col3.number_input(
                    f"Medium ({category.capitalize()})",
                    min_value=0,
                    value=sizes["M"],
                    step=1,
                ),
                "L": col4.number_input(
                    f"Large ({category.capitalize()})",
                    min_value=0,
                    value=sizes["L"],
                    step=1,
                ),
            }

with tab3:
    st.header("Phase-Wise Effort Breakdown")
    st.write(
        "Enter the percentage allocation for each phase (total should add up to 100%)."
    )
    total_allocation = 0
    for phase in sdlc_phases:
        st.session_state.effort_breakdown[phase] = st.number_input(
            f"{phase} (%)",
            min_value=0,
            max_value=100,
            value=st.session_state.effort_breakdown[phase],
        )
        total_allocation += st.session_state.effort_breakdown[phase]

    if total_allocation != 100:
        st.warning(
            f"The total allocation is {total_allocation}%. Please ensure it adds up to 100%."
        )

# Download button for exporting JSON
export_to_json()
