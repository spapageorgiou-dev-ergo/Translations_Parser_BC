import importlib.util
import os

LABEL_SCRIPTS = [
    "OptionCaptions_Codeunit.py",
    "OptionCaptions_Page.py",
    "OptionCaptions_Report.py",
    "OptionCaptions_Table.py"
]

def run_label_script(script_path, project_dir, txt_path):
    spec = importlib.util.spec_from_file_location("label_module", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Extract translations
    translations= module.extract_translations_from_txt(txt_path)
    # Run injection
    module.inject_translations_to_captions(translations, "el_GR",project_dir)

if __name__ == "__main__":
    # Set your paths here
    project_dir = r"C:/Users/s.papageorgiou/Desktop/Parser Test AL"
    txt_path = r"C:/Users/s.papageorgiou/Desktop/Useful Scripts/Parser_for_BC_Migration/translation_table.txt"
    base_dir = r"C:/Users/s.papageorgiou/Desktop/Useful Scripts/Parser_for_BC_Migration/optioncaptions"

    for script in LABEL_SCRIPTS:
        script_path = os.path.join(base_dir, script)
        print(f"Running {script_path} ...")
        run_label_script(script_path, project_dir, txt_path)