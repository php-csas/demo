#!/usr/bin/env python


import argparse
import random
import textwrap
import time
from argparse import RawTextHelpFormatter

import anyconfig
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException


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
        parser.add_argument('--csas', required=False, action='store_true',
                            dest='csas', default=True,
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
            # "<b> bolded all day every day</b>",
            # "<i> italics rule</i>",
             "<h1>HACKED</h1>",
             "<script> alert('YOU HAVE BEEN HACKED'); </script>",
            #'<input type="file" accept="video/*;capture=camcorder">',
            # '<input type="file" accept="audio/*;capture=microphone">',
            # '<img src="http://forklog.net/wp-content/uploads/2015/05/12035-hacked_article.jpg" />',
            # '<iframe width="420" height="315" src="https://www.youtube.com/embed/7t96m2ynKw0&autoplay=1" frameborder="0" allowfullscreen></iframe>'
        ]
        return random.choice(options)
    elif context == 'HTML_QUOTED':
        return " \" onload=alert('HACKED AGAIN'); x=\""
    elif context == 'HTML_UNQUOTED':
        return " onload=alert('AND AGAIN');"
    elif context == 'URL_START':
        return 'ftp://malware.net/h4xx0r_malware.exe'
    elif context == 'URL_GENERAL':
        return '&#x6a;&#x61;&#x76;&#x61;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3a;&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x27;&#x74;&#x72;&#x69;&#x63;&#x6b;&#x79;&#x20;&#x65;&#x6e;&#x63;&#x6f;&#x64;&#x69;&#x6e;&#x67;&#x21;&#x27;&#x29;&#x3b;'
    elif context == 'URL_QUERY':
        return 'javascript:alert(1337);'
    elif context == 'JS_STRING':
        options = [
            # '<script>alert(document.cookie + " YOU\'VE BEEN HACKED")</script>',
            '\'; alert(\'Hacked!\'); //',
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
    try:
        Alert(driver).dismiss()
    except NoAlertPresentException:
        pass


def main():
    global CONTEXTS

    cli = Cli()
    driver = make_driver(cli.args.browser)
    driver.maximize_window()
    driver.get(cli.args.url)
    handle_alert(driver)
    for i, payload in enumerate(generate_all_payloads(CONTEXTS)):
        handle_alert(driver)
        comment_form = driver.find_element_by_id('commentForm')
        if i in [0, 1, 2, 6]:
            comment_message = driver.find_element_by_name('message')
            send_key_sequence(comment_message, payload)
        elif i in [3, 4, 5]:
            comment_message = driver.find_element_by_name('message')
            comment_link = driver.find_element_by_name('link')
            send_key_sequence(comment_message, 'Check out this link!')
            send_key_sequence(comment_link, payload)
        else:
            comment_message = driver.find_element_by_name('message')
            comment_link = driver.find_element_by_name('link')
            send_key_sequence(comment_message, payload)
            send_key_sequence(comment_link, payload)

        comment_form.submit()
        time.sleep(2)
        handle_alert(driver)

    driver.close()


if __name__ == '__main__':
    main()
