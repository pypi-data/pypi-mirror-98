#
#  Copyright (c) 2021 Russell Smiley
#
#  This file is part of build_harness.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import contextlib
import pathlib
import tempfile
import typing

import git
import pytest
from git import GitCommandError

import build_harness.tools
from build_harness.tools.git import (
    GitRepoError,
    TagData,
    TagDataError,
    _is_commit_tagged,
    _parse_describe,
    get_tag_data,
)
from tests.ci.support.repo import (
    FeatureDryrunTagOnHead,
    FeatureDryrunTags,
    NoTags,
    TagBase,
    TagOnDefaultHeadOnFeature,
    TagOnHead,
)


class SimpleTags(TagBase):
    def __init__(self, tag: str):
        super().__init__(tag)

    def __call__(self, repo: git.Repo, repo_dir: pathlib.Path):
        self._commit_file(repo_dir / "c1", repo)
        repo.create_tag(self.tag, message="default branch tag")
        self._commit_file(repo_dir / "c2", repo)


@contextlib.contextmanager
def temp_repo(repo_init: TagBase) -> typing.Generator[git.Repo, None, None]:
    with tempfile.TemporaryDirectory() as dir:
        repo_path = pathlib.Path(dir)
        repo = git.Repo.init(str(repo_path))
        repo_init(repo, repo_path)

        yield repo, repo_path


class TestIsCommitTagged:
    def test_true(self):
        with temp_repo(SimpleTags("some_tag")) as (git_repo, repo_path):
            assert _is_commit_tagged(git_repo.commit("HEAD^"), git_repo)

    def test_false(self):
        with temp_repo(SimpleTags("some_tag")) as (git_repo, repo_path):
            assert not _is_commit_tagged(git_repo.head.commit, git_repo)


class TestParseDescribe:
    def test_semantic_tag(self):
        mock_describe = "3.1.4"

        result = _parse_describe(mock_describe)

        assert result == TagData(tag="3.1.4", offset=None)

    def test_semantic_tag_offset(self):
        mock_describe = "3.1.4-14-gc3ba625"

        result = _parse_describe(mock_describe)

        assert result == TagData(tag="3.1.4", offset="14")

    def test_pep440_tag_offset(self):
        mock_describe = "3!1.4.15.92a6.post5.dev4-14-gc3ba625"

        result = _parse_describe(mock_describe)

        assert result == TagData(tag="3!1.4.15.92a6.post5.dev4", offset="14")

    def test_no_match(self, mocker):
        mock_describe = "3!1.4.15.92a6.post5.dev4-some-stuff"

        # The regex pattern seems to be quite strong, so not an obvious path to an
        # error here. Just use a patch to force the error state.
        mocker.patch("build_harness.tools.git.re.search", return_value=None)

        with pytest.raises(TagDataError):
            _parse_describe(mock_describe)


class TestGetTagData:
    def test_semantic_tag(self):
        expected_tag_data = TagData(tag="1!2.3a4.dev6", offset=None)

        with temp_repo(TagOnHead("1!2.3a4.dev6")) as (git_repo, repo_path):
            result = get_tag_data(repo_path)

        assert result == expected_tag_data

    def test_dryrun_on_head(self):
        """Dryrun tag on HEAD gets used as-is."""
        expected_tag_data = TagData(tag="3.1+dryrun2")

        with temp_repo(FeatureDryrunTagOnHead("1!2.3a4.dev6")) as (git_repo, repo_path):
            result = get_tag_data(repo_path)

        assert result == expected_tag_data

    def test_dryrun_in_history(self):
        """Dryrun tags in commit history get ignored."""
        expected_tag_data = TagData(tag="1!2.3a4.dev6", offset="4")

        with temp_repo(FeatureDryrunTags("1!2.3a4.dev6")) as (git_repo, repo_path):
            result = get_tag_data(repo_path)

        assert result == expected_tag_data

    def test_nondefault_branch(self):
        expected_tag_data = TagData(tag="0.0.0", offset="1")

        with temp_repo(NoTags()) as (git_repo, repo_path):
            nb = git_repo.create_head("other_branch")
            git_repo.head.reference = nb
            git_repo.head.reset(index=True, working_tree=True)
            git_repo.delete_head(git_repo.heads.master)

            result = get_tag_data(repo_path, default_branch_name="other_branch")

        assert result == expected_tag_data

    def test_semantic_tag_offset(self):
        expected_tag_data = TagData(tag="3.1.4", offset="2")
        with temp_repo(TagOnDefaultHeadOnFeature("3.1.4")) as (git_repo, repo_path):
            result = get_tag_data(repo_path)

        assert result == expected_tag_data

    def test_no_tag(self):
        expected_tag_data = TagData(tag="0.0.0", offset="1")

        with temp_repo(NoTags()) as (git_repo, repo_path):
            result = get_tag_data(repo_path)

        assert result == expected_tag_data

    def test_bad_tag(self):
        with tempfile.TemporaryDirectory() as this_dir:
            mock_path = pathlib.Path(this_dir)

            with pytest.raises(GitRepoError, match=r"^Invalid git repository"):
                get_tag_data(mock_path)
