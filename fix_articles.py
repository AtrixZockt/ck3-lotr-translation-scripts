#C:\Users\atrix\OneDrive\Desktop\english\lotr_titles_l_german.yml

import os
import time
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

file_to_fix = os.getenv("FIX_ARTICLES_FILE_PATH")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
ERROR_LOG_FILE = "translation_errors.log"

def get_correct_article(phrase, key=""):
    """
    Sendet einen Ausdruck an die KI mit der Aufgabe, den Artikel zu korrigieren.
    Nimmt jetzt optional einen Key für zusätzlichen Kontext.
    """
    if key and phrase.strip() == "$the_$":
        # === ÄNDERUNG HIER: Anweisung und Beispiel geben jetzt keinen Unterstrich mehr aus ===
        prompt = f"""
        You are a German grammar expert. The context for the following task is J.R.R. Tolkien's Lord of the Rings.
        Your task is to determine the correct German article for a noun hinted at by a localization key.
        You will receive a localization `key` and a `value` which is a placeholder like "$the_$".
        Use the `key` (e.g., "k_rohan_article") to infer the noun (e.g., "Rohan").
        Based on the noun's gender, replace the placeholder "$the_$" with ONLY the correct German definite article ("der", "die", "das", "den" or "dem").
        Return ONLY the article. Do not add any other text, explanations, quotes, or the underscore.

        EXAMPLE 1:
        Key: k_king_of_gondor_article
        Value: $the_$
        ---
        OUTPUT:
        der
        ---
        EXAMPLE 2:
        Key: k_rohan_article
        Value: $the_$
        ---
        OUTPUT:
        das
        ---
        Key: {key}
        Value: {phrase}
        ---
        OUTPUT:
        """
    else:
        prompt = f"""
        You are a German grammar expert. The context for the following task is J.R.R. Tolkien's Lord of the Rings.
        Your task is to correct the article in a given phrase.
        The placeholder "$the_$" must be replaced with the correct German definite article ("der", "die", "das", "den" or "dem"). The trailing underscore from the placeholder should be removed.
        Return ONLY the corrected phrase. Do not add any other text or explanations.

        EXAMPLE INPUT:
        $the_$ King of Gondor
        ---
        EXAMPLE OUTPUT:
        der König von Gondor
        ---
        Phrase to correct:
        "{phrase}"
        """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip() + " "
    except Exception as e:
        print(f"    - 🛑 Fehler bei der Artikel-Anfrage für '{phrase}': {e}")
        return phrase

def fix_articles_in_file(filepath):
    """
    Liest eine Datei, findet Zeilen mit dem '$the_$'-Platzhalter,
    korrigiert sie und speichert die Datei.
    """
    print(f"--- Starte Artikel-Korrektur für die Datei: '{filepath}' ---")
    if not os.path.exists(filepath):
        print(f"🛑 FEHLER: Die Datei '{filepath}' wurde nicht gefunden.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()

        new_lines = list(lines)
        needs_update = False

        print(f"Prüfe {len(lines)} Zeilen auf '$the_$'-Platzhalter...")

        for i, line in enumerate(lines):
            if '"$the_$' in line:
                try:
                    full_key = line.split(':')[0].strip()
                    value_part = re.search(r'"(.*?)"', line).group(1)
                except (AttributeError, IndexError):
                    continue

                if value_part.strip() == "$the_$":
                    print(f"  - Analysiere Zeile {i+1} (Key: {full_key})...")
                    corrected_value = get_correct_article(value_part, full_key)
                else:
                    print(f"  - Analysiere Zeile {i+1}...")
                    corrected_value = get_correct_article(value_part)
                
                if corrected_value != value_part:
                    key_part = line.split('"')[0]
                    rest_of_line = line.split('"')[-1]
                    
                    new_line = f'{key_part}"{corrected_value} "{rest_of_line}'
                    new_lines[i] = new_line
                    needs_update = True
                    
                    print(f"    -> '{value_part}' zu '{corrected_value}' korrigiert.")
                
                time.sleep(1)

        if needs_update:
            print("💾 Speichere die korrigierte Datei...")
            with open(filepath, 'w', encoding='utf-8-sig') as f:
                f.writelines(new_lines)
        else:
            print("✅ Keine Korrekturen notwendig.")

    except Exception as e:
        print(f"🛑 Ein schwerwiegender Fehler ist aufgetreten: {e}")

    print("\n✨ Artikel-Korrektur abgeschlossen.")


if __name__ == '__main__':
    if not file_to_fix or not os.path.isfile(file_to_fix):
        print("🛑 Bitte gib den Pfad zur zu korrigierenden Datei im Skript an.")
    else:
        fix_articles_in_file(file_to_fix)