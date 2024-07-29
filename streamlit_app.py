import streamlit as st
# import os
# from openai import OpenAI
# from dotenv import load_dotenv
import streamlit_antd_components as sac

fields = [
    'customer_group', 'customer_plant', 'complaint_title', 'description', 'severity', 'urgency',
    'customer_part_no', 'je_part_no', 'je_lot_no', 'je_product_date_code', 'lot_qty', 'returned_samples',
    'defect_qty', 'description_attach', 'customer_contact_name', 'customer_contact_email', 'customer_contact_phone',
    'je_contact_name', 'je_contact_email', 'je_contact_phone', 'who', 'when', 'why', 'what', 'how', 'how_much', 'where'
]

QuestionAnswer = {
    "What is Johnson Electric?": "Johnson Electric is a company that designs and manufactures motion systems like electric motors and actuators for automotive and consumer applications.",
    "What products do you offer?": "We offer a wide range of products including electric motors, actuators, and motion systems for various applications.",
}

with st.form('Mandatory'):
    
    col1_head, col2_head = st.columns(spec=[0.8, 0.2])
    with col1_head:
        st.subheader("Please provide the following information before you raise a complaint")
    with col2_head:
        option = st.selectbox("Language", ("English", "Chinese"))

    sac.divider(label='Mandatory', icon='house', align='center', color='gray')

    col1_mid, col2_mid = st.columns(spec=[0.4, 0.6])
    with col1_mid:
        customer_group = st.text_input("*Customer group", key='customer_group')
        customer_part_no = st.text_input("*Customer part No.", key='customer_part_no')
    with col2_mid:
        customer_plant = st.text_input("*Customer plant", key='customer_plant')
    complaint_title = st.text_input("*Complaint title", key='complaint_title')
    description = st.text_area("*Problem Description", key='description')

    col1, col2, col3 = st.columns([0.2, 0.4, 0.4])
    with col1:
        complaint_type = st.write("Complaint type")
    with col2:
        severity = st.text_input("*Severity", key='severity')
    with col3:
        urgency = st.text_input("Urgency", key='urgency')

    col8, col9, col10 = st.columns([0.2, 0.4, 0.4])
    with col8:
        quantity = st.write("Quantity")
    with col9:
        lot_qty = st.number_input("Lot Qty", min_value=0, key='lot_qty')
        returned_samples = st.number_input("Returned samples", min_value=0, key='returned_samples')
    with col10:
        defect_qty = st.number_input("*Defect Qty", min_value=0, key='defect_qty')

    col11, col12 = st.columns([0.25, 0.75])
    with col11:
        st.markdown("Attachment & Photos")
    with col12:
        attachments = st.file_uploader("", accept_multiple_files=True)
        description_attach = st.text_area("Attachment Description", key='description_attach')

    col13, col14, col15, col16 = st.columns([0.25, 0.15, 0.3, 0.3])
    with col13:
        st.write("*Customer contact")
    with col14:
        customer_contact_name = st.text_input("Name", key="customer_contact_name")
    with col15:
        customer_contact_email = st.text_input("E-mail", key="customer_contact_email")
    with col16:
        customer_contact_phone = st.text_input("Phone", key="customer_contact_phone")

    sac.divider(label='Optional', icon='chat-left-text', align='center', color='gray')
    st.info(
            'We sincerely appreciate if you can providing the following information. '
            'With this information, we will be able to expedite the follow-up process for your case. '
            'Thank you.'
        )

    col5, col6, col7 = st.columns(3)
    with col5:
        je_lot_no = st.text_input("JE lot No.", key='je_lot_no')
    with col6:
        je_part_no = st.text_input("JE part No.", key='je_part_no')
    with col7:
        je_product_date_code = st.text_input("JE product date code", key='je_product_date_code')

    col17, col18, col19, col20 = st.columns([0.25, 0.15, 0.3, 0.3])
    with col17:
        st.write("JE contact")
    with col18:
        je_contact_name = st.text_input("Name", key="je_contact_name")
    with col19:
        je_contact_email = st.text_input("E-mail", key="je_contact_email")
    with col20:
        je_contact_phone = st.text_input("Phone", key="je_contact_phone")

    col1, col2 = st.columns(2)

    with col1:
        what = st.text_input("What", key='what')
        where = st.text_input("Where", key='where')
        who = st.text_input("Who", key='who')
        how_much = st.text_input("How much", key='how_much')

    with col2:
        why = st.text_input("Why", key='why')
        when = st.text_input("When", key='when')
        how = st.text_input("How", key='how')        

    sac.divider(label='Submission', icon='check2-circle', align='center', color='gray')
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
            st.success("Complaint submitted successfully!")
        else:
            st.error("Please fill in all required fields marked with *")

with st.sidebar:
    st.title("💬 Chatbot")
    st.write(
        "This Chatbot will assit you from filling the form. "
        "If you come across any problem, you could type in your confuse. "
        "The Bot will answer you!"
    )
    col1_side, col2_side = st.columns([2, 1])
    with col2_side:
        if st.button("Clear History!", type="primary"):
            st.session_state.messages = []
    if "messages" not in st.session_state:
        st.session_state.messages = []
    container = st.container()
    for message in st.session_state.messages:
        container.chat_message(message["role"]).write(message["content"])
    for question in QuestionAnswer.keys():
        if st.button(question):
            container.chat_message("user").write(question)
            st.session_state.messages.append({"role": "user", "content": question})
            response = QuestionAnswer[question]
            container.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    if prompt := st.chat_input("What is up?"):
        container.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "Testing"
        container.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})    