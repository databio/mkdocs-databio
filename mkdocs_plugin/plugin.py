from mkdocs.plugins import BasePlugin

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
    Inject certain config variables into the markdown
    """
    config_scheme = (
        ('foo', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default='a default value')),
        ('bar', mkdocs.config.config_options.Type(int, default=0)),
        ('baz', mkdocs.config.config_options.Type(bool, default=True))
    )


    def on_files(self, files, config):

        # Add non docs_dir files that are rendered versions to this.

        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])



        for nb in glob.glob(outpath + "/*.md"):
            nb = os.path.relpath(nb, config["auto"]["JUPYTER_BUILD"])
            print(nb, os.path.abspath(config["auto"]["JUPYTER_BUILD"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nb, os.path.abspath(config["auto"]["JUPYTER_BUILD"]), config['site_dir'], config['use_directory_urls']))

        # for i in files:
        #     if os.path.dirname(i.src_path) != "jupyter":
        #         out.append(i)
        return files


    def on_serve(self, server, config):

        # Here, watch the ipynb files
        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            print("Add to watch: ", nb)
            server.watch(nb)

        return server


    def on_pre_build(self, config):
        global timer
        time.sleep(1)
        print("Running AutoDocumenter plugin")
        print(timer, time.time())
        if time.time() - timer < 3:
            print("Too fast")
        else:
            timer = time.time()

        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            cmd = "jupyter nbconvert --to markdown" + \
            " --template=~/mymarkdown.tpl" + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            print(cmd)
            subprocess.call(cmd, shell=True)

