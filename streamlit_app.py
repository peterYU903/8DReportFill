import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

fields = [
    'customer_group', 'customer_plant', 'complaint_title', 'description', 'severity', 'urgency',
    'customer_part_no', 'je_part_no', 'je_lot_no', 'je_product_date_code', 'lot_qty', 'returned_samples',
    'defect_qty', 'description_attach', 'customer_contact_name', 'customer_contact_email', 'customer_contact_phone',
    'je_contact_name', 'je_contact_email', 'je_contact_phone'
]

col1_head, col2_head = st.columns(spec=[0.8, 0.2])
with col1_head:
    st.subheader("Please provide the following information before you raise a complaint")
with col2_head:
    option = st.selectbox("Language", ("English", "Chinese"))

col1_mid, col2_mid = st.columns(spec=[0.4, 0.6])
with col1_mid:
    customer_group = st.text_input("*Customer group", key='customer_group')
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

col4, col5 = st.columns(2)
with col4:
    customer_part_no = st.text_input("*Customer part No.", key='customer_part_no')
with col5:
    je_part_no = st.text_input("JE part No.", key='je_part_no')

col6, col7 = st.columns(2)
with col6:
    je_lot_no = st.text_input("JE lot No.", key='je_lot_no')
with col7:
    je_product_date_code = st.text_input("JE product date code", key='je_product_date_code')

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

col17, col18, col19, col20 = st.columns([0.25, 0.15, 0.3, 0.3])
with col17:
    st.write("JE contact")
with col18:
    je_contact_name = st.text_input("Name", key="je_contact_name")
with col19:
    je_contact_email = st.text_input("E-mail", key="je_contact_email")
with col20:
    je_contact_phone = st.text_input("Phone", key="je_contact_phone")

if 'valid' not in st.session_state:
    st.session_state.valid = None
col21, col22, col23 = st.columns([0.45, 0.35, 0.2])
with col22:
    if st.button("Submit"):
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
    messages_box = st.container(height=350)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with messages_box.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with messages_box.chat_message("user"):
            st.markdown(prompt)
        with messages_box.chat_message("assistant"):
            response = st.write("Testing")
        st.session_state.messages.append({"role": "assistant", "content": response})