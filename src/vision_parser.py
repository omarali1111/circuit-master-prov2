# src/vision_parser.py
import os
import base64
from anthropic import Anthropic
from dotenv import load_dotenv

# Load the secret keys from your .env file
load_dotenv()

# Initialize the Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def encode_image(image_path):
    """Converts the image into a format Claude can read."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_spice_netlist(image_path):
    """Sends the image to Claude 3.5 Sonnet and asks for a SPICE Netlist."""
    print(f"Scanning circuit diagram: {image_path}...")
    base64_image = encode_image(image_path)

    # This is the "System Prompt" - the strict instructions for the AI
    prompt = """
    You are an expert electrical engineer. Analyze this circuit diagram from the Nilsson & Riedel textbook.
    1. Identify all nodes (assume the bottom wire is Ground / Node 0).
    2. Identify all components (Resistors, Independent Sources, Dependent Sources).
    
    CRITICAL INSTRUCTIONS:
    - Output exactly ONE standard SPICE netlist.
    - Include the .op command at the end.
    - Do NOT include any comments, alternative versions, or conversational text.
    - Output ONLY the raw netlist text.
    """

    response = client.messages.create(
        model="claude-sonnet-4-6", # Updated to the current model
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    
    # Extract the text and tell VS code to ignore the red squiggle
    raw_text = response.content[0].text # type: ignore
    
    # Strip away the markdown backticks
    clean_text = raw_text.replace("```spice\n", "").replace("```", "").strip()
    
    return clean_text

if __name__ == "__main__":
    # We will point this at the image you just uploaded!
    test_image = "data/test_circuit.png"
    
    if os.path.exists(test_image):
        print("Image found! Sending to Claude's brain...\n")
        netlist = get_spice_netlist(test_image)
        print("--- GENERATED SPICE NETLIST ---")
        print(netlist)
    else:
        print(f"Error: I cannot find '{test_image}'.")
        print("Please save one of the textbook screenshots as 'test_circuit.png' inside the 'data' folder.")