import json
import pandas as pd
import streamlit as st

from secretsanta.main import funs as santa

st.set_page_config(page_title="Secret Santa Generator", layout="wide")

st.title("Secret Santa Assignment Generator")

st.write("Add participant names and emails below. You need at least 3 participants for the random assignment to work.")

# Initialize session state for assignments
if "assignments" not in st.session_state:
    st.session_state.assignments = None
if "assignments_viewed" not in st.session_state:
    st.session_state.assignments_viewed = False
if "show_email_form" not in st.session_state:
    st.session_state.show_email_form = False

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
    participants_df.dropna(subset=["Name", "Email"], inplace=True)
    participants_df = participants_df[participants_df["Name"].str.strip() != ""]
    participants_df = participants_df[participants_df["Email"].str.strip() != ""]

    if len(participants_df) < 3:
        st.error("You need at least 3 participants with both Name and Email.")
        st.session_state.assignments = None
    else:
        participants_dict = dict(zip(participants_df["Name"], participants_df["Email"]))
        st.session_state.assignments = santa.make_santa_dict(participants_dict)
        st.session_state.assignments_viewed = False
        st.session_state.show_email_form = False

if st.session_state.assignments:
    st.success("Assignments have been generated!")

    if st.session_state.assignments_viewed:
        st.warning("You have viewed the assignments. Sending emails for this set of assignments is disabled.")
    else:
        st.info("Choose to view assignments or send emails. Viewing will prevent sending.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("View Assignments"):
                st.session_state.assignments_viewed = True
                st.rerun()
        with col2:
            if st.button("Send Emails"):
                st.session_state.show_email_form = True

    if st.session_state.get("show_email_form") and not st.session_state.assignments_viewed:
        with st.form("email_form"):
            st.subheader("Email Sender Configuration")
            smtp_server = st.text_input("SMTP Server:Port", "smtp.gmail.com:587")
            sender_email = st.text_input("Sender Email", "santa.claus@acme-example.com")
            password = st.text_input("Password", type="password")
            test_run = st.checkbox("Test Run", help="Check this to perform a test run, will send test emails.")

            submitted = st.form_submit_button("Send")
            if submitted:
                if test_run:
                    st.info("Running in test mode - no emails will be sent")
                with st.spinner("Sending emails..." if not test_run else "Sending test emails..."):
                    check = santa.send_santa_dict(
                        smtp_server, sender_email, password, st.session_state.assignments, test=test_run
                    )
                if not check:
                    if test_run:
                        st.success("Test run completed successfully! Test emails sent.")
                    else:
                        st.success("All emails sent successfully!")
                else:
                    if test_run:
                        st.error(f"Test run failed: {check}")
                    else:
                        st.error(f"Failed to send some emails: {check}")
                if not test_run:
                    st.session_state.assignments_viewed = True  # Allow viewing after sending
                st.session_state.show_email_form = False
                st.rerun()

    if st.session_state.assignments_viewed:
        st.header("Generated Assignments")
        st.write("Below are the assignments. Each person on the left is the Secret Santa for the person on the right.")

        assignments_json = json.dumps(st.session_state.assignments, indent=4)
        st.code(assignments_json, language="json")

        assignments_csv = "Secret Santa,Recipient\n" + "\n".join(
            [f"{giver},{receiver}" for giver, receiver in st.session_state.assignments.items()]
        )
        st.download_button(
            label="Download Assignments as CSV",
            data=assignments_csv,
            file_name="secret_santa_assignments.csv",
            mime="text/csv",
        )
