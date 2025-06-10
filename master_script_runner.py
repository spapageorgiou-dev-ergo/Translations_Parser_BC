import subprocess
import sys
import os

# List your runner scripts with their full paths
RUNNER_SCRIPTS = [
    r"ToolTips/script_runner_tooltip.py",
    r"Labels/script_runner_label.py",
    r"Captions/script_runner_caption.py",
    r"OptionCaptions/script_runner_optioncaption.py"
]

# If you want to pass arguments, add them here
project_dir = r"C:/Users/s.papageorgiou/Desktop/Parser Test AL"
txt_path = r"C:/Users/s.papageorgiou/Desktop/Useful Scripts/Parser_for_BC_Migration/translation_table.txt"

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for script in RUNNER_SCRIPTS:
        script_path = os.path.join(base_dir, script)
        print(f"\n=== Running {script_path} ===")
        # If your runner scripts accept arguments, add them here:
        subprocess.run([sys.executable, script_path, project_dir, txt_path])