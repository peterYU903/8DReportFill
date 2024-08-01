import streamlit as st
# import os
# from openai import OpenAI
# from dotenv import load_dotenv

fields = [
    'customer_group', 'customer_plant', 'complaint_title', 'description', 'severity',
    'customer_part_no', 'je_part_no', 'je_lot_no', 'je_product_date_code', 'lot_qty', 'returned_samples',
    'defect_qty', 'description_attach', 'customer_contact_name', 'customer_contact_email', 'customer_contact_phone',
    'je_contact_name', 'je_contact_email', 'je_contact_phone', 'who', 'when', 'why', 'what', 'how', 'how_much', 'where',
    'further_info', 'option', 'customer_complaint_id'
]

QuestionAnswer = {
    # "What is Johnson Electric?": "Johnson Electric is a company that designs and manufactures motion systems like electric motors and actuators for automotive and consumer applications.",
    # "What products do you offer?": "We offer a wide range of products including electric motors, actuators, and motion systems for various applications.",
}

@st.dialog("Summary List")
def summary():
    st.write("### Please review your inputs before final submission:")
    st.divider()
    st.write("#### Mandatory Information")
    st.write(f"**Language:** {st.session_state.get('option', 'Not specified')}")
    st.write(f"**Customer Group:** {st.session_state.customer_group}")
    st.write(f"**Customer Part No.:** {st.session_state.customer_part_no}")
    st.write(f"**Customer Plant:** {st.session_state.customer_plant}")
    st.write(f"**Complaint Title:** {st.session_state.complaint_title}")
    st.write(f"**Problem Description:** {st.session_state.description}")
    st.write(f"**Severity:** {st.session_state.severity}")
    st.write(f"**Defect Qty:** {st.session_state.defect_qty}")
    st.write(f"**Lot Qty:** {st.session_state.get('lot_qty', 'Not specified')}")
    st.write(f"**Returned Samples:** {st.session_state.get('returned_samples', 'Not specified')}")
    st.write(f"**Customer Contact Name:** {st.session_state.customer_contact_name}")
    st.write(f"**Customer Contact Email:** {st.session_state.customer_contact_email}")
    st.write(f"**Customer Contact Phone:** {st.session_state.customer_contact_phone}")
    st.divider()
    st.write("#### Optional Information")
    st.write(f"**JE Lot No.:** {st.session_state.get('je_lot_no', 'Not specified')}")
    st.write(f"**JE Part No.:** {st.session_state.get('je_part_no', 'Not specified')}")
    st.write(f"**JE Product Date Code:** {st.session_state.get('je_product_date_code', 'Not specified')}")
    st.write(f"**JE Contact Name:** {st.session_state.get('je_contact_name', 'Not specified')}")
    st.write(f"**JE Contact Email:** {st.session_state.get('je_contact_email', 'Not specified')}")
    st.write(f"**JE Contact Phone:** {st.session_state.get('je_contact_phone', 'Not specified')}")
    st.write(f"**What:** {st.session_state.get('what', 'Not specified')}")
    st.write(f"**Where:** {st.session_state.get('where', 'Not specified')}")
    st.write(f"**Who:** {st.session_state.get('who', 'Not specified')}")
    st.write(f"**How Much:** {st.session_state.get('how_much', 'Not specified')}")
    st.write(f"**Why:** {st.session_state.get('why', 'Not specified')}")
    st.write(f"**When:** {st.session_state.get('when', 'Not specified')}")
    st.write(f"**How:** {st.session_state.get('how', 'Not specified')}")
    st.write(f"**Customer Complaint ID No.:** {st.session_state.get('customer_complaint_id', 'Not specified')}")
    st.divider()
    st.write("#### Attachments")
    if st.session_state.get('attachments'):
        for attachment in st.session_state.attachments:
            st.write(f"- {attachment.name}")
    else:
        st.write("No attachments uploaded.")
    st.write(f"**Attachment Description:** {st.session_state.get('description_attach', 'Not specified')}")
    st.write(f"**Further Information / Special Notes:** {st.session_state.get('further_info', 'Not specified')}")

    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("Confirm and Submit"):
            st.session_state.submit = True
            st.rerun()
    with col_2:
        if st.button("Back to Edit"):
            st.session_state.submit = None
            st.session_state.valid = None
            st.rerun()
    st.warning("Please review your inputs and click 'Confirm and Submit' to finalize your case.")

with st.sidebar:
    st.title("💬 Quality Chatbot")
    st.write(
        "Welcome to the JE Quality Chatbot. "
        "I will guide you on how to submit cases for quality issues. "
    )
    col1_side, col2_side = st.columns([2, 1])
    with col2_side:
        if st.button("Clear History!", type="primary"):
            st.session_state.messages = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Please start by filling in the required fields with the necessary information."})
    container = st.container()
    for message in st.session_state.messages:
        message_box = st.container(border=True)
        container.chat_message(message["role"]).write(message["content"])
    for question in QuestionAnswer.keys():
        if st.button(question):
            container.chat_message("user").write(question)
            st.session_state.messages.append({"role": "user", "content": question})
            response = QuestionAnswer[question]
            container.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    if prompt := st.chat_input("Ask me anything..."):
        container.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "Testing"
        container.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

