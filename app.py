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

# --- UI LAYOUT ARCHITECTURE ---
    
    # 1. Create 11 distinct tabs
    tab_ch1, tab_ch2, tab_ch3, tab_ch4, tab_ch5, tab_ch6, tab_ch7, tab_ch8, tab_ch9, tab_ch10 = st.tabs([ 
        "Ch 1", "Ch 2", "Ch 3", "Ch 4", "Ch 5", 
        "Ch 6", "Ch 7", "Ch 8", "Ch 9", "Ch 10"
    ])


    # 3. Chapter 1 Practice Tab
    with tab_ch1:
        st.header("Chapter 1: Circuit Variables")
        
        # Paste your massive 100-question chunk here!
        mcq_database_ch1 = [
                    {
            "question": "What is the SI base unit for electrical charge, and how is it related to the electron?",
            "options": ["Ampere; 1 A = 1.602e-19 electrons", "Coulomb; 1 C = 6.24e18 electrons", "Joule; 1 J = 6.24e18 electrons", "Volt; 1 V = 1.602e-19 electrons"],
            "answer": "Coulomb; 1 C = 6.24e18 electrons",
            "explanation": "Charge is measured in Coulombs (C). One electron has a charge of -1.602 x 10^-19 C, meaning it takes roughly 6.24 x 10^18 electrons to make up -1 C of charge."
        },
        {
            "question": "Current is mathematically defined as the rate of charge flow. If q(t) = 4t^2 + 2t (mC), what is the current at t = 3 seconds?",
            "options": ["26 mA", "14 mA", "38 mA", "42 mA"],
            "answer": "26 mA",
            "explanation": "Current i = dq/dt. The derivative of 4t^2 + 2t is 8t + 2. Plugging in t = 3 yields 8(3) + 2 = 26 mA."
        },
        {
            "question": "How is electrical voltage fundamentally defined in circuit theory?",
            "options": ["The rate of charge flow past a given point.", "The energy required to move a unit charge through an element.", "The opposition to the flow of current.", "The total power dissipated by a component."],
            "answer": "The energy required to move a unit charge through an element.",
            "explanation": "Voltage (v) is the change in energy (dw) per unit of charge (dq). Mathematically, v = dw/dq. 1 Volt = 1 Joule / 1 Coulomb."
        },
        {
            "question": "Under the Passive Sign Convention, if current enters the POSITIVE voltage terminal of an element, the power equation is p = vi. What does a POSITIVE calculated power mean?",
            "options": ["The element is absorbing (dissipating) power.", "The element is supplying (generating) power.", "The circuit violates the conservation of energy.", "The element must be an ideal voltage source."],
            "answer": "The element is absorbing (dissipating) power.",
            "explanation": "When current enters the positive terminal (passive sign convention), a positive result for p = vi means the element is acting as a load and absorbing power."
        },
        {
            "question": "An element has a voltage drop of v = -12 V (top to bottom) and a current of i = 3 A entering the top terminal. How much power is being absorbed or supplied?",
            "options": ["36 W absorbed", "36 W supplied", "4 W absorbed", "4 W supplied"],
            "answer": "36 W supplied",
            "explanation": "Using the passive sign convention (current entering the top terminal): p = vi = (-12 V)(3 A) = -36 W. A negative absorbed power means it is supplying 36 W to the rest of the circuit."
        },
        {
            "question": "A 12V car battery supplies a constant current of 50A to a starter motor for 3 seconds. How much energy is transferred?",
            "options": ["600 J", "1800 J", "50 J", "150 J"],
            "answer": "1800 J",
            "explanation": "First find power: P = vi = (12V)(50A) = 600W. Energy (W) is power multiplied by time (for constant power). W = (600 W)(3 s) = 1800 Joules."
        },
        {
            "question": "What is the defining characteristic of an ideal independent voltage source?",
            "options": ["It supplies a constant current regardless of the voltage across it.", "It maintains a specified voltage across its terminals regardless of the current flowing through it.", "It always supplies power to the circuit.", "Its voltage output depends on a current elsewhere in the circuit."],
            "answer": "It maintains a specified voltage across its terminals regardless of the current flowing through it.",
            "explanation": "An ideal voltage source locks the voltage difference between its terminals to a specific value. It will supply or absorb whatever current is necessary to maintain that voltage."
        },
        {
            "question": "Which of the following circuit connections is fundamentally INVALID and impossible in ideal circuit theory?",
            "options": ["Two different ideal resistors in parallel.", "Two different ideal current sources in parallel.", "Two different ideal voltage sources in parallel.", "An ideal voltage source in parallel with an ideal current source."],
            "answer": "Two different ideal voltage sources in parallel.",
            "explanation": "Components in parallel must share the exact same voltage. If you place a 5V ideal source and a 10V ideal source in parallel, they contradict each other, violating KVL."
        },
        {
            "question": "Which of the following circuit connections is fundamentally INVALID and impossible in ideal circuit theory?",
            "options": ["Two different ideal current sources in series.", "Two identical ideal voltage sources in series.", "An ideal current source in series with a resistor.", "An ideal voltage source in series with an ideal current source."],
            "answer": "Two different ideal current sources in series.",
            "explanation": "Components in series must share the exact same current. A 2A ideal source and a 5A ideal source in the same branch contradict each other, violating KCL."
        },
        {
            "question": "A dependent source outputs a voltage based on the formula v_s = 4 * i_x, where i_x is the current through another resistor. What type of source is this?",
            "options": ["Voltage-Controlled Voltage Source (VCVS)", "Current-Controlled Voltage Source (CCVS)", "Voltage-Controlled Current Source (VCCS)", "Current-Controlled Current Source (CCCS)"],
            "answer": "Current-Controlled Voltage Source (CCVS)",
            "explanation": "The source outputs a voltage (so it's a Voltage Source), and its controlling variable is a current (i_x). Therefore, it is a CCVS."
        },
        {
            "question": "The Law of Conservation of Energy dictates that in any closed electrical circuit...",
            "options": ["The sum of all voltages must be zero.", "The algebraic sum of all power (absorbed and supplied) at any instant must equal zero.", "Total current supplied must be greater than total current absorbed.", "Only independent sources can supply power."],
            "answer": "The algebraic sum of all power (absorbed and supplied) at any instant must equal zero.",
            "explanation": "In any valid circuit, the total power generated by the sources must exactly equal the total power dissipated or absorbed by the rest of the components. Sum of P = 0."
        },
        {
            "question": "If charge is given by q(t) = 10*sin(120*pi*t) mC, what is the equation for the current i(t)?",
            "options": ["1.2*pi*cos(120*pi*t) A", "1200*pi*cos(120*pi*t) A", "120*pi*cos(120*pi*t) mA", "1200*pi*cos(120*pi*t) mA"],
            "answer": "1200*pi*cos(120*pi*t) mA",
            "explanation": "i(t) = dq/dt. Taking the derivative of 10*sin(120*pi*t) yields 10 * 120*pi * cos(120*pi*t) = 1200*pi*cos(120*pi*t) mA."
        },
        {
            "question": "In a given circuit element, current i = 5 A enters the negative terminal, and the voltage across the element is v = 10 V. What is the power?",
            "options": ["50 W absorbed", "50 W supplied", "2 W absorbed", "2 W supplied"],
            "answer": "50 W supplied",
            "explanation": "Because current enters the negative terminal, we use p = -vi (or calculate p = vi and flip the perspective). p = -(10)(5) = -50 W. A negative absorbed power means 50 W is being supplied."
        },
        {
            "question": "What shape is standardly used in circuit diagrams to represent a DEPENDENT (controlled) ideal source?",
            "options": ["Circle", "Diamond", "Square", "Triangle"],
            "answer": "Diamond",
            "explanation": "Independent sources are drawn as circles, while dependent (controlled) sources are universally drawn as diamond shapes."
        },
        {
            "question": "A 100 W incandescent lightbulb is left on for 10 hours. How much energy is consumed in kilowatt-hours (kWh)?",
            "options": ["1000 kWh", "100 kWh", "10 kWh", "1 kWh"],
            "answer": "1 kWh",
            "explanation": "Power = 100 W = 0.1 kW. Energy = Power * Time = 0.1 kW * 10 hours = 1.0 kWh."
        },
        {
            "question": "If an ideal current source of 5A is placed in series with an ideal voltage source of 10V, what is the total current flowing through that branch?",
            "options": ["0 A", "2 A", "5 A", "It cannot be determined."],
            "answer": "5 A",
            "explanation": "The ideal current source dictates the current for the entire branch it is in, regardless of what other components (like the voltage source) are in series with it."
        },
        {
            "question": "Which variable represents the 'effort' required to push electrons through a circuit?",
            "options": ["Current", "Power", "Charge", "Voltage"],
            "answer": "Voltage",
            "explanation": "Voltage (or electromotive force) is the energy per unit charge, acting as the 'push' or 'pressure' that causes current to flow."
        },
        {
            "question": "Calculate the power for an element where v(t) = 10e^(-2t) V and i(t) = 5e^(-2t) A (current entering the positive terminal).",
            "options": ["15e^(-4t) W", "50e^(-4t) W", "50e^(-2t) W", "15e^(-2t) W"],
            "answer": "50e^(-4t) W",
            "explanation": "Power p(t) = v(t) * i(t). Multiplying the two expressions yields (10)(5) * e^(-2t) * e^(-2t) = 50e^(-4t) W."
        },
        {
            "question": "If the energy supplied to an element is w(t) = 25t^2 Joules, what is the power absorbed by the element at t = 4 seconds?",
            "options": ["400 W", "200 W", "100 W", "50 W"],
            "answer": "200 W",
            "explanation": "Power is the derivative of energy: p = dw/dt. The derivative of 25t^2 is 50t. At t = 4, p = 50(4) = 200 W."
        },
        {
            "question": "In the equation v = dw/dq, what does the variable 'w' represent?",
            "options": ["Watts (Power)", "Work (Energy)", "Weight", "Angular frequency"],
            "answer": "Work (Energy)",
            "explanation": "In this specific differential equation defining voltage, 'w' stands for Work (or Energy), measured in Joules."
        },
        {
            "question": "A circuit contains three elements. Element A absorbs 15 W, and Element B supplies 40 W. According to the conservation of energy, what is Element C doing?",
            "options": ["Absorbing 55 W", "Supplying 25 W", "Absorbing 25 W", "Supplying 55 W"],
            "answer": "Absorbing 25 W",
            "explanation": "The sum of all power in a circuit must equal zero: P_A + P_B + P_C = 0. Using the absorbed power convention: 15 W + (-40 W) + P_C = 0. Therefore, P_C = 25 W (positive means absorbing)."
        },
        {
            "question": "If the voltage across an element is v(t) = 5V and the current entering the positive terminal is i(t) = -3A, what is the power of the element?",
            "options": ["15 W absorbed", "15 W supplied", "8 W absorbed", "2 W supplied"],
            "answer": "15 W supplied",
            "explanation": "Using the passive sign convention: p = vi = (5 V)(-3 A) = -15 W. A negative absorbed power means the element is actually supplying 15 W to the circuit."
        },
        {
            "question": "A circuit diagram shows a diamond-shaped symbol with an arrow inside pointing down. Next to it is the label '0.5 * v_x'. What specific component is this?",
            "options": ["Current-Controlled Voltage Source (CCVS)", "Voltage-Controlled Voltage Source (VCVS)", "Voltage-Controlled Current Source (VCCS)", "Current-Controlled Current Source (CCCS)"],
            "answer": "Voltage-Controlled Current Source (VCCS)",
            "explanation": "The diamond shape indicates a dependent source. The arrow inside indicates it outputs a current. The controlling variable 'v_x' indicates it is controlled by a voltage."
        },
        {
            "question": "How much charge flows through a battery if it supplies a constant current of 2 Amperes for exactly 3 hours?",
            "options": ["6 C", "360 C", "7200 C", "21600 C"],
            "answer": "21600 C",
            "explanation": "Current is the rate of charge flow: i = Q/t, so Q = i * t. Time must be in seconds. 3 hours = 10,800 seconds. Q = 2 A * 10,800 s = 21,600 Coulombs."
        },
        {
            "question": "Which of the following describes the conventional direction of electrical current?",
            "options": ["The direction of actual electron flow.", "The direction of positive charge flow.", "From the negative terminal to the positive terminal.", "The direction of neutron drift."],
            "answer": "The direction of positive charge flow.",
            "explanation": "By historical convention established by Benjamin Franklin, current is defined as the flow of positive charge. Since electrons are negatively charged, actual electron flow is in the exact opposite direction of conventional current."
        },
        {
            "question": "The power absorbed by an element is given by p(t) = 10*sin(2t) Watts. How much total energy is absorbed between t = 0 and t = pi/2 seconds?",
            "options": ["0 J", "5 J", "10 J", "20 J"],
            "answer": "10 J",
            "explanation": "Energy is the integral of power. W = integral(10*sin(2t) dt) from 0 to pi/2. The integral is -5*cos(2t). Evaluating from 0 to pi/2 gives (-5*cos(pi)) - (-5*cos(0)) = 5 - (-5) = 10 Joules."
        },
        {
            "question": "What is the SI unit equivalent of 1 Volt expressed in basic mechanical units?",
            "options": ["1 Joule per Coulomb", "1 Coulomb per Second", "1 Watt per Ampere", "1 Newton per Meter"],
            "answer": "1 Joule per Coulomb",
            "explanation": "Voltage is defined as energy per unit charge (v = dw/dq). Therefore, 1 Volt is exactly equal to 1 Joule of energy per 1 Coulomb of charge."
        },
        {
            "question": "If you push 5 Coulombs of charge through a potential difference of 12 Volts, how much work was done?",
            "options": ["2.4 J", "17 J", "60 J", "120 J"],
            "answer": "60 J",
            "explanation": "Work (or Energy) W = V * Q. Therefore, W = 12 V * 5 C = 60 Joules."
        },
        {
            "question": "An ideal basic circuit element is defined by three fundamental attributes. Which of the following is NOT one of those attributes?",
            "options": ["It has only two terminals.", "It is described mathematically in terms of current and voltage.", "It cannot be subdivided into other elements.", "It must dissipate energy as heat."],
            "answer": "It must dissipate energy as heat.",
            "explanation": "An ideal basic circuit element does not have to dissipate heat; it could be a source that supplies energy, or an ideal capacitor/inductor that purely stores energy without loss."
        },
        {
            "question": "Is it valid to connect an ideal 5V voltage source in parallel with an ideal short circuit (a plain wire)?",
            "options": ["Yes, the voltage will drop to 0V.", "Yes, it creates a 5A current.", "No, it violates Kirchhoff's Voltage Law (KVL).", "No, it violates Kirchhoff's Current Law (KCL)."],
            "answer": "No, it violates Kirchhoff's Voltage Law (KVL).",
            "explanation": "A short circuit is an ideal wire with 0V across it. Connecting a 5V source in parallel with a 0V component creates an impossible contradiction, violating KVL."
        },
        {
            "question": "The total energy consumed by a household is billed in kilowatt-hours (kWh). How many Joules are in 1 kWh?",
            "options": ["1,000 J", "3,600 J", "3.6 x 10^6 J", "1 x 10^6 J"],
            "answer": "3.6 x 10^6 J",
            "explanation": "1 kWh = 1000 Watts * 1 hour. Since 1 hour = 3600 seconds, 1000 W * 3600 s = 3,600,000 Joules (or 3.6 MJ)."
        },
        {
            "question": "The charge entering a terminal is given by q(t) = 5e^(-2t) C. What is the current i(t) at t = 1 second?",
            "options": ["-10e^(-2) A", "10e^(-2) A", "-5e^(-2) A", "0 A"],
            "answer": "-10e^(-2) A",
            "explanation": "Current i(t) = dq/dt. The derivative of 5e^(-2t) is -10e^(-2t). Evaluating at t=1 gives -10e^(-2) A."
        },
        {
            "question": "A diamond symbol with '+ -' inside is labeled 'alpha * i_x'. What does this component represent?",
            "options": ["Current-Controlled Voltage Source (CCVS)", "Current-Controlled Current Source (CCCS)", "Voltage-Controlled Voltage Source (VCVS)", "Voltage-Controlled Current Source (VCCS)"],
            "answer": "Current-Controlled Voltage Source (CCVS)",
            "explanation": "The '+ -' inside the diamond means it outputs a voltage. The control variable 'i_x' means it is controlled by a current. Hence, a CCVS."
        },
        {
            "question": "In standard engineering prefixes, what does 1 picoampere (1 pA) represent?",
            "options": ["10^-6 A", "10^-9 A", "10^-12 A", "10^-15 A"],
            "answer": "10^-12 A",
            "explanation": "Micro is 10^-6, Nano is 10^-9, Pico is 10^-12, and Femto is 10^-15."
        },
        {
            "question": "Which component fundamentally dictates the voltage across a branch, completely ignoring the current flowing through it?",
            "options": ["Ideal Resistor", "Ideal Current Source", "Ideal Voltage Source", "Ideal Capacitor"],
            "answer": "Ideal Voltage Source",
            "explanation": "An ideal voltage source maintains its specified terminal voltage regardless of how much current it must supply or absorb to do so."
        },
        {
            "question": "Voltage v(t) = 10*cos(10t) V and current i(t) = 2*sin(10t) A. What is the maximum instantaneous power absorbed by the element?",
            "options": ["20 W", "10 W", "5 W", "0 W"],
            "answer": "10 W",
            "explanation": "Power p(t) = v*i = 20*cos(10t)*sin(10t). Using the trig identity 2*sin(x)*cos(x) = sin(2x), this simplifies to p(t) = 10*sin(20t) W. The maximum value of a sine wave is 1, so the max power is 10 W."
        },
        {
            "question": "Is it valid to connect an ideal 2A current source in parallel with an ideal 3A current source?",
            "options": ["No, it violates KVL.", "No, it violates KCL.", "Yes, it is equivalent to a 5A current source.", "Yes, it is equivalent to a 1A current source."],
            "answer": "Yes, it is equivalent to a 5A current source.",
            "explanation": "Current sources in parallel are perfectly valid; they simply add together (or subtract if facing opposite directions) according to KCL. This combination acts as a single 5A source."
        },
        {
            "question": "Current flows into the positive terminal of a battery. Is the battery charging or discharging?",
            "options": ["Charging (absorbing power)", "Discharging (supplying power)", "Neither, current must flow out of the positive terminal.", "It depends on the internal resistance."],
            "answer": "Charging (absorbing power)",
            "explanation": "According to the passive sign convention, if current enters the positive terminal, the component is acting as a load (absorbing power). Therefore, the battery is charging."
        },
        {
            "question": "If you want to measure the voltage across a resistor in a physical lab, how must the voltmeter be connected?",
            "options": ["In series with the resistor.", "In parallel with the resistor.", "In series with the power supply.", "Between the resistor and ground only."],
            "answer": "In parallel with the resistor.",
            "explanation": "Because components in parallel share the same voltage, a voltmeter must be connected in parallel across the component you are measuring."
        },
        {
            "question": "A component absorbs a constant power of 500 mW. How long will it take to absorb 2 Joules of energy?",
            "options": ["4 seconds", "250 seconds", "0.25 seconds", "1000 seconds"],
            "answer": "4 seconds",
            "explanation": "Power = Energy / Time. Therefore, Time = Energy / Power = 2 J / 0.5 W = 4 seconds."
        },
        {
            "question": "A Current-Controlled Current Source (CCCS) has a gain factor traditionally denoted by beta (β). What are the SI units of β?",
            "options": ["Amperes (A)", "Volts (V)", "Amperes per Volt (A/V)", "Dimensionless (A/A)"],
            "answer": "Dimensionless (A/A)",
            "explanation": "Because a CCCS outputs a current based on an input current (i_out = β * i_in), the gain factor β is simply a ratio of currents (A/A), making it completely dimensionless."
        },
        {
            "question": "A Voltage-Controlled Current Source (VCCS) has an output defined by i_s = g * v_x. What are the units of the gain factor 'g'?",
            "options": ["Dimensionless", "Ohms (V/A)", "Siemens or Mhos (A/V)", "Watts (V*A)"],
            "answer": "Siemens or Mhos (A/V)",
            "explanation": "The gain factor 'g' multiplies a voltage to produce a current. Therefore, its units must be Amperes per Volt (A/V), which is known as Conductance (measured in Siemens or Mhos)."
        },
        {
            "question": "If the energy of an element is defined as w(t) = 15e^(-3t) Joules, what is the power of the element at t = 1 second?",
            "options": ["-45e^(-3) W", "45e^(-3) W", "-5e^(-3) W", "5e^(-3) W"],
            "answer": "-45e^(-3) W",
            "explanation": "Power is the derivative of energy with respect to time: p(t) = dw/dt. Taking the derivative of 15e^(-3t) yields -45e^(-3t). Plugging in t=1 gives -45e^(-3) W."
        },
        {
            "question": "Many batteries, like those in smartphones, are rated in 'Milliampere-hours' (mAh) or 'Ampere-hours' (Ah). What fundamental physical quantity does this unit actually measure?",
            "options": ["Energy", "Power", "Current", "Charge"],
            "answer": "Charge",
            "explanation": "Amperes = Coulombs/Second. Hours = 3600 Seconds. Multiplying Current by Time (C/s * s) cancels out the seconds, leaving only Coulombs, which is a measure of total Charge capacity."
        },
        {
            "question": "Calculate the total charge inside a standard 100 Ah (Amp-hour) 12V car battery.",
            "options": ["100 C", "1,200 C", "3,600 C", "360,000 C"],
            "answer": "360,000 C",
            "explanation": "Charge Q = I * t. 100 Amps flowing for 1 hour (3600 seconds) equals 100 * 3600 = 360,000 Coulombs."
        },
        {
            "question": "According to the passive sign convention, if current LEAVES the positive terminal of an element, how should you calculate power?",
            "options": ["p = vi", "p = -vi", "p = v/i", "Power cannot be calculated this way."],
            "answer": "p = -vi",
            "explanation": "The passive sign convention formally states that current must ENTER the positive terminal to use p = vi. If it leaves the positive terminal (meaning it enters the negative terminal), you must use p = -vi."
        },
        {
            "question": "How is an ideal 'open circuit' defined in electrical engineering terms?",
            "options": ["Voltage is zero, regardless of current.", "Current is zero, regardless of voltage.", "Both voltage and current are zero.", "It dissipates maximum power."],
            "answer": "Current is zero, regardless of voltage.",
            "explanation": "An open circuit is a physical break in the path. Therefore, no current can flow (i=0). However, a large voltage potential can exist across the open gap."
        },
        {
            "question": "How is an ideal 'short circuit' defined?",
            "options": ["Voltage is zero, regardless of current.", "Current is infinite.", "Resistance is infinite.", "It acts as a perfect insulator."],
            "answer": "Voltage is zero, regardless of current.",
            "explanation": "A short circuit is an ideal wire with zero resistance. Therefore, the voltage drop across it is always 0V, even if massive amounts of current are flowing through it."
        },
        {
            "question": "If an ideal 12V independent voltage source is connected to an open circuit, how much power does it supply?",
            "options": ["12 W", "Infinite W", "0 W", "It depends on the internal resistance."],
            "answer": "0 W",
            "explanation": "Because it is connected to an open circuit, the current flowing out of the source is 0A. Power p = vi = (12V)(0A) = 0 Watts."
        },
        {
            "question": "A system has 4 basic elements. Element A absorbs 10W. Element B supplies 20W. Element C absorbs 15W. What is Element D doing?",
            "options": ["Supplying 5W", "Absorbing 5W", "Supplying 25W", "Absorbing 45W"],
            "answer": "Supplying 5W",
            "explanation": "Sum of power must equal zero. Let's use the absorbed convention: 10 + (-20) + 15 + P_D = 0. This gives 5 + P_D = 0, so P_D = -5W. A negative absorbed power means it is supplying 5W."
        },
        {
            "question": "If charge q(t) = 2t^3 + t (in millicoulombs), what is the current i(t) at t = 2 seconds?",
            "options": ["9 mA", "17 mA", "25 mA", "33 mA"],
            "answer": "25 mA",
            "explanation": "i(t) = dq/dt. The derivative of 2t^3 + t is 6t^2 + 1. Plugging in t=2 yields 6(2^2) + 1 = 24 + 1 = 25 mA."
        },
        {
            "question": "An element's voltage is v(t) = 100*cos(50t) V, and its current entering the positive terminal is i(t) = 10*cos(50t) A. Is this element always absorbing power, always supplying, or oscillating?",
            "options": ["Always absorbing power", "Always supplying power", "Oscillating between absorbing and supplying", "Zero power at all times"],
            "answer": "Always absorbing power",
            "explanation": "Power p(t) = v*i = (100*cos(50t))(10*cos(50t)) = 1000*cos^2(50t). Because the cosine term is squared, the power will always be positive (or zero). Thus, it never supplies power."
        },
        {
            "question": "Voltage is defined as V = dw/dq. Current is defined as i = dq/dt. By mathematical chain rule, what is the product of Voltage and Current?",
            "options": ["Charge (q)", "Power (dw/dt)", "Energy (w)", "Resistance (v/i)"],
            "answer": "Power (dw/dt)",
            "explanation": "v * i = (dw/dq) * (dq/dt). The 'dq' terms cancel out, leaving dw/dt, which is the definition of Power (rate of change of energy)."
        },
        {
            "question": "A component has a recorded power of 50 W (absorbed) and a voltage drop of 10 V. If current is defined as entering the NEGATIVE terminal, what is the value of the current?",
            "options": ["5 A", "-5 A", "500 A", "-500 A"],
            "answer": "-5 A",
            "explanation": "Because current enters the negative terminal, the power equation is p = -vi. Therefore, 50 = -10 * i. Solving for i gives i = -5 A."
        },
        {
            "question": "What is the fundamental difference between an independent source and a dependent source?",
            "options": ["Independent sources provide AC; dependent sources provide DC.", "Independent sources have infinite power limits; dependent sources do not.", "Independent sources provide a fixed value regardless of the circuit; dependent sources rely on a specific voltage or current elsewhere in the circuit.", "There is no functional difference."],
            "answer": "Independent sources provide a fixed value regardless of the circuit; dependent sources rely on a specific voltage or current elsewhere in the circuit.",
            "explanation": "An independent source locks a circuit to its value natively. A dependent source must 'listen' to a control variable somewhere else in the network to determine its output."
        },
        {
            "question": "A voltage-controlled voltage source (VCVS) has the equation v_s = μ * v_x. What does the variable μ (mu) represent?",
            "options": ["Voltage gain", "Transconductance", "Current gain", "Transresistance"],
            "answer": "Voltage gain",
            "explanation": "Because it multiplies an input voltage to produce an output voltage, μ represents the dimensionless voltage gain of the source."
        },
        {
            "question": "An ideal independent current source is completely characterized by which of the following?",
            "options": ["It always has zero voltage across it.", "It maintains its specified current regardless of the voltage across its terminals.", "It always dissipates power.", "It behaves like a short circuit."],
            "answer": "It maintains its specified current regardless of the voltage across its terminals.",
            "explanation": "The defining trait of an ideal current source is that it forces exactly its rated current through its branch, absorbing or supplying whatever voltage is necessary to make that happen."
        },
        {
            "question": "If you graph Charge q(t) on the Y-axis and Time t on the X-axis, what does the slope of the tangent line at any point represent?",
            "options": ["Voltage", "Power", "Energy", "Current"],
            "answer": "Current",
            "explanation": "The slope of a curve on a graph is its derivative (dy/dx). The derivative of charge with respect to time (dq/dt) is exactly the definition of current."
        },
        {
            "question": "If you graph Power p(t) on the Y-axis and Time t on the X-axis, what does the total area under the curve between t1 and t2 represent?",
            "options": ["Total Voltage", "Total Charge", "Total Energy transferred", "Total Current"],
            "answer": "Total Energy transferred",
            "explanation": "The area under a curve represents the mathematical integral. The integral of power with respect to time is Work, or Energy."
        },
        {
            "question": "Which basic circuit element requires the presence of an external power supply to function, but is modeled using dependent sources?",
            "options": ["Resistor", "Operational Amplifier (Op-Amp)", "Inductor", "Capacitor"],
            "answer": "Operational Amplifier (Op-Amp)",
            "explanation": "While resistors, capacitors, and inductors are passive, the Op-Amp is an active element. Inside ideal circuit theory, the amplification behavior of an Op-Amp is modeled using a Voltage-Controlled Voltage Source (VCVS)."
        },
        {
            "question": "A graph of current i(t) versus time forms a triangle. It starts at 0 A at t = 0 s, peaks at 4 A at t = 1 s, and drops back to 0 A at t = 2 s. What is the total charge transferred between t = 0 and t = 2 s?",
            "options": ["8 C", "4 C", "2 C", "0 C"],
            "answer": "4 C",
            "explanation": "Charge is the integral of current, which is visually the area under the i(t) curve. The area of a triangle is 1/2 * base * height. 1/2 * 2 s * 4 A = 4 Coulombs."
        },
        {
            "question": "By definition in ideal circuit theory, what is the internal resistance of an ideal independent voltage source?",
            "options": ["Infinite Ohms", "It depends on the load", "0 Ohms", "1 Ohm"],
            "answer": "0 Ohms",
            "explanation": "An ideal voltage source has exactly 0 Ohms of internal resistance, allowing it to maintain its rated voltage regardless of how much current is drawn from it."
        },
        {
            "question": "By definition in ideal circuit theory, what is the internal resistance of an ideal independent current source?",
            "options": ["0 Ohms", "1 Ohm", "It depends on the voltage", "Infinite Ohms"],
            "answer": "Infinite Ohms",
            "explanation": "An ideal current source has infinite internal resistance. This ensures that no current 'leaks' back through the source itself, forcing 100% of its rated current out into the connected circuit."
        },
        {
            "question": "If the voltage notation is given as v_ab = -5 V, what does this mathematically mean regarding the electrical potential?",
            "options": ["Node a is 5V higher than Node b.", "Node b is 5V higher than Node a.", "Current is flowing backwards.", "The element is absorbing 5 Watts."],
            "answer": "Node b is 5V higher than Node a.",
            "explanation": "The notation v_ab means the potential at node 'a' with respect to node 'b'. If v_ab is negative (-5V), it means node 'a' is lower than node 'b'. Thus, node 'b' is 5V higher than node 'a'."
        },
        {
            "question": "The energy of a system is given by w(t) = 10*sin(pi*t) Joules. What is the instantaneous power at exactly t = 0.5 seconds?",
            "options": ["10*pi W", "0 W", "10 W", "-10*pi W"],
            "answer": "0 W",
            "explanation": "Power p(t) = dw/dt. The derivative of 10*sin(pi*t) is 10*pi*cos(pi*t). Plugging in t = 0.5 yields 10*pi*cos(pi/2). Since cos(pi/2) = 0, the power is 0 W."
        },
        {
            "question": "An ideal 5V voltage source is connected in a circuit. A constant current of 10A is measured LEAVING the positive terminal of this source. What is the power condition of the source?",
            "options": ["50 W absorbed", "50 W supplied", "2 W absorbed", "2 W supplied"],
            "answer": "50 W supplied",
            "explanation": "Since 10A leaves the positive terminal, it must be entering the negative terminal. Using the passive sign convention: p = -vi = -(5V)(10A) = -50 W. A negative absorbed power means it is supplying 50 W."
        },
        {
            "question": "A smartphone battery is rated at 5000 mAh and operates at a constant 5 Volts. What is the total energy stored in the battery in kiloJoules (kJ)?",
            "options": ["25 kJ", "90 kJ", "25,000 kJ", "90,000 kJ"],
            "answer": "90 kJ",
            "explanation": "First, convert mAh to Coulombs. 5000 mA = 5 A. Q = 5 A * 3600 s = 18,000 C. Energy W = V * Q = 5 V * 18,000 C = 90,000 Joules, which is 90 kJ."
        },
        {
            "question": "A constant current of 5 mA flows through a wire for exactly 2 minutes. How much charge has passed through the wire?",
            "options": ["10 mC", "600 mC", "0.6 C", "Both 600 mC and 0.6 C"],
            "answer": "Both 600 mC and 0.6 C",
            "explanation": "Charge Q = I * t. Time must be in seconds (2 min = 120 s). Q = (5 x 10^-3 A) * 120 s = 0.6 Coulombs. 0.6 C is equal to 600 mC."
        },
        {
            "question": "Kirchhoff's Current Law (KCL) is fundamentally based on which physical principle?",
            "options": ["Conservation of Energy", "Conservation of Charge", "Newton's Third Law", "Faraday's Law"],
            "answer": "Conservation of Charge",
            "explanation": "KCL states that the sum of currents entering a node equals the sum leaving. This is a direct application of the Law of Conservation of Charge (charge cannot be created or destroyed at a node)."
        },
        {
            "question": "Kirchhoff's Voltage Law (KVL) is fundamentally based on which physical principle?",
            "options": ["Conservation of Energy", "Conservation of Charge", "Conservation of Momentum", "Ohm's Law"],
            "answer": "Conservation of Energy",
            "explanation": "KVL states that the sum of voltage drops around any closed loop must be zero. This means the total energy supplied to a charge by the sources equals the total energy lost in the loads, perfectly satisfying the Conservation of Energy."
        },
        {
            "question": "A power vs. time graph p(t) is a horizontal flat line at p = 4 W from t = 0 to t = 3 seconds. What is the total energy transferred?",
            "options": ["4 J", "12 J", "0 J", "1.33 J"],
            "answer": "12 J",
            "explanation": "Energy is the area under the power curve. For a constant power, it forms a rectangle. Area = base * height = 3 s * 4 W = 12 Joules."
        },
        {
            "question": "The SI unit for Voltage is the Volt (V). If you break the Volt down into base SI units (kg, m, s, A), what is the correct expression?",
            "options": ["kg*m^2 / (s^3*A)", "kg*m / (s^2*A)", "kg*m^2 / (s^2*A)", "kg*m^2 / (s^3*A^2)"],
            "answer": "kg*m^2 / (s^3*A)",
            "explanation": "1 V = 1 Joule/Coulomb. 1 Joule (Work) = Force * distance = (kg*m/s^2) * m = kg*m^2/s^2. 1 Coulomb = 1 Ampere * second (A*s). Dividing J by C yields kg*m^2 / (s^3*A)."
        },
        {
            "question": "In a circuit, Node A is at a potential of 10V and Node B is at 4V. If a positive 3 Coulomb charge moves from Node A to Node B, how much energy is transferred?",
            "options": ["18 Joules released to the circuit", "18 Joules absorbed from the circuit", "42 Joules released to the circuit", "12 Joules absorbed from the circuit"],
            "answer": "18 Joules released to the circuit",
            "explanation": "The change in voltage delta_V = V_final - V_initial = 4V - 10V = -6V. Work = Q * delta_V = 3C * (-6V) = -18J. A negative change in energy of the charge means the energy was released to (supplied to) the circuit components."
        },
        {
            "question": "Which of the following circuit elements is completely immune to Kirchhoff's Current Law (KCL)?",
            "options": ["Ideal Voltage Source", "Ideal Current Source", "Supernodes", "None. KCL applies to all nodes."],
            "answer": "None. KCL applies to all nodes.",
            "explanation": "Kirchhoff's Current Law is a fundamental law of physics (Conservation of Charge). It applies universally to every single node in any lumped-parameter circuit, without exception."
        },
        {
            "question": "In basic circuit terminology, what constitutes a 'Node'?",
            "options": ["Any electrical component.", "A closed loop path.", "A point where two or more circuit elements are joined together.", "The connection to earth ground."],
            "answer": "A point where two or more circuit elements are joined together.",
            "explanation": "A node is simply the junction point connecting two or more components. Even if it is drawn as a long wire in a diagram, the entire wire is considered a single node."
        },
        {
            "question": "In basic circuit terminology, what constitutes a 'Branch'?",
            "options": ["A path that contains only resistors.", "Any single circuit element and the nodes at either end of it.", "A loop that contains no other loops.", "A point where three or more wires meet."],
            "answer": "Any single circuit element and the nodes at either end of it.",
            "explanation": "A branch represents a single path in a network, which in standard analysis means a single component (like a resistor or a source) connected between two nodes."
        },
        {
            "question": "A circuit contains exactly two elements connected in a single loop. If Element 1 is a 10V source supplying 20W, what MUST be true about Element 2?",
            "options": ["It is a 10V source supplying 20W.", "It is absorbing 20W.", "It has a current of 0.5A.", "It must be a resistor."],
            "answer": "It is absorbing 20W.",
            "explanation": "By the conservation of energy (sum of power = 0), if one element supplies 20W, the other element in the circuit must absorb exactly 20W. (It doesn't have to be a resistor; it could be a charging battery)."
        },
        {
            "question": "The unit of Power is the Watt (W). Which of the following is equivalent to 1 Watt?",
            "options": ["1 Joule * Second", "1 Volt / Ampere", "1 Joule / Second", "1 Coulomb / Second"],
            "answer": "1 Joule / Second",
            "explanation": "Power is the rate of energy transfer. Therefore, 1 Watt is exactly equal to 1 Joule of energy being transferred per second (J/s)."
        },
        {
            "question": "Is it possible for an ideal independent voltage source to absorb power?",
            "options": ["Yes, if current enters its positive terminal.", "No, sources can only supply power.", "Yes, but only if it is connected to a dependent source.", "No, it violates conservation of energy."],
            "answer": "Yes, if current enters its positive terminal.",
            "explanation": "Independent sources can act as loads (absorbing power). A classic real-world example is a rechargeable battery being charged by a wall adapter—the adapter supplies power, and the battery absorbs it."
        },
        {
            "question": "If a dependent source's output is governed by the equation v_s = 5 * v_y, what type of component is it?",
            "options": ["CCCS", "VCCS", "CCVS", "VCVS"],
            "answer": "VCVS",
            "explanation": "The output is a voltage (v_s), making it a Voltage Source. The controlling variable is also a voltage (v_y), making it Voltage-Controlled. Therefore, it is a Voltage-Controlled Voltage Source (VCVS)."
        },
        {
            "question": "What is the fundamental physical assumption that allows us to use standard 'lumped-parameter' circuit theory?",
            "options": ["The circuit only uses direct current (DC).", "The physical dimensions of the circuit are small compared to the wavelength of the electrical signals.", "All components are ideal and have no internal resistance.", "The circuit operates in a vacuum."],
            "answer": "The physical dimensions of the circuit are small compared to the wavelength of the electrical signals.",
            "explanation": "Lumped-parameter theory assumes signals travel instantaneously across wires. This is only mathematically valid if the circuit is much smaller than the electromagnetic wavelength of the signal passing through it."
        },
        {
            "question": "If current i(t) = 10e^(-t) A, what is the total charge transferred from t = 0 to t = infinity?",
            "options": ["10 C", "0 C", "Infinite C", "-10 C"],
            "answer": "10 C",
            "explanation": "Charge is the integral of current. The integral of 10e^(-t) is -10e^(-t). Evaluating from 0 to infinity: (0) - (-10e^0) = 0 - (-10) = 10 Coulombs."
        },
        {
            "question": "An element has a voltage of 12 V across it and a current of -2 A entering the NEGATIVE terminal. How much power is it absorbing?",
            "options": ["24 W", "-24 W", "6 W", "-6 W"],
            "answer": "24 W",
            "explanation": "Because current enters the negative terminal, we use p = -vi. Therefore, p = -(12 V)(-2 A) = 24 W. Since the result is positive, it is absorbing 24 W."
        },
        {
            "question": "Tellegen's Theorem, which applies to any lumped-parameter network, is a direct mathematical consequence of what?",
            "options": ["Kirchhoff's Laws (KVL and KCL)", "Ohm's Law", "Faraday's Law of Induction", "Newton's Second Law"],
            "answer": "Kirchhoff's Laws (KVL and KCL)",
            "explanation": "Tellegen's Theorem (which implies the sum of power in a circuit is zero) is derived entirely from the topological constraints of KCL and KVL, without needing to know what the actual components are."
        },
        {
            "question": "If 10 Joules of energy is required to move 2 Coulombs of charge from Node A to Node B, what is the voltage difference v_AB?",
            "options": ["20 V", "5 V", "0.2 V", "12 V"],
            "answer": "5 V",
            "explanation": "Voltage is Work divided by Charge (v = W/Q). Therefore, 10 J / 2 C = 5 Volts."
        },
        {
            "question": "Under what specific condition does an ideal independent voltage source behave exactly like a short circuit?",
            "options": ["When connected in parallel with a resistor.", "When its specified voltage is exactly 0 V.", "When the current drawn is infinite.", "An ideal voltage source can never act as a short circuit."],
            "answer": "When its specified voltage is exactly 0 V.",
            "explanation": "A short circuit is defined as a path with 0V across it. Therefore, an ideal voltage source set to 0V is mathematically and physically identical to a short circuit (a plain wire)."
        },
        {
            "question": "Under what specific condition does an ideal independent current source behave exactly like an open circuit?",
            "options": ["When its specified current is exactly 0 A.", "When connected in series with an open switch.", "When its voltage drops to zero.", "An ideal current source can never act as an open circuit."],
            "answer": "When its specified current is exactly 0 A.",
            "explanation": "An open circuit is defined as a path with 0A flowing through it. Therefore, an ideal current source set to 0A forces zero current to flow, making it mathematically identical to a broken wire (open circuit)."
        },
        {
            "question": "In basic circuit analysis, how is a 'ground' or 'reference' node mathematically defined?",
            "options": ["It is the physical connection to the earth.", "It is the point of maximum current.", "It is an arbitrary node assigned a potential of exactly 0 Volts.", "It is the negative terminal of the main battery."],
            "answer": "It is an arbitrary node assigned a potential of exactly 0 Volts.",
            "explanation": "While 'ground' can mean physical earth in real life, in circuit analysis it simply means the node you have arbitrarily chosen to be your 0V reference point for all other node calculations."
        },
        {
            "question": "By formal textbook definition, what distinguishes an 'active' circuit element from a 'passive' one?",
            "options": ["Active elements move physically; passive elements do not.", "Active elements can supply infinite power; passive elements cannot.", "Active elements can generate average power greater than zero over time; passive elements cannot.", "Active elements are dependent sources; passive elements are independent sources."],
            "answer": "Active elements can generate average power greater than zero over time; passive elements cannot.",
            "explanation": "A passive element (like a resistor) can only absorb energy. While capacitors/inductors can supply energy temporarily, they can never supply more than they previously absorbed. Active elements (like batteries or op-amps) can introduce new energy to the circuit."
        },
        {
            "question": "In SI engineering prefixes, what is the correct symbol and multiplier for 'Tera'?",
            "options": ["T, 10^12", "T, 10^9", "t, 10^15", "G, 10^12"],
            "answer": "T, 10^12",
            "explanation": "Tera (T) is 10^12. Giga (G) is 10^9. Mega (M) is 10^6."
        },
        {
            "question": "In SI engineering prefixes, what is the correct multiplier for 'Femto' (f)?",
            "options": ["10^-9", "10^-12", "10^-15", "10^-18"],
            "answer": "10^-15",
            "explanation": "Milli is 10^-3, Micro is 10^-6, Nano is 10^-9, Pico is 10^-12, and Femto is 10^-15."
        },
        {
            "question": "The instantaneous power of a component is p(t) = 5*sin(t) W. What is the total energy transferred from t = 0 to t = pi seconds?",
            "options": ["0 J", "5 J", "10 J", "2.5 J"],
            "answer": "10 J",
            "explanation": "Energy is the integral of power. Integral of 5*sin(t) from 0 to pi is [-5*cos(t)] from 0 to pi. Evaluated: (-5*cos(pi)) - (-5*cos(0)) = 5 - (-5) = 10 Joules."
        },
        {
            "question": "If an element absorbs exactly 0 W of power, but has a 100 V drop measured across it, what MUST the current flowing through it be?",
            "options": ["100 A", "1 A", "0 A", "Infinite A"],
            "answer": "0 A",
            "explanation": "Power p = v*i. If p = 0 W and v = 100 V, then i must mathematically equal 0 A (this is an open circuit with a voltage potential across the gap)."
        },
        {
            "question": "What is the primary conceptual difference between Charge (q) and Current (i)?",
            "options": ["Charge is measured in Watts; Current is measured in Amps.", "Charge is a quantity of electricity; Current is the rate at which that quantity moves.", "Charge is potential energy; Current is kinetic energy.", "There is no difference; they are interchangeable."],
            "answer": "Charge is a quantity of electricity; Current is the rate at which that quantity moves.",
            "explanation": "Charge is an absolute amount (like gallons of water). Current is a rate of flow over time (like gallons per minute)."
        },
        {
            "question": "A component has a constant voltage V across it. If the current I through the component suddenly reverses direction, what happens to the power?",
            "options": ["Power drops to zero.", "Power is squared.", "The component switches from absorbing power to supplying power (or vice versa).", "Nothing, power remains exactly the same."],
            "answer": "The component switches from absorbing power to supplying power (or vice versa).",
            "explanation": "Power p = vi. If the sign of the current 'i' flips while 'v' remains constant, the sign of the power 'p' flips. This means a component that was acting as a load is now acting as a source."
        },
        {
            "question": "Which of the following is an example of an ACTIVE circuit component?",
            "options": ["Resistor", "Capacitor", "Inductor", "Operational Amplifier"],
            "answer": "Operational Amplifier",
            "explanation": "Op-amps require external power supply rails (Vcc and Vee) to function and can inject power into a signal, making them active components. Resistors, capacitors, and inductors are passive."
        },
        {
            "question": "To convert 50 Megawatts (MW) into kilowatts (kW), you would write:",
            "options": ["50,000 kW", "5,000 kW", "0.05 kW", "500,000 kW"],
            "answer": "50,000 kW",
            "explanation": "Mega (10^6) is one thousand times larger than kilo (10^3). Therefore, 50 MW = 50 * 1,000 kW = 50,000 kW."
        },
        {
            "question": "A dependent source outputs a current i_s = g * v_x. If this source is placed in a circuit where v_x is 0 V, what component does this dependent source momentarily act like?",
            "options": ["A resistor.", "A short circuit.", "An open circuit.", "An independent voltage source."],
            "answer": "An open circuit.",
            "explanation": "If v_x = 0, then i_s = g * 0 = 0 A. A component that forces 0 A to flow through it is physically acting as an open circuit."
        },
        {
            "question": "When building mathematical models of physical transistors (like BJTs or MOSFETs), which circuit elements are absolutely required to model their amplification behavior?",
            "options": ["Only resistors and capacitors.", "Independent voltage sources.", "Dependent (controlled) sources.", "Only inductors."],
            "answer": "Dependent (controlled) sources.",
            "explanation": "Transistors act as amplifiers or switches where the current/voltage in one part of the device controls the current/voltage in another. This behavior is perfectly modeled by dependent sources."
        },
        {
            "question": "In a complete, isolated circuit diagram, you count 5 nodes and 7 branches. According to KCL, how many INDEPENDENT current equations can you write?",
            "options": ["5", "4", "7", "6"],
            "answer": "4",
            "explanation": "In any circuit with 'N' essential nodes, you can only write N-1 independent KCL equations. The Nth equation is always redundant. Therefore, 5 - 1 = 4."
        }
        ]

        # The loop MUST be indented underneath "with tab_ch1:"
        for i, q in enumerate(mcq_database_ch1):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            
            # Notice the key includes "ch1_" to prevent crashes!
            user_choice = st.radio(
                "Select your answer:", 
                q["options"], 
                index=None, 
                key=f"ch1_q{i}",
                label_visibility="collapsed"
            )
            
            if st.button(f"Check Answer for Q{i+1}", key=f"ch1_btn{i}"):
                if user_choice == q["answer"]:
                    st.success(f"✅ Correct! {q['explanation']}")
                elif user_choice is None:
                    st.warning("Please select an answer first.")
                else:
                    st.error("❌ Incorrect. Try again.")
            st.divider()

    # 4. Chapter 2 Practice Tab
    with tab_ch2:
        st.header("Chapter 2: Resistive Circuits")
        st.info("Currently locked. Question bank compiling...")
        
        # When we generate Chapter 2, you will paste mcq_database_ch2 here!

    # 5. Placeholder for future chapters
    with tab_ch3:
        st.header("Chapter 3: Node-Voltage & Mesh-Current")
        st.info("Currently locked. Question bank compiling...")