import contextlib
import importlib.util
import json
import os
from json import JSONDecodeError

import click


help_text = """\
Rally CLI - execute Decision Engine presets locally

Please set the following environment variables:

\b
    {prefix}{cmd} RALLY_URL=https://silo.sdvi.com
    {prefix}{cmd} RALLY_API_TOKEN=<your API token>
    {prefix}rally run preset.py
""".format(
    cmd="export" if os.name == "posix" else "set",
    prefix="$ " if os.name == "posix" else "> ",
)


@click.group(help=help_text)
def cmd():
    pass


@cmd.command()
@click.argument('preset', type=str)
@click.option('--asset', '-a', type=str, default=None,
              help='specify an asset to run on')
@click.option('--dpd', '-d', default=None,
              help='specify Dynamic Preset Data as a JSON string or a JSON filename')
def run(preset, asset, dpd):
    """ Runs the eval_main function in the given preset python file

    :param preset: Required. The name of a preset file to run, must contain an `eval_main` function.
    """

    eval_context = make_context(asset, dpd)

    # import the user preset as a module
    spec = importlib.util.spec_from_file_location('preset', preset)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    userScript = module.eval_main
    args = (eval_context,) if userScript.__code__.co_argcount == 1 else tuple()

    return userScript(*args)


def make_context(asset_name, dynamic_preset_data):
    """
    The actual context of eval2 jobs run inside a workflow will contain several more attributes set in the connector
    the following are required by the CLI:

    'assetId',
    'apiToken',
    'rallyUrl',
    'dynamicPresetData',
    """

    apiToken = os.environ.get('RALLY_API_TOKEN')
    rallyUrl = os.environ.get('RALLY_URL')

    assert apiToken, 'RALLY_API_TOKEN must be set in your environment'
    assert rallyUrl, 'RALLY_URL must be set in your environment'

    assert rallyUrl.startswith('https://') and rallyUrl.endswith('.sdvi.com'), \
        f'RALLY_URL must be a like https://silo.sdvi.com, not {rallyUrl}'

    rallyUrl = f'{rallyUrl}/api'
    dynamicPresetData = None
    if dynamic_preset_data:
        with contextlib.suppress(FileNotFoundError):
            with open(dynamic_preset_data) as f:
                dynamicPresetData = json.load(f)

        if not dynamicPresetData:
            try:
                dynamicPresetData = json.loads(dynamic_preset_data)
            except JSONDecodeError as err:
                raise ValueError('dynamic preset data must be a JSON file or JSON string') from err

    context = {
        'assetName': asset_name,
        'apiToken': apiToken,
        'rallyUrl': rallyUrl,
        'dynamicPresetData': dynamicPresetData
    }
    os.environ['rallyContext'] = json.dumps(context)

    return context
