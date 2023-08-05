#!/usr/bin/env python

"""
Skulk.

A tool to help get your repo in good shape before pushing.

It works for packages intended for PyPi.

It has 2 public functions:

1. main() : A wizard that guides you to chhoosing a version that does not conflict with any git tags or PyPi versions.

2. run_pre_push_checks() : A function that is designed to be called from a git pre-push hook.

Assumptions:
1. You have a file named VERSION at the top level of the repo. It should contain a simple semver such as 1.2.3
2. You have a CHANGELOG.md  at the top level of the repo.


"""

from __future__ import print_function
from builtins import input
import datetime
import os
import re
import json
import subprocess
import sys
from distutils.version import LooseVersion
from shutil import rmtree

from git import InvalidGitRepositoryError, Repo

PROD_PYPI_INDEX = u"https://pypi.org/simple/"
TEST_PYPI_INDEX = u"https://test.pypi.org/simple/"

def _green(rhs):
    return "\033[92m{}\033[0m".format(rhs)


def _red(rhs):
    return "\033[91m{}\033[0m".format(rhs)


def _get_commits_since_last_tag(repo):
    """Return recent commits, or all commits if no tag."""
    last_tag = _get_last_tag_version(repo)
    if last_tag:
        rev_spec = "{}..HEAD".format(last_tag)
        commits = repo.iter_commits(rev_spec)
    else:
        commits = repo.iter_commits(repo.head)
    return commits


def _get_commit_messages_since_last_tag(repo):
    """Return recent commit messages with truncated hashes."""
    commits = _get_commits_since_last_tag(repo)
    messages = []
    for commit in commits:
        msg = commit.message.encode('utf-8').strip()
        messages.append(
            "* {}. [{}]".format(msg.capitalize(),  commit.hexsha[:7]))
    return messages


def _get_version_file(repo):
    """Get the VERSION file from the top level of the repo."""
    version_file = os.path.join(repo.working_dir, "VERSION")
    if not os.path.isfile(version_file):
        msg = "VERSION file does not exist at the top level of the repo.\n"
        msg += "Add a file (VERSION) with a numeric only version such as 1.2.3\n"
        sys.stderr.write(msg)
        sys.exit(1)
    return version_file


def _get_changelog(repo):
    """Get the CHANGELOG file from the top level of the repo."""
    changelog = os.path.join(
        repo.working_dir, "CHANGELOG.md")
    if not os.path.isfile(changelog):
        sys.stderr.write(
            "CHANGELOG does not exist. Please create it and try again. {}\n".format(changelog))
        sys.exit(1)
    return changelog


def _get_version(version_file):
    """Pull the version from the VERSION file.
    """
    try:
        return _first_nonblank_line(version_file)
    except:
        sys.stderr.write(
            "Can't get version used in the changelog. {}\n".format(version_file))


def _get_test_pypi_versions(pip_name):
    return _get_pypi_versions(pip_name, TEST_PYPI_INDEX)


def _get_prod_pypi_versions(pip_name):
    return _get_pypi_versions(pip_name, PROD_PYPI_INDEX)


def _get_pypi_versions(pip_name, index):
    """
    Return a list of all PyPi versions for the named package.

    The package may not exist on PyPi, in which case we return an empty list. We
    don't error out, because it's perfectly valid for no package to exist. We
    can still deploy there.
    """
    result = []

    # notice this command says: Install version== (i.e. it requests an invalid
    # version). It fails as intended, and the result is a message to say can't
    # find version in versions. It lists the existing versions which we split
    # and return.
    args = ['pip', 'install', '--index-url', index, "{}==".format(pip_name)]

    output = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()

    try:
        output = output[1]
    except IndexError:
        return []

    regex = re.compile(
        r'^.*Could not find a version.*from versions:(.*)\).*', re.DOTALL)
    match = regex.match(output.decode('utf-8'))
    if match:
        result = [v.strip() for v in match.group(1).split(r', ')]
        result = _sorted_numeric_versions(result)
    return result


def _get_pip_name(repo):
    """
    Return the pip name, which may be different than the repo name.

    If the pip name is different, it should be the first line of the MANIFEST
    file as a comment.
    """
    manifest_file = os.path.join(repo.working_dir, "MANIFEST.in")
    try:
        first_line = _first_nonblank_line(manifest_file)
        if first_line[0] == "#":
            return first_line.split(" ")[1]
    finally:
        return os.path.basename(repo.working_dir)


