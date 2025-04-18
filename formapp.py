# Refactored Streamlit Form
# Full unified form without st.form(), preserving all logic and ensuring all answers are saved in order

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import time
import io
import os

DATA_FILE = "reviewer_responses.csv"
st.title("2025 AP Peer Reviewer")
st.write(f"\U0001F4C5 {datetime.today().strftime('%Y-%m-%dT%H:%M:%S')}")

st.subheader("Reviewer and Program Identifiers")

# --- Top Inputs ---
reviewer_name = st.text_input("1. Reviewer's Name *", help="Enter your full name")
college_name = st.text_input("2. Name of College (for the program) *", help="Enter the college's name")
program_name = st.text_input("3. Program Name (as written on the plan) *", help="Enter the official program name")

st.subheader("Plan Completion Rate")
program_info_complete = st.radio("4. The table for Program Information is complete (first table). *", ["Yes", "No"], index=None)

st.subheader("Yearly Assessment Timeline and Responsibilities")
yearly_assessment_complete = st.radio("5. The Yearly Assessment Timeline and Responsibilities table is complete. *", ["Yes", "No"], index=None)

missing_items = []
if yearly_assessment_complete == "No":
    st.write("6. If No, indicate what is missing. Choose all that apply.")
    missing_items = st.multiselect("Select missing elements:", [
        "Timeline: Data Collection",
        "Timeline: Data Analysis",
        "Timeline: Discuss With Faculty",
        "Person(s) Responsible: Data Collection",
        "Person(s) Responsible: Data Analysis",
        "Person(s) Responsible: Discuss With Faculty"
    ])

st.subheader("Curriculum Map Review")
st.write("7. Review the Curriculum Map in the assessment plan and indicate whether each of the following components are present.")
options = ["Yes", "No", "Cannot Confirm"]
curriculum_map_responses = {
    "All PSLOs are listed": st.radio("All PSLOs are listed.", options, horizontal=True, index=None),
    "All core/required program courses are listed": st.radio("All core/required program courses are listed.", options, horizontal=True, index=None),
    "The map contains indicators for which courses address a PSLO (X or I, R)": st.radio("The map contains indicators for which courses address a PSLO (X or I, R).", options, horizontal=True, index=None),
    "The map indicates where each PSLO is assessed (A)": st.radio("The map indicates where each PSLO is assessed (A).", options, horizontal=True, index=None),
    "The Assessment Schedule is indicated for each PSLO": st.radio("The Assessment Schedule is indicated for each PSLO.", options, horizontal=True, index=None),
    "At least one assessment instrument is listed for each PSLO": st.radio("At least one assessment instrument is listed for each PSLO.", options, horizontal=True, index=None),
}

st.subheader("PSLO Quality Review")
st.markdown("### PSLO1")
pslo1_quality = {
    "PSLO1 Quality 1": st.radio("The PSLO is appropriate for the degree program level (undergraduate or graduate).", options, key="pslo1_q1", index=None),
    "PSLO1 Quality 2": st.radio("The PSLO clearly describes expected student performance or competencies.", options, key="pslo1_q2", index=None),
    "PSLO1 Quality 3": st.radio("The PSLO uses precise learning verbs (e.g., Bloom's/Marzano’s).", options, key="pslo1_q3", index=None),
    "PSLO1 Quality 4": st.radio("The PSLO includes verbs at different cognitive levels.", options, key="pslo1_q4", index=None),
    "PSLO1 Quality 5": st.radio("The PSLO clearly specifies knowledge, skills, and/or abilities.", options, key="pslo1_q5", index=None),
}

st.write("")
st.markdown("### PSLO2")
pslo2_quality = {
    "PSLO2 Quality 1": st.radio("The PSLO is appropriate for the degree program level (undergraduate or graduate).", options, key="pslo2_q1", index=None),
    "PSLO2 Quality 2": st.radio("The PSLO clearly describes expected student performance or competencies.", options, key="pslo2_q2", index=None),
    "PSLO2 Quality 3": st.radio("The PSLO uses precise learning verbs (e.g., Bloom's/Marzano’s).", options, key="pslo2_q3", index=None),
    "PSLO2 Quality 4": st.radio("The PSLO includes verbs at different cognitive levels.", options, key="pslo2_q4", index=None),
    "PSLO2 Quality 5": st.radio("The PSLO clearly specifies knowledge, skills, and/or abilities.", options, key="pslo2_q5", index=None),
}

