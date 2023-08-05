from argparse import ArgumentParser
from datetime import datetime
from getpass import getpass
from pathlib import Path
import sys
import time

from dateutil.parser import parse as parse_date

from client import DEFAULT_INTERVAL_SECONDS
from client.gui import PacketRavenGUI
from client.retrieve import retrieve_packets
from packetraven.connections import APRSDatabaseTable, APRSfi, APRSis, SerialTNC, TextFileTNC
from packetraven.predicts import PredictionAPIURL, PredictionError, get_predictions
from packetraven.utilities import get_logger, read_configuration, repository_root
from packetraven.writer import write_packet_tracks

LOGGER = get_logger('packetraven')

CREDENTIALS_FILENAME = repository_root() / 'credentials.config'


def main():
    args_parser = ArgumentParser()
    args_parser.add_argument('--callsigns', help='comma-separated list of callsigns to track')
    args_parser.add_argument(
        '--aprsfi-key', help='APRS.fi API key (from https://aprs.fi/page/api)'
    )
    args_parser.add_argument(
        '--tnc',
        help='comma-separated list of serial ports / text files of a TNC parsing APRS packets from analog audio to ASCII'
             ' (set to `auto` to use the first open serial port)',
    )
    args_parser.add_argument(
        '--database', help='PostGres database table `user@hostname:port/database/table`'
    )
    args_parser.add_argument('--tunnel', help='SSH tunnel `user@hostname:port`')
    args_parser.add_argument(
        '--igate', action='store_true', help='send new packets to APRS-IS'
    )
    args_parser.add_argument('--start', help='start date / time, in any common date format')
    args_parser.add_argument('--end', help='end date / time, in any common date format')
    args_parser.add_argument('--log', help='path to log file to save log messages')
    args_parser.add_argument('--output', help='path to output file to save packets')
    args_parser.add_argument(
        '--prediction', help='path to output file to save most up-to-date predicted trajectory'
    )
    args_parser.add_argument(
        '--prediction-ascent-rate', help='ascent rate to use for prediction (m/s)'
    )
    args_parser.add_argument(
        '--prediction-burst-altitude', help='burst altitude to use for prediction (m)'
    )
    args_parser.add_argument(
        '--prediction-descent-rate', help='descent rate to use for prediction (m/s)'
    )
    args_parser.add_argument(
        '--prediction-api',
        help=f'API URL to use for prediction (one of {[entry.value for entry in PredictionAPIURL]})',
    )
    args_parser.add_argument(
        '--interval',
        default=DEFAULT_INTERVAL_SECONDS,
        type=float,
        help=f'seconds between each main loop (default: {DEFAULT_INTERVAL_SECONDS})',
    )
    args_parser.add_argument(
        '--gui', action='store_true', help='start the graphical interface'
    )

    args = args_parser.parse_args()

    using_gui = args.gui
    using_igate = args.igate

    if args.callsigns is not None:
        callsigns = [callsign.upper() for callsign in args.callsigns.strip('"').split(',')]
    else:
        callsigns = None

    kwargs = {}

    if args.aprsfi_key is not None:
        kwargs['aprs_fi_key'] = args.aprsfi_key

    if args.tnc is not None:
        kwargs['tnc'] = [tnc.strip() for tnc in args.tnc.split(',')]

    if args.database is not None:
        database = args.database
        if database.count('/') != 2:
            LOGGER.error(
                f'unable to parse hostname, database name, and table name from input "{database}"'
            )
        else:
            (
                kwargs['database_hostname'],
                kwargs['database_database'],
                kwargs['database_table'],
            ) = database.split('/')
            if '@' in kwargs['database_hostname']:
                kwargs['database_username'], kwargs['database_hostname'] = kwargs[
                    'database_hostname'
                ].split('@', 1)
                if ':' in kwargs['database_username']:
                    kwargs['database_username'], kwargs['database_password'] = kwargs[
                        'database_username'
                    ].split(':', 1)

    if args.tunnel is not None:
        kwargs['ssh_hostname'] = args.tunnel
        if '@' in kwargs['ssh_hostname']:
            kwargs['ssh_username'], kwargs['ssh_hostname'] = kwargs['ssh_hostname'].split(
                '@', 1
            )
            if ':' in kwargs['ssh_username']:
                kwargs['ssh_username'], kwargs['ssh_password'] = kwargs['ssh_username'].split(
                    ':', 1
                )

    start_date = parse_date(args.start.strip('"')) if args.start is not None else None
    end_date = parse_date(args.end.strip('"')) if args.end is not None else None

    if start_date is not None and end_date is not None:
        if start_date > end_date:
            temp_start_date = start_date
            start_date = end_date
            end_date = temp_start_date
            del temp_start_date

    if args.log is not None:
        log_filename = Path(args.log).expanduser()
        if log_filename.is_dir() or (not log_filename.exists() and log_filename.suffix == ''):
            log_filename = log_filename / f'packetraven_log_{datetime.now():%Y%m%dT%H%M%S}.txt'
        if not log_filename.parent.exists():
            log_filename.parent.mkdir(parents=True, exist_ok=True)
        get_logger(LOGGER.name, log_filename)
    else:
        log_filename = None

    if args.output is not None:
        output_filename = Path(args.output).expanduser()
        if output_filename.is_dir() or (
            not output_filename.exists() and output_filename.suffix == ''
        ):
            output_filename = (
                output_filename / f'packetraven_output_{datetime.now():%Y%m%dT%H%M%S}.geojson'
            )
        if not output_filename.parent.exists():
            output_filename.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_filename = None

    if args.prediction is not None:
        prediction_filename = Path(args.prediction).expanduser()
        if prediction_filename.is_dir() or (
            not prediction_filename.exists() and prediction_filename.suffix == ''
        ):
            prediction_filename = (
                prediction_filename
                / f'packetraven_predict_{datetime.now():%Y%m%dT%H%M%S}.geojson'
            )
        if not prediction_filename.parent.exists():
            prediction_filename.parent.mkdir(parents=True, exist_ok=True)

        if args.prediction_ascent_rate is not None:
            kwargs['prediction_ascent_rate'] = float(args.prediction_ascent_rate)

        if args.prediction_burst_altitude is not None:
            kwargs['prediction_burst_altitude'] = float(args.prediction_burst_altitude)

        if args.prediction_descent_rate is not None:
            kwargs['prediction_sea_level_descent_rate'] = float(args.prediction_descent_rate)

        if args.prediction_api_url is not None:
            kwargs['prediction_api_url'] = args.prediction_api_url
    else:
        prediction_filename = None

    interval_seconds = args.interval if args.interval >= 1 else 1

    if CREDENTIALS_FILENAME.exists():
        credentials = kwargs.copy()
        for section in read_configuration(CREDENTIALS_FILENAME).values():
            credentials.update(section)
        kwargs = {
            key: value if key not in kwargs or kwargs[key] is None else kwargs[key]
            for key, value in credentials.items()
        }

    if using_gui:
        PacketRavenGUI(
            callsigns,
            start_date,
            end_date,
            log_filename,
            output_filename,
            prediction_filename,
            interval_seconds,
            using_igate,
            **kwargs,
        )
    else:
        connections = []
        if 'tnc' in kwargs:
            for tnc_location in kwargs['tnc']:
                tnc_location = tnc_location.strip()
                try:
                    if 'txt' in tnc_location:
                        tnc_location = TextFileTNC(tnc_location, callsigns)
                        LOGGER.info(f'reading file {tnc_location.location}')
                        connections.append(tnc_location)
                    else:
                        tnc_location = SerialTNC(tnc_location, callsigns)
                        LOGGER.info(f'opened port {tnc_location.location}')
                        connections.append(tnc_location)
                except ConnectionError as error:
                    LOGGER.warning(f'{error.__class__.__name__} - {error}')

        if 'aprs_fi_key' in kwargs:
            aprs_fi_kwargs = {key: kwargs[key] for key in ['aprs_fi_key'] if key in kwargs}
            try:
                aprs_api = APRSfi(callsigns=callsigns, api_key=aprs_fi_kwargs['aprs_fi_key'])
                LOGGER.info(f'connected to {aprs_api.location}')
                connections.append(aprs_api)
            except ConnectionError as error:
                LOGGER.warning(f'{error.__class__.__name__} - {error}')

        if 'database_hostname' in kwargs:
            database_kwargs = {
                key: kwargs[key]
                for key in [
                    'database_hostname',
                    'database_database',
                    'database_table',
                    'database_username',
                    'database_password',
                ]
                if key in kwargs
            }
            ssh_tunnel_kwargs = {
                key: kwargs[key]
                for key in ['ssh_hostname', 'ssh_username', 'ssh_password']
                if key in kwargs
            }

            try:
                if 'ssh_hostname' in ssh_tunnel_kwargs:
                    if (
                        'ssh_username' not in ssh_tunnel_kwargs
                        or ssh_tunnel_kwargs['ssh_username'] is None
                    ):
                        ssh_username = input(
                            f'enter username for SSH host "{ssh_tunnel_kwargs["ssh_hostname"]}": '
                        )
                        if ssh_username is None or len(ssh_username) == 0:
                            raise ConnectionError('missing SSH username')
                        ssh_tunnel_kwargs['ssh_username'] = ssh_username

                    if (
                        'ssh_password' not in ssh_tunnel_kwargs
                        or ssh_tunnel_kwargs['ssh_password'] is None
                    ):
                        ssh_password = getpass(
                            f'enter password for SSH user "{ssh_tunnel_kwargs["ssh_username"]}": '
                        )
                        if ssh_password is None or len(ssh_password) == 0:
                            raise ConnectionError('missing SSH password')
                        ssh_tunnel_kwargs['ssh_password'] = ssh_password

                if (
                    'database_username' not in database_kwargs
                    or database_kwargs['database_username'] is None
                ):
                    database_username = input(
                        f'enter username for database '
                        f'"{database_kwargs["database_hostname"]}/{database_kwargs["database_database"]}": '
                    )
                    if database_username is None or len(database_username) == 0:
                        raise ConnectionError('missing database username')
                    database_kwargs['database_username'] = database_username

                if (
                    'database_password' not in database_kwargs
                    or database_kwargs['database_password'] is None
                ):
                    database_password = getpass(
                        f'enter password for database user "{database_kwargs["database_username"]}": '
                    )
                    if database_password is None or len(database_password) == 0:
                        raise ConnectionError('missing database password')
                    database_kwargs['database_password'] = database_password

                database = APRSDatabaseTable(
                    **database_kwargs, **ssh_tunnel_kwargs, callsigns=callsigns
                )
                LOGGER.info(f'connected to {database.location}')
                connections.append(database)
            except ConnectionError:
                database = None
        else:
            database = None

        if using_igate:
            try:
                aprs_is = APRSis(callsigns)
            except ConnectionError:
                aprs_is = None
        else:
            aprs_is = None

        if len(connections) == 0:
            LOGGER.error(f'no connections started')
            sys.exit(1)

        filter_message = 'retrieving packets'
        if start_date is not None and end_date is None:
            filter_message += f' sent after {start_date:%Y-%m-%d %H:%M:%S}'
        elif start_date is None and end_date is not None:
            filter_message += f' sent before {end_date:%Y-%m-%d %H:%M:%S}'
        elif start_date is not None and end_date is not None:
            filter_message += f' sent between {start_date:%Y-%m-%d %H:%M:%S} and {end_date:%Y-%m-%d %H:%M:%S}'
        if callsigns is not None:
            filter_message += f' from {len(callsigns)} callsigns: {callsigns}'
        LOGGER.info(filter_message)

        LOGGER.info(
            f'listening for packets every {interval_seconds}s from {len(connections)} connection(s): '
            f'{", ".join([connection.location for connection in connections])}'
        )

        packet_tracks = {}
        try:
            while len(connections) > 0:
                try:
                    new_packets = retrieve_packets(
                        connections,
                        packet_tracks,
                        database,
                        output_filename,
                        start_date=start_date,
                        end_date=end_date,
                        logger=LOGGER,
                    )

                    if prediction_filename is not None:
                        try:
                            predictions = get_predictions(
                                packet_tracks,
                                **{
                                    key.replace('prediction_', ''): value
                                    for key, value in kwargs
                                    if 'prediction_' in key
                                },
                            )
                            write_packet_tracks(predictions.values(), prediction_filename)
                        except PredictionError as error:
                            LOGGER.warning(f'{error.__class__.__name__} - {error}')
                        except Exception as error:
                            LOGGER.warning(
                                f'error retrieving prediction trajectory - {error.__class__.__name__} - {error}'
                            )

                except Exception as error:
                    LOGGER.exception(f'{error.__class__.__name__} - {error}')
                    new_packets = {}
                if aprs_is is not None:
                    for packets in new_packets.values():
                        aprs_is.send(packets)
                time.sleep(interval_seconds)
        except KeyboardInterrupt:
            for connection in connections:
                connection.close()
            sys.exit(0)


if __name__ == '__main__':
    main()
