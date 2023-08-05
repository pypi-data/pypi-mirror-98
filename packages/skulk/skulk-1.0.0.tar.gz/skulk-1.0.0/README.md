# skulk

## Install

```bash
pip install skulk
```

## Git hook usage

The intention is to put the following code into the file `./.git/hooks/pre-push`

```
#!/usr/bin/env python

import sys
from skulk import skulk
skulk.run_pre_push_checks()
sys.exit(0)
```

When you push your code, if the checks fail the push will be blocked and you'll be asked to run `skulk` from the command-line.

## Command-line usage

Simply run skulk from your repo. It runs as a wizard and helps you to set a valid version and update your changelog.

```
skulk
```