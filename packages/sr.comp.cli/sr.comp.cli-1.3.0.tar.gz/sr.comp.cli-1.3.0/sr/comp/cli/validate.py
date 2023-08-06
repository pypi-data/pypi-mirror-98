def command(settings):
    from sr.comp.comp import SRComp
    from sr.comp.validation import validate

    comp = SRComp(settings.compstate)

    if settings.lax:
        error_count = 0
    else:
        error_count = validate(comp)

    exit(error_count)


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'validate',
        help="validate the state of a compstate repository",
    )
    parser.add_argument('compstate', help="competition state repository")
    parser.add_argument(
        '-l', '--lax',
        action='store_true',
        help="only check if it loads, rather than run a validation",
    )
    parser.set_defaults(func=command)
