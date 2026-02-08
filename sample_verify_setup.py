"""
Sample: Verify that the Aristotle SDK and API key are configured correctly.

This script checks the setup without making network calls.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def main():
    # 1. Check aristotlelib is installed
    try:
        import aristotlelib
        print(f"[OK] aristotlelib {aristotlelib.__spec__.origin}")
    except ImportError:
        print("[FAIL] aristotlelib not installed. Run: pip install aristotlelib")
        sys.exit(1)

    # 2. Check API key is set
    api_key = os.environ.get("ARISTOTLE_API_KEY", "")
    if not api_key:
        print("[FAIL] ARISTOTLE_API_KEY not set. Check your .env file.")
        sys.exit(1)

    if not api_key.startswith("arstl_"):
        print(f"[WARN] API key doesn't start with 'arstl_' — may be invalid.")
    else:
        print(f"[OK] ARISTOTLE_API_KEY is set (arstl_...{api_key[-4:]})")

    # 3. Verify SDK can be initialized
    aristotlelib.set_api_key(api_key)
    print("[OK] aristotlelib.set_api_key() succeeded")

    # 4. Check enums are available
    from aristotlelib import ProjectInputType, ProjectStatus
    print(f"[OK] Input types: {[t.name for t in ProjectInputType]}")
    print(f"[OK] Statuses: {[s.name for s in ProjectStatus]}")

    print("\nSetup verified. You're ready to submit problems to Aristotle!")
    print("  python sample_informal.py   — natural language math problem")
    print("  python sample_formal.py     — Lean 4 theorem with sorry")
    print("  python sample_list_projects.py — list your projects")


if __name__ == "__main__":
    main()
