import re
import os
def extract_translations_from_txt(txtfilepath):
    section2_values = {"P8631", "P8629", "P8632", "P2818", "P26171"}
    section3_values = {"A1032", "A1033"}

    translations = {}
    translation_lines = []

    with open(txtfilepath, "r", encoding='UTF-8') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue
            key_part, value = line.split(':', 1)
            sections = key_part.split('-')
            section1 = sections[0] if len(sections) > 0 else None
            section2 = next((s for s in sections if s in section2_values), None)
            section3 = next((s for s in sections if s in section3_values), None)
            section4 = next((s for s in sections if s.startswith('L')), None)
            if not (section1 and section2 and section3 and section4):
                continue
            new_key = f"{section1}-{section2}-{section3}-{section4}"
            if new_key not in translations:
                translations[new_key] = []
            translations[new_key].append(value.strip())
            translation_lines.append((new_key, value.strip()))
    return translations, translation_lines
def inject_translations_to_captions(translations,translation_lines, lang_code,project_dir):
    AL_object_name_pattern = re.compile(r'^(table|page|report|codeunit)\s+(\d+)\b(?!")', re.UNICODE)
    caption_pattern = re.compile(r'^\s*("?[\w\s.]+?"?)\s*:\s*Label\s*\'([^\']+)\'\s*;')
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.al'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                new_lines = []
                modified = False
                id_number = None
                object_type = None
                for line in lines:
                    AL_object_match = AL_object_name_pattern.match(line)
                    if AL_object_match:
                        object_type = AL_object_match.group(1)
                        id_number = AL_object_match.group(2)
                    caption_match = caption_pattern.match(line)
                    if caption_match and id_number and object_type and object_type.lower() == "report":
                        caption_name = caption_match.group(1)
                        caption_value = caption_match.group(2)
                        english_key = f"R{id_number}-P26171-A1033-L999"
                        greek_key = f"R{id_number}-P26171-A1032-L999"
                        # Find the index of the English key in the translation_lines
                        for idx, (k, v) in enumerate(translation_lines):
                            if k == english_key and v == caption_value:
                                # Check if previous line is the Greek key with same prefix
                                if idx > 0:
                                    prev_k, prev_v = translation_lines[idx - 1]
                                    if prev_k == greek_key:
                                        greek_value = prev_v
                                        if "Comment =" not in line:
                                            inject = caption_pattern.sub(
                                                rf"\1: Label '\2' , Comment = '{lang_code}={greek_value}';", line
                                            )
                                            new_lines.append(inject)
                                            modified = True
                                            break
                                # If not, do not inject
                        else:
                            new_lines.append(line)
                            continue
                        continue  # Skip appending original line if injected
                    new_lines.append(line)
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.writelines(new_lines)
                    print(f"✅ Translated: {file_path}")
