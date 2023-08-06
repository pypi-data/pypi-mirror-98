
# clss

**C**ommand-**l**ine **S**pread**s**heets.

```
clss -s SPREADSHEET_ID -w WORKSHEET [-r RANGE] [-f FORMAT] (append | dump | upload)
```

Small utility for interacting with Google spreadsheets, appending rows
or syncing data back and forth between local ASCII/CSV/JSON files.

## Usage: timesheets

The motivating use case was keeping timesheets for projects. After
looking at several web-based solutions which were either way too heavy
or noisy (as in bells and whistles) for this use-case, I got the idea
of simply using shared spreadsheets via Google Sheets.

Let's say we were keeping timesheets for projects in a Google
spreadsheet like so:

| Date       | User    | Project  | Hours | Description                                   | Comment                    |
| ----:      | :----   | -------: | ----: | :-----------                                  | :-------                   |
| 2021-03-01 | franksh | 1002     | 5.0   | Stared out of the window                      |                            |
| 2021-03-02 | franksh | 1001     | 3.5   | Invested in pyramid schemes                   |                            |
| 2021-03-02 | franksh | 4001     | 4.0   | Went outside to stare into the window         |                            |
| 2021-03-03 | franksh | 7777     | 9.0   | Resolved the Langlands program in one sitting | Margin too short for proof |

Configuring `clss` to target this worksheet by making a `~/.config/clss/sheet.json` or `.sheet.json` file:

```json
{
  "spreadsheet_id": "1d6Jn6lgj7wRX_HF3pOqj-hm6VMC4A5CvrRnJYuCIk30",
  "worksheet": "Upload",
  "format": "ascii"
}
```

The same file could also be created with the command `clss -s
1d6Jn6lgj7wRX_HF3pOqj-hm6VMC4A5CvrRnJYuCIk30 -w Upload -f ascii args
save`. Leaving out a `range` parameter (which works like a normal
spreadsheet range like "B2:F800") means the entire worksheet named
`Upload` will be used.

And the workflow would be something like this:

``` bash

$ clss dump
Date       | User    | Project | Hours | Description                                   | Comment                   
2021-03-01 | franksh |    1002 |     5 | Stared out of the window                      |                           
2021-03-02 | franksh |    1001 |   3.5 | Invested in pyramid schemes                   |                           
2021-03-02 | franksh |    1002 |     4 | Went outside to stare into the window         |                           
2021-03-03 | franksh |    7777 |     9 | Resolved the Langlands program in one sitting | Margin too short for proof
$ clss append `date +%Y-%m-%d` "$USER" 2001 2.5 "Wrote README and documentation"
$ clss dump
Date       | User    | Project | Hours | Description                                   | Comment                   
2021-03-01 | franksh |    1002 |     5 | Stared out of the window                      |                           
2021-03-02 | franksh |    1001 |   3.5 | Invested in pyramid schemes                   |                           
2021-03-02 | franksh |    1002 |     4 | Went outside to stare into the window         |                           
2021-03-03 | franksh |    7777 |     9 | Resolved the Langlands program in one sitting | Margin too short for proof
2021-03-14 | franksh |    2001 |   2.5 | Wrote README and documentation                |                           


```

Alternatively the file could be kept offline in a `.txt`, `.csv`, or `.json` and then regularly synced up to the worksheet with `clss upload timesheet.csv`.



## Install and Setup

### Requirements

Make sure you have `python 3.7+` installed with its `pip` package
installer:

    $ pip --version
	pip 20.0.2 from /usr/lib/python3/dist-packages/pip (python 3.8)
	
(Note: `python` and `pip` might be called `python3` and `pip3` on
legacy-oriented distros such as Ubuntu.) If you don't have `pip`
installed as a separate command, note that `pip [args...]` is
equivalent to running `python -m pip [args...]`:

    $ python39 -m pip --version
    pip 21.0.1 from /home/franksh/envs/py39/lib/python3.9/site-packages/pip (python 3.9)

### Install

    $ pip install clss
	
(If not using a virtual environments, it's recommended to add the
`--user` flag to install to `~/.local` instead: `pip install --user
clss`)

Now `clss` should work:

	$ clss
	Usage: clss [OPTIONS] COMMAND [ARGS]...

	  Command-Line SpreadSheet utility.

	  Modifies Google spreadheets from command-line via Sheets API.

	Options:
	  --version                      Show the version and exit.
	  -v, --verbose                  Increase verbosity level. Use '-vv' to also
                                     show debug messages.
    ...

### Setup

Configure `clss` use a fixed spreadsheet document and worksheet for
future invocations:

``` bash
$ clss -s SPREADSHEET_ID -w WORKSHEET [-r RANGE] [-f FORMAT] args save
```

To allow the utility to interact with your Google spreadsheets it
needs Google API credentials (which allows it to request login tokens
with certain permissions from a Google user). There's several ways of
making these credentials, but the absolute easiest way is to click the
`[Enable the Google Sheets API]` button on the [API quickstart
page](https://developers.google.com/sheets/api/quickstart/python).
(Everything else on this page is irrelevant.)

Now run a command like `clss -C CREDENTIALS_FILE dump` and it should
open a browser window asking you to verify the app's login with your
Google account. (Google will complain it's unsafe and attempt to hide
the button under `[Advanced]` and `[Go to Quickstart (unsafe)]`, but
there's not much to be done about that.) The login will be cached and
refreshed in the future so this step only happens once.

(See also `clss help` and `clss help credentials` for further walls of
text essentially giving the same information.)
