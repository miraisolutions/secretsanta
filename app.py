import json
import pandas as pd
import streamlit as st

from secretsanta.main import funs as santa

st.set_page_config(page_title="Secret Santa Generator", layout="wide")

st.title("Secret Santa Assignment Generator")

st.write(
    "Add participant names and emails below. You need at least 3 participants for the random assignment to work."
)

# Initialize session state for assignments
if "assignments" not in st.session_state:
    st.session_state.assignments = None

# Create a sample DataFrame for the data editor
initial_df = pd.DataFrame(
    [
        {"Name": "Jane", "Email": "jane.smith@acme-example.com"},
        {"Name": "John", "Email": "john.doe@acme-example.com"},
        {"Name": "Bob", "Email": "robert.lambda@acme-example.com"},
    ],
    columns=["Name", "Email"],
)

st.header("Participants")

edited_df = st.data_editor(
    initial_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Name": st.column_config.TextColumn(
            "Name",
            help="The name of the participant.",
            required=True,
        ),
        "Email": st.column_config.TextColumn(
            "Email",
            help="The email address of the participant.",
            required=True,
        ),
    },
)

if st.button("Generate Assignments", type="primary"):
    participants_df = edited_df.copy()

    # Filter out rows where 'Name' or 'Email' is missing or empty string.
    participants_df.dropna(subset=['Name', 'Email'], inplace=True)
    participants_df = participants_df[participants_df['Name'].str.strip() != '']
    participants_df = participants_df[participants_df['Email'].str.strip() != '']

    if len(participants_df) < 3:
        st.error("You need at least 3 participants with both Name and Email.")
        st.session_state.assignments = None
    else:
        participants_dict = dict(zip(participants_df["Name"], participants_df["Email"]))
        st.session_state.assignments = santa.make_santa_dict(participants_dict)

if st.session_state.assignments:
    st.header("Generated Assignments")
    st.write("Below are the assignments. Each person on the left is the Secret Santa for the person on the right.")

    assignments_json = json.dumps(st.session_state.assignments, indent=4)
    st.code(assignments_json, language="json")

    assignments_str = "\n".join(
        [f"{giver} -> {receiver}" for giver, receiver in st.session_state.assignments.items()]
    )
    st.download_button(
        label="Download Assignments as TXT",
        data=assignments_str,
        file_name="secret_santa_assignments.txt",
        mime="text/plain",
    )
