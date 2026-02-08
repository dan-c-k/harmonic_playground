"""
Sample: Submit an informal (natural language) math problem to Aristotle.

Aristotle will autoformalize the problem into Lean 4 and generate a verified proof.
"""

import asyncio
import os

from dotenv import load_dotenv

import aristotlelib
from aristotlelib import ProjectInputType

load_dotenv()

API_KEY = os.environ["ARISTOTLE_API_KEY"]

PROBLEM = r"""
Prove that for all natural numbers n, the sum 0 + 1 + 2 + ... + n equals n * (n + 1) / 2.
"""


async def main():
    aristotlelib.set_api_key(API_KEY)

    print("Submitting informal math problem to Aristotle...")
    print(f"Problem: {PROBLEM.strip()}\n")

    # Create an informal project and submit
    project = await aristotlelib.Project.create(
        project_input_type=ProjectInputType.INFORMAL,
    )
    print(f"Project created: {project.project_id}")
    print(f"Status: {project.status}\n")

    # Submit the problem as inline content
    await project.solve(input_content=PROBLEM)
    print("Problem submitted, waiting for Aristotle to solve...")
    print(f"Status: {project.status}\n")

    # Poll for completion
    output_path = await project.wait_for_completion(
        output_file_path="output/gauss_sum.lean",
        polling_interval_seconds=15,
    )
    print(f"\nSolution saved to: {output_path}")

    # Print the solution
    with open(output_path) as f:
        print("\n--- Solution (Lean 4) ---")
        print(f.read())


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    asyncio.run(main())
