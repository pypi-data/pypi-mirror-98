import random
import sys
from collections import Counter
from itertools import product
from math import gcd


class PatienceCounter:
    def __init__(self, threshold):
        self.threshold = threshold
        self.level = 0

    def bump(self):
        self.level += 1

    def reset(self):
        self.level = 0

    def reached(self):
        return self.level >= self.threshold


def prime_factors(n):
    d = 2
    while d * d <= n:
        while n % d == 0:
            yield d
            n //= d
        d += 1
    if n > 1:
        yield n


class Scheduler:
    def __init__(
        self,
        teams,
        max_match_periods,
        arenas=('main',),
        num_corners=4,
        random=random,
        appearances_per_round=1,
        separation=2,
        max_matchups=2,
        enable_lcg=True,
        base_matches=(),
    ):
        self.tag = ''
        self.num_corners = num_corners
        self.random = random
        self.arenas = tuple(arenas)
        self.max_match_periods = max_match_periods
        self.appearances_per_round = appearances_per_round
        self._base_matches = list(base_matches)
        for match in base_matches:
            for n, entry in enumerate(match):
                if entry is None:
                    match[n] = '~'
        self._calculate_teams(teams)
        self._calculate_rounds()
        if len(self._base_matches) % self.round_length > 0:
            self.lprint(
                "Warning: matches for partial reschedule are not a multiple of "
                "the round-length",
            )
        self.separation = separation
        self.max_matchups = max_matchups
        if enable_lcg:
            self._compute_lcg_params()
        else:
            self._lcg_params = None

    def lprint(self, *args, **kwargs):
        if self.tag:
            print(self.tag, end='', file=sys.stderr)
        print(*args, file=sys.stderr, **kwargs)

    @property
    def entrants_per_match_period(self):
        return len(self.arenas) * self.num_corners

    def _is_pseudo(self, team):
        return team[0] == '~'

    def _calculate_teams(self, base_teams):
        teams = list(base_teams) * self.appearances_per_round
        # account for overflow
        overflow = (
            self.entrants_per_match_period -
            (len(teams) % self.entrants_per_match_period)
        )
        if overflow < self.entrants_per_match_period:
            for n in range(overflow):
                teams.append(f'~{n}')
        self._teams = teams

    @property
    def total_matches(self):
        return self.num_rounds * self.round_length

    def _calculate_rounds(self):
        self.num_rounds = int(
            self.max_match_periods *
            self.entrants_per_match_period //
            len(self._teams),
        )
        self.round_length = len(self._teams) // self.entrants_per_match_period

    def _validate(
        self,
        schedule,
        matchup_max=None,
        matchup_impatience_bump=lambda: None,
    ):
        is_pseudo = self._is_pseudo
        if matchup_max is None:
            matchup_max = self.max_matchups
        multi_per_match_mode = self.appearances_per_round > 1
        # 4 tests in this function:
        #  (1) validate that teams aren't scheduled too tightly
        #  (2) validate that matchups aren't too frequent
        #  (3) validate that no match has two teams sitting out (or if it is, that it's blank)
        # if operating multiple appearances per match, also:
        #  (4) make sure that a team doesn't appear in a match twice
        matchups = Counter()
        for match_id, match in enumerate(schedule):
            entrants = set(
                entrant
                for entrant in match
                if not is_pseudo(entrant)
            )
            if multi_per_match_mode:
                # Test constraint (4)
                if len(entrants) != len([
                    entrant
                    for entrant in match
                    if not is_pseudo(entrant)
                ]):
                    return False
            # Test constraint (1)
            previous_matches = schedule[match_id - self.separation:match_id]
            for previous_match in previous_matches:
                for previous_entrant in previous_match:
                    if is_pseudo(previous_entrant):
                        continue
                    if previous_entrant in entrants:
                        return False
            # Update constraint (2)
            for arena_id in range(len(self.arenas)):
                game = match[arena_id * self.num_corners:(arena_id + 1) * self.num_corners]
                for a, b in product(game, repeat=2):
                    if a >= b:
                        continue
                    a_pseudo, b_pseudo = is_pseudo(a), is_pseudo(b)
                    # Check constraint (3) while we're here
                    if (
                        a_pseudo and
                        b_pseudo and
                        not all(is_pseudo(x) for x in game)
                    ):
                        return False
                    elif not a_pseudo and not b_pseudo:
                        matchups.update([(a, b)])
        # No collisions, determine whether teams face a broad range of other teams
        top_repeated_matchups = max(matchups.values())
        if top_repeated_matchups > self.max_matchups:
            # team faces off against one other team too many times
            matchup_impatience_bump()
            return False
        # No objections, your honour!
        return True

    def _compute_lcg_params(self):
        m = len(self._teams)
        for a in range(m - 1, 1, -1):
            am1 = a - 1
            if am1 % 4 != 0:
                continue
            if any(am1 % factor != 0 for factor in prime_factors(m)):
                continue
            for c in range(m - 1, 0, -1):
                if gcd(c, m) != 1:
                    continue
                epm = self.entrants_per_match_period
                acceptable = True
                for sm in range(1, self.separation + 1):
                    overlap = 1 + self.separation - sm
                    dst_a = 0
                    dst_b = epm * overlap
                    src_a = (self.round_length - sm) * epm
                    src_b = (1 + self.round_length - sm) * epm
                    src = set((a * x + c) % m for x in range(src_a, src_b))
                    dst = set(range(dst_a, dst_b))
                    if not src.isdisjoint(dst):
                        acceptable = False
                if not acceptable:
                    continue
                self._lcg_params = (a, c)
                self.lprint(f"Found LCG settings: ({a}, {c})")
                return
        self.lprint("No valid LCG parameters")
        self._lcg_params = None

    def _lcg_permute(self, teams):
        if self._lcg_params is None:
            return None
        a, c = self._lcg_params
        m = len(teams)
        if m != len(self._teams):
            return None
        permutation = [teams[(a * n + c) % m] for n in range(len(teams))]
        if set(permutation) != set(teams):
            raise ValueError("permutation fault")
        return permutation

    def run(self):
        matchup_impatience = PatienceCounter(200000)
        max_matchups = self.max_matchups
        matches = list(self._base_matches)
        teams = list(self._teams)
        self.random.shuffle(teams)
        while (
            len(matches) < self.total_matches and
            len(matches) + self.round_length <= self.max_match_periods
        ):
            this_round = len(matches) // self.round_length
            self.lprint("Scheduling round {round} ({prev}/{tot} complete)".format(
                round=this_round,
                prev=len(matches),
                tot=self.total_matches,
            ))
            # Attempt the LCG
            lcg_round = self._lcg_permute(teams)
            if lcg_round is not None:
                matches_prime = matches + self._match_partition(lcg_round)
                if self._validate(matches_prime, max_matchups, matchup_impatience.bump):
                    matches = matches_prime
                    self.lprint("  completed via LCG permutation")
                    continue
            for _ in range(10000):
                if matchup_impatience.reached():
                    matchup_impatience.reset()
                    self.lprint("  Easing off on matchup constraint.")
                    max_matchups += 1
                self.random.shuffle(teams)
                matches_prime = matches + self._match_partition(teams)
                if self._validate(matches_prime, max_matchups, matchup_impatience.bump):
                    matches = matches_prime
                    break
            else:
                if len(matches) > len(self._base_matches):
                    self.lprint("  backtracking")
                    matches = matches[:-self.round_length]
        return self._clean(matches)

    def _match_partition(self, teams):
        entries = []
        for n in range(0, len(teams), self.entrants_per_match_period):
            entries.append(teams[n:n + self.entrants_per_match_period])
        return entries

    def _clean(self, matches):
        def get_match(match_id, match):
            data = {}
            for arena_id, arena in enumerate(self.arenas):
                entrants = match[arena_id * self.num_corners:(arena_id + 1) * self.num_corners]
                # Shuffle entrants to get statistically sensible zone distribution
                if match_id >= len(self._base_matches):  # don't shuffle provided matches!
                    self.random.shuffle(entrants)
                entrants = [
                    None if self._is_pseudo(entrant) else entrant
                    for entrant in entrants
                ]
                data[arena] = entrants
            return data
        return {match_id: get_match(match_id, match) for match_id, match in enumerate(matches)}
