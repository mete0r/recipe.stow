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
import logging
import os.path


logger = logging.getLogger(__name__)


class Recipe:

    def __init__(self, buildout, name, options):
        sections = tuple(options_get_items(options, 'sections'))
        # trigger install other sections
        for section in sections:
            buildout[section]

        destination = buildout['buildout']['parts-directory']
        destination = os.path.join(destination, name)
        destination = options.setdefault('destination', destination)
        # TODO: check whether source & destination overwrap

        self.__buildout = buildout
        self.__sections = sections
        self.__destination = destination

    def install(self):
        buildout = self.__buildout
        sections = self.__sections
        destination = self.__destination
        destination = os.path.abspath(destination)
        buildout_directory = buildout['buildout']['directory']
        buildout_directory = os.path.abspath(buildout_directory)
        installed_sections = buildout_read_installed_options(buildout,
                                                             sections)
        for installed_section in installed_sections:
            section_name = installed_section.name
            logger.debug('* Section %s:', section_name)

            installed_files = options_get_items(installed_section,
                                                '__buildout_installed__')
            for src_abspath in installed_files:
                relpath = os.path.relpath(src_abspath, buildout_directory)
                dst_abspath = os.path.join(destination, relpath)

                if not os.path.exists(src_abspath):
                    logger.warning('- Skipping %s: not exists',
                                   src_abspath)
                    continue
                if os.path.isdir(src_abspath):
                    # TODO:
                    continue
                logger.debug('- Symlinking %s -> %s', relpath, dst_abspath)
                try:
                    dst_dir = os.path.dirname(dst_abspath)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    os.symlink(src_abspath, dst_abspath)
                except Exception as e:
                    logger.exception(e)
                    logger.warning('  ! Failed to symlink at: %s', dst_abspath)
                else:
                    yield dst_abspath

    def update(self):
        return self.install()


def buildout_read_installed_options(buildout, sections):

    # XXX: using private API
    installed_part_options, installed_exists =\
        buildout._read_installed_part_options()

    for name in sections:
        if name in installed_part_options:
            options = installed_part_options[name]
        else:
            options = buildout.Options(buildout, name, {})
        yield options


def options_get_items(options, name):
    if name in options:
        lines = options[name]
        lines = lines.strip()
        if not lines:
            return ()
        lines = lines.split()
        lines = (path.strip() for path in lines)
        return lines
    else:
        return ()
