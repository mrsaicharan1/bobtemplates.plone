# -*- coding: utf-8 -*-

from base import dummy_contextmanager
from base import file_exists
from base import generate_answers_ini

import os.path
import subprocess


def test_addon_content_type(tmpdir, capsys, config):
    template = """[variables]
package.description = Dummy package
package.example = True

author.name = The Plone Collective
author.email = collective@plone.org
author.github.user = collective

plone.version = {version}
""".format(
        version=config.version,
    )
    generate_answers_ini(tmpdir.strpath, template)

    # generate template addon:
    config.template = 'addon'
    config.package_name = 'collective.task'
    result = subprocess.call(
        [
            'mrbob',
            '-O', config.package_name,
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=tmpdir.strpath,
    )
    assert result == 0

    wd = os.path.abspath(
        os.path.join(tmpdir.strpath, config.package_name),
    )

    # generate subtemplate content_type:
    template = """[variables]
dexterity_type_name = Tasks Container
dexterity_type_base_class = Container
dexterity_type_create_class = Yes
dexterity_type_global_allow = Yes
dexterity_type_filter_content_types = No
subtemplate_warning = Yes
dexterity_type_desc = A tasks container for Plone
dexterity_type_supermodel = Yes
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    # generate 2. subtemplate content_type with Item instead of Container:
    template = """[variables]
dexterity_type_name = Task Item
dexterity_type_base_class = Item
dexterity_type_create_class = Yes
dexterity_type_global_allow = Yes
subtemplate_warning = Yes
dexterity_type_desc = A task Task content type for Plone
dexterity_type_supermodel = Yes
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    # generate subtemplate content_type with generic class:
    template = """[variables]
dexterity_type_name = Generic Tasks Container
dexterity_type_base_class = Container
dexterity_type_create_class = No
dexterity_type_global_allow = Yes
dexterity_type_filter_content_types = No
subtemplate_warning = Yes
dexterity_type_desc = A tasks container for Plone
dexterity_type_supermodel = Yes
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    # generate subtemplate content_type with generic class:
    template = """[variables]
dexterity_type_name = Task Item Python Schema
dexterity_type_base_class = Item
dexterity_type_create_class = Yes
dexterity_type_global_allow = Yes
dexterity_type_filter_content_types = No
subtemplate_warning = Yes
dexterity_type_desc = A tasks container for Plone
dexterity_type_supermodel = No
"""
    generate_answers_ini(wd, template)

    config.template = 'content_type'
    result = subprocess.call(
        [
            'mrbob',
            'bobtemplates.plone:' + config.template,
            '--config', 'answers.ini',
            '--non-interactive',
        ],
        cwd=wd,
    )
    assert result == 0

    assert file_exists(wd, '/src/collective/task/configure.zcml')

    with capsys.disabled() if config.verbose else dummy_contextmanager():
        setup_virtualenv_result = subprocess.call(
            [
                'virtualenv',
                '.',
            ],
            cwd=wd,
        )
        assert setup_virtualenv_result == 0
        install_buildout_result = subprocess.call(
            [
                './bin/pip',
                'install',
                '-U',
                '-r',
                'requirements.txt',
            ],
            cwd=wd,
        )
        assert install_buildout_result == 0
        annotate_result = subprocess.call(
            [
                'bin/buildout',
                'code-analysis:return-status-codes=True',
                'annotate',
            ],
            cwd=wd,
        )
        assert annotate_result == 0
        buildout_result = subprocess.call(
            [
                'bin/buildout',
                'code-analysis:return-status-codes=True',
            ],
            cwd=wd,
        )
        assert buildout_result == 0
        test_result = subprocess.call(
            ['bin/test'],
            cwd=wd,
        )
        assert test_result == 0
        test__code_convention_result = subprocess.call(
            ['bin/code-analysis'],
            cwd=wd,
        )
        assert test__code_convention_result == 0
