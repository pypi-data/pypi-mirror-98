#!/usr/bin/env python3
# coding: utf-8

import os
import sys
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from distutils.core import run_setup
from redbaron import RedBaron

from release_new.changelog import generate_changelog


class RepositoryNotReadForReleaseError(ValueError):
    pass


def _compute_release_tags():
    commit_desc_since_last_release = (
        subprocess.check_output(
            "hg log -r 'ancestors(.) - ancestors(last(tag() and ancestors(.)))' "
            "-T '{desc}\n'",
            shell=True,
        )
        .decode("utf-8")
        .casefold()
    )

    # XXX this may be a little bit too naive. But let's make things simple for a
    # first implementation.

    if "break" in commit_desc_since_last_release:
        return "major"
    if "feat" in commit_desc_since_last_release:
        return "minor"
    if "fix" in commit_desc_since_last_release:
        return "patch"

    raise RepositoryNotReadForReleaseError(
        "We did not find any breaking change, nor feature nor fix in your "
        "commits. Are you sure you are using conventional commits ? "
        "Please, update your commit descriptions, or specify explicitly your "
        "release choice using the --release-type CLI argument."
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--release-type",
        "-r",
        choices=["patch", "minor", "major", "auto"],
        default="auto",
    )
    parser.add_argument("--no-previous-tag-check", action="store_true")
    parser.add_argument(
        "-c",
        "--preview-changelog",
        action="store_true",
        help="only display generated changelog without actually doing the release",
    )

    args = parser.parse_args()

    if args.preview_changelog:
        print(generate_changelog("upcoming release").strip())
        return

    try:
        do_release(args.release_type, args.no_previous_tag_check)
    except RepositoryNotReadForReleaseError as exception:
        # kdo Arthur
        print(f"⚠️ Error: {exception} 🤯🙉🙈💥")
        sys.exit(1)


