"""Dossier case specifications for EVID-001A."""

from __future__ import annotations

from scripts.evid_001a.config import DossierSpec


def all_dossier_specs() -> list[DossierSpec]:
    """Return all 18 required dossier specifications in deterministic order."""

    return [
        DossierSpec(
            case_id="mormon-narrator-vs-historical-actor",
            title="Mormon — narrator/editor vs historical actor",
            release_goals=["explorer-person-identity", "speaker-attribution"],
            person_name_patterns=["Mormon"],
            scripture_ranges=[
                "Words of Mormon 1:1-11",
                "3 Nephi 5:8-20",
                "Mormon 1:1-5",
                "Mormon 6:6",
            ],
            pm_questions=[
                "Which Mormon mentions refer to the narrator/editor compiling the record?",
                "Which Mormon mentions refer to the historical Nephite leader and general?",
                "Should narrator/editor annotations remain separate from historical-actor Event participation?",
                "Which 005C participation proposals should be withheld pending narrator/historical separation?",
            ],
            notes="Keep historical Mormon evidence separate from narrator/editor evidence.",
        ),
        DossierSpec(
            case_id="mormon-vs-moroni",
            title="Mormon vs Moroni — contamination/confusion risk",
            release_goals=["explorer-person-identity", "retrieval-quality"],
            person_name_patterns=["Mormon", "Moroni"],
            scripture_ranges=[
                "Moroni 10:1-2",
                "Mormon 8:1-5",
                "Mormon 9:1",
            ],
            pm_questions=[
                "Where do retrieval or alias patterns risk conflating Mormon and Moroni?",
                "Are overlapping scripture contexts causing incorrect 005C endpoint attachment?",
            ],
        ),
        DossierSpec(
            case_id="nephites-broad-label",
            title="Nephites — broad civilizational label",
            release_goals=["explorer-group-continuity", "era-bounding"],
            group_name_patterns=["Nephite", "Nephites"],
            scripture_ranges=["Jacob 1:13-14", "Omni 1:12-13", "Helaman 3:49"],
            pm_questions=[
                "Should Nephites remain a single broad Group or be era-bounded?",
                "Which Event associations imply institutional vs civilizational usage?",
                "Which subordinate operational Group IDs should link to the broad Nephite label?",
            ],
            notes="Do not define eras in this dossier.",
        ),
        DossierSpec(
            case_id="lamanites-broad-label",
            title="Lamanites — broad civilizational label",
            release_goals=["explorer-group-continuity", "era-bounding"],
            group_name_patterns=["Lamanite", "Lamanites"],
            scripture_ranges=["2 Nephi 5:14", "Enos 1:20", "Alma 43:44"],
            pm_questions=[
                "Should Lamanites remain a single broad Group or be era-bounded?",
                "Which military/government/institutional contexts warrant separate operational Groups?",
            ],
        ),
        DossierSpec(
            case_id="generic-nephite-armies",
            title="Generic Nephite armies/forces",
            release_goals=["explorer-group-continuity", "military-forces"],
            group_name_patterns=["Nephite army", "armies of the Nephites", "Nephite host", "Nephite force", "army of Moroni"],
            scripture_ranges=["Alma 43:17-23", "Alma 62:40-43"],
            pm_questions=[
                "Which generic Nephite army labels denote the same force within one episode?",
                "Which widely separated army mentions must remain distinct Groups?",
            ],
            notes="Do not declare false collapse.",
        ),
        DossierSpec(
            case_id="generic-lamanite-armies",
            title="Generic Lamanite armies/forces",
            release_goals=["explorer-group-continuity", "military-forces"],
            group_name_patterns=["Lamanite army", "armies of the Lamanites", "Lamanite host", "Lamanite force"],
            scripture_ranges=["Alma 43:17-23", "Alma 47:1-4"],
            pm_questions=[
                "Which generic Lamanite army labels denote the same force within one episode?",
                "Which widely separated army mentions must remain distinct Groups?",
            ],
        ),
        DossierSpec(
            case_id="people-of-ammon-anti-nephi-lehi",
            title="People of Ammon / Anti-Nephi-Lehi — continuity and renaming",
            release_goals=["explorer-group-continuity", "group-renaming"],
            group_name_patterns=["People of Ammon", "Anti-Nephi-Lehi", "people of Anti-Nephi-Lehi", "Ammonites"],
            scripture_ranges=["Alma 23:15-18", "Alma 27:26-27", "Alma 43:11-13"],
            pm_questions=[
                "Are People of Ammon and Anti-Nephi-Lehi one continuous Group with renaming?",
                "Which migration Events mark a boundary vs continuity?",
                "Should canonical relationships encode rename vs successor Group?",
            ],
            notes="Do not merge.",
        ),
        DossierSpec(
            case_id="stripling-warriors-count",
            title="Stripling warriors — 2,000 → 2,060",
            release_goals=["explorer-group-identity", "membership-count"],
            group_name_patterns=["stripling", "two thousand", "two thousand and sixty", "2060", "2000"],
            scripture_ranges=["Alma 53:18-22", "Alma 56:10-12", "Alma 57:25-26"],
            pm_questions=[
                "Does the increase from 2,000 to 2,060 require a new Group entity?",
                "Is the count change within-episode reinforcement or a distinct formation?",
            ],
        ),
        DossierSpec(
            case_id="antipus-army-vs-stripling-warriors",
            title="Antipus's army vs stripling warriors",
            release_goals=["explorer-group-relationships", "military-forces"],
            person_name_patterns=["Antipus", "Helaman"],
            group_name_patterns=["stripling", "army of Antipus"],
            scripture_ranges=["Alma 56:1-12", "Alma 57:1-6"],
            pm_questions=[
                "How should canonical data represent the parent army and stripling sub-force?",
                "Which participation edges belong to Antipus's army vs the stripling warriors alone?",
            ],
        ),
        DossierSpec(
            case_id="king-men-vs-amalickiahites",
            title="King-men vs Amalickiahites",
            release_goals=["explorer-group-identity", "political-factions"],
            group_name_patterns=["king-men", "king men", "Amalickiahite", "Amalickiahites"],
            scripture_ranges=["Alma 46:4-10", "Alma 51:5-8", "Alma 61:3-4"],
            pm_questions=[
                "Are king-men and Amalickiahites distinct Groups or overlapping labels?",
                "Which political Events attach to which faction label?",
            ],
            notes="Do not merge.",
        ),
        DossierSpec(
            case_id="church-institution-vs-congregations",
            title="Church institution vs local congregations",
            release_goals=["explorer-group-structure", "institutional-groups"],
            group_name_patterns=["church", "congregation", "body of Christ"],
            scripture_ranges=["Mosiah 25:18-24", "Mosiah 18:17-18", "Alma 6:1-6"],
            pm_questions=[
                "Should there be one institutional Church Group with local congregation subgroups?",
                "How should Mosiah 25 be represented without collapsing local congregations?",
            ],
        ),
        DossierSpec(
            case_id="house-of-israel-joseph-conceptual",
            title="House of Israel / house of Joseph conceptual Groups",
            release_goals=["explorer-group-ontology", "conceptual-groups"],
            group_name_patterns=["house of Israel", "house of Joseph", "seed of Joseph"],
            scripture_ranges=["1 Nephi 15:12-14", "3 Nephi 20:25-27", "2 Nephi 3:3-5"],
            pm_questions=[
                "Which conceptual Group labels are operational vs genealogical metaphor?",
                "Which 005C military/political proposals inappropriately attach to conceptual Groups?",
            ],
            notes="Do not make theological judgments.",
        ),
        DossierSpec(
            case_id="akish-oath-vs-army",
            title="Akish oath/secret group vs army",
            release_goals=["explorer-group-identity", "secret-combinations"],
            person_name_patterns=["Akish"],
            group_name_patterns=["oath", "secret", "Akish"],
            scripture_ranges=["Ether 8:10-18", "Ether 9:1-6", "Ether 9:26-33"],
            pm_questions=[
                "Should the oath/combination organization and Akish's military force remain separate Groups?",
                "Which Events belong to secret combination activity vs open warfare?",
            ],
            notes="Do not merge oath group and army.",
        ),
        DossierSpec(
            case_id="prophecy-subject-vs-participant",
            title="Prophecy subject vs present participant",
            release_goals=["explorer-relationship-semantics", "prophecy-edges"],
            scripture_ranges=["1 Nephi 22:1-6", "2 Nephi 25:17-19", "3 Nephi 21:1-7"],
            pm_questions=[
                "Which 005C candidates confuse prophetic subject with present participant?",
                "Which relationships should be typed as prophecy-about vs participation-in?",
            ],
        ),
        DossierSpec(
            case_id="quoted-history-vs-current-event",
            title="Quoted/recounted history vs current Event",
            release_goals=["explorer-event-boundaries", "narration-context"],
            scripture_ranges=["Alma 36:1-30", "Helaman 7:7-9", "Mosiah 11:20-25"],
            pm_questions=[
                "Which 005C Event edges attach to recounted history rather than current narrative action?",
                "What contiguous passage context is required to preserve retrospective vs present action?",
            ],
        ),
        DossierSpec(
            case_id="cumorah-preparation-vs-battle",
            title="Cumorah preparation/gathering vs final battle",
            release_goals=["explorer-event-boundaries", "cumorah-episode"],
            place_ids=[],
            group_name_patterns=["Nephite", "Lamanite"],
            scripture_ranges=["Mormon 6:1-6", "Mormon 6:7-15", "Mormon 8:1-3"],
            pm_questions=[
                "Should Cumorah gathering/preparation and final battle be one Event or distinct Events?",
                "Which participant Groups change between preparation and battle phases?",
            ],
        ),
        DossierSpec(
            case_id="coriantumr-shiz-terminal",
            title="Coriantumr/Shiz terminal conflict",
            release_goals=["explorer-event-boundaries", "jaredite-terminal"],
            person_name_patterns=["Coriantumr", "Shiz"],
            scripture_ranges=["Ether 15:1-34"],
            pm_questions=[
                "Should multi-day terminal conflict phases be separate Events or one Event with phases?",
                "How should day-by-day progression be represented without losing episode unity?",
            ],
            notes="Preserve phases/days but make the full episode visible.",
        ),
        DossierSpec(
            case_id="event-place-high-impact",
            title="Event→Place high-impact proposal clusters",
            release_goals=["explorer-event-place", "005c-review"],
            pm_questions=[
                "For each high-impact cluster, is the Place attested inside direct Event evidence?",
                "Which Event→Place proposals rely on Reynolds only vs scripture-primary evidence?",
            ],
            notes="Top 10 clusters selected deterministically by proposal count.",
        ),
    ]


DEFERRED_EDGE_CASE_CANDIDATES = [
    {
        "candidate_id": "samuel-lamanite-prophet-vs-lamanite-group",
        "reason": "Potential Person/Group label collision; surfaced during spec review, out of EVID-001A scope.",
    },
    {
        "candidate_id": "brother-of-jared-name-identity",
        "reason": "Name vs title ambiguity; requires separate adjudication pass.",
    },
]
