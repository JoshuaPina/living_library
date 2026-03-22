import os
filepath = ".jules/sentinel.md"
content = """## 2025-03-08 - Prevent Information Disclosure in 500 Responses
**Vulnerability:** API endpoints were catching general exceptions (`Exception as e`) and returning the raw stringified exception (`str(e)`) directly in the HTTP 500 response payload (`HTTPException(status_code=500, detail=str(e))`). This could potentially leak sensitive internal information, stack traces, database schema details, or system configurations to an attacker.
**Learning:** Returning detailed server-side error messages to the client is a security risk known as Information Disclosure. Even if the error seems harmless, it can provide attackers with clues about the underlying technology stack or system state.
**Prevention:** Never expose raw exception details (like `str(e)`) in API responses. Log detailed exceptions server-side using the `logging` module and return generic error messages (e.g., 'Internal server error') to the client.
"""
if os.path.exists(filepath):
    # check if it starts with the entry
    with open(filepath, "r") as f:
        existing = f.read()
    if not existing.startswith("## "):
        with open(filepath, "a") as f:
            f.write("\n" + content)
    else:
        # It's our only entry.
        pass
else:
    with open(filepath, "w") as f:
        f.write(content)
