time_parse_pattern = r'^((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?$'


class BadDurationException(ValueError):
    def __init__(self, time_str):
        msg = "Unable to parse duration string '{0}'.".format(time_str)
        super().__init__(msg)


def parse_duration(time_str):
    from datetime import timedelta
    import re

    parts = re.match(time_parse_pattern, time_str)
    if not parts:
        if not time_str.isdigit():
            raise BadDurationException(time_str)
        else:
            s = int(time_str)
            return timedelta(seconds=s)
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def parse_datetime(when_str):
    import re
    from datetime import datetime
    from dateutil.parser import parse as parse_date
    from dateutil.tz import tzlocal

    def parse_now(match):
        return datetime.now()

    def parse_future(match):
        offset = parse_duration(match.group(1))
        return datetime.now() + offset

    def parse_past(match):
        offset = parse_duration(match.group(1))
        return datetime.now() - offset

    def parse_absolute(match):
        return parse_date(match.group(0))

    DATETIME_PATTERNS = [
        (r'^([^ ]+)\s*ago$', parse_past),
        (r'^in\s*([^ ]+)$', parse_future),
        (r'^now$', parse_now),
        (r'^.+$', parse_absolute),
    ]

    for pattern, parse_fn in DATETIME_PATTERNS:
        match = re.match(pattern, when_str)
        if match is None:
            continue
        try:
            when = parse_fn(match)
            break
        except ValueError:
            continue
    else:
        raise ValueError(
            "Unable to parse date string: {0!r}".format(when_str),
        )

    # Timezone information gets ignored, and the resulting datetime is
    # timezone-unaware. However the compstate needs timezone data to be
    # present.
    # Assume that the user wants their current timezone.
    when = when.replace(tzinfo=tzlocal())
    return when


def get_current_match_start(compstate_path):
    from sr.comp.comp import SRComp
    compstate = SRComp(compstate_path)
    now = compstate.schedule.datetime_now
    current_matches = tuple(compstate.schedule.matches_at(now))
    if not current_matches:
        raise Exception("Not currently in a match, specify a valid time instead")

    return min(x.start_time for x in current_matches)


def parse_time(compstate_path, when_str):
    if when_str == "current match":
        return get_current_match_start(compstate_path)
    else:
        return parse_datetime(when_str)


def add_delay(schedule, delay_seconds, when):
    delays = schedule.get('delays')
    if not delays:
        delays = schedule['delays'] = []
    new_delay = {
        'delay': delay_seconds,
        'time': when,
    }
    delays.append(new_delay)


def command(settings):
    import os.path

    from sr.comp.cli import yaml_round_trip as rtyaml

    schedule_path = os.path.join(settings.compstate, "schedule.yaml")
    schedule = rtyaml.load(schedule_path)

    how_long = parse_duration(settings.how_long)
    how_long_seconds = how_long.seconds

    when = parse_time(settings.compstate, settings.when)
    when = when.replace(microsecond=0)

    add_delay(schedule, how_long_seconds, when)

    rtyaml.dump(schedule_path, schedule)

    return how_long, when


def add_arguments(parser):
    parser.add_argument(
        'how_long',
        help=(
            "How long to delay the competition for. Specify either as a number "
            "of seconds or as a string of the form 1m30s."
        ),
    )
    parser.add_argument(
        'when',
        nargs='?',
        default='now',
        help=(
            "When the delay should occur. This can be anything which PHP's "
            "strtotime would be able to parse. Assumes all times are in the "
            "current timezone, regardless of input."
        ),
    )


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'add-delay',
        help="Add a delay the competition state",
    )
    parser.add_argument('compstate', help="competition state repository")
    add_arguments(parser)
    parser.set_defaults(func=command)
