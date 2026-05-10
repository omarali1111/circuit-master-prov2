# src/main.py
import os
from vision_parser import get_spice_netlist # type: ignore
from spice_solver import solve_netlist # type: ignore

def analyze_and_solve(image_path):
    print("\n=========================================")
    print(" 🚀 MASTERING SFU: CIRCUIT ANALYSIS ENGINE ")
    print("=========================================\n")
    
    if not os.path.exists(image_path):
        print(f"[!] Error: Cannot find {image_path}")
        return

    # STAGE 1: Let Claude see the image
    print("STAGE 1: Vision Processing...")
    clean_netlist = get_spice_netlist(image_path)
    print("✅ Netlist Extracted.\n")
    
    # STAGE 2: Send it to the Ngspice Truth Engine
    print("STAGE 2: Math Verification...")
    solve_netlist(clean_netlist)
    print("\n=========================================\n")

if __name__ == "__main__":
    # Point this at your test image!
    analyze_and_solve("data/test_circuit.png")