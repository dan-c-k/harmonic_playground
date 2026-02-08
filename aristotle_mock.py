"""
Mock client for the Aristotle API.

Provides realistic simulated responses when the real API is unreachable
(e.g., in sandboxed environments). Set ARISTOTLE_MOCK=true to force mock mode,
or let the sample scripts auto-detect and fall back.
"""

import asyncio
import os
import uuid
from datetime import datetime, timezone

MOCK_PROOFS = {
    "gauss_sum": """\
import Mathlib

theorem gauss_sum (n : Nat) : 2 * (Finset.range (n + 1)).sum id = n * (n + 1) := by
  induction n with
  | zero => simp
  | succ n ih =>
    simp [Finset.sum_range_succ]
    omega
""",
    "add_comm": """\
import Mathlib

theorem add_comm_example (a b : Nat) : a + b = b + a := by
  omega
""",
    "informal_default": """\
import Mathlib

-- Aristotle autoformalized from natural language:
-- "Prove that for all natural numbers n, the sum 0 + 1 + 2 + ... + n
--  equals n * (n + 1) / 2."

theorem sum_first_n (n : Nat) : 2 * (Finset.range (n + 1)).sum id = n * (n + 1) := by
  induction n with
  | zero =>
    simp
  | succ k ih =>
    rw [Finset.sum_range_succ]
    simp [Nat.mul_add, Nat.add_mul]
    omega
""",
}


def is_mock_mode() -> bool:
    return os.environ.get("ARISTOTLE_MOCK", "").lower() in ("true", "1", "yes")


async def mock_create_project(project_input_type=None):
    """Simulate project creation."""
    return {
        "project_id": f"mock-{uuid.uuid4().hex[:12]}",
        "status": "NOT_STARTED",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


async def mock_solve(project_id: str, content: str):
    """Simulate submitting a problem."""
    await asyncio.sleep(0.5)  # Simulate network latency
    return {"status": "QUEUED"}


async def mock_wait_for_completion(project_id: str, content: str, proof_key: str = "informal_default"):
    """Simulate waiting for proof completion with progress updates."""
    stages = [
        ("QUEUED", "Waiting in queue...", 1.0),
        ("IN_PROGRESS", "Aristotle is searching for a proof...", 1.5),
        ("IN_PROGRESS", "Formalizing into Lean 4...", 1.0),
        ("IN_PROGRESS", "Verifying proof in Lean...", 1.0),
        ("COMPLETE", "Proof verified!", 0),
    ]
    for status, msg, delay in stages:
        print(f"  [{status}] {msg}")
        if delay:
            await asyncio.sleep(delay)

    return MOCK_PROOFS.get(proof_key, MOCK_PROOFS["informal_default"])


async def mock_list_projects():
    """Simulate listing projects."""
    now = datetime.now(timezone.utc)
    return [
        {
            "project_id": "mock-a1b2c3d4e5f6",
            "status": "COMPLETE",
            "created_at": now.isoformat(),
            "description": "Gauss sum formula (informal)",
            "percent_complete": 100,
        },
        {
            "project_id": "mock-f6e5d4c3b2a1",
            "status": "COMPLETE",
            "created_at": now.isoformat(),
            "description": "Nat.add_comm (formal Lean)",
            "percent_complete": 100,
        },
    ]


async def try_real_api(coro):
    """Try a real API call; return (True, result) or (False, error)."""
    try:
        result = await coro
        return True, result
    except Exception as e:
        err = str(e)
        if "403" in err or "Proxy" in err or "name resolution" in err or "Connection" in err:
            return False, err
        raise
