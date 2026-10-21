import streamlit as st

from src.screens.ui.base_layout import style_background_dashboard, style_base_layout
from src.screens.components.header import header_dashboard
from src.screens.database.db import check_teacher_exists, create_teacher, teacher_login

    style_background_dashboard()
    style_base_layout()

    if st.session_state.get("is_logged_in", False):
        teacher_dashboard()

    elif st.session_state.get("teacher_login_type", "login") == "register":
        teacher_screen_register()

    else:
        teacher_screen_login()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1,c2= st.columns(2,vertical_alignment="center",gap="xxlarge")
    with c1:
        header_dashboard()
    
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}!")
        if st.button("Logout",type="secondary", key="loginbackbtn"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data
            st.rerun()


    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    tab1, tab2 ,tab3 = st.columns(3)

    with tab1:
        type1= "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance",type=type1,width="stretch", icon=":material/assignment_turned_in:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
            type2= "primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
            if st.button("Manage Subjects",type=type2,width="stretch", icon=":material/menu_book:"):
                st.session_state.current_teacher_tab = "manage_subjects"
                st.rerun()

    with tab3:
            type3= "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
            if st.button("Attendance Records",type=type3,width="stretch", icon=":material/overview:"):
                st.session_state.current_teacher_tab = "attendance_records"
                st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab=="take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab=="manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab=="attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendance():
    st.header("Take AI attendance")

def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data["teacher_id"]
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage Subjects",width="stretch")
    with col2:
        if st.button("Create New Subject",width="Content"):
            create_subject_dialog(teacher_id)
    st.header("Manage Subjects")

def teacher_tab_attendance_records():
    st.header("Attendance Records")

def login_teacher(teacher_username, teacher_pass):
    if not teacher_username or not teacher_pass:
        st.error("Please enter both username and password.")
        return False
    teacher=teacher_login(teacher_username, teacher_pass)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False



def teacher_screen_login():
    c1,c2= st.columns(2,vertical_alignment="center",gap="xxlarge")
    with c1:
        header_dashboard()

    with c2:
        if st.button("Go back to Home",type="secondary", key="loginbackbtn"):
            st.session_state['login_type'] = None
            st.rerun()
        

    st.header("Login to your Teacher Profile",text_alignment="center")
    st.space()
    st.space()
    st.markdown("""
    <style>
    [data-testid="stWidgetLabel"] p {
        color: black !important;
    }
    div[data-baseweb="input"] {
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    teacher_username = st.text_input("Username", placeholder="Enter your username")

    teacher_pass= st.text_input("Password", placeholder="Enter your password", type="password")

    st.divider()

    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button("Login", icon=":material/passkey:" ,shortcut="control+enter",width="stretch"):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("Login successful!", icon="✅")
                
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.", icon="❌")
                

    with btnc2:
        if st.button("Register",type="primary", icon=":material/passkey:" ,width="stretch"):
            st.session_state.teacher_login_type="register"
            st.rerun()
            
            
def register_teacher(teacher_username, teacher_name , teacher_pass, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
        return False, "Please fill in all fields."
    
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."
    
    
    if check_teacher_exists(teacher_username):
        return False, "Username already exists. Please choose a different username."
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Teacher profile created successfully. You can now log in."
    except Exception as e:    
        return False, "An error occurred while creating the teacher profile. Please try again."


def teacher_screen_register():
    c1,c2= st.columns(2,vertical_alignment="center",gap="xxlarge")
    with c1:
            header_dashboard()
    
    with c2:
            if st.button("Go back to Home",type="secondary", key="loginbackbtn", shortcut="control+backspace"):
                st.session_state['login_type'] = None
                st.rerun()
    
    
    st.header('Register your Teacher Profile')

    st.space()
    st.space()
    st.markdown("""
        <style>
        [data-testid="stWidgetLabel"] p {
            color: black !important;
        }
        div[data-baseweb="input"] {
            background-color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
    teacher_username = st.text_input("Username", placeholder="Enter your username")

    teacher_name= st.text_input("Enter name", placeholder="Enter your name")
    
    teacher_pass= st.text_input("Password", placeholder="Enter your password", type="password")

    teacher_pass_confirm= st.text_input("Confirm Password", placeholder="Confirm your password", type="password")
    
    st.divider()
    
    btnc1,btnc2=st.columns(2)
    
    with btnc1:
        if st.button("Register now", icon=":material/passkey:" ,shortcut="control+enter",width="stretch"):
            success, message= register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)

    
    with btnc2:
        if st.button("Login Instead",type="primary", icon=":material/passkey:" ,width="stretch"):
            st.session_state.teacher_login_type="login"
            st.rerun()
                
    