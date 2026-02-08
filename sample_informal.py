"""
Sample: Submit an informal (natural language) math problem to Aristotle.

Aristotle will autoformalize the problem into Lean 4 and generate a verified proof.
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

PROBLEM = r"""
Prove that for all natural numbers n, the sum 0 + 1 + 2 + ... + n equals n * (n + 1) / 2.
"""


async def main():
    aristotlelib.set_api_key(API_KEY)
    os.makedirs("output", exist_ok=True)

    print("=" * 60)
    print("  Aristotle — Informal Math Problem")
    print("=" * 60)
    print(f"\nProblem: {PROBLEM.strip()}\n")

    # Try real API first
    print("Connecting to Aristotle API...")
    ok, result = await try_real_api(
        aristotlelib.Project.create(project_input_type=ProjectInputType.INFORMAL)
    )

    if ok:
        project = result
        print(f"[LIVE] Project created: {project.project_id}")
        print(f"[LIVE] Status: {project.status}\n")

        await project.solve(input_content=PROBLEM)
        print("[LIVE] Problem submitted, waiting for Aristotle to solve...")

        output_path = await project.wait_for_completion(
            output_file_path="output/gauss_sum.lean",
            polling_interval_seconds=15,
        )
        print(f"\nSolution saved to: {output_path}")
        with open(output_path) as f:
            solution = f.read()
    else:
        print(f"[MOCK] API unreachable ({result[:60]}...)")
        print("[MOCK] Falling back to mock mode for demonstration\n")

        proj = await mock_create_project(project_input_type="INFORMAL")
        print(f"Project created: {proj['project_id']}")

        await mock_solve(proj["project_id"], PROBLEM)
        print("Problem submitted, waiting for Aristotle to solve...\n")

        solution = await mock_wait_for_completion(
            proj["project_id"], PROBLEM, proof_key="informal_default"
        )

        output_path = "output/gauss_sum.lean"
        with open(output_path, "w") as f:
            f.write(solution)
        print(f"\nSolution saved to: {output_path}")

    print("\n--- Solution (Lean 4) ---")
    print(solution)


if __name__ == "__main__":
    asyncio.run(main())
