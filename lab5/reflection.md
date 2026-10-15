# Reflection

> Note: replace the question headings below with the exact wording from your handout if it differs.

**1. Which issues were easiest and hardest to fix?**
Easiest were style issues (naming, `is None`, docstrings, unused imports) because the tools say exactly what to change. Hardest was `eval()` in `calculate_fine`, since removing it meant changing the function's design (a numeric rate instead of an expression string) and its caller.

**2. Did the tools report any false positives or miss anything?**
Bandit's B311 on `random` is a false positive for non-security uses, but for a PIN it is correct. More importantly, no tool caught the logic bug where returning a never-issued book increased stock; I only found it by reading the program's output. The hard-coded `librarian_key` was also not flagged by Bandit because of its variable name.

**3. How would you integrate static analysis into a real workflow?**
Run Flake8, Pylint and Bandit as pre-commit hooks locally and again in CI (e.g. GitHub Actions) so merges fail on High/Medium Bandit findings or a Pylint score below a threshold.

**4. What did you learn about the limits of static analysis?**
Tools find patterns (dangerous functions, style, unused code) but cannot know what the program is *supposed* to do. A clean 10/10 score does not mean the code is correct; tests and code review are still needed.
