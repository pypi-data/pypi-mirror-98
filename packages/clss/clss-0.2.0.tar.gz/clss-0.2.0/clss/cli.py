
import argparse
import json
from pathlib import Path
from datetime import datetime
import csv
import os
import sys
import re
from itertools import zip_longest
import logging as log

import click

from .meta import *
from .auth import GoogleAuth, MissingCredentialsError
from .sysdirs import app_config, user_relative
from .jsdict import jsdict
from .sheets import Spreadsheet
from .a1syntax import A1Syntax

# Default config file to read parameters from.
DEFAULT_FILE = 'sheet.json'

DEFAULT_CRED_FILE = app_config('clss') / 'credentials.json'
DEFAULT_CACHE_FILE = app_config('clss') / 'sessioncache.pickle'

defaults = {
  'credentials': DEFAULT_CRED_FILE,
  'session': DEFAULT_CACHE_FILE,
}

# Verbose output log format.
log.basicConfig(format='%(asctime)s %(funcName)s:%(lineno)d %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')

# Regular expression to match number-like right-adjusted strings.
rjust_re = re.compile(r"""
   ^ =.* $  # =formula
 | ^ [$£€]?[+-]? [0-9][0-9,._ ]* (%|[eE][+-]?[0-9]+)? $  # numeric-like (currency, float)
 | ^ [0-9]+ ([/: -][0-9]+)* $  # date-like?
 """, re.VERBOSE)


# Walls of text for help.

quickstart_help = f"""
Setup quickstart:

1. Go to https://developers.google.com/sheets/api/quickstart/python
   and click the "Enable the Google Sheets API" button. (Just accept
   the defaults it gives you.) Download the credentials file into
   {app_config('clss')} and name it "credentials.json" (or anywhere
   and specify it with the "-C CREDENTIALS" parameter).

2. Figure out the spreadsheet you want to interact with. Spreadsheets
   are identified by an ID that looks like a long random string of
   characters like "1d6Jn6lgj7wRX_HF3pOqj-hm6VMC4A5CvrRnJYuCIk30".
   You'll find it in the URL when looking at the spreadsheet in a web
   browser.

3. (Optional) Create a Json file "{DEFAULT_FILE}" in
   {app_config('clss')} containing parameter defaults so you don't
   have to specify them with each command invocation.

   {{ "spreadsheet_id": "1d6Jn6lgj7wRX_HF3pOqj-hm6VMC4A5CvrRnJYuCIk30",
      "worksheet": "Sheet1",
      "range": "A1:D1000" }}

   (If you leave out "range" it defaults to covering the entire
   worksheet, roughly equivalent to "A:ZZ".)

   You can also create this file automatically by saving parameters:

   $ clss -s 1d6Jn6lgj7wRX_HF3pOqj-hm6VMC4A5CvrRnJYuCIk30 -w Foobar -f csv args save

   Whenever you run clss in the future, it will act as if these
   parameters were implicitly given.

The first time you try to interact with the Sheets API you will be
asked to log in. (Google will complain that it's unsafe because the
application hasn't been verified, but there's not much you can do
about that.) The login token will be cached in {app_config('clss')} so
this only happens once.

"""

credentials_help = f"""

An API credentials file is needed to use the Google API.

To just use the Sheets API for personal use, the "quickstart" way of
doing it is as follows:

1. Visit https://developers.google.com/sheets/api/quickstart/python
   and click the "Enable the Google Sheets API" button. (You might
   have to log in to your Google account to see this page.)

   It should automatically create a project and make a credentials
   file for you in one step.

2. Download this file to "{DEFAULT_CRED_FILE}" or give it explicitly
   with the "--credentials <file>" parameter.

3. That's it! Repeating the command should open a browser window
   asking you to authenticate the application. Google will complain
   that this is unsafe because the application is not verified, but
   there's not much to do about that for this kind of setup.

Below are the full steps to do it manually if you have more advanced
needs:

1. Visit https://console.developers.google.com/project and create a
   new project (or select an existing one).

   (Use whatever name you prefer.)

2. Use the meny on the left to navigate to the "Credentials" page and
   create a new OAuth client ID if you don't already have one.

   You probably want to select "other" or "desktop application" for
   type of application. Again the name is up to you.

3. (Optional) Customize the "OAuth consent screen". This determines
   what information is displayed to the user when this program is
   requesting their login.

4. Download the OAuth credentials you've just created and name it
   "{DEFAULT_CRED_FILE}".

   (This file should remain secret or only given to trusted users; a
   malicious user could use it to expend your API quota.)

5. Enable the APIs you want to use for this project. For example, to
   use the Google Drive API and Google Sheets API, click the "Enable"
   button on both of these pages:

   https://console.developers.google.com/apis/library/sheets.googleapis.com/
   https://console.developers.google.com/apis/library/drive.googleapis.com/

"""

