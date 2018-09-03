#! /usr/bin/python

from git import Repo
import os
import io
import shutil
import sys
import getopt
import tempfile
import argparse

IGNORE_PATTERNS = ('.git', ".DS_Store")
SAFE_CHARS = ["-", "_", "."]
DEFAULT_STEP_BRANCH = "master"
IS_BRANCH_STRING = "Step"

MAX_LENGTH = 100

def makeBranches(repo_directory, branch_code_steps, verbose, test):
    print repo_directory
    print branch_code_steps
    repo = Repo(repo_directory)

    repo.git.checkout(branch_code_steps)
    for commitHash in repo.git.rev_list(branch_code_steps).split("\n"):
        commit = repo.commit(commitHash)

        branch_name = get_branch_name_from_commit_message(commit.message)
        if verbose:
            print "Branch: ", branch_name, " for commit ", commitHash

        if test == False and IS_BRANCH_STRING in branch_name:
            if branch_name in repo.branches:
                 repo.git.branch(branch_name, "-D")
            new_branch = repo.create_head(branch_name)
            new_branch.set_commit(commitHash)
            

def get_branch_name_from_commit_message(message):
    first_line = message.splitlines()[0]
    safe_message = "".join(
        c for c in first_line if c.isalnum() or c in SAFE_CHARS).strip()
    return (safe_message[:MAX_LENGTH]
            if len(safe_message) >
            MAX_LENGTH else safe_message)



DESCRIPTION = "This script "

EPILOG = " To make changes to "


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        epilog=EPILOG,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-d', '--directory',
                        default=os.getcwd(),
                        help="the directory of the repository")

    parser.add_argument('-b', '--branch', default=DEFAULT_STEP_BRANCH,
                        help="branch where the steps are. Default is master")

    parser.add_argument('-v', '--verbose', default=False, const=True,
			help="print out expected results. Default is false",
                        nargs='?')

    parser.add_argument('-t', '--test', default=False, const=True,
                        help="test only. Do not create branches",
                        nargs='?')

    parsed = parser.parse_args()

    makeBranches(
        parsed.directory,
        parsed.branch,
	parsed.verbose,
        parsed.test
        )


if __name__ == "__main__":
    sys.exit(main())
