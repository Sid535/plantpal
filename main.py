import subprocess
import sys
import os

def main():
    print("Launching PlantPal Client...")
    # This runs 'streamlit run client/app.py'
    process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "client/app.py"])
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("\nStopping PlantPal...")
        os._exit(0)

if __name__ == "__main__":
    main()