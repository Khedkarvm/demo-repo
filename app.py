import streamlit as st
from nl_to_sql import run_question

st.set_page_config(page_title="NL-to-SQL Chat", layout="wide")

st.title("Natural Language to SQL")

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# Sidebar
st.sidebar.header("Query History")

if st.session_state.history:
    for idx, item in enumerate(st.session_state.history):
        if st.sidebar.button(item["question"], key=f"hist_{idx}"):
            st.session_state.selected_index = idx
else:
    st.sidebar.info("No queries yet")

# Input
question = st.text_input("Ask a Northwind question (NL → SQL):")

# Submit Button
if st.button("Submit"):
    if question.strip():
        with st.spinner("Generating SQL and querying database..."):
            df, sql = run_question(question)

        st.session_state.history.append({
            "question": question,
            "df": df,
            "sql": sql
        })

        st.session_state.selected_index = len(st.session_state.history) - 1

    else:
        st.warning("Please enter a question")

# Display Selected Query
if st.session_state.selected_index is not None:

    item = st.session_state.history[st.session_state.selected_index]

    st.markdown("---")
    st.header("Selected Query")

    st.markdown(f"**Question:** {item['question']}")

    st.subheader("Generated SQL")
    st.code(item["sql"], language="sql")

    if "error" in item["df"].columns:
        st.warning(item["df"].iloc[0]["error"])
    else:
        st.success("Query executed successfully")

        # Bigger dataframe
        st.dataframe(
            item["df"],
            use_container_width=True,
            height=500
        )