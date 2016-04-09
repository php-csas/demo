#!/usr/bin/env python


import argparse
import random
import textwrap
import time
from argparse import RawTextHelpFormatter

import anyconfig
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert


CONTEXTS = [
    'HTML_PCDATA',
    'HTML_QUOTED',
    'HTML_UNQUOTED',
    'URL_START',
    'URL_QUERY',
    'URL_GENERAL',
    'JS_STRING',
]


class Cli:

    def __init__(self):
        self.__parser = self.__setup_argparser()
        self.args = self.__parser.parse_args()

    def __setup_argparser(self):
        parser = argparse.ArgumentParser(prog='php_csas_demo',
                                         formatter_class=RawTextHelpFormatter,
                                         description=textwrap.dedent('''\
                                               ___  __ _____      ____________   ____
                                              / _ \/ // / _ \____/ ___/ __/ _ | / __/
                                             / ___/ _  / ___/___/ /___\ \/ __ |_\ \
                                            /_/  /_//_/_/       \___/___/_/ |_/___/

                                            ------------------------------------------
                                            PHP-CSAS DEMO
                                            Version: 0.1.0
                                            ------------------------------------------
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


def generate_payload(context):
    if context == 'HTML_PCDATA':
        options = [
            "<b> bolded all day every day</b>",
            "<i> italics rule</i>",
            " \\\ & \\\" a\\ra\\na\\va\\fa\\t",
            "<h1>HACKED</h1>",
            '<input type="file" accept="video/*;capture=camcorder">',
            '<input type="file" accept="audio/*;capture=microphone">',
            '<img src="http://forklog.net/wp-content/uploads/2015/05/12035-hacked_article.jpg" />',
            '<iframe width="420" height="315" src="https://www.youtube.com/embed/7t96m2ynKw0&autoplay=1" frameborder="0" allowfullscreen></iframe>'
        ]
        return random.choice(options)
    elif context == 'HTML_QUOTED':
        return " \" onload=alert('HACKED AGAIN'); x=\""
    elif context == 'HTML_UNQUOTED':
        return " onload=alert('AND AGAIN');"
    elif context == 'URL_START':
        return 'ftp://malware.net/h4xx0r_malware.exe'
    elif context == 'URL_GENERAL':
        return 'http://google.com/'
    elif context == 'URL_QUERY':
        return 'https://bank.com/transfer?id=hacker&amount=1000000000'
    elif context == 'JS_STRING':
        options = [
            '<script>alert(document.cookie + " YOU\'VE BEEN HACKED")</script>',
            '</script>alert("XSSSSSSSSSSSED AGAIN")</script>',
            "javascript:(function(){var s=document.createElement('style');s.innerHTML='%40-moz-keyframes roll { 100%25 { -moz-transform: rotate(360deg); } } %40-o-keyframes roll { 100%25 { -o-transform: rotate(360deg); } } %40-webkit-keyframes roll { 100%25 { -webkit-transform: rotate(360deg); } } body{ -moz-animation-name: roll; -moz-animation-duration: 4s; -moz-animation-iteration-count: 1; -o-animation-name: roll; -o-animation-duration: 4s; -o-animation-iteration-count: 1; -webkit-animation-name: roll; -webkit-animation-duration: 4s; -webkit-animation-iteration-count: 1; }';document.getElementsByTagName('head')[0].appendChild(s);}());",
        ]
        return random.choice(options)


def generate_all_payloads(contexts):
    for context in contexts:
        yield generate_payload(context)


def send_key_sequence(element, sequence):
    for k in sequence:
        element.send_keys(k)


def handle_alert(driver):
    # Maybe this should be Alert(driver).accept()
    Alert(driver).dismiss()


def main():
    cli = Cli()
    driver = make_driver(cli.args.browser)
    driver.get(cli.args.url)
    comment_form = driver.find_element_by_id('commentForm')
    comment_message = driver.find_element_by_name('message')
    comment_link = driver.find_element_by_name('link')
    for payload in generate_all_payloads():
        send_key_sequence(comment_message, payload)
        # Try this later
        # send_key_sequence(comment_link, payload)
        comment_form.submit()
        # Maybe make this shorter or longer in order to see the effect of XSS
        time.sleep(2)
        handle_alert(driver)
    driver.close()


if __name__ == '__main__':
    main()
