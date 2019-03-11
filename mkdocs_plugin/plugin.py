"""
Databio group plugin for MkDocs

Group software page: http://databio.org/software/
"""

import os
import glob
import subprocess
import time

import mkdocs
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import build

from lucidoc import run_lucidoc

TIMER = 0


class AutoDocumenter(BasePlugin):
    """ Populate automatic documentation markdown. """
    config_scheme = (
        ("jupyter_source", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_jupyter")),
        ("jupyter_build", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_jupyter/build")),
        ("autodoc_package", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=None)),
        ("docstring_style", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="rst")),
        ("no_top_level", mkdocs.config.config_options.Type(bool, default=False)),
        ("include_inherited", mkdocs.config.config_options.Type(bool, default=False)),
        ("autodoc_build", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_build")),
        ("usage_template", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs/usage_template.md")),
        ("usage_cmds", mkdocs.config.config_options.Type((list, mkdocs.utils.string_types), default=[])),
    )

    def on_files(self, files, config):

        # Add non docs_dir files that are rendered versions to this.
        # This will allow them to be used in the final rendered HTML pages,
        # even though they are not in the primary docs_dir.

        inpath = os.path.join(os.path.dirname(config["config_file_path"]), self.config["jupyter_source"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), self.config["jupyter_build"])

        for nb in glob.glob(outpath + "/*.md"):
            nb = os.path.relpath(nb, self.config["jupyter_build"])
            # print(nb, os.path.abspath(config["jupyter_build"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nb, os.path.abspath(self.config["jupyter_build"]), config['site_dir'], config['use_directory_urls']))
            nbm = os.path.splitext(nb)[0]+'.ipynb'
            # print(nbm, os.path.abspath(config["jupyter_source"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nbm, os.path.abspath(self.config["jupyter_source"]), config['site_dir'], config['use_directory_urls']))

        # for i in files:
        #     if os.path.dirname(i.src_path) != "jupyter":
        #         out.append(i)
        return files

    def on_serve(self, server, config):

        # Add the jupyter source files to the watchlist, so that changes
        # will trigger a rebuild of the docs in dev mode

        inpath = os.path.join(os.path.dirname(config["config_file_path"]), self.config["jupyter_source"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            print("Add to watch: {}".format(nb))

            def builder():
                build(config, live_server=True)

            server.watch(nb, builder)

        return server

    def on_pre_build(self, config):
        """
        Convert jupyter notebooks into markdown so they can be rendered by
        mkdocs.
        """

        global TIMER
        # time.sleep(1)
        print("Running AutoDocumenter plugin")
        if time.time() - TIMER < 3:
            print("Too fast")
            print(TIMER, time.time())
            time.sleep(1)
            return True
        else:
            TIMER = time.time()

        template = os.path.join(os.path.dirname(__file__), "templates/jupyter_markdown.tpl")
        inpath = get_path_relative_to_config(config, self.config["jupyter_source"])
        outpath = get_path_relative_to_config(config, self.config["jupyter_build"])


        # The custom template here allows us to flag output blocks as such
        # so they can be styled differently with css
        for nb in glob.glob(inpath + "/*.ipynb"):
            cmd = "jupyter nbconvert --to markdown" + \
            " --template={tpl}".format(tpl=template) + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            # print(cmd)
            subprocess.call(cmd, shell=True)

        # If possible, create API documentation.
        try:
            api_pkg = self.config["autodoc_package"]
        except KeyError:
            print("No package name declared for API autodocumentation (use 'autodoc_package')")
        else:
            if api_pkg:
                docs_file = get_path_relative_to_config(config, os.path.join(self.config["autodoc_build"], api_pkg + ".md"))
                print("Writing API documentation for package {} to {}".format(api_pkg, docs_file))
                run_lucidoc(api_pkg, self.config["docstring_style"], docs_file, self.config["no_top_level"], self.config["include_inherited"])


def get_path_relative_to_config(cfg, relpath):
    """
    Join relative path to config's parent.

    :param Mapping cfg: config key-value mapping
    :param relpath: relative path to join
    :return str: path relative to the given config's config file
    """
    return os.path.join(os.path.dirname(cfg["config_file_path"]), relpath)
