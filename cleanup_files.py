import os
from dotenv import load_dotenv

load_dotenv()

folder_to_cleanup = os.getenv("FOLDER_PATH")

def delete_non_lotr_yml_files(main_folder):
    """
    Löscht rekursiv alle .yml-Dateien in einem Ordner und dessen Unterordnern,
    deren Namen NICHT mit 'lotr_' beginnen.
    """
    files_to_delete = []

    # Schritt 1: Sicher alle zu löschenden Dateien sammeln, ohne sie sofort zu löschen.
    print("Suche nach zu löschenden Dateien...")
    for root, _, files in os.walk(main_folder):
        for filename in files:
            # Prüft, ob die Datei auf .yml endet UND NICHT mit lotr_ beginnt
            if filename.endswith(".yml") and not filename.startswith("lotr_"):
                filepath = os.path.join(root, filename)
                files_to_delete.append(filepath)

    if not files_to_delete:
        print("\n✅ Keine .yml-Dateien gefunden, die den Kriterien entsprechen. Nichts zu tun.")
        return

    # Dem Benutzer genau zeigen, was gelöscht wird
    print("\nFolgende Dateien wurden zum Löschen markiert:")
    for filepath in files_to_delete:
        print(f"  - {filepath}")

    # Schritt 2: Eine explizite Sicherheitsabfrage
    print("\n---------------------------------------------------------")
    confirm = input(f"Bist du absolut sicher, dass du diese {len(files_to_delete)} Dateien endgültig löschen möchtest? (ja/nein): ")
    print("---------------------------------------------------------")
    
    if confirm.lower() != 'ja':
        print("Aktion abgebrochen. Es wurden keine Dateien gelöscht.")
        return

    # Schritt 3: Die eigentliche Löschung durchführen
    deleted_count = 0
    print("\nLösche Dateien...")
    for filepath in files_to_delete:
        try:
            os.remove(filepath)
            # print(f"  - Gelöscht: {filepath}") # Optional: Für detailliertes Logging einkommentieren
            deleted_count += 1
        except Exception as e:
            print(f"  - 🛑 FEHLER beim Löschen von {filepath}: {e}")
    
    print(f"\n✨ Prozess abgeschlossen. {deleted_count} Dateien wurden gelöscht.")


if __name__ == '__main__':
    if not folder_to_cleanup or not os.path.isdir(folder_to_cleanup):
        print("🛑 FEHLER: Bitte gib einen gültigen Pfad zum Zielordner im Skript an.")
    else:
        delete_non_lotr_yml_files(folder_to_cleanup)