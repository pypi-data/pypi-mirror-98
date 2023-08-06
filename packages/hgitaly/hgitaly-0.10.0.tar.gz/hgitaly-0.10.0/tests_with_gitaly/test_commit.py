# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import grpc
import pytest
from hgitaly.stub.commit_pb2 import (
    ListLastCommitsForTreeRequest,
)
from hgitaly.stub.commit_pb2_grpc import CommitServiceStub

from . import skip_comparison_tests
if skip_comparison_tests():  # pragma no cover
    pytestmark = pytest.mark.skip


def test_compare_list_last_commits_for_tree(gitaly_comparison):
    fixture = gitaly_comparison
    repo_message = fixture.gitaly_repo
    git_repo = fixture.git_repo

    wrapper = fixture.hg_repo_wrapper
    ctx0 = wrapper.write_commit('foo', message="Some foo")
    git_shas = {
        ctx0.hex(): git_repo.branches()[b'branch/default']['sha'],
    }

    sub = (wrapper.path / 'sub')
    sub.mkdir()
    subdir = (sub / 'dir')
    subdir.mkdir()
    (sub / 'bar').write_text('bar content')
    (sub / 'ba2').write_text('ba2 content')
    (subdir / 'bar').write_text('bar content')
    (subdir / 'ba2').write_text('ba2 content')
    # TODO OS indep for paths (actually TODO make wrapper.commit easier to
    # use, e.g., check how to make it accept patterns)
    ctx1 = wrapper.commit(rel_paths=['sub/bar', 'sub/ba2',
                                     'sub/dir/bar', 'sub/dir/ba2'],
                          message="zebar", add_remove=True)
    git_shas[ctx1.hex()] = git_repo.branches()[b'branch/default']['sha']
    ctx2 = wrapper.write_commit('sub/bar', message='default head')
    ctx3 = wrapper.write_commit('foo', parent=ctx1, branch='other',
                                message='other head')

    # mirror worked
    git_branches = git_repo.branches()
    assert set(git_branches) == {b'branch/default', b'branch/other'}

    # TODO check if we can access the hg-git map, would be easier
    git_shas[ctx2.hex()] = git_branches[b'branch/default']['sha']
    git_shas[ctx3.hex()] = git_branches[b'branch/other']['sha']

    hg_shas = {git: hg for hg, git in git_shas.items()}

    commit_stubs = dict(git=CommitServiceStub(fixture.gitaly_channel),
                        hg=CommitServiceStub(fixture.hgitaly_channel))

    def do_rpc(vcs, rev, path, offset=0, limit=None):
        if vcs == 'git' and len(rev) == 40:
            # defaulting useful for tests of unknown revs
            rev = git_shas.get(rev, rev)

        request = ListLastCommitsForTreeRequest(
            repository=repo_message,
            revision=rev,
            offset=offset,
            limit=1000 if limit is None else limit,
            path=path)

        def convert(sha):
            sha = sha.encode()
            if vcs == 'hg':
                return sha
            # fallback to incoming value for easier debugging than `None`
            return hg_shas.get(sha, sha)

        return [(cft.path_bytes, convert(cft.commit.id))
                for chunk in commit_stubs[vcs].ListLastCommitsForTree(request)
                for cft in chunk.commits]

    for path in (b'sub/dir', b'sub/dir/', b'', b'.', b'/', b'./',
                 b'sub', b'sub/', b'foo'):
        for rev in ('branch/default', 'branch/other', ctx2.hex(), ctx3.hex()):
            # assert do_rpc('hg', rev, path) == do_rpc('git', rev, path)
            hg_resp = do_rpc('hg', rev, path)
            git_resp = do_rpc('git', rev, path)
            assert hg_resp == git_resp

    assert (do_rpc('hg', 'branch/default', b'sub', offset=1)
            ==
            do_rpc('git', 'branch/default', b'sub', offset=1))

    rev, path = ctx2.hex(), b''
    assert (do_rpc('hg', rev, path, limit=0)
            ==
            do_rpc('git', rev, path, limit=0))

    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', rev, path, limit=-1)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', rev, path, limit=-1)
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', rev, path, offset=-1)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', rev, path, offset=-1)
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()

    # error won't be due to invalidity as a SHA
    # (let's not depend on Gitaly accepting revisions, here)
    rev = b'be0123ef' * 5
    with pytest.raises(grpc.RpcError) as exc_info_hg:
        do_rpc('hg', rev, path)
    with pytest.raises(grpc.RpcError) as exc_info_git:
        do_rpc('git', rev, path)
    assert exc_info_hg.value.code() == exc_info_git.value.code()
    assert exc_info_hg.value.details() == exc_info_git.value.details()
