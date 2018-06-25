#!/usr/bin/env python3
# MIT License
# Copyright (c) 2018 Nathan Wilson

import argparse
from log_parser.log_parser import LogParser


DEFAULT_ALERT_THRESHOLD = 10
DEFAULT_ALERT_WINDOW = 120
DEFAULT_INTERVAL = 10
DEFAULT_LOG = "/var/log/access.log"


def main():
    arg_parser = setup_arg_parser()
    args = arg_parser.parse_args()
    log_parser = LogParser(args)
    try:
        log_parser.run(args.log)
    except FileNotFoundError:
        print("\nUnable to read the log file {}\n".format(args.log))
        arg_parser.print_help()


ARGS = [
    [("-l", "--log"),
     {
         "help": "File to read log from. Default: {}".format(DEFAULT_LOG),
         "default": DEFAULT_LOG,
     }],
    [("-t", "--threshold"),
     {
         "help": ("Alert threshold in calls/second. "
                  "Default: {}".format(DEFAULT_ALERT_THRESHOLD)),
         "type": int,
         "default": DEFAULT_ALERT_THRESHOLD,
     }],
    [("-w", "--window"),
     {
         "help": ("Alert window in total seconds. "
                  "Default: {}".format(DEFAULT_ALERT_WINDOW)),
         "type": int,
         "default": DEFAULT_ALERT_WINDOW,
     }],
    [("-i", "--interval"),
     {
         "help": ("Interval between reports in seconds. "
                  "Default: {}".format(DEFAULT_INTERVAL)),
         "type": int,
         "default": DEFAULT_INTERVAL,
     }],
    [("-r", "--referer-expected"),
     {
         "help": ("Log lines are expected to have referer and user-agent "
                  "fields. Off by default."),
         "action": "store_true",
     }]
]


def setup_arg_parser():
    parser = argparse.ArgumentParser()
    for (args, kwargs) in ARGS:
        parser.add_argument(*args, **kwargs)
    return parser


if __name__ == "__main__":
    # execute only if run as a script
    main()
