import re
import os
def extract_translations_from_txt(txtfilepath):
    # Define the section values to look for
    section2_values = {"P8631", "P8629", "P8632", "P2818", "P26171"}
    section3_values = {"A1032", "A1033"}

    translations = {}

    with open(txtfilepath, "r", encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key_part, value = line.split(':', 1)
            sections = key_part.split('-')

            # Section1mykey
            section1 = sections[0] if len(sections) > 0 else None

            # Section2mykey
            section2 = next((s for s in sections if s in section2_values), None)

            # Section3mykey
            section3 = next((s for s in sections if s in section3_values), None)

            # Section4mykey
            section4 = next((s for s in sections if s.startswith('L')), None)

            # Skip if any required section is missing
            if not (section1 and section2 and section3 and section4):
                continue

            new_key = f"{section1}-{section2}-{section3}-{section4}"
            if new_key not in translations:
                translations[new_key] = []
            translations[new_key].append(value.strip())
    return translations
def inject_translations_to_captions(translations_dict, lang_code,project_dir):
    AL_object_name_pattern = re.compile(r'^(table|page|report|codeunit)\s+(\d+)\b(?!")', re.UNICODE)
    caption_pattern = re.compile(r"^\s*OptionCaption\s*=\s*'([^']+)'\s*(;|,)?")
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.al'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                new_lines = []
                modified = False
                id_number = None
                object_type= None
      # ...existing code...
                for line in lines:
                    AL_object_match = AL_object_name_pattern.match(line)
                    if AL_object_match:
                        object_type = AL_object_match.group(1)
                        id_number = AL_object_match.group(2)
                    caption_match = caption_pattern.match(line)
                    if caption_match and id_number and object_type and object_type.lower() == "table":
                        caption_value = caption_match.group(1)
                        # Find the English key that matches this caption value
                        english_key = next(
                            (k for k in translations_dict
                            if k.startswith(f"T{id_number}-") and "P8632-A1033-" in k and caption_value in translations_dict[k]),
                            None
                        )
                        if english_key:
                            greek_key = english_key.replace("A1033", "A1032")
                            # Only inject if Greek key exists and has a value at the same index
                            if greek_key in translations_dict and translations_dict[greek_key]:
                                idx = translations_dict[english_key].index(caption_value)
                                if idx < len(translations_dict[greek_key]):
                                    greek_value = translations_dict[greek_key][idx]
                                    if "Comment =" not in line:
                                        inject = caption_pattern.sub(
                                            rf"OptionCaption = '\1' , Comment = '{lang_code}={greek_value}';", line
                                        )
                                        new_lines.append(inject)
                                        modified = True
                                        continue
                                    else:
                                        # Already has a comment, skip or optionally update it
                                        new_lines.append(line)
                                        continue
                    new_lines.append(line)
            # ...existing code...
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"✅ Translated: {file_path}")

