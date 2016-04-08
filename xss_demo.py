#!/usr/bin/env python


import argparse
import textwrap
from argparse import RawTextHelpFormatter

import anyconfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Cli:

    def __init__(self):
        self.__parser = self.__setup_argparser()
        self.args = self.__parser.parse_args()

    def __setup_argparser(self):
        parser = argparse.ArgumentParser(prog='php_csas_demo',
                                         formatter_class=RawTextHelpFormatter,
                                         description=textwrap.dedent('''\
                                                    __        __    _
                                                   / /  ___  / /__ (_)
                                                  / /__/ _ \/  '_// /
                                                 /____/\___/_/\_\/_/
                                            ------------------------------------
                                            PHP-CSAS DEMO
                                            Version: 0.1.0
                                            ------------------------------------
                                            '''),
                                         epilog=textwrap.dedent('''\
                                            Author: Jared M. Smith
                                            Contact: jared@jaredsmith.io
                                            ''')
                                         )

        parser.add_argument('--url', required=True, dest='url',
                            help=textwrap.dedent('''\
                                The URL of the address to test against.
                            '''))
        parser.add_argument('--csas', required=True, action='store_true',
                            dest='csas',
                            help=textwrap.dedent('''\
                                Whether CSAS is enabled on site.'''))
        parser.add_argument('--browser', required=False,
                            dest='browser', default='firefox',
                            choices=('firefox', 'chrome', 'ie', 'opera'),
                            help=textwrap.dedent('''\
                                Which browser to test with. Options are:
                                "firefox", "chrome", "ie", or "opera".'''))
        parser.add_argument('--quiet', required=False, action='store_false',
                            dest='log', default=False,
                            help=textwrap.dedent('''\
                                Whether to silence logging.'''))
        parser.add_argument('--logfile', required=False,
                            dest='logfile', default='/tmp/php_csas_demo_log.out', type=str,
                            help=textwrap.dedent('''\
                                If logging is enabled, log to
                                this filename.'''))
        return parser


def make_driver(browser):
    if browser == 'firefox':
        return webdriver.Firefox()
    elif browser == 'chrome':
        return webdriver.Chrome()
    elif browser == 'ie':
        return webdriver.Ie()
    elif browser == 'opera':
        return webdriver.Opera()


def get_config(config_file):
    try:
        return anyconfig.get(config_file)
    except Exception:
        raise ValueError('Invalid configuration file type. Try JSON or YAML.')


def main():
    cli = Cli()
    driver = make_driver(cli.args.browser)
    driver.get(cli.args.url)


if __name__ == '__main__':
    main()
