"""
Sample: List existing Aristotle projects and check their status.

Falls back to mock mode if the API is unreachable.
"""

import asyncio
import os

from dotenv import load_dotenv

import aristotlelib
from aristotle_mock import mock_list_projects, try_real_api

load_dotenv()

API_KEY = os.environ["ARISTOTLE_API_KEY"]


async def main():
    aristotlelib.set_api_key(API_KEY)

    print("=" * 60)
    print("  Aristotle — Project List")
    print("=" * 60)

    print("\nFetching projects...")
    ok, result = await try_real_api(
        aristotlelib.Project.list_projects(limit=10)
    )

    if ok:
        projects, pagination_key = result
        print(f"[LIVE] Found {len(projects)} project(s)\n")
        for p in projects:
            print(f"  ID:      {p.project_id}")
            print(f"  Status:  {p.status}")
            print(f"  Created: {p.created_at}")
            if p.description:
                print(f"  Desc:    {p.description}")
            if p.percent_complete is not None:
                print(f"  Progress: {p.percent_complete}%")
            print()
        if pagination_key:
            print(f"More projects available (pagination key: {pagination_key})")
    else:
        print(f"[MOCK] API unreachable ({result[:60]}...)")
        print("[MOCK] Showing mock project data\n")
        projects = await mock_list_projects()
        for p in projects:
            print(f"  ID:       {p['project_id']}")
            print(f"  Status:   {p['status']}")
            print(f"  Created:  {p['created_at']}")
            if p.get("description"):
                print(f"  Desc:     {p['description']}")
            if p.get("percent_complete") is not None:
                print(f"  Progress: {p['percent_complete']}%")
            print()

    if not ok:
        print("(These are simulated results. Run outside this sandbox for live data.)")


if __name__ == "__main__":
    asyncio.run(main())
