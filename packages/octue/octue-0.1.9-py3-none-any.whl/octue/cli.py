import functools
import os
import sys
import click
import pkg_resources

from octue.definitions import CHILDREN_FILENAME, FOLDER_DEFAULTS, MANIFEST_FILENAME, VALUES_FILENAME
from octue.logging_handlers import get_remote_handler
from octue.resources.communication import Service, service_backends
from octue.runner import Runner
from twined import Twine


global_cli_context = {}


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--id",
    default=None,
    type=click.UUID,
    show_default=True,
    help="UUID of the analysis being undertaken. None (for local use) will cause a unique ID to be generated.",
)
@click.option(
    "--skip-checks/--no-skip-checks",
    default=False,
    is_flag=True,
    show_default=True,
    help="Skips the input checking. This can be a timesaver if you already checked "
    "data directories (especially if manifests are large).",
)
@click.option("--logger-uri", default=None, show_default=True, help="Stream logs to a websocket at the given URI.")
@click.option(
    "--log-level",
    default="info",
    type=click.Choice(["debug", "info", "warning", "error"], case_sensitive=False),
    show_default=True,
    help="Log level used for the analysis.",
)
@click.option(
    "--show-twined-logs",
    is_flag=True,
    default=False,
    show_default=True,
    help="Show logs from the whole package in addition to logs just from your app.",
)
@click.option(
    "--force-reset/--no-force-reset",
    default=True,
    is_flag=True,
    show_default=True,
    help="Forces a reset of analysis cache and outputs [For future use, currently not implemented]",
)
@click.version_option(version=pkg_resources.get_distribution("octue").version)
def octue_cli(id, skip_checks, logger_uri, log_level, show_twined_logs, force_reset):
    """Octue CLI, enabling a data service / digital twin to be run like a command line application.

    When acting in CLI mode, results are read from and written to disk (see
    https://octue-python-sdk.readthedocs.io/en/latest/ for how to run your application directly without the CLI).
    Once your application has run, you'll be able to find output values and manifest in your specified --output-dir.
    """
    global_cli_context["analysis_id"] = id
    global_cli_context["skip_checks"] = skip_checks
    global_cli_context["logger_uri"] = logger_uri
    global_cli_context["log_handler"] = None
    global_cli_context["log_level"] = log_level.upper()
    global_cli_context["show_twined_logs"] = show_twined_logs
    global_cli_context["force_reset"] = force_reset

    if global_cli_context["logger_uri"]:
        global_cli_context["log_handler"] = get_remote_handler(
            logger_uri=global_cli_context["logger_uri"], log_level=global_cli_context["log_level"]
        )


@octue_cli.command()
@click.option(
    "--app-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Directory containing your source code (app.py)",
)
@click.option(
    "--data-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Location of directories containing configuration values and manifest, input values and manifest, and output "
    "directory.",
)
@click.option(
    "--config-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory containing configuration (overrides --data-dir).",
)
@click.option(
    "--input-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory containing input (overrides --data-dir).",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory to write outputs as files (overrides --data-dir).",
)
@click.option("--twine", type=click.Path(), default="twine.json", show_default=True, help="Location of Twine file.")
def run(app_dir, data_dir, config_dir, input_dir, output_dir, twine):
    config_dir = config_dir or os.path.join(data_dir, FOLDER_DEFAULTS["configuration"])
    input_dir = input_dir or os.path.join(data_dir, FOLDER_DEFAULTS["input"])
    output_dir = output_dir or os.path.join(data_dir, FOLDER_DEFAULTS["output"])

    twine = Twine(source=twine)

    (
        configruation_values,
        configuration_manifest,
        input_values,
        input_manifest,
        children,
    ) = set_unavailable_strand_paths_to_none(
        twine,
        (
            ("configuration_values", os.path.join(config_dir, VALUES_FILENAME)),
            ("configuration_manifest", os.path.join(config_dir, MANIFEST_FILENAME)),
            ("input_values", os.path.join(input_dir, VALUES_FILENAME)),
            ("input_manifest", os.path.join(input_dir, MANIFEST_FILENAME)),
            ("children", os.path.join(config_dir, CHILDREN_FILENAME)),
        ),
    )

    runner = Runner(
        twine=twine,
        configuration_values=configruation_values,
        configuration_manifest=configuration_manifest,
        log_level=global_cli_context["log_level"],
        handler=global_cli_context["log_handler"],
        show_twined_logs=global_cli_context["show_twined_logs"],
    )

    analysis = runner.run(
        app_src=app_dir,
        analysis_id=global_cli_context["analysis_id"],
        input_values=input_values,
        input_manifest=input_manifest,
        children=children,
        output_manifest_path=os.path.join(output_dir, MANIFEST_FILENAME),
        skip_checks=global_cli_context["skip_checks"],
    )
    analysis.finalise(output_dir=output_dir)
    return 0


