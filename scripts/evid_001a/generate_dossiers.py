#!/usr/bin/env python3
"""CLI entrypoint for EVID-001A dossier generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.evid_001a.config import DEFAULT_PROJECT_ROOT, DataPaths, OutputPaths
from scripts.evid_001a.generator import generate_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate EVID-001A priority evidence dossiers.")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=DEFAULT_PROJECT_ROOT,
        help="Project root (default: repository root)",
    )
    args = parser.parse_args(argv)

    data_paths = DataPaths.from_project_root(args.project_root)
    output_paths = OutputPaths.from_project_root(args.project_root)
    result = generate_all(data_paths, output_paths)

    print(f"Generated {result['dossier_count']} dossiers")
    print(f"Index: {result['index_path']}")
    print(f"Summary: {result['summary_path']}")
    if result["load_errors"]:
        print("Source load errors:", file=sys.stderr)
        for key, err in sorted(result["load_errors"].items()):
            print(f"  {key}: {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
