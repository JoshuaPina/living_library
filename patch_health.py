import sys
content = open("main.py").read()
content = content.replace('return {"status": "unhealthy", "error": str(e)}', 'logger.exception("Health check failed")\n            return {"status": "unhealthy", "error": "Internal server error"}')
with open("main.py", "w") as f:
    f.write(content)
