import streamlit as st
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh
import sqlite3
import os

from database import (
    create_tables,
    register_user,
    login_user,
    save_result,
    get_results,
    add_question,
    get_all_questions,
    delete_question,
    get_questions_by_category,
    get_total_users,
    get_total_questions,
    get_total_tests,
    get_average_score,
    get_all_results,
    update_question,
    get_all_users,
    get_user_results,
    update_user_name,
    update_user_password,
    validate_password,
    validate_user_details
)

# Create db_files tables
create_tables()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Page configuration
st.set_page_config(
    page_title="BrainBoost IQ Test",
    page_icon="⚡",
    layout="wide"
)

# ===== Load Custom CSS =====
css_file = os.path.join(os.path.dirname(__file__), "style.css")

if os.path.exists(css_file):
    with open(css_file, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "name" not in st.session_state:
    st.session_state.name = ""

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if "test_start_time" not in st.session_state:
    st.session_state.test_start_time = None

if "test_finished" not in st.session_state:
    st.session_state.test_finished = False

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}


# --------------------------------------------------
# LOGIN / REGISTER PAGE
# --------------------------------------------------

if not st.session_state.logged_in:

    st.title("🧠⚡ BrainBoost IQ Test")
    st.write("#####  -- Welcome to the IQ Test System!🙏")

    st.divider()

    st.subheader("🔐 User Account")

    option = st.radio(
        "Choose an option:",
        ["Login", "Create New Account"],
        horizontal=True
    )

    # ---------------- LOGIN ----------------

    # ---------------- LOGIN ----------------

    if option == "Login":

        st.markdown("""
        <div class="form-heading">
            <div class="form-title">🔑 Welcome Back</div>
            <div class="form-subtitle">Login to your already existing account & continue your BrainBoost journey</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
                "Login",
                type="primary",
                key="login_button"
        ):

            # ------------------------------
            # VALIDATE USERNAME
            # ------------------------------

            if not username.strip():

                st.warning(
                    "⚠️ Please enter your username."
                )

            # ------------------------------
            # VALIDATE PASSWORD
            # ------------------------------

            elif not password:

                st.warning(
                    "⚠️ Please enter your password."
                )

            # ------------------------------
            # LOGIN
            # ------------------------------

            else:

                user = login_user(
                    username.strip(),
                    password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.username = user[2]

                    st.session_state.name = user[1]

                    st.success(
                        f"Welcome, {user[1]}! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password ❌"
                    )

    # ---------------- REGISTER ----------------

    else:

        st.write("## 📝 Create New Account")

        name = st.text_input("Full Name")

        username = st.text_input(
            "Choose Username"
        )

        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
                "Create Account",
                type="primary",
                key="create_account_button"
        ):

            if not name or not username or not password:

                st.warning(
                    "Please fill all the fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                # Validate name and username
                valid_details, details_message = validate_user_details(
                    name,
                    username
                )

                if not valid_details:

                    st.warning(
                        f"⚠️ {details_message}"
                    )

                else:

                    # Validate password
                    valid_password, password_message = validate_password(
                        password
                    )

                    if not valid_password:

                        st.warning(
                            f"⚠️ {password_message}"
                        )

                    else:

                        # Create account
                        result = register_user(
                            name.strip(),
                            username.strip(),
                            password
                        )

                        if result:

                            st.success(
                                "Account created successfully! ✅"
                            )

                            st.info(
                                "You can now login."
                            )

                        else:

                            st.error(
                                "Username already exists ❌"
                            )




# --------------------------------------------------
# USER DASHBOARD
# --------------------------------------------------

else:

    # Sidebar
    st.sidebar.title("🧠⚡ BrainBoost")

    st.sidebar.write(
        f"Welcome, **{st.session_state.name}**"
    )

    st.sidebar.divider()

    # Open Test page when a dashboard category is selected
    if st.session_state.get("dashboard_start_test", False):

        st.session_state.dashboard_start_test = False
        st.session_state.main_navigation = "📝 Test"

    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 My Profile",
            "📝 Test",
            "📊 My Results",
            "🔐 Admin",
            "ℹ️ About / Info"
        ],
        key="main_navigation"
    )

    st.sidebar.divider()

    if st.sidebar.button(
            "🚪 Logout",
            key="logout_button"
    ):
        # Clear login information
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.name = ""

        # Clear admin login
        st.session_state.admin_logged_in = False

        # Clear test information
        st.session_state.answers = {}
        st.session_state.current_question = 0
        st.session_state.test_started = False
        st.session_state.test_finished = False
        st.session_state.test_score = 0
        st.session_state.test_total = 0
        st.session_state.test_start_time = None

        st.rerun()

    # --------------------------------------------------
    # BRAINBOOST HEADER
    # --------------------------------------------------

    st.markdown(
        """
        <div class="brainboost-header">
            <div class="brainboost-name">🧠⚡ BrainBoost IQ Test</div>
            <div class="brainboost-tagline">
               || Challenge Your Mind • Improve Your Knowledge • Track Your Progress ||
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    if menu == "🏠 Dashboard":

        st.title("🏠 Dashboard")

        st.markdown(
            f"### Welcome, {st.session_state.name}! 👋"
        )

        st.caption(
            "Ready to test your knowledge and improve your skills?"
        )

        st.divider()

        # --------------------------------------------------
        # DASHBOARD STATISTICS
        # --------------------------------------------------



        # --------------------------------------------------
        # REAL TEST STATISTICS
        # --------------------------------------------------

        results = get_results(
            st.session_state.username
        )

        tests_taken = len(results)

        if results:

            scores = [row[1] for row in results]
            percentages = [row[3] for row in results]

            best_score = max(scores)

            average_percentage = (
                    sum(percentages) / len(percentages)
            )

        else:

            best_score = 0
            average_percentage = 0

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "📝 Tests Taken",
                tests_taken
            )

        with col2:

            st.metric(
                "🏆 Best Score",
                best_score
            )

        with col3:

            st.metric(
                "📊 Average Score",
                f"{average_percentage:.1f}%"
            )

        st.divider()

        st.subheader("📚 Test Categories")

        col1, col2, col3, col4, col5 = st.columns(
             [1, 1, 1.2, 1.25, 1.6]
        )

        with col1:
            if st.button("🧮 Maths", key="dashboard_maths", use_container_width=True):
                st.session_state.selected_category = "Maths"
                st.session_state.dashboard_start_test = True
                st.rerun()

        with col2:
            if st.button("🔬 Science", key="dashboard_science", use_container_width=True):
                st.session_state.selected_category = "Science"
                st.session_state.dashboard_start_test = True
                st.rerun()

        with col3:
            if st.button("💻 Computer", key="dashboard_computer", use_container_width=True):
                st.session_state.selected_category = "Computer"
                st.session_state.dashboard_start_test = True
                st.rerun()

        with col4:
            if st.button("🌱 Environment", key="dashboard_environment", use_container_width=True):
                st.session_state.selected_category = "Environment"
                st.session_state.dashboard_start_test = True
                st.rerun()

        with col5:
            if st.button("🌎 General Knowledge", key="dashboard_gk", use_container_width=True):
                st.session_state.selected_category = "General Knowledge"
                st.session_state.dashboard_start_test = True
                st.rerun()


    # --------------------------------------------------
    # MY PROFILE
    # --------------------------------------------------

    elif menu == "👤 My Profile":

        st.title("👤 My Profile")

        username = st.session_state.username

        # Get user's test results
        user_results = get_results(username)

        # ------------------------------------------
        # GET USER INFORMATION
        # ------------------------------------------

        conn = sqlite3.connect("iq_test.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name, username
            FROM users
            WHERE username = ?
        """, (username,))

        user_data = cursor.fetchone()

        conn.close()

        if user_data:

            name = user_data[0]
            username = user_data[1]

            # --------------------------------------
            # PROFILE INFORMATION
            # --------------------------------------

            st.subheader("📋 Account Information")

            col1, col2 = st.columns(2)

            with col1:

                st.info(
                    f"👤 **Name**\n\n{name}"
                )

            with col2:

                st.info(
                    f"🔑 **Username**\n\n{username}"
                )

            st.divider()

            # --------------------------------------
            # TEST STATISTICS
            # --------------------------------------

            st.subheader("📊 Test Statistics")

            if user_results:

                total_tests = len(user_results)

                percentages = [
                    result[3]
                    for result in user_results
                ]

                average_score = (
                        sum(percentages)
                        / total_tests
                )

                best_score = max(percentages)

                total_correct = sum(
                    result[1]
                    for result in user_results
                )

            else:

                total_tests = 0
                average_score = 0
                best_score = 0
                total_correct = 0

            col1, col2, col3, col4 = st.columns(4)

            with col1:

                st.metric(
                    "📝 Tests Taken",
                    total_tests
                )

            with col2:

                st.metric(
                    "📊 Average Score",
                    f"{average_score:.1f}%"
                )

            with col3:

                st.metric(
                    "🏆 Best Score",
                    f"{best_score:.1f}%"
                )

            with col4:

                st.metric(
                    "✅ Correct Answers",
                    total_correct
                )

            st.divider()

            # --------------------------------------
            # ACCOUNT STATUS
            # --------------------------------------

            st.subheader("🔐 Account Status")

            st.success(
                "🟢 Account Active"
            )

            st.caption(
                "Your profile information is "
                "linked to your BrainBoost IQ account."
            )

            # ------------------------------------------
            # EDIT PROFILE
            # ------------------------------------------

            st.divider()

            st.subheader("✏️ Edit Profile")

            new_name = st.text_input(
                "👤 Your Name",
                value=name,
                key="profile_name",
                help="Enter the name you want to display on your BrainBoost account."
            )

            if st.button(
                    "💾 Update Name",
                    type="primary",
                    key="update_profile_name"
            ):

                if not new_name.strip():

                    st.warning(
                        "⚠️ Name cannot be empty."
                    )

                else:

                    update_user_name(
                        username,
                        new_name.strip()
                    )

                    st.success(
                        "✅ Your name has been updated successfully!"
                    )

                    st.rerun()

            # ------------------------------------------
            # CHANGE PASSWORD
            # ------------------------------------------

            st.divider()

            st.subheader("🔐 Change Password")

            current_password = st.text_input(
                "Current Password",
                type="password",
                key="current_password"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                key="confirm_new_password"
            )

            if st.button(
                    "🔐 Change Password",
                    type="primary",
                    key="change_password_button"
            ):

                if not current_password:

                    st.warning(
                        "⚠️ Please enter your current password."
                    )

                elif not new_password:

                    st.warning(
                        "⚠️ Please enter a new password."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "❌ New passwords do not match."
                    )

                else:

                    conn = sqlite3.connect("iq_test.db")
                    cursor = conn.cursor()

                    cursor.execute("""
                        SELECT password
                        FROM users
                        WHERE username = ?
                    """, (username,))

                    stored_password = cursor.fetchone()

                    conn.close()

                    if (
                            stored_password
                            and current_password == stored_password[0]
                    ):

                        update_user_password(
                            username,
                            new_password
                        )

                        st.success(
                            "✅ Password changed successfully!"
                        )

                    else:

                        st.error(
                            "❌ Current password is incorrect."
                        )


    # --------------------------------------------------
    # TEST
    # --------------------------------------------------

    # --------------------------------------------------
    # TEST
    # --------------------------------------------------

    elif menu == "📝 Test":

        st.title("📝 IQ Test")

        # Question bank
        categories = [
            "Maths",
            "Science",
            "Computer",
            "Environment",
            "General Knowledge"
        ]

        # ----------------------------------------------
        # SELECT CATEGORY
        # ----------------------------------------------

        available_categories = [
            "Maths",
            "Science",
            "Computer",
            "Environment",
            "General Knowledge"
        ]

        default_category = st.session_state.get(
            "selected_category",
            available_categories[0]
        )

        if default_category in available_categories:

            default_index = available_categories.index(
                default_category
            )

        else:

            default_index = 0

        category = st.selectbox(
            "📚 Choose Test Category",
            available_categories,
            index=default_index,
            key="test_category_select"
        )

        # ----------------------------------------------
        # GET QUESTIONS FROM DATABASE
        # ----------------------------------------------

        db_questions = get_questions_by_category(category)

        if not db_questions:

            st.warning(
                f"No questions available for {category}."
            )

            st.info(
                "Ask the admin to add questions from "
                "🔐 Admin → ➕ Add Question."
            )

        else:

            # ------------------------------------------
            # START TEST
            # ------------------------------------------

            if not st.session_state.get(
                    "test_started",
                    False
            ):

                if st.button(
                        "🚀 Start Test",
                        key="start_test_button"
                ):
                    # Start a completely new test
                    st.session_state.test_started = True
                    st.session_state.test_finished = False
                    st.session_state.test_score = 0
                    st.session_state.test_total = 0
                    st.session_state.current_question = 0
                    st.session_state.answers = {}

                    # Store selected category
                    st.session_state.selected_category = category

                    # Start timer
                    st.session_state.test_start_time = datetime.now()

                    st.rerun()

            else:

                st.info(
                    "🧠 A test is currently in progress."
                )

            # ------------------------------------------
            # RUNNING TEST
            # ------------------------------------------

            if st.session_state.get(
                    "test_started",
                    False
            ):

                test_category = (
                    st.session_state.selected_category
                )

                db_questions = get_questions_by_category(
                    test_category
                )

                total_questions = len(db_questions)

                current_question = (
                    st.session_state.current_question
                )

                # --------------------------------------
                # QUESTION PROGRESS
                # --------------------------------------

                question_number = current_question + 1

                st.write(
                    f"### Question {question_number} of {total_questions}"
                )

                progress = question_number / total_questions

                st.progress(
                    progress
                )

                # --------------------------------------
                # TIMER
                # --------------------------------------

                test_duration = timedelta(minutes=2)

                elapsed_time = (
                        datetime.now()
                        - st.session_state.test_start_time
                )

                remaining_time = (
                        test_duration - elapsed_time
                )

                if remaining_time.total_seconds() <= 0:

                    st.warning(
                        "⏰ Time is up! "
                        "Submitting your test..."
                    )

                    score = 0

                    for i, q in enumerate(
                            db_questions
                    ):

                        correct_answer = q[6]

                        if (
                                st.session_state.answers.get(i)
                                == correct_answer
                        ):
                            score += 1

                    percentage = (
                                         score / total_questions
                                 ) * 100

                    save_result(
                        st.session_state.username,
                        test_category,
                        score,
                        total_questions,
                        percentage
                    )

                    st.session_state.test_score = score
                    st.session_state.test_total = total_questions
                    st.session_state.test_finished = True
                    st.session_state.test_started = False
                    st.session_state.test_start_time = None

                    st.rerun()

                # --------------------------------------
                # TIMER DISPLAY
                # --------------------------------------

                remaining_seconds = int(
                    remaining_time.total_seconds()
                )

                minutes = remaining_seconds // 60
                seconds = remaining_seconds % 60

                # ------------------------------------------
                # IMPROVED TIMER DISPLAY
                # ------------------------------------------

                if remaining_seconds <= 30:

                    st.error(
                        f"🔴 TIME RUNNING OUT: "
                        f"**{minutes:02d}:{seconds:02d}**"
                    )

                elif remaining_seconds <= 60:

                    st.warning(
                        f"🟠 Time Remaining: "
                        f"**{minutes:02d}:{seconds:02d}**"
                    )

                else:

                    st.markdown(
                        f"""
                        <div class="test-timer">
                            ⏱️ Time Remaining: {minutes:02d}:{seconds:02d}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st_autorefresh(
                    interval=1000,
                    key="test_timer"
                )

                # --------------------------------------
                # TEST HEADER
                # --------------------------------------

                st.subheader(
                    f"📚 {test_category} Test"
                )



                st.progress(progress)


                # ------------------------------------------
                # QUESTION NAVIGATION
                # ------------------------------------------

                st.write("### 🔢 Questions")

                questions_per_row = 5

                for start in range(
                        0,
                        total_questions,
                        questions_per_row
                ):

                    row_questions = min(
                        questions_per_row,
                        total_questions - start
                    )

                    nav_columns = st.columns(questions_per_row)

                    for j in range(row_questions):

                        i = start + j

                        with nav_columns[j]:

                            if i in st.session_state.answers:
                                label = f"🟢 Q{i + 1}"
                            else:
                                label = f"⚪ Q{i + 1}"

                            if st.button(
                                    label,
                                    key=f"nav_question_{i}"
                            ):
                                st.session_state.current_question = i
                                st.rerun()
                # --------------------------------------
                # CURRENT QUESTION
                # --------------------------------------

                question = db_questions[
                    current_question
                ]

                question_text = question[1]

                options = [
                    question[2],
                    question[3],
                    question[4],
                    question[5]
                ]

                # ------------------------------------------
                # QUESTION CARD
                # ------------------------------------------

                st.markdown(
                    f"""
                        <div class="question-card">
                            <div class="question-number">
                                🧠 Question {current_question + 1}
                            </div>
                            <div class="question-text">
                                {question_text}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <div class="question-progress">
                        Question {current_question + 1} of {total_questions}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                answer = st.radio(
                    "👇 Select your answer:",
                    options,
                    key=f"question_{current_question}"
                )

                # Save answer
                st.session_state.answers[
                    current_question
                ] = answer

                st.divider()

                # --------------------------------------
                # PREVIOUS / NEXT
                # --------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    if current_question > 0:

                        if st.button("⬅️ Previous"):
                            st.session_state.current_question -= 1

                            st.rerun()

                with col2:

                    if current_question < total_questions - 1:

                        if st.button("Next ➡️"):
                            st.session_state.current_question += 1

                            st.rerun()

                    else:

                        # ------------------------------------------
                        # TEST REVIEW SUMMARY
                        # ------------------------------------------

                        st.divider()

                        st.subheader("📝 Test Summary")

                        answered_count = len(
                            st.session_state.answers
                        )

                        unanswered_count = (
                                total_questions - answered_count
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            st.success(
                                f"✅ Answered: {answered_count}"
                            )

                        with col2:

                            if unanswered_count > 0:

                                st.warning(
                                    f"⚪ Unanswered: {unanswered_count}"
                                )

                            else:

                                st.success(
                                    "🎉 All questions answered!"
                                )

                                # ------------------------------------------
                                # REVIEW QUESTION STATUS
                                # ------------------------------------------

                                st.write("### 🔍 Review Questions")

                                review_columns = st.columns(5)

                                for i in range(total_questions):

                                    with review_columns[i % 5]:

                                        if i in st.session_state.answers:

                                            if st.button(
                                                    f"🟢 Q{i + 1}",
                                                    key=f"review_question_{i}"
                                            ):
                                                st.session_state.current_question = i

                                                st.rerun()

                                        else:

                                            if st.button(
                                                    f"⚪ Q{i + 1}",
                                                    key=f"review_question_{i}"
                                            ):
                                                st.session_state.current_question = i

                                                st.rerun()
                        # ------------------------------------------
                        # FINAL SUBMISSION CONFIRMATION
                        # ------------------------------------------

                        st.divider()

                        confirm_submit = st.checkbox(
                            "✅ I have reviewed my answers and "
                            "I am ready to submit the test.",
                            key="confirm_test_submission"
                        )
                        # ------------------------------------------
                        # SUBMIT TEST
                        # ------------------------------------------

                        if st.button(
                                "🏆 Submit Test",
                                type="primary",
                                key="submit_test_button"
                        ):

                            if not confirm_submit:

                                st.warning(
                                    "⚠️ Please confirm that you have "
                                    "reviewed your answers before submitting."
                                )

                            else:

                                unanswered = []

                                for i in range(total_questions):

                                    if i not in st.session_state.answers:
                                        unanswered.append(i + 1)

                                if unanswered:

                                    question_numbers = ", ".join(
                                        [f"Q{x}" for x in unanswered]
                                    )

                                    st.warning(
                                        f"⚠️ You still have "
                                        f"{len(unanswered)} unanswered "
                                        f"question(s): {question_numbers}"
                                    )

                                else:

                                    # Calculate score
                                    score = 0

                                    for i, q in enumerate(db_questions):

                                        correct_answer = q[6]

                                        if (
                                                st.session_state.answers.get(i)
                                                == correct_answer
                                        ):
                                            score += 1

                                    percentage = (
                                                         score / total_questions
                                                 ) * 100

                                    # Save result
                                    save_result(
                                        st.session_state.username,
                                        test_category,
                                        score,
                                        total_questions,
                                        percentage
                                    )

                                    # Store result
                                    st.session_state.test_score = score
                                    st.session_state.test_total = total_questions
                                    st.session_state.test_finished = True
                                    st.session_state.test_started = False
                                    st.session_state.test_start_time = None

                                    st.rerun()

            # ------------------------------------------
            # TEST RESULT
            # ------------------------------------------

            if st.session_state.get(
                    "test_finished",
                    False
            ):

                score = st.session_state.test_score
                total = st.session_state.test_total

                percentage = (
                                     score / total
                             ) * 100

                # ------------------------------------------
                # PERFORMANCE LEVEL
                # ------------------------------------------

                if percentage >= 90:

                    performance_level = "🏆 Outstanding"

                elif percentage >= 80:

                    performance_level = "🌟 Excellent"

                elif percentage >= 60:

                    performance_level = "👍 Good"

                elif percentage >= 40:

                    performance_level = "📚 Needs Improvement"

                else:

                    performance_level = "💪 Keep Practicing"

                st.success(
                    "🎉 Test Completed!"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "🏆 Your Score",
                        f"{score} / {total}"
                    )

                with col2:

                    st.metric(
                        "📊 Percentage",
                        f"{percentage:.1f}%"
                    )

                with col3:

                    st.metric(
                        "🎯 Performance",
                        performance_level
                    )

                if percentage >= 80:

                    st.balloons()

                    st.success(
                        "🌟 Excellent performance!"
                    )

                elif percentage >= 50:

                    st.info(
                        "👍 Good job! Keep improving."
                    )

                else:

                    st.warning(
                        "💪 Keep practicing and try again!"
                    )

                if st.button(
                        "🔄 Take Another Test"
                ):
                    st.session_state.test_finished = False
                    st.session_state.current_question = 0
                    st.session_state.answers = {}

                    st.rerun()

        # Subject selection

    # --------------------------------------------------
    # MY RESULTS
    # --------------------------------------------------

    elif menu == "📊 My Results":

        st.title(" 📊 MY RESULT")

        results = get_results(
            st.session_state.username
        )

        if not results:

            st.info(
                "📝 You have not completed any tests yet."
            )

        else:

            # ------------------------------------------
            # SUMMARY CALCULATIONS
            # ------------------------------------------

            total_tests = len(results)

            percentages = [
                result[3]
                for result in results
            ]

            average_percentage = (
                    sum(percentages) / total_tests
            )

            best_percentage = max(
                percentages
            )

            total_questions = sum(
                result[2]
                for result in results
            )

            total_correct = sum(
                result[1]
                for result in results
            )

            # ------------------------------------------
            # SUMMARY CARDS
            # ------------------------------------------

            st.subheader(
                "🏆 Performance Summary"
            )

            col1, col2, col3, col4 = st.columns(
                [1, 1, 1.1, 1.1]
            )

            with col1:

                st.metric(
                    "📝 Tests Taken",
                    total_tests
                )

            with col2:

                st.metric(
                    "🏆 Best Score",
                    f"{best_percentage:.1f}%"
                )

            with col3:

                st.metric(
                    "📊 Average Score",
                    f"{average_percentage:.1f}%"
                )

            with col4:

                st.metric(
                    "✅ Correct Answers",
                    total_correct
                )

            st.divider()

            # ------------------------------------------
            # PERFORMANCE MESSAGE
            # ------------------------------------------

            if average_percentage >= 80:

                st.success(
                    "🌟 Excellent! Your overall "
                    "performance is outstanding."
                )

            elif average_percentage >= 60:

                st.info(
                    "👍 Good performance! "
                    "Keep practicing to improve further."
                )

            elif average_percentage >= 40:

                st.warning(
                    "💪 You're making progress. "
                    "More practice will help."
                )

            else:

                st.warning(
                    "📚 Keep practicing regularly "
                    "to improve your score."
                )

            # ------------------------------------------
            # RESULT HISTORY
            # ------------------------------------------

            st.subheader(
                "📋 Test History"
            )

            for result in results:
                category = result[0]
                score = result[1]
                total = result[2]
                percentage = result[3]
                test_date = result[4]

                with st.expander(
                        f"📚 {category}  |  "
                        f"🏆 {score}/{total}  |  "
                        f"📊 {percentage:.1f}%"
                ):

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.markdown(
                            f"""
                            **📚 Subject**

                            {category}
                            """
                        )

                    with col2:
                        st.markdown(
                            f"""
                            **🏆 Score**

                            {score}/{total}
                            """
                        )

                    with col3:
                        st.markdown(
                            f"""
                            **📅 Date**

                            {test_date}
                            """
                        )

                    st.progress(
                        min(
                            percentage / 100,
                            1.0
                        )
                    )

                    st.caption(
                        f"Your score: {percentage:.1f}%"
                    )

                    # ------------------------------------------
                    # SUBJECT-WISE PERFORMANCE
                    # ------------------------------------------

                    st.divider()

                    st.subheader(
                        "📈 Subject-Wise Performance"
                    )

                    subject_scores = {}

                    for result in results:

                        category = result[0]
                        percentage = result[3]

                        if category in subject_scores:

                            subject_scores[category].append(
                                percentage
                            )

                        else:

                            subject_scores[category] = [
                                percentage
                            ]

                    subject_average = {}

                    for subject, scores in subject_scores.items():
                        subject_average[subject] = (
                                sum(scores) / len(scores)
                        )

                    for subject, average in subject_average.items():

                        st.markdown(
                            f"""
                            <div class="subject-performance">
                                <div class="subject-performance-name">
                                    📚 {subject}
                                </div>
                                <div class="subject-performance-score">
                                    {average:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        st.progress(
                            min(average / 100, 1.0)
                        )
    # --------------------------------------------------
    # ADMIN
    # --------------------------------------------------

    elif menu == "🔐 Admin":

        st.title("🔐 Admin Panel")

        if not st.session_state.admin_logged_in:

            st.subheader("Admin Login")

            admin_username = st.text_input(
                "Admin Username"
            )

            admin_password = st.text_input(
                "Admin Password",
                type="password"
            )

            if st.button(
                    "🔑 Admin Login",
                    type="primary"
            ):

                if (
                        admin_username == ADMIN_USERNAME
                        and
                        admin_password == ADMIN_PASSWORD
                ):

                    st.session_state.admin_logged_in = True

                    st.success(
                        "Admin login successful! ✅"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid admin username or password ❌"
                    )

        else:

            st.success("Admin logged in successfully! 👨‍💼")

            admin_menu = st.radio(
                "Admin Menu",
                [
                    "📊 Dashboard",
                    "➕ Add Question",
                    "📚 Question Bank",
                    "✏️ Edit Question",
                    "👥 Users",
                    "🗑️ Delete Question"
                ]
                ,
                horizontal=True
            )
            # ------------------------------------------
            # ADMIN DASHBOARD
            # ------------------------------------------

            if admin_menu == "📊 Dashboard":
                st.subheader("📊 Admin Dashboard")

                # Get statistics
                total_users = get_total_users()
                total_questions = get_total_questions()
                total_tests = get_total_tests()
                average_score = get_average_score()

                # Dashboard cards
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "👥 Total Users",
                        total_users
                    )

                with col2:
                    st.metric(
                        "❓ Total Questions",
                        total_questions
                    )

                with col3:
                    st.metric(
                        "📝 Tests Taken",
                        total_tests
                    )

                with col4:
                    st.metric(
                        "📊 Average Score",
                        f"{average_score:.1f}%"
                    )

                st.divider()

                st.info(
                    "💡 These statistics are automatically "
                    "calculated from the BrainBoost database."
                )

                st.divider()

                st.subheader("📈 User Performance")

                all_results = get_all_results()

                if not all_results:

                    st.info("No tests have been completed yet.")

                else:

                    for result in all_results:
                        username = result[0]
                        category = result[1]
                        score = result[2]
                        total = result[3]
                        percentage = result[4]
                        test_date = result[5]

                        with st.container():
                            col1, col2, col3, col4, col5 = st.columns(5)

                            with col1:
                                st.write(f"👤 **{username}**")

                            with col2:
                                st.write(f"📚 {category}")

                            with col3:
                                st.write(f"🏆 {score}/{total}")

                            with col4:
                                st.write(f"📊 {percentage:.1f}%")

                            with col5:
                                st.write(f"📅 {test_date}")

                            st.divider()

            # ------------------------------------------
            # ADD QUESTION
            # ------------------------------------------

            if admin_menu == "➕ Add Question":

                st.subheader("➕ Add New Question")

                category = st.selectbox(
                    "Select Subject",
                    [
                        "Maths",
                        "Science",
                        "Computer",
                        "Environment",
                        "General Knowledge"
                    ]
                )

                question = st.text_area(
                    "Question"
                )

                col1, col2 = st.columns(2)

                with col1:

                    option1 = st.text_input(
                        "Option 1"
                    )

                    option2 = st.text_input(
                        "Option 2"
                    )

                with col2:

                    option3 = st.text_input(
                        "Option 3"
                    )

                    option4 = st.text_input(
                        "Option 4"
                    )

                answer = st.selectbox(
                    "Correct Answer",
                    [
                        option1,
                        option2,
                        option3,
                        option4
                    ]
                )

                if st.button(
                        "➕ Add Question",
                        type="primary"
                ):

                    if not question:

                        st.warning(
                            "Please enter a question."
                        )

                    elif not option1 or not option2 or not option3 or not option4:

                        st.warning(
                            "Please fill all four options."
                        )

                    else:

                        add_question(
                            category,
                            question,
                            option1,
                            option2,
                            option3,
                            option4,
                            answer
                        )

                        st.success(
                            "Question added successfully! ✅"
                        )

            # ------------------------------------------
            # QUESTION BANK
            # ------------------------------------------

            elif admin_menu == "📚 Question Bank":

                st.subheader("📚 Question Bank")

                questions = get_all_questions()

                # ------------------------------------------
                # SEARCH AND FILTER
                # ------------------------------------------

                col1, col2 = st.columns(2)

                with col1:

                    search_text = st.text_input(
                        "🔍 Search Question",
                        placeholder="Type a question...",
                        key="question_search"
                    )

                with col2:

                    category_filter = st.selectbox(
                        "📚 Filter by Category",
                        [
                            "All",
                            "Maths",
                            "Science",
                            "Computer",
                            "Environment",
                            "General Knowledge"
                        ],
                        key="question_category_filter"
                    )

                    # ------------------------------------------
                    # APPLY FILTERS
                    # ------------------------------------------

                    filtered_questions = questions

                    if category_filter != "All":
                        filtered_questions = [
                            q for q in filtered_questions
                            if q[1] == category_filter
                        ]

                    if search_text.strip():
                        search_lower = search_text.lower()

                        filtered_questions = [
                            q for q in filtered_questions
                            if search_lower in q[2].lower()
                        ]

                        st.divider()

                        if not filtered_questions:

                            st.info(
                                "🔎 No questions found matching your search."
                            )

                        else:

                            st.write(
                                f"Showing **{len(filtered_questions)}** "
                                f"question(s)"
                            )

                            for q in filtered_questions:
                                question_id = q[0]
                                category = q[1]
                                question = q[2]
                                option1 = q[3]
                                option2 = q[4]
                                option3 = q[5]
                                option4 = q[6]
                                answer = q[7]

                                with st.expander(
                                        f"Q{question_id} — {category} — {question}"
                                ):
                                    st.write(
                                        f"**Question:** {question}"
                                    )

                                    st.write(
                                        f"**A.** {option1}"
                                    )

                                    st.write(
                                        f"**B.** {option2}"
                                    )

                                    st.write(
                                        f"**C.** {option3}"
                                    )

                                    st.write(
                                        f"**D.** {option4}"
                                    )

                                    st.success(
                                        f"✅ Correct Answer: {answer}"
                                    )
                if not questions:

                    st.info(
                        "No questions have been added yet."
                    )

                else:

                    st.write(
                        f"Total Questions: **{len(questions)}**"
                    )

                    for q in questions:
                        question_id = q[0]
                        category = q[1]
                        question_text = q[2]
                        option1 = q[3]
                        option2 = q[4]
                        option3 = q[5]
                        option4 = q[6]
                        answer = q[7]

                        with st.expander(
                                f"#{question_id} | {category} | {question_text}"
                        ):
                            st.write(
                                f"**Question:** {question_text}"
                            )

                            st.write(
                                f"1️⃣ {option1}"
                            )

                            st.write(
                                f"2️⃣ {option2}"
                            )

                            st.write(
                                f"3️⃣ {option3}"
                            )

                            st.write(
                                f"4️⃣ {option4}"
                            )

                            st.success(
                                f"Correct Answer: {answer}"
                            )

            elif admin_menu == "✏️ Edit Question":

                st.subheader("✏️ Edit Question")

                questions = get_all_questions()

                if not questions:

                    st.info("❓ No questions available to edit.")

                else:

                    question_options = {}

                    for q in questions:
                        question_id = q[0]
                        question_text = q[2]

                        question_options[
                            f"Q{question_id}: {question_text}"
                        ] = question_id

                    selected_question = st.selectbox(
                        "Select Question",
                        list(question_options.keys()),
                        key="edit_question_select"
                    )

                    selected_id = question_options[
                        selected_question
                    ]

                    selected_data = None

                    for q in questions:

                        if q[0] == selected_id:
                            selected_data = q
                            break

                    if selected_data:

                        question_id = selected_data[0]
                        category = selected_data[1]
                        question = selected_data[2]
                        option1 = selected_data[3]
                        option2 = selected_data[4]
                        option3 = selected_data[5]
                        option4 = selected_data[6]
                        answer = selected_data[7]

                        edit_category = st.selectbox(
                            "📚 Category",
                            [
                                "Maths",
                                "Science",
                                "Computer",
                                "Environment",
                                "General Knowledge"
                            ],
                            index=[
                                "Maths",
                                "Science",
                                "Computer",
                                "Environment",
                                "General Knowledge"
                            ].index(category)
                            if category in [
                                "Maths",
                                "Science",
                                "Computer",
                                "Environment",
                                "General Knowledge"
                            ]
                            else 0
                        )

                        edit_question = st.text_area(
                            "🧠 Question",
                            value=question,
                            key="edit_question_text"
                        )

                        edit_option1 = st.text_input(
                            "Option 1",
                            value=option1,
                            key="edit_option1"
                        )

                        edit_option2 = st.text_input(
                            "Option 2",
                            value=option2,
                            key="edit_option2"
                        )

                        edit_option3 = st.text_input(
                            "Option 3",
                            value=option3,
                            key="edit_option3"
                        )

                        edit_option4 = st.text_input(
                            "Option 4",
                            value=option4,
                            key="edit_option4"
                        )

                        edit_answer = st.selectbox(
                            "✅ Correct Answer",
                            [
                                edit_option1,
                                edit_option2,
                                edit_option3,
                                edit_option4
                            ],
                            index=[
                                edit_option1,
                                edit_option2,
                                edit_option3,
                                edit_option4
                            ].index(answer)
                            if answer in [
                                edit_option1,
                                edit_option2,
                                edit_option3,
                                edit_option4
                            ]
                            else 0,
                            key="edit_answer"
                        )

                        if st.button(
                                "💾 Update Question",
                                type="primary",
                                key="update_question_button"
                        ):

                            if not edit_question.strip():

                                st.warning(
                                    "⚠️ Question cannot be empty."
                                )

                            else:

                                update_question(
                                    question_id,
                                    edit_category,
                                    edit_question,
                                    edit_option1,
                                    edit_option2,
                                    edit_option3,
                                    edit_option4,
                                    edit_answer
                                )

                                st.success(
                                    "✅ Question updated successfully!"
                                )

                                st.rerun()

            elif admin_menu == "👥 Users":

                st.subheader("👥 User Management")

                users = get_all_users()

                # --------------------------------------
                # SEARCH USERS
                # --------------------------------------

                search_user = st.text_input(
                    "🔍 Search User",
                    placeholder="Search by name or username...",
                    key="admin_user_search"
                )

                if search_user.strip():
                    search_lower = search_user.lower()

                    users = [
                        user
                        for user in users
                        if search_lower in user[1].lower()
                           or search_lower in user[2].lower()
                    ]

                    if users:
                        st.caption(
                            f"👥 Showing {len(users)} user(s)"
                        )

                if not users:

                    st.info(
                        "👤 No users have registered yet."
                    )

                else:

                    st.write(
                        f"Total registered users: "
                        f"**{len(users)}**"
                    )

                    # --------------------------------------
                    # SELECT USER
                    # --------------------------------------

                    user_options = {}

                    for user in users:
                        user_id = user[0]
                        name = user[1]
                        username = user[2]

                        user_options[
                            f"{name} ({username})"
                        ] = username

                    selected_user = st.selectbox(
                        "👤 Select User",
                        list(user_options.keys()),
                        key="admin_user_select"
                    )

                    selected_username = user_options[
                        selected_user
                    ]

                    # --------------------------------------
                    # USER DETAILS
                    # --------------------------------------

                    selected_user_data = None

                    for user in users:

                        if user[2] == selected_username:
                            selected_user_data = user
                            break

                    if selected_user_data:

                        user_id = selected_user_data[0]
                        name = selected_user_data[1]
                        username = selected_user_data[2]

                        st.divider()

                        st.subheader(
                            "👤 User Details"
                        )

                        col1, col2, col3 = st.columns(3)

                        with col1:

                            st.metric(
                                "🆔 User ID",
                                user_id
                            )

                        with col2:

                            st.metric(
                                "👤 Name",
                                name
                            )

                        with col3:

                            st.metric(
                                "🔑 Username",
                                username
                            )

                        # ----------------------------------
                        # USER RESULTS
                        # ----------------------------------

                        user_results = get_user_results(
                            selected_username
                        )

                        st.divider()

                        st.subheader(
                            "📊 User Performance"
                        )

                        if not user_results:

                            st.info(
                                "📝 This user has not "
                                "completed any tests yet."
                            )

                        else:

                            total_tests = len(
                                user_results
                            )

                            percentages = [
                                result[3]
                                for result in user_results
                            ]

                            average_score = (
                                    sum(percentages)
                                    / total_tests
                            )

                            best_score = max(
                                percentages
                            )

                            col1, col2, col3 = st.columns(3)

                            with col1:

                                st.metric(
                                    "📝 Tests Taken",
                                    total_tests
                                )

                            with col2:

                                st.metric(
                                    "📊 Average Score",
                                    f"{average_score:.1f}%"
                                )

                            with col3:

                                st.metric(
                                    "🏆 Best Score",
                                    f"{best_score:.1f}%"
                                )

                            # ----------------------------------
                            # TEST HISTORY
                            # ----------------------------------

                            st.subheader(
                                "📋 Test History"
                            )

                            for result in user_results:
                                category = result[0]
                                score = result[1]
                                total = result[2]
                                percentage = result[3]
                                test_date = result[4]

                                with st.expander(
                                        f"📚 {category} | "
                                        f"🏆 {score}/{total} | "
                                        f"📊 {percentage:.1f}%"
                                ):
                                    st.write(
                                        f"**Subject:** {category}"
                                    )

                                    st.write(
                                        f"**Score:** "
                                        f"{score}/{total}"
                                    )

                                    st.write(
                                        f"**Percentage:** "
                                        f"{percentage:.1f}%"
                                    )

                                    st.write(
                                        f"**Date:** {test_date}"
                                    )

                                    st.progress(
                                        min(
                                            percentage / 100,
                                            1.0
                                        )
                                    )
            # ------------------------------------------
            # DELETE QUESTION
            # ------------------------------------------

            elif admin_menu == "🗑️ Delete Question":

                st.subheader("🗑️ Delete Question")

                questions = get_all_questions()

                if not questions:

                    st.info(
                        "No questions available."
                    )

                else:

                    question_options = {
                        f"#{q[0]} | {q[1]} | {q[2]}":
                            q[0]
                        for q in questions
                    }

                    selected_question = st.selectbox(
                        "Select Question",
                        list(question_options.keys())
                    )

                    question_id = question_options[
                        selected_question
                    ]

                    if st.button(
                            "🗑️ Delete Question",
                            type="primary"
                    ):
                        delete_question(
                            question_id
                        )

                        st.success(
                            "Question deleted successfully! ✅"
                        )

                        st.rerun()

            if st.button("🚪 Logout Admin"):
                st.session_state.admin_logged_in = False

                st.rerun()
    # --------------------------------------------------
    # ABOUT / INFO
    # --------------------------------------------------

    elif menu == "ℹ️ About / Info":

        # --------------------------------------------------
        # INFO PAGE HERO
        # --------------------------------------------------

            st.markdown(
                """<div class="info-hero">
        <div class="info-hero-icon">🧠 ⚡</div>
        <div class="info-hero-title">BrainBoost IQ Test</div>
        <div class="info-hero-tagline">Think • Challenge • Improve</div>
        <div class="info-hero-description">Challenge your knowledge, test your thinking and keep improving with BrainBoost.</div>
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - WHAT IS BRAINBOOST
        # --------------------------------------------------

            st.markdown(
                """<div class="info-about">
        <div class="info-about-title">🎯 What is BrainBoost?</div>
        <div class="info-about-text">BrainBoost IQ Test is a student-developed educational web application designed to make learning more interactive and enjoyable. It allows users to test their knowledge, challenge themselves and track their progress across different subjects.</div>
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - FEATURES
        # --------------------------------------------------

            st.markdown(
                """<div class="info-features-title">✨ What You Can Do</div>
        <div class="info-features">
        <div class="info-feature-card">
        <div class="info-feature-icon">🧩</div>
        <div class="info-feature-title">Choose Subjects</div>
        <div class="info-feature-text">Test yourself across different subjects.</div>
        </div>
        <div class="info-feature-card">
        <div class="info-feature-icon">📊</div>
        <div class="info-feature-title">Track Progress</div>
        <div class="info-feature-text">See your performance and improvement.</div>
        </div>
        <div class="info-feature-card">
        <div class="info-feature-icon">🏆</div>
        <div class="info-feature-title">View Results</div>
        <div class="info-feature-text">Check your scores after every test.</div>
        </div>
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - AVAILABLE SUBJECTS
        # --------------------------------------------------

            st.markdown(
                """<div class="info-subjects-title">📚 Available Subjects</div>
        <div class="info-subjects">
        <div class="info-subject-card"><span>🧮</span><b>Mathematics</b></div>
        <div class="info-subject-card"><span>🔬</span><b>Science</b></div>
        <div class="info-subject-card"><span>💻</span><b>Computer</b></div>
        <div class="info-subject-card"><span>🌱</span><b>Environment</b></div>
        <div class="info-subject-card"><span>🌎</span><b>General Knowledge</b></div>
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - HOW IT WORKS
        # --------------------------------------------------

            st.markdown(
                """<div class="info-how-title">🚀 How BrainBoost Works</div>
        <div class="info-how">
        <div class="info-how-step">
        <div class="info-how-number">1</div>
        <div class="info-how-icon">📚</div>
        <div class="info-how-name">Choose</div>
        <div class="info-how-text">Select a subject you want to test.</div>
        </div>
        <div class="info-how-arrow">→</div>
        <div class="info-how-step">
        <div class="info-how-number">2</div>
        <div class="info-how-icon">🧠</div>
        <div class="info-how-name">Challenge</div>
        <div class="info-how-text">Answer questions and challenge yourself.</div>
        </div>
        <div class="info-how-arrow">→</div>
        <div class="info-how-step">
        <div class="info-how-number">3</div>
        <div class="info-how-icon">📊</div>
        <div class="info-how-name">Improve</div>
        <div class="info-how-text">Check your results and track progress.</div>
        </div>
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - QUOTE & FOOTER
        # --------------------------------------------------

            st.markdown(
                """<div class="info-quote">
        <div class="info-quote-icon">💡</div>
        <div class="info-quote-text">“Every question is a chance to learn something new.”</div>
        <div class="info-quote-subtext">Keep learning. Keep challenging yourself.</div>
        </div>
        <div class="info-footer">
        Made with ❤️ using Python & Streamlit
        </div>""",
                unsafe_allow_html=True
            )

        # --------------------------------------------------
        # INFO PAGE - TECHNOLOGIES & CREATOR
        # --------------------------------------------------

            st.markdown(
                """<div class="info-tech-title">🛠️ Technologies Used</div>
            <div class="info-tech">
            <div class="info-tech-card">
            <div class="info-tech-icon">🐍</div>
            <div class="info-tech-name">Python</div>
            </div>
            <div class="info-tech-card">
            <div class="info-tech-icon">🎈</div>
            <div class="info-tech-name">Streamlit</div>
            </div>
            <div class="info-tech-card">
            <div class="info-tech-icon">🗄️</div>
            <div class="info-tech-name">SQLite</div>
            </div>
            <div class="info-tech-card">
            <div class="info-tech-icon">🎨</div>
            <div class="info-tech-name">CSS</div>
            </div>
            </div>
            <div class="info-creator">
            <div class="info-creator-divider">
            <span>💎💎💎</span>©️
            <span>💎💎💎</span>
            </div>
            <div class="info-creator-text">Created by</div>
            <div class="info-creator-name">SPARK ⚡</div>
            </div>""",
                unsafe_allow_html=True
            )