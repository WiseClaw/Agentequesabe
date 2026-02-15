import os

CONTEXT_FILE = "/a0/usr/workdir/data/live_context.md"

def get_live_context():
    try:
        if os.path.exists(CONTEXT_FILE):
            with open(CONTEXT_FILE, "r") as f:
                return f.read()
    except Exception as e:
        print(f"[CONTEXT ERROR] Could not read context: {e}")
    return ""

def update_context(new_text):
    try:
        with open(CONTEXT_FILE, "a") as f:
            f.write("\n" + str(new_text))
    except Exception as e:
        print(f"[CONTEXT ERROR] Could not update context: {e}")