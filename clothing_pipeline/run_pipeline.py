import os
import subprocess
import sys

def main():
    scripts = [
        "1_generator.py",
        "2_canvas_baker.py",
        "3_printify_sync.py",
        "4_local_vto.py",
        "5_content_generator.py"
    ]

    print("Starting the T-Shirt Design Pipeline...")
    print("=" * 40)

    for script in scripts:
        print(f"\n---> Starting: {script} <---")
        try:
            # Phase 4 requires the vto_env virtual environment because it uses heavy ML libraries
            executable = sys.executable
            if script == "4_local_vto.py" and os.path.exists("vto_env/bin/python"):
                executable = "vto_env/bin/python"
                
            # We don't capture stdout/stderr or pipe stdin. 
            # By default, subprocess.run connects these to the current terminal,
            # allowing input() and print() to work interactively.
            result = subprocess.run(
                [executable, script],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"\n[ERROR] Pipeline stopped. '{script}' exited with non-zero status (code {e.returncode}).")
            sys.exit(e.returncode)
        except KeyboardInterrupt:
            print(f"\n[ERROR] Pipeline aborted by user during '{script}'.")
            sys.exit(1)
        
        print(f"--- Finished: {script} ---")

    print("\n" + "=" * 40)
    print("[SUCCESS] All scripts in the pipeline completed successfully.")

if __name__ == "__main__":
    main()
