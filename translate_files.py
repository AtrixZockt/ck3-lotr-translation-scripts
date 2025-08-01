import os
import time
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

folder_to_translate = os.getenv("TRANSLATE_FOLDER_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Globale Einstellungen ---
TRANSLATION_MARKER = "#~TR~"
BATCH_SIZE = 50
ERROR_LOG_FILE = "translation_errors.log"

def translate_batch_with_gemini(text_list, filename):
    """Übersetzt eine ganze Liste (Batch) von Texten mit einer einzigen API-Anfrage."""
    json_input = json.dumps(text_list, ensure_ascii=False)
    prompt = f"""
    You are an expert translator for video game mods, specifically for a "Lord of the Rings" mod for the game "Crusader Kings 3".
    **CONTEXT:** You are translating content from the file named: `{filename}`.
    **TASK:** You will receive a JSON array of English strings. Translate every string to German. Return a valid JSON array.
    **CRITICAL INSTRUCTIONS:**
    1.  **USE OFFICIAL TOLKIEN TRANSLATIONS:** ('Frodo Baggins' -> 'Frodo Beutlin'). Do not translate names that remain in English ('Gondor').
    2.  **DO NOT TRANSLATE GAME CODE:** Preserve text inside `[]` EXACTLY.
    3.  **PRESERVE IN-TEXT VARIABLES:** Preserve text inside `$$` EXACTLY.
    4.  **PRESERVE FORMATTING MARKERS:** Preserve single words starting with `#` EXACTLY.
    5.  **PRESERVE ICON CODES:** Preserve text from `@` to `!` EXACTLY.
    6.  **USE CK3 TERMINOLOGY:** ('vassal' -> 'Vasall').
    7.  **TONE:** Use the informal German "du/dein/euch".
    8.  **OUTPUT FORMAT:** Your entire output MUST be a single, valid JSON array of strings.
    ---
    JSON array to translate:
    {json_input}
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        translated_list = json.loads(cleaned_response)
        if len(translated_list) == len(text_list): return translated_list
        return None
    except Exception as e:
        print(f"  🛑 Fehler bei der Batch-API-Anfrage: {e}")
        return None

def translate_single_line_safely(english_text, filename):
    """Übersetzt eine einzelne Zeile. Dient als Sicherheits-Fallback, wenn eine Batch-Anfrage fehlschlägt."""
    prompt = f"""
    You are an expert translator for video game mods, specifically for a "Lord of the Rings" mod for the game "Crusader Kings 3".
    **CONTEXT:** You are translating content from the file named: `{filename}`.
    **TASK:** Translate the single following English text to German.
    **CRITICAL INSTRUCTIONS:**
    1.  **USE OFFICIAL TOLKIEN TRANSLATIONS:** ('Frodo Baggins' -> 'Frodo Beutlin'). Do not translate names that remain in English ('Gondor').
    2.  **DO NOT TRANSLATE GAME CODE:** Preserve text inside `[]` EXACTLY.
    3.  **PRESERVE IN-TEXT VARIABLES:** Preserve text inside `$$` EXACTLY.
    4.  **PRESERVE FORMATTING MARKERS:** Preserve single words starting with `#` EXACTLY.
    5.  **PRESERVE ICON CODES:** Preserve text from `@` to `!` EXACTLY.
    6.  **USE CK3 TERMINOLOGY:** ('vassal' -> 'Vasall').
    7.  **TONE:** Use the informal German "du/dein/euch".
    8.  **OUTPUT:** Return ONLY the final translated German text.
    ---
    English text: "{english_text}"
    ---
    German translation:
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"    - 🛑 Fehler bei Einzelanfrage: {e}")
        return None

