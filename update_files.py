import os
from dotenv import load_dotenv

load_dotenv()

folder_to_update = os.getenv("FOLDER_PATH")

def update_lotr_yml_files(main_folder):
    """
    Aktualisiert .yml-Dateien, die mit 'lotr_' beginnen, in einem Verzeichnis und dessen Unterverzeichnissen.
    - Benennt Dateien von '_english.yml' in '_german.yml' um.
    - Ändert die erste Zeile von 'l_english:' in 'l_german:'.
    - Speichert die neue Datei mit UTF-8-BOM-Kodierung.

    Args:
        main_folder (str): Der Pfad zum Hauptordner.
    """
    print(f"--- Starte den Umbenennungs- und Bearbeitungsprozess in: '{main_folder}' ---")

    if not os.path.isdir(main_folder):
        print(f"🛑 FEHLER: Der angegebene Ordner '{main_folder}' existiert nicht.")
        return

    files_processed = 0
    # Durchlaufe das Hauptverzeichnis und alle Unterverzeichnisse
    for root, _, files in os.walk(main_folder):
        for filename in files:
            if filename.endswith("_english.yml"):
                old_filepath = os.path.join(root, filename)
                
                try:
                    # Lese die Datei mit 'utf-8-sig', um ein eventuell vorhandenes BOM zu ignorieren
                    with open(old_filepath, 'r', encoding='utf-8-sig') as f:
                        lines = f.readlines()
                except Exception as e:
                    print(f"Fehler beim Lesen von {old_filepath}: {e}")
                    continue

                if lines and lines[0].strip() == "l_english:":
                    lines[0] = "l_german:\n"
                else:
                    # Überspringe Dateien, die nicht den Kriterien entsprechen
                    continue

                new_filename = filename.replace("_english.yml", "_german.yml")
                new_filepath = os.path.join(root, new_filename)

                try:
                    # === ÄNDERUNG HIER ===
                    # Schreibe die neue Datei mit 'utf-8-sig', um das BOM am Anfang hinzuzufügen
                    with open(new_filepath, 'w', encoding='utf-8-sig') as f:
                        f.writelines(lines)
                except Exception as e:
                    print(f"Fehler beim Schreiben in {new_filepath}: {e}")
                    continue

                try:
                    os.remove(old_filepath)
                    files_processed += 1
                except Exception as e:
                    print(f"Fehler beim Löschen von {old_filepath}: {e}")

    print("\n--- Prozess abgeschlossen ---")
    if files_processed > 0:
        print(f"✨ Insgesamt wurden {files_processed} Dateien erfolgreich bearbeitet.")
    else:
        print("Es wurden keine Dateien gefunden, die den Kriterien entsprachen.")


if __name__ == '__main__':
    if not folder_to_update or not os.path.isdir(folder_to_update):
         print("🛑 FEHLER: FOLDER_PATH in der .env-Datei ist nicht gesetzt oder kein gültiger Ordner.")
    else:
        translate_lotr_files(folder_to_update)