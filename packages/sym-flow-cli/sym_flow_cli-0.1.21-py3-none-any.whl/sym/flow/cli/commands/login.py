import click
import requests
import validators

from sym.flow.cli.errors import SymAPIUnknownError
from sym.flow.cli.helpers.config import store_login_config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.login.login_flow import LoginFlow
from sym.flow.cli.helpers.sym_api_client import SymAPIClient
from sym.flow.cli.helpers.sym_api_service import SymAPIService


def validate_email(ctx, param, value):
    if value and not validators.email(value):
        raise click.BadParameter("must enter a valid email address")
    return value


@click.command(short_help="Log in to your Sym account")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--browser/--no-browser",
    default=True,
    is_flag=True,
)
@click.option(
    "--port",
    default=11001,
)
@click.option(
    "--email",
    callback=validate_email,
    prompt=True,
)
def login(options: GlobalOptions, browser: bool, port: int, email: str) -> None:
    api_service = SymAPIService(api_client=SymAPIClient(url=options.api_url))
    org = api_service.get_organization_from_email(email)
    click.echo("Found org: {slug} ({client_id})\n".format(**org))

    flow = LoginFlow.get_login_flow(email, browser, port)

    if browser:
        (url, *_) = flow.gen_browser_login_params(options, org)
        styled_url = click.style(requests.utils.requote_uri(url), fg="white", bold=True)
        click.echo(
            f"Attempting to open the SSO authorization page in your default browser.\n"
            f"If the browser doesn't open or you want to use a different device, open the following URL:\n"
            f"\n{styled_url}\n"
        )

    auth_token = flow.login(options, org)
    api_service.set_access_token(auth_token.get("access_token"))
    fail_msg = "Sym could not verify this login. Please try again, or visit https://docs.symops.com/docs/login-sym-flow for more details."

    try:
        login_success = api_service.verify_login(email)
        if not login_success:
            click.echo(fail_msg)
            return
    except SymAPIUnknownError:
        click.echo(fail_msg)
        return

    options.dprint(auth_token=auth_token)
    click.echo("Login succeeded")

    store_login_config(email, org, auth_token)
