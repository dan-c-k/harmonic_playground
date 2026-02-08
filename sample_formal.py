"""
Sample: Submit a formal Lean 4 file with `sorry` placeholders for Aristotle to fill.

Aristotle will replace each `sorry` with a verified proof.
"""

import asyncio
import os

from dotenv import load_dotenv

import aristotlelib
from aristotlelib import ProjectInputType

load_dotenv()

API_KEY = os.environ["ARISTOTLE_API_KEY"]

# A Lean 4 theorem with `sorry` that Aristotle will prove
LEAN_CONTENT = r"""
import Mathlib

theorem add_comm_example (a b : Nat) : a + b = b + a := by
  sorry
"""


async def main():
    aristotlelib.set_api_key(API_KEY)

    print("Submitting formal Lean 4 theorem to Aristotle...")
    print(f"Input:\n{LEAN_CONTENT.strip()}\n")

    project = await aristotlelib.Project.create(
        project_input_type=ProjectInputType.FORMAL_LEAN,
    )
    print(f"Project created: {project.project_id}")
    print(f"Status: {project.status}\n")

    await project.solve(input_content=LEAN_CONTENT)
    print("Submitted, waiting for Aristotle to fill the sorry...")
    print(f"Status: {project.status}\n")

    output_path = await project.wait_for_completion(
        output_file_path="output/add_comm_solved.lean",
        polling_interval_seconds=15,
    )
    print(f"\nSolution saved to: {output_path}")

    with open(output_path) as f:
        print("\n--- Solution (Lean 4) ---")
        print(f.read())


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    asyncio.run(main())
