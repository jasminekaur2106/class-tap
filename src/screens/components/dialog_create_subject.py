import streamlit as st
from src.database.db import create_subject

@st.dialog("create new subject")
def create_subject_dialog(teacher_id):
    st.write("enter details of new subjects")
    sub_id=st.text_input("Subject Code",placeholder="CS101")
    sub_name=st.text_input("Subject Name",palceholder="Introduction to Computer Science")
    sub_section=st.text_input("Section",placeholder="A")

    if st.button("create subject now" , type ="primary" ,width="stretch"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subject Created successfully!")
                st.rerun()

            except Exception as e:
                st.error(f"Error:{str(e)}")
        else:
            st.warning("Please fill all the fields")