def _version_is_valid(last_versions, version):
    """
    Return True if the version is the most recent and unique.

    The version is tested agfainst both the tags, and the PyPi versions.
    """
    versions = _sorted_numeric_versions([
        last_versions["testpypi"],
        last_versions["prodpypi"],
        last_versions["tag"], 
        version])
    print("Current version: " ,version)
    return (versions[-1] == version) and (versions[-2] != versions[-1])

def _get_last_versions(repo):
    """Get the most recent of each version: testpypi, prodpypi, git-tag."""
    pip_name = _get_pip_name(repo)
    print("Getting PyPi versions for",  )
    test_pypi_versions = _get_test_pypi_versions(pip_name)
    prod_pypi_versions = _get_prod_pypi_versions(pip_name)
    return {
        "testpypi": test_pypi_versions[-1] if test_pypi_versions else "0.0.0",
        "prodpypi": prod_pypi_versions[-1] if prod_pypi_versions else "0.0.0",
        "tag": _get_last_tag_version(repo) or "0.0.0"
    }

def _get_last_tag_version(repo):
    """Get the most recent git tag version"""
    tags = _sorted_numeric_versions(repo.tags)
    if tags:
        return str(tags[-1])


def _get_last_changelog_version(changelog):
    """
    Extract the version from first line of the changelog.
    """
    try:
        return _first_nonblank_line(changelog).split(":")[1].split(" ")[0].strip()
    except:
        sys.stderr.write(
            "Can't get the last version used in the changelog. {}\n".format(changelog))


def _nonblank_lines(fileobject):
    """Generator to help search a file."""
    for line in fileobject:
        line = line.rstrip()
        if line:
            yield line


def _first_nonblank_line(filename):
    """Use a generator to return the first non blank line, or None."""
    try:
        with open(filename) as f:
            gen = _nonblank_lines(f)
            return next(gen, None)
    except:
        pass


def _get_repo():
    """Return the Repository object.

    Exit if not in a workable state.
    """
    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        sys.stderr.write("Not a git repo. Can't continue.\n")
        sys.exit(1)
    if repo.untracked_files:
        sys.stderr.write("Untracked files. Can't continue.\n")
        sys.exit(1)
    if repo.is_dirty():
        sys.stderr.write("Dirty repo. Can't continue.\n")
        sys.exit(1)
    return repo


def _resolve_version(repo, version, version_file):
    """
    Resolve and return the version we want to use.

    If currentr version is valid, user has the option to bump it.
    Otherwise he must bump it.
    """
    last_versions  = _get_last_versions(repo) 

    print("Latest Versions:")
    print(json.dumps(last_versions, indent=3))

    
    versions = _sorted_numeric_versions([
        last_versions["testpypi"],
        last_versions["prodpypi"],
        last_versions["tag"], 
        version])
    
    valid =  _version_is_valid(last_versions, version)
    do_bump = True
    if not valid:
        print("Version invalid: ({}) must be greater than ({})".format(version, versions[-1]))
    else:
        print("Version is valid ({}). However, you may bump it if you wish.".format(version))
        do_bump = _yes_no("Do you wish to bump the version anyway?")

    if not do_bump:
        return version
        
    print("To bump the version, please enter the type of change this push represents...")

    options = ["Fix.",
               "Feature.",
               "Breaking change.",
               "Abort!"]
    for i, opt in enumerate(options):
        print("{}:{}".format(i+1, opt))
    inp = int(input(_green("Enter a number: ")))

    if inp not in [1, 2, 3]:
        sys.stderr.write("Aborted:\n")
        sys.exit(1)

    version = _bump(versions[-1], inp)

    print("You bumped the version to: ({})".format(version))

    print("Overwriting version file...")
    with open(version_file, "w") as f:
        f.write(version)

    return version


def _bump(version, which):
    """
    Return a bumped sem-ver version according to which.

    which = 1:patch, 2:minor, 3:major 
    """
    parts = [int(c) for c in version.split(".")]
    if which == 1:
        parts[2] += 1
    elif which == 2:
        parts[1] += 1
        parts[2] = 0
    else:
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    return ".".join([str(p) for p in parts])


