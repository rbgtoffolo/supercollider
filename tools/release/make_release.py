#!/bin/env python

# This script provides an automated checklist for running through all the steps required for a release.

from collections import deque

def check_step(step: str) -> bool:
    print("\nCHECK: ", step)
    response = input("  Press Y OR y to continue; Anything else to Quit: ")
    if response not in ['Y', 'y']:
        return False
    else:
        return True

# Stage base class.
# To make a release, we run through a list of stages in order.
# To undo the work done so far in a release ("bail out"), undo the stages
# completed so far in the reverse order.
class Stage:
    # 'do' should return True to indicate the task succeeded and the release can proceed, or False to indicate the task
    # failed and we should bail out of the release.
    def do(self) -> bool:
        return True

    def undo(self):
        pass

# Performs no actions, simply asks the user whether or not they have completed a task.
class YesNoStage(Stage):
    def __init__(self, prompt):
        self.prompt = prompt

    def do(self) -> bool:
        return check_step(self.prompt)

    def undo(self):
        print("UNDOING:", self.prompt)


def main():
    prompts = [
        "Is the repo clean?",
        "If this is a minor release, have you made the release branch?",
        "Is the repo on the current release branch?",
        "Have all the discussions in the 'x.y.z discussions' ticket been resolved?",
        "If this is a patch release, have all the PRs in the cherry-pick GitHub project been added to the release branch?",
        "Have all the deprecations been either removed or deferred to a later release?\n      Deprecations are removed on a case-by-case basis with each minor (3.x) release.\n      Corresponding UGen and primitive code should also be removed.\n      Be careful when deprecating UGens and be considerate of alternate clients!",
        "Have all the removed deprecations been documented in the changelog?",
        "Have you reviewed the platform support information in the main README.md for accuracy?",

        "Have you updated SCVersion.txt?",
        "Have you updated CHANGELOG.md with information about merged PRs?",
        "Have you updated CHANGELOG.md with information about platform support changes?",

        "Have you made sure the schelp file 'News in 3.x' is up to date with the changelog by running the conversion script?", # XXX where is the script?
        "Have you made sure HelpSource/Help.schelp points to the latest 'News in 3.x' schelp file?",
        "If this is a proper release, have you updated the release history in README.md?",
        "If this is a proper release, have you merged the current release branch into master with git merge --no-ff?",
        "Have you tagged the release?",
        "Did you create the release announcement text?",
        "Have you created a release on GitHub?",
        "Have you run ./package/create_source_tarball.sh -v <version> (where version is the version tag, e.g. Version-3.11.0) to create a source tarball (including submodules)?",
        "Have you optionally run the script with -s <email-or-keyid> (where email-or-keyid is a valid PGP key id of the release manager) to also create a detached PGP signature for the source tarball?",
        "Have you uploaded source tarball (and optionally detached PGP signature)?",
        "Are builds for macOS, Linux, and Windows uploaded from CI?",
        "Have you made sure to note known-to-work platform versions and any changes in platform support on the Github release page?",
        "If it is a full release, did you update the website download page?",

        "Did you do the same for sc3-plugins?", # XXX review what does this mean

        "Did you update the sc3-plugins page (the one at https://github.com/supercollider/sc3-plugins/tree/master/website)?",
        "If it's a proper release, did you update the Wikipedia page?",

        "Have you created the text with an abbreviated changelog for announcing?", # XXX review what does this mean
        "Did you announce on GitHub website?",
        "Did you announce on sc-users mailing list?",
        "Did you announce on sc-dev mailing list?",
        "Did you announce on scsynth.org?",
        "Did you announce on Slack #general?",
        "Did you announce on Facebook group?",
        "Did you announce on Reddit (/r/supercollider)?",

        "If it's a beta release, did you merge the current release branch into develop? Do not merge the release branch into master yet!",
        "If it's a proper release, did you merge master into develop?",
            ];

    stack = deque()
    for prompt in prompts:
        stage = YesNoStage(prompt)
        if stage.do():
            stack.append(stage)
        else:
            print("\nUndoing release stages\n")
            while len(stack):
                stack.pop().undo()
            break

if __name__ == "__main__":
    main()
