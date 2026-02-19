
Personal Finance AI

This is a compact, Excel-friendly subset of the original project. It focuses on quick CSV/XLSX import/export, simple categorization rules, and a tiny sync API so you can edit transactions in Excel and push changes back.

Notes and next steps:
- Editable roundtrip: export XLSX, edit `category`, re-upload to apply edits.
- For live Excel integration consider `xlwings` (optional, included in `requirements.txt`).
- Add tests/CI and a small web UI for bulk editing if you want to scale this beyond a single-user local tool.

