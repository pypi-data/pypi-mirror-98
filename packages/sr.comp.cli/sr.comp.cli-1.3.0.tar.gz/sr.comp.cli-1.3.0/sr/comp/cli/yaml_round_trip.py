_ryaml = None


def _load():
    global _ryaml
    if _ryaml is None:
        import ruamel.yaml as _ryaml

        from sr.comp.yaml_loader import add_time_constructor
        add_time_constructor(_ryaml.RoundTripLoader)
    return _ryaml


def load(yaml_file):
    ryaml = _load()
    with open(yaml_file) as yf:
        return ryaml.load(yf, ryaml.RoundTripLoader, version=(1, 1))


def dump(yaml_file, data):
    ryaml = _load()
    yaml = ryaml.dump(data, Dumper=ryaml.RoundTripDumper)
    yaml = "\n".join(x.rstrip() for x in yaml.splitlines())
    with open(yaml_file, 'w') as yf:
        print(yaml, file=yf)


def command(settings):
    fp = settings.file_path
    dump(fp, load(fp))


def add_subparser(subparsers):
    parser = subparsers.add_parser(
        'round-trip',
        help="Round-trip a yaml file using compstate loading",
    )
    parser.add_argument('file_path', help="target file to round trip")
    parser.set_defaults(func=command)
