from sr.comp.cli import add_delay, deploy


def command(args):
    from sr.comp.raw_compstate import RawCompstate

    compstate = RawCompstate(args.compstate, local_only=False)
    hosts = deploy.get_deployments(compstate)

    deploy.require_no_changes(compstate)

    if not args.no_pull:
        with deploy.exit_on_exception():
            compstate.pull_fast_forward()

    how_long, when = add_delay.command(args)

    if args.when != 'now':
        msg = f"Confirm adding {how_long} delay at {when}"
        if not deploy.query_bool(msg, default_val=True):
            print("Leaving state with local modifications")
            exit()

    deploy.require_valid(compstate)

    with deploy.exit_on_exception(kind=RuntimeError):
        compstate.stage('schedule.yaml')
        msg = f"Adding {args.how_long} delay at {when}"
        compstate.commit(msg)

    deploy.run_deployments(args, compstate, hosts)


def add_subparser(subparsers):
    help_msg = "Add and deploy a delay to the competition"
    parser = subparsers.add_parser('delay', help=help_msg, description=help_msg)
    parser.add_argument(
        '--no-pull',
        action='store_true',
        help="skips updating to the latest revision",
    )
    deploy.add_options(parser)
    parser.add_argument('compstate', help="competition state repository")
    add_delay.add_arguments(parser)
    parser.set_defaults(func=command)
