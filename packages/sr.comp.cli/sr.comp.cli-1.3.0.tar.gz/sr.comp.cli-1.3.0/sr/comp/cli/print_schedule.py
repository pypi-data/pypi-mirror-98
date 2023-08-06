import argparse
from collections import defaultdict


class ScheduleGenerator:
    def __init__(self, target, arenas, state):
        from reportlab.pdfgen import canvas  # type: ignore[import]

        self.canvas = canvas.Canvas(target)
        self.state = state
        self.width = 595
        self.height = 842
        self.margin = 50
        self.page_number = 0
        self.arenas = arenas
        self.columns = 2 + 4 * len(arenas)

    def start_page(self, title="Match Schedule"):
        self.row_height = 800
        if self.page_number != 0:
            self.canvas.showPage()
        self.page_number += 1

        self.draw_header(title)
        self.draw_footer()
        self.draw_vertical_bars()
        self.draw_column_headings()

    def draw_header(self, text):
        self.canvas.setFont('Helvetica', 10)
        self.canvas.drawCentredString(self.width * 0.5, 820, text)

    def draw_footer(self):
        self.canvas.setFont('Helvetica', 8)
        self.canvas.drawCentredString(
            self.width * 0.5,
            10,
            "Page {} • Generated from state {}".format(
                self.page_number,
                self.state[:7],
            ),
        )

    def draw_vertical_bars(self):
        if len(self.arenas) == 1:
            cols = (200,)
        elif len(self.arenas) == 2:
            cols = (134, 353)
        else:
            raise RuntimeError(
                "Unexpected number of arenas: {}".format(len(self.arenas)),
            )

        for x in cols:
            self.canvas.line(x, 30, x, 810)

    def draw_column_headings(self):
        headings = [("Number", 'white', True), ("Time", 'white', True)]
        for arena in self.arenas.values():
            headings += [
                (arena.display_name, 'white', True),
                "",
                "",
                "",
            ]
        self.add_line(headings)

    def add_line(self, line):
        if len(line) != self.columns:
            raise ValueError("Incorrect column count")
        for i, cell in enumerate(line):
            if isinstance(cell, tuple):
                text = cell[0]
                background = cell[1]
                try:
                    bold = cell[2]
                except IndexError:
                    bold = False
            else:
                text = cell
                background = None
                bold = False

            if bold:
                self.canvas.setFont('Helvetica-Bold', 11)
            else:
                self.canvas.setFont('Helvetica', 10)

            centre_x = self.margin + i * (self.width - 2 * self.margin) / (self.columns - 1)
            centre_y = self.row_height

            if background is not None:
                self.canvas.setFillColor(background)
                self.canvas.rect(
                    centre_x - 20,
                    centre_y - 4,
                    40,
                    14,
                    stroke=False,
                    fill=True,
                )
                self.canvas.setFillColor('black')

            self.canvas.drawCentredString(centre_x, centre_y, text)
        self.canvas.line(
            self.margin * 0.5,
            self.row_height - 3.5,
            self.width - (self.margin * 0.5),
            self.row_height - 3.5,
        )
        self.row_height -= 14

    @staticmethod
    def _get_periods(competition, numbers=None):
        comp_periods = competition.schedule.match_periods
        if numbers is None:
            return comp_periods

        periods = []
        for n in numbers:
            periods.append(comp_periods[n])

        return periods

    @staticmethod
    def _get_shepherds(raw_compstate, numbers=None, combined=False):
        def split(shepherds):
            if combined:
                return [shepherds]
            return [(x,) for x in shepherds]

        comp_shepherds = raw_compstate.load_shepherds()
        if numbers is None:
            return split(comp_shepherds)

        shepherds = []
        for n in numbers:
            shepherds.append(comp_shepherds[n])
        return split(shepherds)

    @staticmethod
    def _get_locations(raw_compstate, names=None):
        comp_locations = raw_compstate.layout['teams']
        if names is None:
            return comp_locations

        locations = []
        for name in names:
            for location in comp_locations:
                if location['name'] == name:
                    locations.append(location)
                    break
            else:
                raise KeyError(name)

        return locations

    @staticmethod
    def _get_page_title(period, shepherds, locations, include_locations=True):
        title = str(period)

        if shepherds:
            title += " • Shepherd {}".format(
                ", ".join(
                    shepherd.get('name', "#{}".format(i + 1))
                    for i, shepherd in enumerate(shepherds)
                ),
            )

        if include_locations and locations:
            title += " • {}".format(
                ", ".join(x['display_name'] for x in locations),
            )

        return title

    @staticmethod
    def _match_suitable_for_locations(slot, locations):
        suitable_teams = ['???']
        for location in locations:
            suitable_teams += location['teams']

        for match in slot.values():
            for team in match.teams:
                if team in suitable_teams:
                    return True
        return False

    def _generate(self, period, shepherds, locations, include_locations_in_title, is_plain):
        def find_shepherd_number(team):
            if shepherds is None:
                return None
            for i, shepherd in enumerate(shepherds):
                if team in shepherd['teams']:
                    return i
            return None

        team_colours = {}
        if shepherds:
            for shepherd in shepherds:
                for team in shepherd['teams']:
                    team_colours[team] = shepherd['colour']

        def get_team_cell(team):
            if team == '???':
                team = '____'
            elif not team:
                team = '–'

            if is_plain:
                return team

            colour = team_colours.get(team, 'white')

            # If the shepherd for this team needs to get at least 4
            # teams during this slot them embolden all their teams
            bold = shepherd_counts.get(find_shepherd_number(team), 0) >= 4

            cell = (team, colour, bold)
            return cell

        title = self._get_page_title(
            period,
            shepherds,
            locations,
            include_locations_in_title,
        )
        self.start_page(title)

        n = 0
        for slot in period.matches:
            # Build map of shepherd id -> total teams they need to fetch this slot
            shepherd_counts = defaultdict(int)
            for match in slot.values():
                for team in match.teams:
                    num = find_shepherd_number(team)
                    if num is not None:
                        shepherd_counts[num] += 1

            if self._match_suitable_for_locations(slot, locations):
                cells = ['', '']
                for arena in self.arenas:
                    match = slot.get(arena)
                    if match is not None:
                        cells += list(map(get_team_cell, match.teams))
                        cells[0] = str(match.num)
                        cells[1] = str(match.start_time.strftime('%H:%M'))
                    else:
                        cells += ['–', '–', '–', '–']
                self.add_line(cells)
                n += 1

            if n % 65 == 65:
                self.start_page(title)

    def generate(
        self,
        competition,
        raw_compstate,
        period_numbers,
        shepherd_numbers,
        location_names,
        is_plain,
        combine_shepherds,
    ):
        periods = self._get_periods(competition, period_numbers)
        shepherd_groups = self._get_shepherds(
            raw_compstate, shepherd_numbers,
            combine_shepherds,
        )
        locations = self._get_locations(raw_compstate, location_names)

        for shepherds in shepherd_groups:
            for period in periods:
                self._generate(
                    period, shepherds, locations,
                    location_names is not None, is_plain,
                )

    def write(self):
        self.canvas.save()


