"""
This file provides information of how to build and configure Fast Jet:
http://fastjet.fr

"""

import os

from ejpm.engine.env_gen import Set, Prepend
from ejpm.engine.recipe import Recipe
from ejpm.engine.commands import run, env, workdir


class FastJetRecipe(Recipe):
    """Provides data for building and installing Rave vertex reconstruction package

    (PacketInstallationInstruction is located in recipe.py)
    """

    def __init__(self):
        # Call parent constructor to fill version, app_path ... and others
        # (!) it is called AFTER we override self.version
        super(FastJetRecipe, self).__init__('fastjet')

        self.clone_command = ""
        self.unpack_command = ""         # This command is to untar downloaded array
        self.build_command = ""
        self.config['branch'] = '3.3.3'
        self.config['archive_name'] = 'fastjet-{branch}'
        self.config['repo_address'] = 'http://fastjet.fr/repo/{archive_name}.tar.gz'

    def setup(self, db):
        """Sets all variables like source dirs, build dirs, etc"""

        #
        # use_common_dirs_scheme() sets standard package variables:
        # source_path  = {app_path}/src/{branch}          # Where the sources for the current version are located
        # build_path   = {app_path}/build/{branch}        # Where sources are built. Kind of temporary dir
        # install_path = {app_path}/root-{branch}         # Where the binary installation is
        self.use_common_dirs_scheme()

        # ENV RAVEPATH $INSTALL_DIR_RAVE

        # Git download link. Clone with shallow copy
        self.config['archive_name'] = self.config['archive_name'].format(**self.config)
        self.config['repo_address'] = self.config['repo_address'].format(**self.config)
        self.clone_command = "curl -O {repo_address}".format(**self.config)
        self.unpack_command = 'tar zxvf {archive_name}.tar.gz&& mv {archive_name}/* {source_path}'.format(**self.config)
        self.build_command = './configure --prefix={install_path} &&' \
                             ' make -j{build_threads} &&' \
                             ' make check && make install' \
            .format(**self.config)

    def step_install(self):
        self.step_clone()
        self.step_build()

    def step_clone(self):
        """Clones RAVE from github mirror"""

        # Check the directory exists and not empty
        if self.source_dir_is_not_empty():
            # The directory exists and is not empty. Nothing to do
            return
        else:
            # Create the directory
            run('mkdir -p {}'.format(self.source_path))

        workdir(self.source_path)  # Go to our build directory

        run(self.clone_command)         # Execute git clone command
        run(self.unpack_command)         # Execute git clone command

    def step_build(self):
        # go to our build directory
        workdir(self.source_path)

        # run cmake && make && install
        run(self.build_command)

    @staticmethod
    def gen_env(data):
        install_path = data['install_path']
        yield Prepend('PATH', os.path.join(install_path, 'bin'))
        yield Prepend('LD_LIBRARY_PATH', os.path.join(install_path, 'lib'))

    #
    # OS dependencies are a map of software packets installed by os maintainers
    # The map should be in form:
    # os_dependencies = { 'required': {'ubuntu': "space separated packet names", 'centos': "..."},
    #                     'optional': {'ubuntu': "space separated packet names", 'centos': "..."}
    # The idea behind is to generate easy to use instructions: 'sudo apt-get install ... ... ... '
    os_dependencies = {
        'required': {
            'ubuntu': "",
            'centos': ""
        },
        'optional': {
            'ubuntu': "",
            'centos': ""
        },
    }
