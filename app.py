# app.py
import streamlit as st
import os
import sys
from io import StringIO
from contextlib import redirect_stdout

# Link the app to the engine we just built!
sys.path.append(os.path.abspath('./src'))
from vision_parser import get_spice_netlist # type: ignore
from spice_solver import solve_netlist # type: ignore

# 1. App Styling and Layout
st.set_page_config(page_title="Circuit Master Pro", page_icon="⚡", layout="centered")

st.title("⚡ Circuit Master Pro")
st.markdown("Your personal Nilsson & Riedel solving engine and practice platform.")

# 2. Create the "Mastering" Tabs
tab1, tab2 = st.tabs(["📸 Instant Circuit Solver", "📝 Practice MCQs"])

# --- TAB 1: THE SOLVER ---
with tab1:
    st.header("Upload a Circuit")
    st.write("Paste or upload a screenshot from the textbook.")
    
    # Drag and drop file uploader
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Show the image on the screen cleanly
        st.image(uploaded_file, use_column_width=True)
        
        # The big solve button
        if st.button("🧠 Solve Circuit", use_container_width=True):
            with st.spinner("Claude is analyzing the diagram and extracting the netlist..."):
                
                # Save the image temporarily for Claude to read
                temp_path = "data/temp_ui_upload.png"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Run your AI Engine
                netlist = get_spice_netlist(temp_path)
                
            with st.spinner("Ngspice Physics Engine is verifying the math..."):
                # Run your Math Engine (and quietly capture the terminal output)
                f = StringIO()
                with redirect_stdout(f):
                    solve_netlist(netlist)
                
                # Clean up the output to look nice on the website
                results = f.getvalue().split("--- 100% ACCURATE NODE VOLTAGES ---")[-1].strip()
                
            # Display the final answers in a beautiful green box
            st.success("Analysis Complete!")
            st.subheader("Calculated Node Voltages:")
            st.code(results, language="text")
            
            # Hide the raw SPICE code in a dropdown so the UI stays clean
            with st.expander("View Raw SPICE Netlist"):
                st.code(netlist, language="spice")

# --- TAB 2: THE MCQ SECTION ---
with tab2:
    st.header("Chapter 3/4 Assessment Practice")
    st.write("Test your knowledge. The engine will verify your logic.")
    st.divider()
    
    # 1. Your Question Bank (Add as many as you want here!)
    mcq_database = [
        {
            "question": "If a 20A current source is split in parallel between a 60Ω, 40Ω, and 80Ω resistor, what is the voltage at the top node?",
            "options": ["100.0 V", "133.3 V", "200.0 V", "240.0 V"],
            "answer": "200.0 V",
            "explanation": "The equivalent resistance is 10Ω. Using Ohm's Law (V = IR), V = 20A * 10Ω = 200V."
        },
        {
            "question": "In Node-Voltage analysis, what happens if an independent voltage source is connected directly between a non-reference node and ground?",
            "options": ["It creates a supernode.", "KCL fails at that node.", "The node voltage is known immediately.", "You must use mesh-current analysis instead."],
            "answer": "The node voltage is known immediately.",
            "explanation": "Because the source is tied directly to the 0V reference, that node's voltage is locked to the value of the source."
        },
        {
            "question": "To find the Norton equivalent current (IN) of a circuit, you must...",
            "options": ["Find the open-circuit voltage.", "Find the short-circuit current.", "Turn off all independent sources.", "Calculate the Thevenin voltage first."],
            "answer": "Find the short-circuit current.",
            "explanation": "Norton current is defined as the current flowing through a short circuit placed across the load terminals."
        },
        {
            "question": "If three 30Ω resistors are in a Delta (Δ) configuration, what is the value of each resistor in the equivalent Wye (Y) configuration?",
            "options": ["10Ω", "30Ω", "90Ω", "5Ω"],
            "answer": "10Ω",
            "explanation": "When converting a balanced Delta to a Wye, the formula is R_y = R_delta / 3."
        }
    ]

    # 2. Automatically generate the UI for every question
    for i, q in enumerate(mcq_database):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        
        # Give each radio button a unique key so Streamlit doesn't get confused
        user_choice = st.radio(
            "Select your answer:", 
            q["options"], 
            index=None, 
            key=f"q{i}",
            label_visibility="collapsed"
        )
        
        if st.button(f"Check Answer for Q{i+1}", key=f"btn{i}"):
            if user_choice == q["answer"]:
                st.success(f"✅ Correct! {q['explanation']}")
            elif user_choice is None:
                st.warning("Please select an answer first.")
            else:
                st.error("❌ Incorrect. Try again.")
        st.divider()