@octue_cli.command()
@click.option(
    "--app-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Directory containing your source code (app.py)",
)
@click.option(
    "--data-dir",
    type=click.Path(),
    default=".",
    show_default=True,
    help="Location of directories containing configuration values and manifest.",
)
@click.option(
    "--config-dir",
    type=click.Path(),
    default=None,
    show_default=True,
    help="Directory containing configuration (overrides --data-dir).",
)
@click.option(
    "--service-id",
    type=click.STRING,
    help="The unique ID of the server (this should be unique over all time and space).",
)
@click.option("--twine", type=click.Path(), default="twine.json", show_default=True, help="Location of Twine file.")
@click.option("--timeout", type=click.INT, default=None, show_default=True, help="Timeout in seconds for serving.")
@click.option(
    "--delete-topic-and-subscription-on-exit",
    is_flag=True,
    default=False,
    show_default=True,
    help="Delete Google Pub/Sub topics and subscriptions on exit.",
)
def start(app_dir, data_dir, config_dir, service_id, twine, timeout, delete_topic_and_subscription_on_exit):
    """ Start the service as a server to be asked questions by other services. """
    config_dir = config_dir or os.path.join(data_dir, FOLDER_DEFAULTS["configuration"])
    twine = Twine(source=twine)

    configuration_values, configuration_manifest, children = set_unavailable_strand_paths_to_none(
        twine,
        (
            ("configuration_values", os.path.join(config_dir, VALUES_FILENAME)),
            ("configuration_manifest", os.path.join(config_dir, MANIFEST_FILENAME)),
            ("children", os.path.join(config_dir, CHILDREN_FILENAME)),
        ),
    )

    runner = Runner(
        twine=twine,
        configuration_values=configuration_values,
        configuration_manifest=configuration_manifest,
        log_level=global_cli_context["log_level"],
        handler=global_cli_context["log_handler"],
        show_twined_logs=global_cli_context["show_twined_logs"],
    )

    run_function = functools.partial(
        runner.run,
        app_src=app_dir,
        children=children,
        skip_checks=global_cli_context["skip_checks"],
    )

    backend_configuration_values = runner.configuration["configuration_values"]["backend"]
    backend = service_backends.get_backend(backend_configuration_values.pop("name"))(**backend_configuration_values)

    service = Service(id=service_id, backend=backend, run_function=run_function)
    service.serve(timeout=timeout, delete_topic_and_subscription_on_exit=delete_topic_and_subscription_on_exit)


def set_unavailable_strand_paths_to_none(twine, strands):
    """ Set paths to unavailable strands to None, leaving the paths of available strands as they are. """
    updated_strand_paths = []

    for strand_name, strand in strands:
        if strand_name not in twine.available_strands:
            updated_strand_paths.append(None)
        else:
            updated_strand_paths.append(strand)

    return updated_strand_paths


if __name__ == "__main__":
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    octue_cli(args)
