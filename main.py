import subprocess
import sys

def main():
    print("Launching PlantPal Client...")
    # This runs 'streamlit run client/app.py'
    subprocess.run([sys.executable, "-m", "streamlit", "run", "client/app.py"])

if __name__ == "__main__":
    main()