def main():
  return cli(default_map=defaults)

@click.group()
@click.version_option(version=__version__)
@click.option("--verbose", "-v",
              count=True,
              help="Increase verbosity level. Use '-vv' to also show debug messages.")
@click.option("--credentials", "-C",
              type=Path,
              metavar='FILE',
              show_default=True,
              default=defaults['credentials'],
              help="JSON file containing app credentials for Google API.")
@click.option("--session", "-S",
              type=Path,
              metavar='FILE',
              show_default=True,
              default=defaults['session'],
              help="Cache file to use for saving login token.")
@click.option("--defaults", "-d",
              type=Path,
              metavar='FILE',
              help=f"""

JSON file containing default parameters (such as spreadsheet ID and
worksheet) for reading/writing data. See the "help" command for more
information on its usage. By default, the files "./{DEFAULT_FILE}",
"./.{DEFAULT_FILE}", and "{app_config('clss')/DEFAULT_FILE}" are tried
in that order.

""")
@click.option('--spreadsheet-id', '-s',
              metavar='ID',
              help=f"""Google ID of spreadsheet to use.""")
@click.option('--worksheet', '-w',
              metavar='WORKSHEET',
              help=f"""Name (or index) of worksheet to use within spreadsheet.""")
@click.option('--range', '-r',
              metavar='RANGE',
              help=f"""Cell range (in "A1:B2" notation) to operate on. Defaults to covering entire worksheet.""")
@click.option('--format', '-f',
              # default='ascii',
              type=click.Choice(['json', 'csv', 'ascii'], case_sensitive=False),
              help="Output/input format.")
@click.pass_context
def cli(cxt, verbose, **kwargs):
  """Command-Line SpreadSheet utility.

  Modifies Google spreadheets from command-line via Sheets API.

  """

  obj = cxt.ensure_object(jsdict)
  log.root.setLevel(max(log.DEBUG, 30 - 10*verbose))
  obj.update(kwargs)
  for k,v in get_defaults(obj.defaults).items():
    if not obj.get(k) or obj[k] == defaults.get(k):
      log.debug(f'option override from defaults file: {k}={v}')
      obj[k] = v


@cli.command()
@click.option('--force', '-f', is_flag=True,
              help="Force upload even if data is empty.")
@click.argument('src', type=click.File('rt'))
@click.pass_obj
def upload(cxt, src, force=False):
  """Upload data to sheet.

  "ascii" format is not supported for reading. WARNING: this will
  overwrite all data in range!

  Use "-" to read from STDIN.

  """
  ss, ix = auth_login(cxt)

  log.debug(f"loading {cxt.format} data...")
  try:
    if cxt.format == 'json':
      data = json.load(src)
    elif cxt.format == 'csv':
      data = list(csv.reader(src))
    else:
      data = [[v.strip() for v in ln.split(' | ')] for ln in src if ln.strip()]
  except Exception as e:
    log.error(f'failed to load data: {str(e)}')
    return

  if not isinstance(data, list):
    log.error(f'data type needs to be a list, not {type(data)}')
    return

  if not len(data) or not len(data[0]):
    data = [['']]

  if not force and len(data) == 1 and len(data[0]) == 1 and not data[0][0]:
    log.error(f'aborting due to empty data; use --force if you want to clear data')
    return

  ss.clear_values(ix[cxt.range])
  ss.update_values(ix[cxt.range], data)
  log.info(f'set range "{ix[cxt.range]}" to data: %s', data)


@cli.command()
@click.argument('dest', type=click.File('wt'), default=sys.stdout)
@click.pass_obj
def dump(cxt, dest):
  """Dump sheet data.

  WARNING: this will overwrite the destination file!

  Use "-" to print to STDOUT.

  """
  ss, ix = auth_login(cxt)

  if not dest:
    dest = sys.stdout

  r = ix[cxt.range]
  log.info(f"fetching range {r}...")
  
  data = ss.fetch_values(r)
  log.debug("fetched values: %s", data)

  if 'values' not in data:
    data.values = []

  log.info(f"got {len(data.values)} rows of data")

  if cxt.format == 'json':
    json.dump(data.values, dest, indent=2)
    print(file=dest)
  elif cxt.format == 'csv':
    writer = csv.writer(dest)
    writer.writerows(data.values)
  else:
    max_width = [max(len(str(v)) for v in c) for c in zip_longest(*data.values, fillvalue='')]

    for r in data.values:
      print(' | '.join(fmt_val(w, v) for w,v in zip_longest(max_width, r)),
            file=dest)


