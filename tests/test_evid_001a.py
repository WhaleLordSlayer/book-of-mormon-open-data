"""Tests for EVID-001A dossier generation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.evid_001a.config import DataPaths, OutputPaths
from scripts.evid_001a.generator import generate_all
from scripts.evid_001a.loaders import DataStore
from scripts.evid_001a.resolver import resolve_entity_ids, retrieve_scripture_ranges

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_paths(tmp_path: Path) -> tuple[DataPaths, OutputPaths]:
    data_paths = DataPaths.from_project_root(FIXTURES)
    output_paths = OutputPaths.from_project_root(tmp_path)
    return data_paths, output_paths


def test_id_resolution(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, _ = fixture_paths
    store = DataStore(data_paths)
    result = resolve_entity_ids(
        store,
        person_ids=["person-mormon-historical"],
        group_ids=[],
        place_ids=[],
        event_ids=[],
        person_patterns=["Mormon"],
        group_patterns=[],
    )
    people = result["resolved_entities"]["people"]
    assert any(p["id"] == "person-mormon-historical" for p in people)
    assert not any(u["reference"] == "person-mormon-historical" for u in result["unresolved_entity_references"])


def test_verse_range_retrieval(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, _ = fixture_paths
    store = DataStore(data_paths)
    evidence, unresolved = retrieve_scripture_ranges(store, ["Mormon 6:1-6"], None)
    assert len(evidence) == 1
    assert "Nephites" in evidence[0]["text"]
    assert unresolved == []


def test_reynolds_retrieval(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, _ = fixture_paths
    store = DataStore(data_paths)
    from scripts.evid_001a.resolver import retrieve_reynolds

    passages, unresolved = retrieve_reynolds(store, ["Mormon"], ["Mormon"])
    assert len(passages) >= 1
    assert unresolved == []


def test_deterministic_generation(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, output_paths = fixture_paths
    generate_all(data_paths, output_paths)
    first = (output_paths.dossier_dir / "mormon-narrator-vs-historical-actor.json").read_text()
    generate_all(data_paths, output_paths)
    second = (output_paths.dossier_dir / "mormon-narrator-vs-historical-actor.json").read_text()
    assert first == second


def test_all_dossiers_generated(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, output_paths = fixture_paths
    result = generate_all(data_paths, output_paths)
    assert result["dossier_count"] == 18
    for path in output_paths.dossier_dir.glob("*.json"):
        data = json.loads(path.read_text())
        assert "dossier_id" in data
        assert "pm_questions" in data
        assert "unresolved_evidence_references" in data


def test_json_md_agree_on_metadata(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, output_paths = fixture_paths
    generate_all(data_paths, output_paths)
    json_data = json.loads(
        (output_paths.dossier_dir / "mormon-narrator-vs-historical-actor.json").read_text()
    )
    md_text = (output_paths.dossier_dir / "mormon-narrator-vs-historical-actor.md").read_text()
    assert json_data["dossier_id"] in md_text
    assert json_data["title"] in md_text
    for q in json_data["pm_questions"]:
        assert q in md_text


def test_no_duplicate_evidence_ids(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, output_paths = fixture_paths
    generate_all(data_paths, output_paths)
    json_data = json.loads(
        (output_paths.dossier_dir / "mormon-narrator-vs-historical-actor.json").read_text()
    )
    evidence_ids = [m.get("evidence_id") for m in json_data.get("exact_mentions", []) if m.get("evidence_id")]
    assert len(evidence_ids) == len(set(evidence_ids))


def test_index_written(fixture_paths: tuple[DataPaths, OutputPaths]) -> None:
    data_paths, output_paths = fixture_paths
    generate_all(data_paths, output_paths)
    index = json.loads(output_paths.index_json.read_text())
    assert index["dossiers_completed"] == 18
    assert index["task_id"] == "EVID-001A"
