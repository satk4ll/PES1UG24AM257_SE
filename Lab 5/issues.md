# Static Code Analysis Issues and Fixes

| Issue | Tool | Fix |
|---|---|---|
| Mutable default argument | Pylint | Changed default to None and initialized the list inside the function. |
| SQL query formatting | Security review | Used parameterized SQL queries. |
| Unsafe pickle deserialization | Bandit/security review | Replaced pickle with JSON serialization. |
| Broad exception handling | Pylint | Caught sqlite3.Error specifically. |
| Empty catalog handling | Code review | Added a check before selecting a random song. |
| Naming and formatting | Pylint/Flake8 | Improved naming and code formatting. |

## Verification
Pylint score: 10.00/10.
Bandit: No issues identified in the latest report.
Flake8: Verify using `python -m flake8 music_catalog.py`.