def command(settings):
    import os.path

    from sr.comp.comp import SRComp
    from sr.comp.raw_compstate import RawCompstate

    comp = SRComp(os.path.realpath(settings.compstate))
    raw_comp = RawCompstate(
        os.path.realpath(settings.compstate),
        local_only=True,
    )

    generator = ScheduleGenerator(
        settings.output,
        arenas=comp.arenas,
        state=comp.state,
    )

    generator.generate(
        comp,
        raw_comp,
        settings.periods,
        settings.shepherds,
        settings.locations,
        settings.plain,
        settings.shepherds_combined,
    )

    generator.write()


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'print-schedule',
        help="print a shepherding sheet",
    )
    parser.add_argument('compstate', help="competition state repository")
    parser.add_argument(
        '-o',
        '--output',
        help="output file",
        type=argparse.FileType('wb'),
        required=True,
    )
    parser.add_argument(
        '--plain',
        action='store_true',
        help="output the schedule without any colouring or emboldening",
    )
    parser.add_argument(
        '-p',
        '--periods',
        type=int,
        nargs='+',
        help="specify periods by number",
    )
    parser.add_argument(
        '-s',
        '--shepherds',
        type=int,
        nargs='+',
        help="specify shepherds by number",
    )
    parser.add_argument(
        '-c',
        '--shepherds-combined',
        action='store_true',
        default=False,
        help=(
            "combine the highlighting of shepherds onto a single sheet (default "
            "is to print a separate sheet for each shepherd)"
        ),
    )
    parser.add_argument(
        '-l',
        '--locations',
        nargs='+',
        help="specify locations by name",
    )
    parser.set_defaults(func=command)
