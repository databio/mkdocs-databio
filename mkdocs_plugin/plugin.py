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
        ('bar', mkdocs.config.config_options.Type(int, default=0)),
        ('baz', mkdocs.config.config_options.Type(bool, default=True))
    )

    
    def on_files(self, files, config):

        # Add non docs_dir files that are rendered versions to this.

        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])

        for nb in glob.glob(outpath + "/*.md"):
            nb = os.path.relpath(nb, config["auto"]["JUPYTER_BUILD"])
            # print(nb, os.path.abspath(config["auto"]["JUPYTER_BUILD"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nb, os.path.abspath(config["auto"]["JUPYTER_BUILD"]), config['site_dir'], config['use_directory_urls']))
            nbm = os.path.splitext(nb)[0]+'.ipynb'
            # print(nbm, os.path.abspath(config["auto"]["JUPYTER_SOURCE"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nbm, os.path.abspath(config["auto"]["JUPYTER_SOURCE"]), config['site_dir'], config['use_directory_urls']))

        # for i in files:
        #     if os.path.dirname(i.src_path) != "jupyter":
        #         out.append(i)
        return files


    def on_serve(self, server, config):

        # Here, watch the ipynb files
        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            print("Add to watch: {}".format(nb))

            def builder():
                build(config, live_server=True)

            server.watch(nb, builder)

        return server


    def on_pre_build(self, config):
        global timer
        # time.sleep(1)
        print("Running AutoDocumenter plugin")
        print(timer, time.time())
        if time.time() - timer < 3:
            print("Too fast")
        else:
            timer = time.time()

        template = os.path.join(os.path.dirname(__file__), "templates/jupyter_markdown.tpl")
        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            cmd = "jupyter nbconvert --to markdown" + \
            " --template={tpl}".format(tpl=template) + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            # print(cmd)
            subprocess.call(cmd, shell=True)

