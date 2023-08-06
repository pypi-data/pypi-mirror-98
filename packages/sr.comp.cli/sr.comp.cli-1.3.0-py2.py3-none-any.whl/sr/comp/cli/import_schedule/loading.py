from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from sr.comp.types import ArenaName, MatchNumber, TLA

from .types import ID, RawMatch


def parse_ids(ids: str, sep: str = ',') -> List[ID]:
    return [ID(x) for x in ids.split(sep)]


def tidy(lines: Iterable[str]) -> List[str]:
    "Strip comments and trailing whitespace"
    schedule = []
    for line in lines:
        idx = line.find('#')
        if idx > -1:
            line = line[:idx]

        line = line.strip()

        if line:
            schedule.append(line)

    return schedule


def league_yaml_path(compstate_path: Path) -> Path:
    return compstate_path / 'league.yaml'


def dump_league_yaml(
    matches: Dict[MatchNumber, RawMatch],
    file_path: Path,
) -> None:
    import yaml

    with open(file_path, 'w') as lfp:
        empty = {'matches': matches}
        yaml.dump(empty, lfp)


def load_league_yaml(league_yaml: Path) -> Dict[MatchNumber, RawMatch]:
    import yaml

    with open(league_yaml) as lfp:
        data = yaml.load(lfp)
        matches: Dict[MatchNumber, RawMatch] = data['matches']
        return matches


def load_teams_areans(compstate_path: Path) -> Tuple[List[TLA], List[ArenaName], int]:
    from sr.comp import arenas, teams

    team_ids = sorted(teams.load_teams(compstate_path / 'teams.yaml').keys())
    arenas_yaml = compstate_path / 'arenas.yaml'
    arena_ids = sorted(arenas.load_arenas(arenas_yaml).keys())
    num_corners = len(arenas.load_corners(arenas_yaml))

    return team_ids, arena_ids, num_corners


def load_ids_schedule(
    schedule_lines: Iterable[str],
    num_arenas: int,
    teams_per_game: int,
) -> Tuple[List[ID], List[List[ID]]]:
    """
    Converts an iterable of strings containing pipe-separated ids into
    a tuple: ``(ids, schedule)``. The ``ids`` is a list of unique ids
    in the order which they first appear, the ``schedule`` is a list of
    lists of ids in each line.
    """

    max_teams_per_slot = teams_per_game * num_arenas

    ids: List[ID] = []
    schedule: List[List[ID]] = []

    for match_num, match in enumerate(schedule_lines):
        match_ids = parse_ids(match, sep='|')

        uniq_match_ids = set(match_ids)
        if len(match_ids) != len(uniq_match_ids):
            raise ValueError(
                f"Match {match_num} contains the same id more than once. "
                f"(got ids {match_ids!r})",
            )

        if len(match_ids) > max_teams_per_slot:
            raise ValueError(
                f"Match {match_num} has too many ids. (got {len(match_ids)}, "
                f"can cope with {max_teams_per_slot})",
            )

        if len(match_ids) % teams_per_game != 0:
            raise ValueError(
                f"Match {match_num} has incompatible number of ids: "
                f"{len(match_ids)} is not a multiple of {teams_per_game}.",
            )

        schedule.append(match_ids)

        for id_ in match_ids:
            if id_ not in ids:
                ids.append(id_)

    return ids, schedule
