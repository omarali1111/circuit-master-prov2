# src/spice_solver.py
from PySpice.Spice.Parser import SpiceParser
import PySpice.Logging.Logging as Logging

# Turn off the annoying internal logs from PySpice
logger = Logging.setup_logging(logging_level='ERROR')

def solve_netlist(netlist_text):
    print("Feeding circuit DNA to the Truth Engine...")
    
    try:
        # 1. Read the text from Claude
        parser = SpiceParser(source=netlist_text)
        circuit = parser.build_circuit()
        
        # 2. Fire up the simulator
        simulator = circuit.simulator(temperature=25, nominal_temperature=25)
        
        # 3. Run an "Operating Point" analysis (finds all DC node voltages)
        analysis = simulator.operating_point()

        print("\n--- 100% ACCURATE NODE VOLTAGES ---")
        for node in analysis.nodes.values():
            # Format the output to 3 decimal places
            print(f"Node {node.name}: {float(node[0]):.3f} V")
            
    except Exception as e:
        print(f"\n[!] Simulation Failed: {e}")
        print("Check if Ngspice is properly installed on your computer.")