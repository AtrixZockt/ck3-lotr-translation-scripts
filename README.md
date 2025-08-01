# CK3 LotR Mod - Automated Translation Scripts

This repository contains a collection of Python scripts designed to semi-automate the translation of localization files for a "[Lord of the Rings](https://steamcommunity.com/sharedfiles/filedetails/?id=2291024373)" mod for the game Crusader Kings 3. The scripts use the Google Gemini API to translate English text to German, specifically tailored to handle the complex syntax and context of Paradox game files.

-----

## 🚀 Features

  * **Intelligent Translation:** Uses the Gemini API with a highly-developed prompt that understands context from the filename, as well as Lord of the Rings and CK3 terminology.
  * **Batch Processing:** Translates lines in fast and cost-effective batches for maximum efficiency.
  * **Syntax Handling:** Automatically handles special Paradox syntax, including game code `[...]`, variables `$var$`, formatting codes `#bold`, icons `@icon!`, and version numbers `key:1`.
  * **Crash-Proof & Resumable:** Marks successfully translated lines and skips them on restart, so progress is never lost.
  * **Self-Healing:** Automatically switches to a slower, safer single-line mode if a batch fails, keeping the process running.
  * **Error Logging:** Writes lines that fail to translate even in single-line mode to an `translation_errors.log` file for manual review.
  * **Helper Scripts:** Includes separate tools for file preparation, cleanup, and specific grammar corrections.

-----

## ⚙️ Setup & Configuration

### 1\. Prerequisites

Ensure you have Python 3 installed on your system. Then, install the necessary Python libraries by running the following command in your terminal:

```sh
pip install python-dotenv google-generativeai
```

### 2\. Configuration File (`.env`)

The scripts load sensitive information (your API key and file paths) from a `.env` file to keep them out of your code and off of GitHub.

Create a new file named `.env` in the root directory of your project and add the following content:

```ini
# Your API Key from Google AI Studio
GEMINI_API_KEY="YOUR_REAL_API_KEY"

# The full path to the main folder of your mod's localization files
FOLDER_PATH="C:/Path/To/Your/Mod/Folder"

# The full path to the .yml file where the articles need to be fixed
FIX_ARTICLES_FILE_PATH="C:/Path/To/Your/YML-File"
```

**Important:** Use forward slashes (`/`) or double backslashes (`\\`) for the path in the `.env` file.

### 3\. Git Configuration (`.gitignore`)

To ensure your `.env` file is never uploaded to GitHub, create a file named `.gitignore` in the root directory and add the following:

```
# Ignore the file with secrets
.env

# Ignore log files
*.log
```

-----

## ➡️ Recommended Workflow

The scripts should be used in a specific order to achieve a clean result.

**Step 1: (One-Time) Prepare Files**

  * Run `update_files.py` to copy your original English files, rename them to end in `_german.yml`, and change the header from `l_english:` to `l_german:`.

**Step 2: Main Translation**

  * Run the main script, `translate_files.py`. It will iterate through all files and perform the bulk translation. This process can take some time depending on the size of the mod. You can stop and restart it at any time.

**Step 3: Special Article Correction**

  * After the main translation is complete, open the `fix_articles.py` script.
  * Adjust the path in this script to point **exactly** to your translated `titles` file (e.g., `lotr_titles_l_german.yml`).
  * Run `fix_articles.py` to automatically insert the correct German articles (`der, die, das`).

**Step 4: Manual Review**

  * Check if a `translation_errors.log` file was created and manually correct any lines listed within it.
  * Spot-check the translations in-game for context, tone, and length.

-----

## 📜 Script Descriptions

  * **`translate_files.py`**

      * The core of the project. This script performs the intelligent, crash-proof, batch translation.

  * **`fix_articles.py`**

      * A specialized tool to correct German articles (`der, die, das`) in files that use placeholders like `$the_$` (primarily the `titles` file).

  * **`update_files.py`**

      * A one-time setup script that prepares the source English files for translation.

  * **`cleanup_files.py`**

      * **(Optional & Use with Caution\!)** A dangerous tool that deletes all `.yml` files in the folder that do **not** start with `lotr_`. Useful for cleaning up, but be careful.

  * **Other Scripts (`reset_markers.py`, `repair_quotes.py`, etc.)**

      * Various repair scripts were created during the development process. These are not needed for the standard workflow but can be useful for troubleshooting issues from previous translation runs.