def translate_lotr_files(main_folder):
    """Die Hauptfunktion des Skripts."""
    print(f"--- Starte Batch-Übersetzungsprozess in: '{main_folder}' ---")
    if not GEMINI_API_KEY or GEMINI_API_KEY == "DEIN_GEMINI_API_KEY":
        print("🛑 FEHLER: Bitte füge deinen Gemini API Key in das Skript ein.")
        return
        
    if os.path.exists(ERROR_LOG_FILE):
        os.remove(ERROR_LOG_FILE)
        print(f"Alte Log-Datei '{ERROR_LOG_FILE}' wurde gelöscht.")
    
    # === ÄNDERUNG HIER: Ein präziseres Muster, das Kommentare am Zeilenende korrekt erfasst ===
    # Gruppe 1 (key_part): Erfasst Key, Einrückung und Versionsnummer.
    # Gruppe 2 (value_part): Erfasst nur den Inhalt zwischen den Anführungszeichen.
    # Gruppe 3 (comment_part): Erfasst optional einen echten Kommentar am Ende.
    line_pattern = re.compile(r'^(.*?:\d*\s*)(".*?")(\s*#.*)?$')

    for root, _, files in os.walk(main_folder):
        for filename in files:
            if filename.endswith("_german.yml"):
                filepath = os.path.join(root, filename)
                print(f"\n🔄 Bearbeite Datei: {filepath}")

                try:
                    with open(filepath, 'r', encoding='utf-8-sig') as f: lines = f.readlines()
                    new_lines, batch_to_translate, needs_update = list(lines), [], False

                    for i, line in enumerate(lines):
                        if TRANSLATION_MARKER in line: continue

                        match = line_pattern.match(line.rstrip())
                        if match:
                            key_part = match.group(1)
                            value = match.group(2)
                            original_comment = match.group(3) if match.group(3) else ""

                            if value and value != '""':
                                if value.startswith('"$') and value.endswith('$"') and value.count('$') == 2:
                                    print(f"  - Überspringe (reine Variable): {value}")
                                    continue
                                text_for_api = value.strip('"').replace('""', '"')
                                batch_to_translate.append((i, text_for_api, key_part, original_comment))

                        if (len(batch_to_translate) >= BATCH_SIZE) or (i == len(lines) - 1 and batch_to_translate):
                            if not batch_to_translate: continue
                            start_line, end_line = batch_to_translate[0][0] + 1, batch_to_translate[-1][0] + 1
                            print(f"  - Übersetze Batch (Zeilen {start_line}-{end_line}) aus '{filename}'...")
                            
                            original_texts = [item[1] for item in batch_to_translate]
                            translated_texts = translate_batch_with_gemini(original_texts, filename)
                            
                            if translated_texts:
                                for idx, (line_index, _, key_part, original_comment) in enumerate(batch_to_translate):
                                    translated_text = translated_texts[idx]
                                    processed_translation = translated_text.replace('"', '""').replace('\n', '\\n')
                                    new_line = f'{key_part.rstrip()} "{processed_translation}"{original_comment}  {TRANSLATION_MARKER}\n'
                                    new_lines[line_index] = new_line
                                needs_update = True
                            else:
                                print("  ⚠️ Batch fehlgeschlagen. Wechsle zum sicheren Einzelmodus...")
                                for line_index, original_text, key_part, original_comment in batch_to_translate:
                                    print(f"    - Einzelversuch für Zeile {line_index + 1}...")
                                    translated_text = translate_single_line_safely(original_text, filename)
                                    if translated_text:
                                        processed_translation = translated_text.replace('"', '""').replace('\n', '\\n')
                                        new_line = f'{key_part.rstrip()} "{processed_translation}"{original_comment}  {TRANSLATION_MARKER}\n'
                                        new_lines[line_index] = new_line
                                        needs_update = True
                                    else:
                                        print(f"    - 🛑 Einzelversuch fehlgeschlagen. Wird geloggt.")
                                        try:
                                            with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
                                                f.write(f"Datei: {filename}, Zeile: {line_index + 1}, Text: {original_text}\n")
                                        except Exception as e_log:
                                            print(f"      - 🛑 In Log-Datei schreiben fehlgeschlagen: {e_log}")
                                    time.sleep(1)
                            batch_to_translate = []
                            time.sleep(1)

                    if needs_update:
                        print(f"  💾 Speichere übersetzte Datei...")
                        with open(filepath, 'w', encoding='utf-8-sig') as f: f.writelines(new_lines)
                    else:
                        print("  ✅ Datei bereits vollständig übersetzt oder enthält nur reine Variablen.")
                except Exception as e:
                    print(f"  🛑 Schwerwiegender Fehler bei Datei {filename}: {e}")

    print("\n\n✨ Übersetzungsprozess abgeschlossen.")
    if os.path.exists(ERROR_LOG_FILE):
        print(f"Einige Fehler wurden in '{ERROR_LOG_FILE}' protokolliert.")

if __name__ == '__main__':
    if not folder_to_translate or not os.path.isdir(folder_to_translate):
        print("🛑 Bitte gib den Pfad zur zu korrigierenden Datei im Skript an.")
    else:
        translate_lotr_files(folder_to_translate)