# -- Store PSLO1 and PSLO2 quality responses for merging with main data --
additional_responses = {}
additional_responses.update(pslo1_quality)
additional_responses.update(pslo2_quality)


# Ask whether to continue to PSLO3 (starting point for branching)
more_after_pslo2 = st.radio(
    "Are there more PSLOs to evaluate after PSLO2?",
    ["Yes", "No"],
    key="more_pslo_2",
    horizontal=True,
    index=None
)
# Initialize if not already done
if "num_pslos" not in st.session_state:
    st.session_state.num_pslos = 2

max_pslos = 28

if more_after_pslo2 == "Yes" and st.session_state.num_pslos == 2:
    st.session_state.num_pslos = 3
    st.rerun()

# Loop and collect directly into additional_responses
if st.session_state.num_pslos >= 3:
    for i in range(3, st.session_state.num_pslos + 1):
        st.write("")
        st.markdown(f"### PSLO{i}")
        for q in range(1, 6):
            question_label = [
                "The PSLO is appropriate for the degree program level (undergraduate or graduate).",
                "The PSLO uses precise learning verbs (e.g., verbs from frameworks like Bloom’s or Marzano’s taxonomies).",
                "The PSLO contains/lists multiple learning verbs at different levels of cognition.",
                "The knowledge, skills and/or abilities are clearly specified in the PSLO.",
                "The PSLO contains/lists multiple knowledge, skills and/or abilities students will attain."
            ][q - 1]

            # Store each response in additional_responses
            additional_responses[f"PSLO{i} Quality {q}"] = st.radio(
                question_label,
                options,
                key=f"pslo{i}_q{q}",
                index=None
            )

        more = st.radio(
            f"Are there more PSLOs to evaluate after PSLO{i}?",
            ["Yes", "No"],
            key=f"more_pslo_{i}",
            horizontal=True,
            index=None
        )

        if more == "Yes" and i == st.session_state.num_pslos and i < max_pslos:
            st.session_state.num_pslos += 1
            st.rerun()


# Add Four line breaks
st.write("")
st.write("")
st.write("")
st.write("")



