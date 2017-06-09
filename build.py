import os
from pybuilder.core import use_plugin, init, task

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.install_dependencies")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


@task
def compile_sources():
    os.system('./src/sql/database_setup.sh')


requires_python = ">=3.4"
name = "gongbu"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("integrationtest_inherit_environment", True)
