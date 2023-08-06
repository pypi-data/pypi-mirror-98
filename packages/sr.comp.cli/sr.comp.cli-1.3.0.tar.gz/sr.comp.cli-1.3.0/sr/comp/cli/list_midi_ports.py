__description__ = "List available MIDI output ports."


def command(args):
    import mido  # type: ignore[import]

    ports = mido.get_output_names()
    print(len(ports), "outputs:")
    for port in ports:
        print("-", port)


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'list-midi-ports', help=__description__,
        description=__description__,
    )
    parser.set_defaults(func=command)