def do_release(release_type, no_previous_tag_check):
    if release_type == "auto":
        effective_release_type = _compute_release_tags()
    else:
        effective_release_type = release_type

    root = Path(".")

    # assert there is a pkginfo and a setup.py
    pkginfo_path = root / "__pkginfo__.py"
    if not pkginfo_path.exists():
        try:
            pkginfo_path = next(root.glob("cubicweb*/__pkginfo__.py"))
        except StopIteration:
            raise RepositoryNotReadForReleaseError("no pkginfo")

    setup_path = root / "setup.py"
    if not setup_path.exists():
        raise RepositoryNotReadForReleaseError("no setup.py")

    # assert hg status is happy
    # Check only (d)eleted, (a)dded, (m)odified files
    hg_not_clean = subprocess.check_output("hg status -dram", shell=True)
    if hg_not_clean:
        raise RepositoryNotReadForReleaseError(
            "You have some work in progress. Please, make a commit and "
            "rerun the command"
        )

    current_branch = subprocess.check_output(["hg", "branch"]).strip()

    # assert on public head, and clean environment
    id_last_public = subprocess.check_output(
        [
            "hg",
            "id",
            "-r",
            f"last(public() and branch({current_branch.decode()}))",
            "--template",
            "{node}",
        ]
    )
    current_id = subprocess.check_output(
        ["hg", "id", "-r", ".", "--template", "{node}"]
    )

    if current_id != id_last_public:
        current_id_is_on_last_public = id_last_public.decode("utf-8") in set(
            subprocess.check_output(
                "hg log -r 'ancestors(.) and public()' -T '{node}\n'", shell=True
            )
            .decode("utf-8")
            .strip()
            .split("\n")
        )
        if current_id_is_on_last_public:
            raise RepositoryNotReadForReleaseError(
                "There are some non-public commits.\n"
                "Please, run `hg phase -p .` to publish your commits and rerun the "
                "command"
            )
        raise RepositoryNotReadForReleaseError(
            "You are not on the last public head, please, rebase your work on "
            f"{id_last_public.decode('utf-8')}"
        )

    debian_directory = root / "debian"
    has_debian_pkg = debian_directory.exists()

    if not has_debian_pkg:
        print("no debian directory found")

    # verify there is a debian directory
    #    dch must be installed
    #    DEBEMAIL and DEBEMAIl in os.environ
    if has_debian_pkg:
        try:
            subprocess.check_output(["which", "dch"])
        except subprocess.CalledProcessError:
            raise RepositoryNotReadForReleaseError("no dch command found")

        if "DEBEMAIL" not in os.environ:
            raise RepositoryNotReadForReleaseError("no DEBEMAIL in environment")
        if "DEBFULLNAME" not in os.environ:
            raise RepositoryNotReadForReleaseError("no DEBFULLNAME in environment")

    # get current version in the setup.py -> compare with existing tags. If it

    setup_result = run_setup(setup_path, stop_after="init")
    current_version = setup_result.get_version()

    existing_tags = (
        subprocess.check_output(["hg", "tags", "--template", "{tags}\n"])
        .decode("utf-8")
        .split("\n")
    )

    if not any(current_version in tag for tag in existing_tags):
        if not no_previous_tag_check:
            raise RepositoryNotReadForReleaseError(
                "cannot handle this situation right now. "
                f"Your current version ({current_version}) is not found in "
                f"the existing mercurial tags (last found {existing_tags[1]}).\n"
                "You can by pass previous tag check with the option: --no-previous-tag-check"
            )

    # should we check the version against pypi ?

    # exist, warn and exit
    # ask for :
    #  - patch
    #  - minor
    #  - major

    print(f"Let's go for a {effective_release_type} release")

    red = RedBaron(pkginfo_path.read_text())
    assignement = red.find("assign", target=lambda x: x.value == "numversion")
    assert assignement

    if effective_release_type == "patch":
        assignement.value[2].value = str(int(assignement.value[2].value) + 1)

    elif effective_release_type == "minor":
        assignement.value[2].value = "0"
        assignement.value[1].value = str(int(assignement.value[1].value) + 1)

    elif effective_release_type == "major":
        assignement.value[2].value = "0"
        assignement.value[1].value = "0"
        assignement.value[0].value = str(int(assignement.value[0].value) + 1)

    else:
        raise Exception("unhandled situation")

    pkginfo_path.write_text(red.dumps())

    new_version = ".".join(str(x.value) for x in assignement.value)

    if release_type == "auto":
        print(
            f"Automatic release guesser decided to release the version '{new_version}' "
            f"({effective_release_type})"
        )
        answer = input("Are you ok with that? [Y/n]: ")

        if answer.strip().lower() == "n":
            subprocess.check_call("hg revert .", shell=True)
            return

    changelog_path = Path("CHANGELOG.md")
    if changelog_path.exists():
        previous_content = changelog_path.read_text()
    else:
        previous_content = ""

    changelog_content = (
        generate_changelog(new_version).rstrip() + "\n\n" + previous_content.lstrip()
    ).strip()

    changelog_path.write_text(changelog_content)

    text_editor_command = os.environ.get("EDITOR", "nano")

    subprocess.check_call([f"{text_editor_command}", f"{changelog_path}"])

    subprocess.check_call(f"hg add '{changelog_path}'", shell=True)

    if has_debian_pkg:
        subprocess.check_call(
            f"dch -v {new_version}-1 -D unstable 'New {effective_release_type} release'",
            shell=True,
        )

    subprocess.check_call(
        f'hg commit -m "chore(pkg): new {effective_release_type} release ({new_version})"',
        shell=True,
    )

    subprocess.check_call(f'hg tag "{new_version}"', shell=True)
    subprocess.check_call("hg phase -p .", shell=True)

    # emojis for Arthur
    print(
        f"🎉 Congratulation, we've made a new {effective_release_type} release {new_version} \\o/ 🎇"
    )
    print()
    print("✨ 🍰 ✨")
    print()
    print("Now you need to hg push the new commits")
