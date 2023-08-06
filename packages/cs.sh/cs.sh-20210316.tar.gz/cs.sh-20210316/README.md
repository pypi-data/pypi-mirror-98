Convenience functions for constructing shell commands

*Latest release 20210316*:
Minor doc update.

Functions for safely constructing shell command lines from bare strings.
Somewhat like the inverse of the shlex stdlib module.

As of Python 3.3 the function `shlex.quote()` does what `quotestr()` does.

As of Python 3.8 the function `shlex.join()` does what `quotecmd()` does.

## Function `main_shqstr(argv=None)`

shqstr: emit shell-quoted form of the command line arguments.

## Function `quote(args)`

Quote the supplied strings, return a list of the quoted strings.

As of Python 3.8 the function `shlex.join()` is available for this.

## Function `quotecmd(argv)`

Quote strings, assemble into command string.

## Function `quotestr(s)`

Quote a string for use on a shell command line.

As of Python 3.3 the function `shlex.quote()` is available for this.

# Release Log



*Release 20210316*:
Minor doc update.

*Release 20180613*:
Rework quotestr significantly to provide somewhat friendlier quoting, include "," in the SAFECHARS.

*Release 20170903.2*:
bugfix __main__ boilerplate after setuptools workaround

*Release 20170903.1*:
workaround setuptool's slightly dumb console_scripts call of a "main" function

*Release 20170903*:
shqstr command; new quotecmd(argv) function

*Release 20150118*:
Extend SAFECHARS to include colon.

*Release 20150111*:
minor cleanup

*Release 20150107*:
initial standalone public release
