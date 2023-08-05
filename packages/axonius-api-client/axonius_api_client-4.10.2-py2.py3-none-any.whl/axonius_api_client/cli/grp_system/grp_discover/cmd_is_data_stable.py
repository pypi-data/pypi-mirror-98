# -*- coding: utf-8 -*-
"""Command line interface for Axonius API Client."""
from ...context import CONTEXT_SETTINGS, click
from ...options import AUTH, add_options

OPTIONS = [
    *AUTH,
    click.option(
        "--for-next-minutes",
        "-fnm",
        "for_next_minutes",
        help="Consider data stable only if next discover will not run in less than N minutes",
        type=click.INT,
        default=None,
        show_envvar=True,
        show_default=True,
    ),
]


def get_stability(data, for_next_minutes=None, **kwargs):
    """Pass."""
    if data.is_running:
        if data.is_correlation_finished:
            return "Discover is running but correlation has finished", True

        return "Discover is running and correlation has NOT finished", False

    next_mins = data.next_run_starts_in_minutes
    reason = f"Discover is not running and next is in {next_mins} minutes"

    if for_next_minutes:
        if data.next_run_within_minutes(for_next_minutes):
            return f"{reason} (less than {for_next_minutes} minutes)", False
        return f"{reason} (more than {for_next_minutes} minutes)", True

    return reason, True


@click.command(name="is-data-stable", context_settings=CONTEXT_SETTINGS)
@add_options(OPTIONS)
@click.pass_context
def cmd(ctx, url, key, secret, **kwargs):
    """Return exit code 1 if asset data is stable, 0 if not."""
    client = ctx.obj.start_client(url=url, key=key, secret=secret)

    with ctx.obj.exc_wrap(wraperror=ctx.obj.wraperror):
        data = client.dashboard.get()

    reason, is_stable = get_stability(data=data, **kwargs)

    click.secho(f"Data is stable: {is_stable}, reason: {reason}")
    ctx.exit(int(is_stable))
