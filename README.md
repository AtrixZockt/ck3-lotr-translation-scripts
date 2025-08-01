# CK3 LotR Mod - Automatisierte Übersetzungs-Skripte

Dieses Repository enthält eine Sammlung von Python-Skripten zur teilautomatisierten Übersetzung von Lokalisierungsdateien für eine "Herr der Ringe"-Mod für das Spiel Crusader Kings 3. Die Skripte nutzen die Google Gemini API, um englische Texte ins Deutsche zu übersetzen, wobei sie speziell auf die komplexe Syntax und den Kontext von Paradox-Spieldateien ausgelegt sind.

-----

## 🚀 Features

  * **Intelligente Übersetzung:** Nutzt die Gemini API mit einem hoch entwickelten Prompt, der den Kontext (Dateiname, Tolkien- und CK3-Terminologie) versteht.
  * **Batch-Verarbeitung:** Übersetzt Zeilen in schnellen und kostengünstigen Stapeln (Batches) für maximale Effizienz.
  * **Syntax-Erkennung:** Behandelt automatisch spezielle Paradox-Syntax wie Game-Code `[...]`, Variablen `$var$`, Formatierungen `#bold`, Icons `@icon!` und Versionsnummern `key:1`.
  * **Absturzsicher & Wiederaufnehmbar:** Markiert erfolgreich übersetzte Zeilen und überspringt diese bei einem Neustart, sodass der Fortschritt nie verloren geht.
  * **Selbstheilend:** Schaltet bei seltenen API-Fehlern automatisch in einen langsameren, aber sichereren Einzelmodus, um den Prozess am Laufen zu halten.
  * **Fehler-Protokollierung:** Schreibt Zeilen, die auch im Einzelmodus nicht übersetzt werden können, in eine `translation_errors.log`-Datei für die manuelle Nachbearbeitung.
  * **Hilfsskripte:** Enthält separate Werkzeuge für die Dateivorbereitung, Bereinigung und spezielle Korrekturen.

-----

## ⚙️ Setup & Konfiguration

### 1\. Voraussetzungen

Stelle sicher, dass Python 3 auf deinem System installiert ist. Installiere dann die notwendigen Python-Bibliotheken über das Terminal:

```sh
pip install python-dotenv google-generativeai
```

### 2\. Konfigurations-Datei (`.env`)

Die Skripte laden vertrauliche Informationen (deinen API-Key und Dateipfade) aus einer `.env`-Datei, damit diese nicht auf GitHub landen.

Erstelle im Hauptverzeichnis deines Projekts eine Datei namens `.env` und füge Folgendes ein:

```ini
# Dein API-Key von Google AI Studio
GEMINI_API_KEY="DEIN_ECHTER_API_KEY"

# Der vollständige Pfad zum Hauptordner deiner Mod-Lokalisierungsdateien
FOLDER_PATH="C:/Pfad/zu/deinem/Mod-Ordner"

# Der vollständige Pfad zur .yml Datei dessen Artikel korrigiert werden sollen
FIX_ARTICLES_FILE_PATH="C:/Pfad/zu/deiner/YML-Datei"
```

**Wichtig:** Verwende in der `.env`-Datei normale Schrägstriche (`/`) oder doppelte Backslashes (`\\`) für den Pfad.

### 3\. Git-Konfiguration (`.gitignore`)

Um sicherzustellen, dass deine `.env`-Datei niemals auf GitHub hochgeladen wird, erstelle eine Datei namens `.gitignore` im Hauptverzeichnis und füge Folgendes ein:

```
# Ignoriere die Datei mit den Geheimnissen
.env

# Ignoriere Log-Dateien
*.log
```

-----

## ➡️ Empfohlener Arbeitsablauf (Workflow)

Die Skripte sollten in einer bestimmten Reihenfolge verwendet werden, um ein sauberes Ergebnis zu erzielen.

**Schritt 1: (Einmalig) Dateien vorbereiten**

  * Führe `update_files.py` aus, um deine englischen Originaldateien zu kopieren, sie in `_german.yml` umzubenennen und den Header von `l_english:` auf `l_german:` zu ändern.

**Schritt 2: Hauptübersetzung**

  * Führe das Hauptskript `translate_files.py` aus. Es wird durch alle Dateien gehen und die Massenübersetzung durchführen. Dieser Prozess kann je nach Umfang der Mod einige Zeit dauern. Du kannst ihn jederzeit anhalten und neu starten.

**Schritt 3: Spezialkorrektur für Artikel**

  * Nachdem die Hauptübersetzung fertig ist, öffne das Skript `fix_articles.py`.
  * Passe den Pfad in diesem Skript so an, dass er **exakt** auf die übersetzte `titles`-Datei zeigt (z.B. `lotr_titles_l_german.yml`).
  * Führe `fix_articles.py` aus, um die grammatikalisch korrekten deutschen Artikel (`der, die, das`) automatisch einfügen zu lassen.

**Schritt 4: Manuelle Nachbearbeitung**

  * Prüfe, ob eine `translation_errors.log`-Datei erstellt wurde, und korrigiere die darin gelisteten Zeilen manuell.
  * Überprüfe die Übersetzungen stichprobenartig im Spiel auf Kontext, Tonalität und Länge.

-----

## 📜 Beschreibung der Skripte

  * **`translate_files.py`**

      * Das Herzstück des Projekts. Führt die intelligente, absturzsichere Batch-Übersetzung durch.

  * **`fix_articles.py`**

      * Ein spezialisiertes Werkzeug zur Korrektur der deutschen Artikel (`der, die, das`) in Dateien, die Platzhalter wie `$the_$` verwenden (hauptsächlich die `titles`-Datei).

  * **`update_files.py`**

      * Ein einmaliges Setup-Skript, das die englischen Quelldateien für die Übersetzung ins Deutsche vorbereitet.

  * **`cleanup_files.py`**

      * **(Optional & Vorsicht\!)** Ein gefährliches Werkzeug, das alle `.yml`-Dateien in den Ordnern löscht, die **nicht** mit `lotr_` beginnen. Nützlich zum Aufräumen, aber mit Vorsicht zu genießen.

  * **Andere Skripte (`reset_markers.py`, `repair_quotes.py`, etc.)**

      * Im Laufe der Entwicklung wurden verschiedene Reparatur-Skripte erstellt. Diese werden für den normalen Arbeitsablauf nicht benötigt, können aber zur Fehlerbehebung bei Problemen mit alten Übersetzungs-Durchläufen nützlich sein.
