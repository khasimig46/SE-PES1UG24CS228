# Issues Found – library_catalog_system.py

Baseline: Pylint 5.53/10 · Bandit 2 High / 1 Medium / 2 Low · Flake8 5 errors

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| OS command injection via `os.system` (B605) | Security – High | 58 | `os.system("echo ... " + filename)` builds a shell command from a variable; a filename like `x; rm -rf ~` runs arbitrary commands. | Removed the shell call entirely; use `print()`. If a subprocess is ever needed, use `subprocess.run([...])` with a list and no shell. |
| Weak MD5 hash for patron ID (B324) | Security – High | 47 | MD5 is broken and unsuitable for identifying/protecting patron data. | Switched to `hashlib.sha256`. |
| `eval()` on caller-supplied string (B307 / W0123) | Security – Medium | 40–43 | `calculate_fine(days, calc_expr)` evaluates arbitrary Python, allowing code execution. Also left `days` as an "unused" variable. | Replaced the expression parameter with a numeric `daily_rate` (constant `FINE_PER_DAY = 2.0`), validated `days_overdue >= 0`. |
| Returning a book that was never issued adds stock (logic bug, not flagged by tools) | Logic bug – Medium | 23–27 | Running the program raised B02 from 1 to 2 copies because `return_book("B02")` blindly did `+= 1`. | Added a `total` field per book; `return_book` refuses returns when `copies >= total` and returns True/False. |
| Bare `except: pass` hides errors (E722, W0702, B110) | Quality – Medium | 24–27 | Swallows every exception, including typos and unknown IDs, so failures are silent. | Replaced with an explicit `catalog.get()` check and a boolean result. |
| Mutable default argument `active_issues=[]` (W0102) | Quality – Medium | 15 | The list is created once and shared across all calls, so issue logs leak between callers. | Default is `None`; append only when a list is supplied. |
| Hard-coded secret `librarian_key`, printed to console | Security – Medium | 62, 70 | Token is in source control and echoed to the output. | Read from the `LIBRARIAN_KEY` environment variable; print only whether it is configured. |
| Insecure random for PIN (B311) | Security – Low | 51 | `random.randint` is predictable; unsuitable for PINs. | Use `secrets.randbelow(9000) + 1000`. |
| File opened without `with` / encoding (R1732, W1514) | Quality – Low | 55–57 | File may not close on error; encoding is platform-dependent. | Use `with open(..., encoding="utf-8")` and the `csv` module. |
| Unused import `csv` (F401), unused variables `late_fee`, `days` (F841) | Style – Low | 6, 31, 41 | Dead code that confuses readers. | Used `csv` for the real export; removed dead variables. |
| `== None` comparison (E711, C0121) | Style – Low | 32 | Should use identity check for `None`. | Use `is None` / `is not None`. |
| Redundant if/else returning booleans (R1703, R1705) | Style – Low | 34–37 | Verbose conditional. | `return book is not None and book["copies"] > 0`. |
| camelCase `issueBook`, `%` formatting (C0103, C0209) | Style – Low | 15, 19 | Violates PEP 8 naming; old-style formatting. | Renamed to `issue_book`; use f-string. |
| Missing docstrings (C0116) | Style – Low | all functions | No documentation on public functions. | Added one-line docstrings. |
| `main()` runs on import | Style – Low | 74 | Importing the module triggers the demo. | Added `if __name__ == "__main__":` guard. |

**After fixes:** Pylint 10.00/10 · Bandit 0 issues · Flake8 clean
