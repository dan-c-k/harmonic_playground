"""
Sample: Submit a formal Lean 4 file with `sorry` placeholders for Aristotle to fill.

Aristotle will replace each `sorry` with a verified proof.
Falls back to mock mode if the API is unreachable.
"""

import asyncio
import os

from dotenv import load_dotenv

import aristotlelib
from aristotlelib import ProjectInputType
from aristotle_mock import mock_create_project, mock_solve, mock_wait_for_completion, try_real_api

load_dotenv()

API_KEY = os.environ["ARISTOTLE_API_KEY"]

LEAN_CONTENT = r"""
import Mathlib

theorem add_comm_example (a b : Nat) : a + b = b + a := by
  sorry
"""


async def main():
    aristotlelib.set_api_key(API_KEY)
    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("  Aristotle — Formal Lean 4 Proof")
    print("=" * 60)
    print(f"\nInput:\n{LEAN_CONTENT.strip()}\n")

    # Try real API first
    print("Connecting to Aristotle API...")
    ok, result = await try_real_api(
        aristotlelib.Project.create(project_input_type=ProjectInputType.FORMAL_LEAN)
    )

    if ok:
        project = result
        print(f"[LIVE] Project created: {project.project_id}")
        print(f"[LIVE] Status: {project.status}\n")

        await project.solve(input_content=LEAN_CONTENT)
        print("[LIVE] Submitted, waiting for Aristotle to fill the sorry...")

        output_path = await project.wait_for_completion(
            output_file_path="output/add_comm_solved.lean",
            polling_interval_seconds=15,
        )
        print(f"\nSolution saved to: {output_path}")
        with open(output_path) as f:
            solution = f.read()
    else:
        print(f"[MOCK] API unreachable ({result[:60]}...)")
        print("[MOCK] Falling back to mock mode for demonstration\n")

        proj = await mock_create_project(project_input_type="FORMAL_LEAN")
        print(f"Project created: {proj['project_id']}")

        await mock_solve(proj["project_id"], LEAN_CONTENT)
        print("Submitted, waiting for Aristotle to fill the sorry...\n")

        solution = await mock_wait_for_completion(
            proj["project_id"], LEAN_CONTENT, proof_key="add_comm"
        )

        output_path = "output/add_comm_solved.lean"
        with open(output_path, "w") as f:
            f.write(solution)
        print(f"\nSolution saved to: {output_path}")

    print("\n--- Solution (Lean 4) ---")
    print(solution)


if __name__ == "__main__":
    asyncio.run(main())
