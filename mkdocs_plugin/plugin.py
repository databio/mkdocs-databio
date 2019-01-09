from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import build

import mkdocs
import os
import glob
import subprocess

import time

CONFIG_KEYS = [
    'site_name',
    'site_author',
    'site_url',
    'repo_url',
    'repo_name'
]

timer = 0

class AutoDocumenter(BasePlugin):
    """
    Populate automatic documentation markdown
    """
    config_scheme = (
        ('auto', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=None)),
        ('jupyter_source', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_jupyter")),
        ('jupyter_build', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_jupyter/build")),
        ('autodoc_modules', mkdocs.config.config_options.Type(list, default=None)),
        ('autodoc_build', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_build")),
        ('usage_template', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs/usage_template.md")),
        ('usage_cmds', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=[])),
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
        
        global timer
        # time.sleep(1)
        print("Running AutoDocumenter plugin")
        print(timer, time.time())
        if time.time() - timer < 3:
            print("Too fast")
        else:
            timer = time.time()

        template = os.path.join(os.path.dirname(__file__), "templates/jupyter_markdown.tpl")
        inpath = os.path.join(os.path.dirname(config["config_file_path"]), self.config["jupyter_source"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), self.config["jupyter_build"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            cmd = "jupyter nbconvert --to markdown" + \
            " --template={tpl}".format(tpl=template) + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            # print(cmd)
            subprocess.call(cmd, shell=True)