# ------------------------------------METHODS AND MEASURES-------------------------------------------------
st.subheader("METHODS AND MEASURES")
st.write("")
st.subheader("Methods and Measures for PSLO1")
st.write("PSLO 1: Assess the method and measures.")
methods_measures_pslo1 = {
    "PSLO1 - Direct Measure Exists": st.radio("There is at least one direct measure.", options, horizontal=True, key="m1_q1", index=None),
    "PSLO1 - Instrument/Tool Stated": st.radio("For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, horizontal=True, key="m1_q2", index=None),
    "PSLO1 - Precision of Measure": st.radio("The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed.", options, horizontal=True, key="m1_q3", index=None),
    "PSLO1 - Alignment Explanation": st.radio("Explanation of how the assessment aligns with the PSLO is clear.", options, horizontal=True, key="m1_q4", index=None),
}

additional_measures_pslo1 = st.radio("Are there additional measures listed for PSLO1?", ["Yes", "No"], horizontal=True, key="additional_measures_pslo1", index=None)

if additional_measures_pslo1 == "Yes":
    measure_assessment_pslo1 = st.radio("Collectively assess the extent to which all the additional measures provide the following criteria.",
        [
            "Each additional measure addresses all of the criteria.",
            "Most of the additional measures address all of the criteria.",
            "Some of the additional measures address all of the criteria.",
            "None of the additional measures address all of the criteria."
        ], horizontal=True, key="measure_assessment_pslo1", index=None)
    
else:
    measure_assessment_pslo1 = ""
    
# Feedback should always be shown regardless of yes/no
feedback_pslo1 = st.text_area("Provide your feedback(e.g., what was done well, what could be improved, etc.) on PSLO1.", key="feedback_pslo1")


# -- Store additional sections for merging with main data --
# Save Methods & Measures for PSLO1 into additional_responses
additional_responses.update(methods_measures_pslo1)
additional_responses["PSLO1 - Additional Measures"] = additional_measures_pslo1
additional_responses["PSLO1 - Measure Assessment"] = measure_assessment_pslo1
additional_responses["PSLO1 - Feedback"] = feedback_pslo1

# Methods and Measures for PSLO2
st.subheader("Methods and Measures for PSLO2")
st.write("PSLO 2: Assess the method and measures.")
methods_measures_pslo2 = {
    "PSLO2 - Direct Measure Exists": st.radio("There is at least one direct measure.", options, horizontal=True, key="m2_q1", index=None),
    "PSLO2 - Instrument/Tool Stated": st.radio("For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, horizontal=True, key="m2_q2", index=None),
    "PSLO2 - Precision of Measure": st.radio("The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed.", options, horizontal=True, key="m2_q3", index=None),
    "PSLO2 - Alignment Explanation": st.radio("Explanation of how the assessment aligns with the PSLO is clear.", options, horizontal=True, key="m2_q4", index=None),
    "PSLO2 - Course Matches Curriculum Map": st.radio("Does the course stated in the explanation match the one in the curriculum map indicated by an 'A' for the PSLO?", options, horizontal=True, key="m2_q5", index=None),
    "PSLO2 - Semester Stated": st.radio("Does the explanation state the semester(s) in which the assessment is administered during the assessment cycle?", options, horizontal=True, key="m2_q6", index=None),
    "PSLO2 - Sample Identified": st.radio("Is the sample (who will be assessed) clearly identified?", options, horizontal=True, key="m2_q7", index=None),
    "PSLO2 - Reporting Description": st.radio("Is the description of how the results will be reported appropriate for the collected data and the measure?", options, horizontal=True, key="m2_q8", index=None)
}

additional_measures_pslo2 = st.radio("Are there additional measures listed for PSLO2?", ["Yes", "No"], horizontal=True, key="additional_measures_pslo2", index=None)

if additional_measures_pslo2 == "Yes":
    measure_assessment_pslo2 = st.radio("Collectively assess the extent to which all the additional measures provide the following:",
        [
            "Each additional measure addresses all of the criteria.",
            "Most of the additional measures address all of the criteria.",
            "Some of the additional measures address all of the criteria.",
            "None of the additional measures address all of the criteria."
        ], horizontal=True, key="measure_assessment_pslo2", index=None)
else:
    measure_assessment_pslo2 = ""
    
# Always show feedback
st.write("")
st.write("Provide your feedback (e.g., what was done well, what could be improved, etc.) on PSLO2.")
feedback_pslo2 = st.text_area("Provide your feedback on PSLO2.", key="feedback_pslo2")

# Save Methods & Measures for PSLO2 into additional_responses
additional_responses.update(methods_measures_pslo2)
additional_responses["PSLO2 - Additional Measures"] = additional_measures_pslo2
additional_responses["PSLO2 - Measure Assessment"] = measure_assessment_pslo2
additional_responses["PSLO2 - Feedback"] = feedback_pslo2



# Methods and Measures for PSLO3
# ----- Dynamic Methods and Measures for PSLO3 to PSLO28 -----
# Continue branching
st.write("")
st.write("Is there another PSLO to assess in the assessment plan?")
another_pslo_pslo2 = st.radio("", ["Yes", "No"], key="another_pslo_pslo2", horizontal=True, index=None)

if another_pslo_pslo2 == "Yes":
    if "num_pslos_mm" not in st.session_state:
        st.session_state.num_pslos_mm = 3

    max_pslos_mm = 28  # up to PSLO28
    options = ["Yes", "No", "Cannot be determined"]

    for i in range(3, st.session_state.num_pslos_mm + 1):
        st.subheader(f"Methods and Measures for PSLO{i}")
        st.write(f"{21 + (i - 2) * 5}. PSLO {i}: Assess the method and measures.")

        mm_responses = {
            f"There is at least one direct measure (PSLO{i})": st.radio(
                "There is at least one direct measure.", options, key=f"mm_pslo{i}_q1", horizontal=True, index=None
            ),
            f"The assessment instrument/tools are stated (PSLO{i})": st.radio(
                "For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, key=f"mm_pslo{i}_q2", horizontal=True, index=None
            ),
            f"The first direct measure is precise (PSLO{i})": st.radio(
                "The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed (i.e., is it granular).", options, key=f"mm_pslo{i}_q3", horizontal=True, index=None
            ),
            f"The explanation aligns assessment with PSLO (PSLO{i})": st.radio(
                "For the first direct measure, the explanation of how the assessment aligns with the PSLO is clear.", options, key=f"mm_pslo{i}_q4", horizontal=True, index=None
            ),
            f"The course stated in explanation matches curriculum map (PSLO{i})": st.radio(
                "Does the course stated in the explanation match the one in the curriculum map indicated by an 'A' for the PSLO?", options, key=f"mm_pslo{i}_q5", horizontal=True, index=None
            ),
            f"The semester of assessment is stated (PSLO{i})": st.radio(
                "Does the explanation state the semester(s) in which the assessment is administered during the assessment cycle?", options, key=f"mm_pslo{i}_q6", horizontal=True, index=None
            ),
            f"The sample (who will be assessed) is identified (PSLO{i})": st.radio(
                "Is the sample (who will be assessed) clearly identified?", options, key=f"mm_pslo{i}_q7", horizontal=True, index=None
            ),
            f"Description of reporting results is appropriate (PSLO{i})": st.radio(
                "Is the description of how the results will be reported appropriate for the collected data and the measure?", options, key=f"mm_pslo{i}_q8", horizontal=True, index=None
            ),
        }

        st.write(f"{22 + (i - 2) * 5}. Are there additional measures listed for PSLO{i}?")
        additional_measures = st.radio("", ["Yes", "No"], key=f"additional_measures_pslo{i}", horizontal=True, index=None)

        if additional_measures == "Yes":
            st.write("")
            st.write(f"{23 + (i - 2) * 5}. Collectively assess the extent to which all the additional measures provide the following:")
            st.write("a) Is listed in the curriculum map")
            st.write("b) Whether it is direct or indirect")
            st.write("c) Instrument/tool and items (if applicable) identified")
            st.write("d) Provides a clear explanation of how the assessment aligns with the PSLO")
            st.write("e) Describes how the results will be reported")

            st.radio(
                "", [
                    "Each additional measure addresses all of the criteria.",
                    "Most of the additional measures address all of the criteria.",
                    "Some of the additional measures address all of the criteria.",
                    "None of the additional measures address all of the criteria."
                ],
                key=f"measure_assessment_pslo{i}",
                horizontal=True,
                index=None
            )

        # Always show feedback box
        st.write("")
        st.write(f"{23 + (i - 2) * 5}. Provide your feedback (e.g., what was done well, what could be improved, etc.) on PSLO{i}.")
        st.text_area("", key=f"feedback_pslo{i}")

        st.write("")
        more = st.radio(f"{24 + (i - 2) * 5}. Is there another PSLO to assess in the assessment plan?", ["Yes", "No"], key=f"another_pslo_mm_{i}", horizontal=True, index=None)

        # Save current PSLO{i} M&M responses
        additional_responses.update(mm_responses)
        # Save additional branching fields
        additional_responses[f"PSLO{i} - Additional Measures"] = additional_measures
        additional_responses[f"PSLO{i} - Measure Assessment"] = st.session_state.get(f"measure_assessment_pslo{i}", "")
        additional_responses[f"PSLO{i} - Feedback"] = st.session_state.get(f"feedback_pslo{i}", "")
        additional_responses[f"PSLO{i} - Another PSLO After"] = st.session_state.get(f"another_pslo_mm_{i}", "")


        if more == "Yes" and i == st.session_state.num_pslos_mm and i < max_pslos_mm:
            st.session_state.num_pslos_mm += 1
            st.rerun()
        


# Add THREE line break
st.write("")
st.write("")
st.write("")



# -------------------------------- STUDENT SUCCESS SECTION ------------------------------------------

st.subheader("Student Success Assessment: Methods and Measures")
st.write("")
st.write("")
student_success_outcome = st.radio("The assessment plan identifies at least one student success outcome (e.g. retention, progression, graduation).", ["Yes", "No"], horizontal=True, key="student_success_outcome", index=None)
student_success_measure = st.radio("For at least one student success outcome, a measure is provided.", ["Yes", "No"], horizontal=True, key="student_success_measure", index=None)



# --------------------------------- APPENDIX SECTION ------------------------------------------

st.subheader("Appendix")
st.write("")
st.write("")
appendix_table_of_contents = st.radio("The appendix contains a Table of Contents.", ["Yes", "No"], key="appendix_table_of_contents", horizontal=True, index=None)
appendix_pslo_description = st.radio("For each PSLO, is a copy or detailed description of the instrument/tool included?", ["Yes", "No"], key="appendix_pslo_description", horizontal=True, index=None)
st.write("")

appendix_missing_details = ""
if appendix_pslo_description == "No":
    appendix_missing_details = st.text_area("For missing copies or descriptions, list the PSLO number and name of the missing instrument/tool or write 'mismatch'.", key="appendix_missing_details")



# -------------------------------------- ESTIMATED DURATION ----------------------------------
st.subheader("Estimated Duration")
estimated_duration = st.text_input("Approximately how many minutes did you spend reviewing the assessment plan?", key="estimated_duration")

# -- Add final fields to response dict --
additional_responses["Student Success - Outcome Identified"] = student_success_outcome
additional_responses["Student Success - Measure Provided"] = student_success_measure
additional_responses["Appendix - Table of Contents"] = appendix_table_of_contents
additional_responses["Appendix - PSLO Descriptions Included"] = appendix_pslo_description
additional_responses["Appendix - Missing Details"] = appendix_missing_details
additional_responses["Estimated Duration (Minutes)"] = estimated_duration


# -------------------------------------- SUBMIT BUTTON ----------------------------------
# -- Final Unified Submit Button --
if st.button("Submit Full Form"):
    if not reviewer_name or not college_name or not program_name:
        st.error("Please fill in all required fields.")
    else:
        form_data = {
            "Reviewer Name": reviewer_name,
            "College Name": college_name,
            "Program Name": program_name,
            "Program Info Complete": program_info_complete,
            "Yearly Assessment Complete": yearly_assessment_complete,
            "Missing Items": ", ".join(missing_items) if missing_items else "None",
            "Timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }

        # Merge curriculum responses and everything collected dynamically
        form_data.update(curriculum_map_responses)
        form_data.update(additional_responses)

        # Save for manual Excel copy
        latest_df = pd.DataFrame([form_data])
        buffer = io.BytesIO()
        latest_df.to_excel(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
            label="⬇️ Download This Submission as Excel",
            data=buffer,
            file_name="latest_submission.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        
        # Send data to Power Automate
        try:
            power_automate_url = "https://prod-69.westus.logic.azure.com:443/workflows/b18fd281e82b456dbc7b4dea66ee5878/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=j7KYXt6mfF97vPq1r0wnOQFkACB-jleAxA8fTyxut8M"
            response = requests.post(power_automate_url, json=form_data)
        
            if response.status_code in [200, 202]:
                st.success("YOU ARE AN AWESOME REVIEWER!!!!🎉 ")
                st.write("Hold on while we finalize a few things...")
                st.write("")
                st.write("")     
                st.success("Thank you! Your form was successfully submitted✅ .")
                st.write("")
                st.write("")
                st.write("You can refresh the page to start a new form🔄")

            else:
                st.error(f"⚠️ Submission failed. Couldn't submit to Excel sheet. Status code: {response.status_code}")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

