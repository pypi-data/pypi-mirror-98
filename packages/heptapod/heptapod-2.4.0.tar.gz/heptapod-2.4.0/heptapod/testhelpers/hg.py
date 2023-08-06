# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Compatibility layer for externalisation of testhelpers."""

import os

from mercurial_testhelpers.repo_wrapper import (
    RepoWrapper as CoreRepoWrapper,
    as_bytes,
)


class RepoWrapper(CoreRepoWrapper):

    write_commit = CoreRepoWrapper.commit_file
    commit_remove = CoreRepoWrapper.commit_removal

    def prune(self, revs, successors=(), bookmarks=()):
        # the prune command expects to get all these arguments (it relies
        # on the CLI defaults but doesn't have any at the function call level).
        # They are unconditionally concatened to lists, hence must be lists.
        # (as of Mercurial 5.3.1)
        if isinstance(revs, (bytes, str)):
            revs = [revs]
        return self.command('prune',
                            rev=[as_bytes(r) for r in revs],
                            new=[],  # deprecated yet expected
                            # TODO py3 convert these two to bytes as needed:
                            successor=list(successors),
                            bookmark=list(bookmarks))

    def set_topic(self, topic):
        self.command('topics', as_bytes(topic))

    def amend_file(self, relative_path, content=None, message=None):
        if content is None:
            content = self.random_content()
        content = as_bytes(content)

        if message is None:
            message = content
        else:
            message = as_bytes(message)

        path = os.path.join(self.repo.root, as_bytes(relative_path))
        with open(path, 'wb') as fobj:
            fobj.write(content)
        self.command('amend', message=message)
        return self.repo[b'tip']


RepoWrapper.register_commit_option('topic', 'set_topic')

# compatibility alias
LocalRepoWrapper = RepoWrapper
