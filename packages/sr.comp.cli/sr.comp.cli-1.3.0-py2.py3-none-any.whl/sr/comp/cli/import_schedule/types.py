from typing import (
    Collection,
    Dict,
    List,
    NamedTuple,
    NewType,
    Optional,
    Sequence,
    TypeVar,
)

from sr.comp.types import ArenaName, MatchNumber, TLA

T = TypeVar('T')
ID = NewType('ID', str)
RawMatch = Dict[ArenaName, List[Optional[TLA]]]


class BadMatch(NamedTuple):
    arena: ArenaName
    num: MatchNumber
    num_teams: int


class Configuration(NamedTuple):
    arena_ids: Collection[ArenaName]
    team_ids: Sequence[TLA]

    teams_per_game: int

    first_match_number: MatchNumber

    @property
    def num_arenas(self) -> int:
        return len(self.arena_ids)

    @property
    def num_teams(self) -> int:
        return len(self.team_ids)
