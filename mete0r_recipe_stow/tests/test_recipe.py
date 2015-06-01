# -*- coding: utf-8 -*-
#
#   mete0r.recipe.stow : a buildout recipe to stow/unstow generated files
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from unittest import TestCase
import os.path
import shutil


from ..recipe import Recipe


class WorkspaceLayer:

    WORKSPACE_NAME = '.testworkspace'

    @classmethod
    def setUp(cls):
        if not os.path.isdir(cls.WORKSPACE_NAME):
            os.mkdir(cls.WORKSPACE_NAME)


class RecipeTest(TestCase):

    def test_nothing(self):
        pass


class FunctionsTest(TestCase):

    layer = WorkspaceLayer

    @property
    def workspace(self):
        workspace = os.path.join(self.layer.WORKSPACE_NAME, self.id())
        workspace = os.path.abspath(workspace)
        return workspace

    def setUp(self):
        workspace = self.workspace
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
        os.mkdir(workspace)

    def test_options_get_multiline(self):
        from ..recipe import options_get_items
        options = {
            '__buildout_installed__': '/opt/foo/bar'
        }
        items = list(options_get_items(options, '__buildout_installed__'))
        self.assertEquals(['/opt/foo/bar'], items)

    def test_make_symlink(self):
        from ..recipe import make_symlink
        src = os.path.join(self.workspace, 'src')
        dst = os.path.join(self.workspace, 'dst')
        with open(src, 'w') as f:
            f.write('foobar')
        make_symlink(src, dst)
        self.assertEquals(src, os.readlink(dst))
        make_symlink(src, dst)
        os.remove(dst)

        other = os.path.join(self.workspace, 'other')
        with open(other, 'w') as f:
            f.write('other')
        make_symlink(other, dst)
        self.assertRaises(OSError, make_symlink, src, dst)