def _resolve_changelog(repo, version, changelog):
    """
    Help the user to get the changelog up-to-date.

    We print recent commit messages in the shell, and insert them under a
    heading in the CHANGELOG. The user only needs to edit for human clarity then
    save the file and hit continue.
    """
    print("resolve changelog here:")

    print("Edit and save the changelog now. Here are some recent commits...")

    most_recent_messages = _get_commit_messages_since_last_tag(repo)
    print ("=" * 30)
    for msg in most_recent_messages:
        print(msg)
    print ("=" * 30)

    today = datetime.date.today().strftime("%d %b %Y")
    recent_block = "### Version:{} -- {}\n\n".format(version, today)
    recent_block += "\n".join(most_recent_messages) or ""

    with open(changelog, 'r') as clog:
        data = clog.read() or "--"

    new_content = recent_block + "\n\n" + data

    with open(changelog, 'w') as clog:
        clog.write(new_content)

    print("A new section has been prepended to your changelog.")

    input(
        _green("Please edit and save your CHANGELOG (There's no need to commit), then press enter to continue."))


def _yes_no(question):
    options = ["No", "Yes"]
    print(question)
    for i, opt in enumerate(options):
        print("{}:{}".format(i, opt))
    while True:
        inp = int(input(_green("Enter a number: ")))
        if inp in [0,1]:
            return [False, True][inp]
        else:
            print("You must choose 0 for No, or 1 for Yes..")


def _check_clean(repo):
    options = ["Fix manually and continue",
               "Auto commit and continue", "Abort"]
    while repo.is_dirty():
        print("Repo is dirty. Maybe you changed something else along the way?")
        for i, opt in enumerate(options):
            print("{}:{}".format(i, opt))

        inp = int(input(_green("Enter a number: ")))

        if inp == 1:
            repo.index.add(["*"])
            repo.index.commit(
                "Staged and committed various files to ensure clean repo")
            print("Commit misc files")
        elif inp == 2:
            sys.stderr.write("Aborted:\n")
            sys.stderr.write(
                "NOTE: Although this stage was stopped. Changes may have been mnade t teh version and changelog already.\n")
            sys.exit(1)


def _sorted_numeric_versions(versions):
    if versions:
        return sorted( [str(v) for v in versions if str(v)[0].isdigit()], key=LooseVersion )

    return []


def run_pre_push_checks():
    """
    Non interactive check for version issues.

    This function is intended to be called from a pre_push git hook.

    The content of the hook file should be as follows:

    #!/usr/bin/env python

    import sys
    from skulk import skulk
    skulk.run_pre_push_checks()
    sys.exit(0)

    """
    repo = _get_repo()
    version_file = _get_version_file(repo)
    version = _get_version(version_file)

    last_versions = _get_last_versions(repo) 

    if not _version_is_valid(last_versions, version):
        sys.stderr.write(
            "Version {} is not valid.\nCan't continue. Please run skulk to rectify this.\n".format(version))
        sys.exit(1)

    changelog = _get_changelog(repo)
    last_changelog_version = _get_last_changelog_version(changelog)
    if last_changelog_version != version:
        msg = "The last CHANGELOG entry ({}) is not up to date with the current version ({}).\n"
        msg += "Can't continue. Please run skulk to rectify this.\n"
        sys.stderr.write(msg.format(last_changelog_version, version))
        sys.exit(1)


def main():
    """
    Wizard to guide the user to ensure version and changelog are valid.
    """
    repo = _get_repo()

    version_file = _get_version_file(repo)
    version = _get_version(version_file)
    changelog = _get_changelog(repo)

    version = _resolve_version(repo, version, version_file)
    _resolve_changelog(repo, version, changelog)

    if repo.is_dirty():
        repo.index.add([changelog, version_file])
        repo.index.commit(
            "Updates Changelog and sets version to {}".format(version))

    _check_clean(repo)

    sys.stderr.write("Done! The repo is now in good shape and ready to push.\n")

    do_push = _yes_no("Do you want me to run `git push origin {}` for you?".format(
        repo.active_branch.name))

    if do_push:
        os.system("git push origin {}".format(repo.active_branch.name))
        print("Pushed...\n")
    else:
        print("No worries. Use the above command to push the branch later. Bye\n")

    sys.exit(0)

 
if __name__ == "__main__":
    main()
