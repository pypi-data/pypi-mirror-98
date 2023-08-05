# skulk

## Install

```bash
pip install skulk
```

## Git hook

Put the following code into the file `./.git/hooks/pre-push`

```
#!/usr/bin/env python

import sys
from skulk import skulk
skulk.run_pre_push_checks()
sys.exit(0)
```

Now when you push your code, if the checks fail the push will be blocked and you'll be asked to run `skulk` from the command-line.

## Command-line usage

Simply run skulk from your repo. It runs as a wizard and helps you to set a valid version and update your changelog.

```
skulk
```

Example session:

```
julian@papaya:~/dev/conductor/myproject > skulk
Latest Versions:
{
   "tag": "1.0.0",
   "testpypi": "0.0.1",
   "prodpypi": "0.0.0"
}
Current version:  1.0.0
Version invalid: (1.0.0) must be greater than (1.0.0)
To bump the version, please enter the type of change this push represents...
1:Fix.
2:Feature.
3:Breaking change.
4:Abort!
Enter a number: 1
You bumped the version to: (1.0.1)
Overwriting version file...
resolve changelog here:
Edit and save the changelog now. Here are some recent commits...
==============================
* Fix atomic url and fix bug in get_pip_name. [a9c06d9]
* Better readme grammar. [194f6f8]
==============================
A new section has been prepended to your changelog.
Please edit and save your CHANGELOG (There's no need to commit), then press enter to continue.
Done! The repo is now in good shape and ready to push.
Do you want me to run `git push origin circleci-project-setup` for you?
0:No
1:Yes
Enter a number: 0
No worries. Use the above command to push the branch later. Bye
```