@cli.command()
@click.argument('values', nargs=-1, type=click.UNPROCESSED)
@click.pass_obj
def append(cxt, values):
  """Append a row of data to sheet.

  Each argument represents one column of data. The "--range" parameter
  in this case specifies a range in which to search for a table-like
  structure to append to.

  """
  ss, ix = auth_login(cxt)

  ss.append_values(ix[cxt.range], [values])
  log.info(f"appended data row: %s", values)

  
@cli.command()
@click.argument('action', default='show', type=click.Choice(['show', 'save', 'reset']))
@click.pass_obj
def args(obj, action):
  """Show/save/reset default parameters.

  The configuration is saved to your default home config directory, or
  to the file given with the "--defaults" parameter.

  """
  opts = dict()
  for k,v in obj.items():
    if k in ('defaults', 'action'):
      continue
    if k in ('credentials', 'session'):
      v = str(user_relative(v))
    opts[k] = v

  if action == 'show':
    for k,v in opts.items():
      print(f'{k:>16s}: {v}')
  elif action == 'save':
    fname = obj.defaults or app_config('clss') / DEFAULT_FILE
    log.info(f'saving parameters to {fname}')
    with fname.open('wt') as fil:
      json.dump(opts, fil)
  elif action == 'reset':
    fname = obj.defaults or app_config('clss') / DEFAULT_FILE
    log.info(f'deleting parameter file {fname}')
    fname.unlink()
    

@cli.command()
@click.argument('what', default='quickstart', type=click.Choice(['quickstart', 'credentials']))
@click.pass_context
def help(cxt, what):
  """Show help for setting up Google API app credentials."""
  if what == 'credentials':
    print(credentials_help)
  else:
    print(quickstart_help)


def fmt_val(w, c):
  if isinstance(c, str):
    return c.ljust(w)
  if c is None:
    return ' ' * w
  c = str(c)
  return c.rjust(w) if rjust_re.match(c) else c.ljust(w)


def auth_login(cxt):
  if not cxt.spreadsheet_id:
    raise click.UsageError("spreadsheet ID is missing")
  if not cxt.worksheet:
    raise click.UsageError("worksheet name (or index) is missing")

  log.debug("authenticating...")
  auth = GoogleAuth(cxt.credentials, cxt.session, GoogleAuth.SCOPE_SHEETS_RW)

  log.debug("discovering Sheets API...")
  try:
    service = auth.get_service('sheets', 'v4')
  except MissingCredentialsError:
    print(credentials_help)
    raise click.UsageError("credentials not found")

  # drive = auth.get_service('drive', 'v3')

  log.info(f'fetching spreadsheet "{cxt.spreadsheet_id}"')
  ss = Spreadsheet.fetch(service, cxt.spreadsheet_id)
  ix = A1Syntax(ss[int(cxt.worksheet) if cxt.worksheet.isdigit() else cxt.worksheet].title)
  return ss, ix


def get_defaults(fname=None):
  defs = jsdict()
  for f in [fname,
            Path.cwd() / DEFAULT_FILE,
            Path.cwd() / ('.'+DEFAULT_FILE),
            app_config('clss') / DEFAULT_FILE]:
    if not f or not f.is_file():
      continue
    log.info(f"loading defaults from {f}")
    try:
      with f.open('rt') as fil:
        defs = json.load(fil, object_pairs_hook=jsdict)
    except Exception as e:
      log.error(f"exception occurred while loading {f}: {str(e)}")
  
  for k in ('credentials', 'session'):
    if k in defs:
      defs[k] = Path(defs[k]).expanduser()
  return defs

# REJECTED CODE
#
# "append_extra": [
#         {{ "position": 0, "shell": "date +%Y-%m-%d" }},
#         {{ "position": 2, "shell": "echo hello ${{USER}}" }},
#         {{ "position": -1, "str": "negative=last" }} ]
#
# The "append_extra"
#   is used to specify extra arguments automatically inserted when
#   using the "append" comand:
#   $ clss append A B C D
 
#   This would insert the values:
#   ["2021-03-12", "A", "hello franksh", "B", "C", "D", "negative=last"]

#   p.add_argument('--table', '-t',
#                     default=defs.table,
#                     help="""
# range (in spreadsheet notation) to find the data table, for example
# "A:D" or "B2:G100" """)

#   tlog.add_argument('--comment', '-c', help="""additional comments (usually unnecessary)""")
#   tlog.add_argument('--project', '-p',
#                     default=defs.project,
#                     help="""project to log this work under""")
#   tlog.add_argument('--date', '-d',
#                     default='today',
#                     help="""date to add, the special value "today" will be replaced by today's date""")

#   tlog.add_argument('hours', type=float,
#                     help="""hours (note: fractions like "1.5" works)""")
#   tlog.add_argument('message',
#                     help="""short description of work""")


if __name__ == '__main__':
  main()

