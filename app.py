# app.py

import streamlit as st
from agents import (
    resume_analyzer,
    career_decision_agent,
    roadmap_planner,
    feedback_agent,
    career_readiness_score
)

st.set_page_config(page_title="Agentic AI – Career Mentor")

st.title("🧠 Agentic AI – Career Mentor")

resume_text = st.text_area("📄 Paste your resume here")

if st.button("Analyze Career"):
    profile = resume_analyzer(resume_text)

    role, scores, missing = career_decision_agent(profile)
    roadmap = roadmap_planner(role, missing)
    score = career_readiness_score(scores, role)

    st.session_state["roadmap"] = roadmap

    st.subheader("👤 Extracted Profile")
    st.json(profile)

    st.subheader("🎯 Recommended Career")
    st.write(role)

    st.subheader("📊 Career Match Scores (%)")
    st.json(scores)

    st.subheader("📈 Career Readiness")
    st.progress(score / 100)
    st.write(f"{score}% ready")

    st.subheader("❗ Missing Skills")
    if missing:
        st.write(missing)
    else:
        st.success("All core skills matched")

    st.subheader("🛣️ Career Roadmap")
    st.text(roadmap)


if "roadmap" in st.session_state:
    st.subheader("🔁 Provide Feedback")

    col1, col2 = st.columns(2)

    if col1.button("❌ Rejected"):
        st.text(feedback_agent("Rejected", st.session_state["roadmap"]))

    if col2.button("🎯 Interview"):
        st.text(feedback_agent("Interview", st.session_state["roadmap"]))

