
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Define where to save data
DATA_FILE = "reviewer_responses.csv"

st.title("2025 AP Peer Reviewer")
st.write(f"📅 {datetime.today().strftime('%B %d, %Y')}")

st.subheader("Reviewer and Program Identifiers")

# Form layout
with st.form("reviewer_form"):
    reviewer_name = st.text_input("1. Reviewer's Name *", help="Enter your full name")
    college_name = st.text_input("2. Name of College (for the program) *", help="Enter the college's name")
    program_name = st.text_input("3. Program Name (as written on the plan) *", help="Enter the official program name")

    st.subheader("Plan Completion Rate")
    program_info_complete = st.radio(
        "4. The table for Program Information is complete (first table). *",
        ["Yes", "No"]
    )

    st.subheader("Yearly Assessment Timeline and Responsibilities")
    yearly_assessment_complete = st.radio(
        "5. The Yearly Assessment Timeline and Responsibilities table is complete. *",
        ["Yes", "No"]
    )

    # Conditional checkboxes if "No" is selected
    missing_items = []
    if yearly_assessment_complete == "No":
        st.write("6. If No, indicate what is missing. Choose all that apply.")
        missing_items = st.multiselect(
            "Select missing elements:",
            [
                "Timeline: Data Collection",
                "Timeline: Data Analysis",
                "Timeline: Discuss With Faculty",
                "Person(s) Responsible: Data Collection",
                "Person(s) Responsible: Data Analysis",
                "Person(s) Responsible: Discuss With Faculty"
            ]
        )

    # Curriculum Map Evaluation Section
    st.subheader("Curriculum Map Review")
    st.write("7. Review the Curriculum Map in the assessment plan and indicate whether each of the following components are present.")

    options = ["Yes", "No", "Cannot Confirm"]
    curriculum_map_responses = {
        "All PSLOs are listed": st.radio("All PSLOs are listed.", options, horizontal=True),
        "All core/required program courses are listed": st.radio("All core/required program courses are listed.", options, horizontal=True),
        "The map contains indicators for which courses address a PSLO (X or I, R)": st.radio("The map contains indicators for which courses address a PSLO (X or I, R).", options, horizontal=True),
        "The map indicates where each PSLO is assessed (A)": st.radio("The map indicates where each PSLO is assessed (A).", options, horizontal=True),
        "The Assessment Schedule is indicated for each PSLO": st.radio("The Assessment Schedule is indicated for each PSLO.", options, horizontal=True),
        "At least one assessment instrument is listed for each PSLO": st.radio("At least one assessment instrument is listed for each PSLO.", options, horizontal=True),
    }

    # Add TWO line break
    st.write("")
    st.write("")

    # Individual PSLO Quality Reviews (Unchanged)
    st.subheader("PSLO Quality 1")
    st.write("8. The PSLO is appropriate for the degree program level (undergraduate or graduate).")
    pslo_quality_1_responses = {f"PSLO{i} (Quality 1)": st.radio(f"PSLO{i}", options, horizontal=True) for i in range(1, 31)}
    
    # Add TWO line break
    st.write("")
    st.write("")

    st.subheader("PSLO Quality 2")
    st.write("9. The PSLO clearly describes expected student performance or competencies.")
    pslo_quality_2_responses = {f"PSLO{i} (Quality 2)": st.radio(f"PSLO{i} (Quality 2)", options, key=f"pslo_q2_{i}", horizontal=True) for i in range(1, 31)}

    # Add TWO line break
    st.write("")
    st.write("")

    st.subheader("PSLO Quality 3")
    st.write("10. The PSLO uses precise learning verbs (e.g., verbs from frameworks like Bloom’s or Marzano’s taxonomies).")
    pslo_quality_3_responses = {f"PSLO{i} (Quality 3)": st.radio(f"PSLO{i} (Quality 3)", options, key=f"pslo_q3_{i}", horizontal=True) for i in range(1, 31)}

    # Add TWO line break
    st.write("")
    st.write("")

    st.subheader("PSLO Quality 4")
    st.write("11. The PSLO contains/lists multiple learning verbs at different levels of cognition.")
    pslo_quality_4_responses = {f"PSLO{i} (Quality 4)": st.radio(f"PSLO{i} (Quality 4)", options, key=f"pslo_q4_{i}", horizontal=True) for i in range(1, 31)}

    # Add TWO line break
    st.write("")
    st.write("")

    st.subheader("PSLO Quality 5")
    st.write("12. The knowledge, skills and/or abilities are clearly specified in the PSLO.")
    pslo_quality_5_responses = {f"PSLO{i} (Quality 5)": st.radio(f"PSLO{i}", options, key=f"pslo_q5_{i}", horizontal=True) for i in range(1, 31)}

    # Add TWO line break
    st.write("")
    st.write("")

    st.subheader("PSLO Quality 6")
    st.write("13. The PSLO contains/lists multiple knowledge, skills and/or abilities students will attain.")
    pslo_quality_6_responses = {f"PSLO{i} (Quality 6)": st.radio(f"PSLO{i}", options, key=f"pslo_q6_{i}", horizontal=True) for i in range(1, 31)}

    # Add TWO line break
    st.write("")
    st.write("")

    # Methods and Measures for PSLO1 (Section 14)
    st.subheader("Methods and Measures for PSLO1")
    st.write("14. PSLO 1: Assess the method and measures.")

    methods_measures_pslo1 = {
        "There is at least one direct measure": st.radio("There is at least one direct measure.", options, horizontal=True),
        "The assessment instrument/tools are stated": st.radio("For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, horizontal=True),
        "The first direct measure is precise": st.radio("The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed (i.e., is it granular).", options, horizontal=True),
        "The explanation aligns assessment with PSLO": st.radio("For the first direct measure, the explanation of how the assessment aligns with the PSLO is clear.", options, horizontal=True),
    }

    # Add TWO line break
    st.write("")
    st.write("")

    # Additional Measures for PSLO1 (NEW)
    st.write("15. Are there additional measures listed for PSLO1?")
    additional_measures = st.radio("", ["Yes", "No"], horizontal=True)

    # Add TWO line break
    st.write("")
    st.write("")

    st.write("16. Collectively assess the extent to which all the additional measures provide the following criteria.")
    measure_assessment = st.radio(
        "", [
            "Each additional measure addresses all of the criteria.",
            "Most of the additional measures address all of the criteria.",
            "Some of the additional measures address all of the criteria.",
            "None of the additional measures address all of the criteria."
        ], horizontal=True
    )

    # Add line break
    st.write("")

    st.write("17. Provide your feedback (e.g., what was done well, what could be improved, etc.) on PSLO1.")
    feedback = st.text_area("\n", key= "feedback")

    # Add TWO line break
    st.write("")
    st.write("")

    st.write("18. Is there another PSLO to assess in the assessment plan?")
    another_pslo = st.radio('\n', ["Yes", "No"], horizontal=True)

    # Add THREE line break
    st.write("")
    st.write("")
    st.write("")

        # Methods and Measures for PSLO2
    st.subheader("Methods and Measures for PSLO2")
    st.write("19. PSLO 2: Assess the method and measures.")

    options = ["Yes", "No", "Cannot be determined"]

    methods_measures_pslo2 = {
        "There is at least one direct measure (PSLO2)": st.radio(
            "There is at least one direct measure.", options, horizontal=True
        ),
        "The assessment instrument/tools are stated (PSLO2)": st.radio(
            "For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, horizontal=True
        ),
        "The first direct measure is precise (PSLO2)": st.radio(
            "The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed (i.e., is it granular).", options, horizontal=True
        ),
        "The explanation aligns assessment with PSLO (PSLO2)": st.radio(
            "For the first direct measure, the explanation of how the assessment aligns with the PSLO is clear.", options, horizontal=True
        ),
        "The course stated in explanation matches curriculum map (PSLO2)": st.radio(
            "Does the course stated in the explanation match the one in the curriculum map indicated by an 'A' for the PSLO?", options, horizontal=True
        ),
        "The semester of assessment is stated (PSLO2)": st.radio(
            "Does the explanation state the semester(s) in which the assessment is administered during the assessment cycle?", options, horizontal=True
        ),
        "The sample (who will be assessed) is identified (PSLO2)": st.radio(
            "Is the sample (who will be assessed) clearly identified?", options, horizontal=True
        ),
        "Description of reporting results is appropriate (PSLO2)": st.radio(
            "Is the description of how the results will be reported appropriate for the collected data and the measure?", options, horizontal=True
        ),
    }

    # Add TWO line break
    st.write("")
    st.write("")

        # Additional Measures for PSLO2
    st.write("20. Are there additional measures listed for PSLO2?")
    additional_measures_pslo2 = st.radio("\n",["Yes", "No"],key="additional_measures_pslo2",horizontal=True)

    # Add TWO line break
    st.write("")
    st.write("")


    st.write("21. Collectively assess the extent to which all the additional measures provide the following: \n"
             "\n a) Is listed in the curriculum map,\n"
             "\n b) Whether it is direct or indirect,\n"
             "\n c) Instrument/tool and items (if applicable) identified,\n"
             "\n d) Provides a clear explanation of how the assessment aligns with the PSLO,\n"
             "\n e) Describes how the results will be reported.")

    measure_assessment_pslo2 = st.radio(
        "", [
            "Each additional measure addresses all of the criteria.",
            "Most of the additional measures address all of the criteria.",
            "Some of the additional measures address all of the criteria.",
            "None of the additional measures address all of the criteria."
        ], key="measure_assessment_pslo2", horizontal=True
    )

    # Add TWO line break
    st.write("")
    st.write("")


    st.write("22. Provide your feedback (e.g., what was done well, what could be improved, etc.) on PSLO2.")
    feedback_pslo2 = st.text_area("\n", key="feedback_pslo2")

    # Add TWO line break
    st.write("")
    st.write("")

    st.write("23. Is there another PSLO to assess in the assessment plan?")
    another_pslo_pslo2 = st.radio("\n", ["Yes", "No"], key = 'another_pslo_pslo2', horizontal=True)

    # Add THREE line break
    st.write("")
    st.write("")
    st.write("")

        # Methods and Measures for PSLO3
    st.subheader("Methods and Measures for PSLO3")
    st.write("24. PSLO 3: Assess the method and measures.")

    options = ["Yes", "No", "Cannot be determined"]

    methods_measures_pslo3 = {
        "There is at least one direct measure (PSLO3)": st.radio(
            "There is at least one direct measure.", options, key="pslo3_direct_measure", horizontal=True
        ),
        "The assessment instrument/tools are stated (PSLO3)": st.radio(
            "For the first direct measure, the assessment instrument/tools is stated and if applicable, relevant items are listed.", options, key="pslo3_tools_stated", horizontal=True
        ),
        "The first direct measure is precise (PSLO3)": st.radio(
            "The first direct measure precisely and reliably targets the knowledge, skills and/or ability being assessed (i.e., is it granular).", options, key="pslo3_precise_measure", horizontal=True
        ),
        "The explanation aligns assessment with PSLO (PSLO3)": st.radio(
            "For the first direct measure, the explanation of how the assessment aligns with the PSLO is clear.", options, key="pslo3_alignment", horizontal=True
        ),
        "The course stated in explanation matches curriculum map (PSLO3)": st.radio(
            "Does the course stated in the explanation match the one in the curriculum map indicated by an 'A' for the PSLO?", options, key="pslo3_course_match", horizontal=True
        ),
        "The semester of assessment is stated (PSLO3)": st.radio(
            "Does the explanation state the semester(s) in which the assessment is administered during the assessment cycle?", options, key="pslo3_semester_stated", horizontal=True
        ),
        "The sample (who will be assessed) is identified (PSLO3)": st.radio(
            "Is the sample (who will be assessed) clearly identified?", options, key="pslo3_sample_identified", horizontal=True
        ),
        "Description of reporting results is appropriate (PSLO3)": st.radio(
            "Is the description of how the results will be reported appropriate for the collected data and the measure?", options, key="pslo3_reporting_description", horizontal=True
        ),
    }

    # Add TWO line break
    st.write("")
    st.write("")

    # Additional Measures for PSLO3
    st.write("25. Are there additional measures listed for PSLO3?")
    additional_measures_pslo3 = st.radio("", ["Yes", "No"], key="additional_measures_pslo3", horizontal=True)

    # Add TWO line break
    st.write("")
    st.write("") 

    st.write("26. Collectively assess the extent to which all the additional measures provide the following: \n"
             "\n a) Is listed in the curriculum map, \n"
             "\n b) Whether it is direct or indirect, \n"
             "\n c) Instrument/tool and items (if applicable) identified, \n"
             "\n d) Provides a clear explanation of how the assessment aligns with the PSLO, \n"
             "\n e) Describes how the results will be reported.")

    measure_assessment_pslo3 = st.radio(
        "", [
            "Each additional measure addresses all of the criteria.",
            "Most of the additional measures address all of the criteria.",
            "Some of the additional measures address all of the criteria.",
            "None of the additional measures address all of the criteria."
        ], key="measure_assessment_pslo3", horizontal=True
    )

    # Add TWO line break
    st.write("")
    st.write("")

    st.write("27. Provide your feedback (e.g., what was done well, what could be improved, etc.) on PSLO3.")
    feedback_pslo3 = st.text_area("\n", key="feedback_pslo3")
    
    # Add TWO line break
    st.write("")
    st.write("")

    st.write("28. Is there another PSLO to assess in the assessment plan?")
    another_pslo_pslo3 = st.radio("\n", ["Yes", "No"], key="another_pslo_pslo3", horizontal=True)

    # Add THREE line break
    st.write("")
    st.write("")
    st.write("")


    # Student Success Assessment: Methods and Measures
    st.subheader("Student Success Assessment: Methods and Measures")

    st.write("29. The assessment plan identifies at least one student success outcome (e.g. retention, progression, graduation).")
    student_success_outcome = st.radio("", ["Yes", "No"], key= "student_success_outcome", horizontal=True)
    # Add TWO line break
    st.write("")
    

    st.write("30. For at least one student success outcome, a measure is provided.")
    student_success_measure = st.radio("", ["Yes", "No"], key= "student_success_measure", horizontal=True)

    # Add TWO line break
    st.write("")
    st.write("")

    # Appendix Section
    st.subheader("Appendix")

    st.write("31. The appendix contains a Table of Contents.")
    appendix_table_of_contents = st.radio("", ["Yes", "No"], key= "appendix_table_of_contents", horizontal=True)
    
    # Add TWO line break
    st.write("")
    

    st.write("32. For each PSLO, is a copy or detailed description (e.g., standardized/certification exams) of the instrument/tool for each measure described in the Description of Measures included?")
    appendix_pslo_description = st.radio("", ["Yes", "No"], key= "appendix_pslo_description", horizontal=True)

    # Add TWO line break
    st.write("")
    st.write("")

    st.write("33. For missing copies or descriptions, list the PSLO number and name of the missing instrument/tool or items (refer to the Description of Measures for names). If the instrument/tool provided in the Appendix does not match what is stated in the Description of Measures, write 'mismatch' for the measure")
    appendix_missing_details = st.text_area('\n', key= "appendix_missing_details")

    #appendix_missing_details = st.text_area(
        #"33. For missing copies or descriptions, list the PSLO number and name of the missing instrument/tool or items (refer to the Description of Measures for names). "
        #"If the instrument/tool provided in the Appendix does not match what is stated in the Description of Measures, write 'mismatch' for the measure."
    #)

    # Add TWO line break
    st.write("")
    st.write("")

    # Estimated Duration
    st.subheader("Estimated Duration")

    st.write("34. Approximately how many minutes did you spend reviewing the assessment plan, including the minutes to complete this form.")
    estimated_duration = st.text_input("\n", key= "estimated_duration")


    # Submit button
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not reviewer_name or not college_name or not program_name:
            st.error("Please fill in all required fields.")
        else:
            # Save responses
            data = {
                "Reviewer Name": reviewer_name,
                "College Name": college_name,
                "Program Name": program_name,
                "Timestamp": datetime.now(),
            }

            data.update(curriculum_map_responses)
            data.update(pslo_quality_1_responses)
            data.update(pslo_quality_2_responses)
            data.update(pslo_quality_3_responses)
            data.update(pslo_quality_4_responses)
            data.update(pslo_quality_5_responses)
            data.update(pslo_quality_6_responses)
            data.update(methods_measures_pslo1)
            data["PSLO1 - Additional Measures"] = additional_measures
            data["PSLO1 - Measure Assessment"] = measure_assessment
            data["PSLO1 - Feedback"] = feedback
            data["Another PSLO to Assess"] = another_pslo
            data.update(methods_measures_pslo2)
            data["PSLO2 - Additional Measures"] = additional_measures_pslo2
            data["PSLO2 - Measure Assessment"] = measure_assessment_pslo2
            data["PSLO2 - Feedback"] = feedback_pslo2
            data["Another PSLO to Assess (PSLO2)"] = another_pslo_pslo2
            data.update(methods_measures_pslo3)
            data["PSLO3 - Additional Measures"] = additional_measures_pslo3
            data["PSLO3 - Measure Assessment"] = measure_assessment_pslo3
            data["PSLO3 - Feedback"] = feedback_pslo3
            data["Another PSLO to Assess (PSLO3)"] = another_pslo_pslo3
            data["Student Success - Outcome Identified"] = student_success_outcome
            data["Student Success - Measure Provided"] = student_success_measure
            data["Appendix - Table of Contents"] = appendix_table_of_contents
            data["Appendix - PSLO Descriptions Included"] = appendix_pslo_description
            data["Appendix - Missing Details"] = appendix_missing_details
            data["Estimated Duration (Minutes)"] = estimated_duration


            df = pd.DataFrame([data])
            df.to_csv(DATA_FILE, mode='a', header=not pd.read_csv(DATA_FILE).shape[0], index=False)

            st.success("Form submitted successfully!")



