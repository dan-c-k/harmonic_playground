"""
Sample: List existing Aristotle projects and check their status.

This is useful for monitoring submitted problems and retrieving results.
"""

import asyncio
import os

from dotenv import load_dotenv

import aristotlelib

load_dotenv()

API_KEY = os.environ["ARISTOTLE_API_KEY"]


async def main():
    aristotlelib.set_api_key(API_KEY)

    print("Fetching Aristotle projects...\n")

    projects, pagination_key = await aristotlelib.Project.list_projects(limit=10)

    if not projects:
        print("No projects found. Submit a problem first!")
        return

    for p in projects:
        print(f"  ID: {p.project_id}")
        print(f"  Status: {p.status}")
        print(f"  Created: {p.created_at}")
        if p.description:
            print(f"  Description: {p.description}")
        if p.percent_complete is not None:
            print(f"  Progress: {p.percent_complete}%")
        print()

    if pagination_key:
        print(f"More projects available (pagination key: {pagination_key})")


if __name__ == "__main__":
    asyncio.run(main())