if 'submit' not in st.session_state:
    st.session_state['submit'] = None

if st.session_state.submit is None:
    st.title("Quality Issue Form")
    with st.form('Mandatory'):

        col1_head, col2_head = st.columns(spec=[0.8, 0.2])
        with col1_head:
            st.subheader("Please provide the following information for your quality issue")
        with col2_head:
            option = st.selectbox("Language", ("English", "Chinese"), key='option')
        st.divider()
        col1_mid, col2_mid = st.columns(spec=[0.4, 0.6])
        with col1_mid:
            customer_group = st.text_input("*Customer Group", key='customer_group')
        with col2_mid:
            customer_plant = st.text_input("*Customer Plant", key='customer_plant')
        complaint_title = st.text_input("*Complaint Title", key='complaint_title')
        description = st.text_area("*Problem Description", key='description')
        col1, col2 = st.columns(2)
        with col1:
            customer_part_no = st.text_input("*Customer Part No.", key='customer_part_no')
        with col2:
            severity = st.text_input("*Severity", key='severity')

        col8, col9, col10 = st.columns([0.2, 0.4, 0.4])
        with col8:
            quantity = st.write("Quantity")
        with col9:
            lot_qty = st.number_input("Lot Qty", min_value=0, key='lot_qty')
            returned_samples = st.number_input("Returned Samples", min_value=0, key='returned_samples')
        with col10:
            defect_qty = st.number_input("*Defect Qty", min_value=0, key='defect_qty')

        col13, col14, col15, col16 = st.columns([0.25, 0.15, 0.3, 0.3])
        with col13:
            st.write("*Customer Contact")
        with col14:
            customer_contact_name = st.text_input("Name", key="customer_contact_name")
        with col15:
            customer_contact_email = st.text_input("E-mail", key="customer_contact_email")
        with col16:
            customer_contact_phone = st.text_input("Phone", key="customer_contact_phone")
        with st.expander("💬 Optional"):
            st.info(
                    'We sincerely appreciate if you can providing the following information. '
                    'With this information, we will be able to expedite the follow-up process for your case. '
                    'Thank you.'
                )
            col5, col6, col7 = st.columns(3)
            with col5:
                je_lot_no = st.text_input("JE Lot No.", key='je_lot_no')
            with col6:
                je_part_no = st.text_input("JE Part No.", key='je_part_no')
            with col7:
                je_product_date_code = st.text_input("JE Product Date Code", key='je_product_date_code')

            col17, col18, col19, col20 = st.columns([0.25, 0.15, 0.3, 0.3])
            with col17:
                st.write("JE Contact (if any)")
            with col18:
                je_contact_name = st.text_input("Name", key="je_contact_name")
            with col19:
                je_contact_email = st.text_input("E-mail", key="je_contact_email")
            with col20:
                je_contact_phone = st.text_input("Phone No.", key="je_contact_phone")
            col1, col2 = st.columns(2)
            with col1:
                what = st.text_input("What is the problem?", key='what')
                where = st.text_input("Where was the issue found?", key='where')
                who = st.text_input("Who discovered the issues?", key='who')
                how_much = st.text_input("How many products are affected?", key='how_much')
                customer_complaint_id = st.text_input("Customer Complaint ID No. (if any)", key='customer_complaint_id')
            with col2:
                why = st.text_input("Why did the issue occur?", key='why')
                when = st.text_input("When was the issue happened?", key='when')
                how = st.text_input("How did it happen?", key='how') 
            col11, col12 = st.columns([0.25, 0.75])
            with col11:
                st.write("Picture of Defect Product and/or Other Information")
            with col12:
                attachments = st.file_uploader("", accept_multiple_files=True)
                description_attach = st.text_area("Attachment Description", key='description_attach')
            further_info = st.text_area("Further Information / Special Notes", key='further_info', max_chars=500)
        st.divider()
        if 'valid' not in st.session_state:
            st.session_state.valid = None
        _, col21, _ = st.columns([0.45, 0.35, 0.2])
        with col21:
            if st.form_submit_button("Submit"):
                if not st.session_state.customer_plant or not st.session_state.description  \
                    or st.session_state.defect_qty == 0 or not st.session_state.customer_contact_name \
                    or not st.session_state.customer_contact_email or not st.session_state.customer_contact_phone \
                    or not st.session_state.customer_group or not st.session_state.complaint_title \
                    or not st.session_state.severity or not st.session_state.customer_part_no:
                    st.session_state.valid = False
                else:
                    st.session_state.valid = True

    if st.session_state.valid is not None:
        if st.session_state.valid:
            summary()
        else:
            st.error("Please fill in all required fields marked with *")
            st.stop()
else:
    st.success("Complaint submitted successfully!")
    st.write(
        'Thank you for providing your information. Your case number is: xxxxxx.\n'
        'You will receive a notification email shortly. If you require urgent assistance, please do not hesitate to contact xxxx for immediate support.\n'
        'Should you have any further questions, feel free to continue the discussion with our chatbot. We're here to support your enquiry.'
    )
