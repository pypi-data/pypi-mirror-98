__description__ = "Summaries the teams scoring the most match points"


def command(settings):
    import os.path
    from collections import defaultdict
    from functools import partial
    from itertools import chain

    from sr.comp.comp import SRComp

    comp = SRComp(os.path.realpath(settings.compstate))

    all_scores = (comp.scores.tiebreaker, comp.scores.knockout, comp.scores.league)
    all_points = dict(chain.from_iterable(s.game_points.items() for s in all_scores))

    points_map = defaultdict(partial(defaultdict, list))

    for match, points in all_points.items():
        for tla, team_points in points.items():
            points_map[team_points][tla].append(match)

    count = len(points_map)

    for idx, (points, team_info) in enumerate(sorted(points_map.items())):
        if idx + 2 < count:
            print(f"{len(team_info):>3} teams scored {points}")
        else:
            print()
            print(f"The following {len(team_info)} team(s) scored {points} points:")
            for tla, matches in team_info.items():
                print(f"- {tla} in match(es): " + ", ".join(
                    "{}{}".format(*x)
                    for x in matches
                ))


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'top-match-points',
        help=__description__,
        description=__description__,
    )
    parser.add_argument(
        'compstate',
        help="competition state repo",
    )
    parser.set_defaults(func=command)
