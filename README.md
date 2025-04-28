# ParametricTextUpdate Fusion 360 Add-In

## Purpose

ParametricTextUpdate is a Fusion 360 add-in designed to automate the process of cutting text (or other shapes) from plate components. It allows users to:
- Select multiple plate/text component pairs in a user-friendly dialog.
- Save and load sets of component pairs for repeated use.
- Quickly update and re-run the combine/cut operation for all selected pairs.

This add-in is especially useful for workflows where you need to create signs, stencils, or other designs where text or shapes are cut out of plates, and the number of bodies or text can change parametrically.

## Features
- Add as many plate/text pairs as needed.
- Save and load your selection sets for future sessions.
- User-friendly interface with tooltips and reminders.
- Explanation dialog for why manual selection is required (due to Fusion 360 API limitations).

## Usage
1. Install the add-in in Fusion 360 (place the folder in your AddIns directory).
2. Start the add-in from the Add-Ins dialog.
3. In the Solid workspace, find the **Combine Cut** button in the **Modify** panel.
4. Use the dialog to select plate and text components, add/remove pairs, and run the combine/cut operation.
5. Use the Save/Load buttons to store and restore your selection sets.

## .env Location
This project does **not** require a `.env` file for normal operation. If you wish to use environment variables for development or deployment, place your `.env` file in the root directory of the repository. For public publishing, ensure that your `.env` file is **not** committed to the repository (add `.env` to your `.gitignore`).

## Publishing to GitHub
- Remove any sensitive or personal data before publishing.
- Add `.env` to your `.gitignore` if you use one.
- Commit all source files, the `README.md`, and your `plate_text_pairs.json` example (if desired).

---

**Enjoy automating your parametric text cutting workflow in Fusion 360!** 