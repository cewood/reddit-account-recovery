# Reddit Account Recovery

I had an old/early Reddit account that I unfortunately lost the credentials for, and sadly it was early enough that email wasn't mandatory for signup then and I also evidently lost the password as well. There was a chance that back then I used some kind of site specific password, derived from a pool of passwords and suffixes. So I put the following together as a last ditch attempt to see if I could guess the password to the account.

For anyone wondering why I'm using this instead of say the Reddit API, that's becaue the API requires a token to authenticate against it, which I didn't have, thus I couldn't use that option. Thus Splinter with help of Selenium to drive a headless Firefox instance or similar and doing an interactive login with a full-blown browser was the only available option.


## Requirements

This script requires Python 3 as well as the `splinter` and `urllib3` packages to be present. To install these package dependencies use the included `requirements.txt` or `Pipfile`, whichever you prefer.


## Usage
### Generating the input list

Firs you'll need to update `generate-input.sh` with some suitable password inputs, it generates the password list using three inputs; `{front}`, `{middle}`, and `{end}`. Then it will generate the following permuations from those inputs:

 1. `{front}`
 1. `{front}{middle}`
 1. `{front}{middle}{end}`

The run `generate-input.sh` and save the output somewhere, `input.txt` is expected by default, like so... e.g. `./generate-input.sh > input.txt`.


### Running the recovery script

To run the script issue the following command `python process-input.py --user YOURUSERHERE`, if you used a different name for the input then include the `--file YOURINPUTFILE` flag to specify the filename.

If you have any kind of lengthy input list, then you'll have to run this script for many days, even weeks. In which case I would recommend piping the output through `tee` to keep a log, incase you need to restart it later, which you can then manually do by truncating the altready tried passwords from the input file, and then rerunning the script. To run the script with `tee` you'll need to disable buffering, which you can do like so... `python -u process-input.py --user YOURUSERHERE | tee -a output.log`
