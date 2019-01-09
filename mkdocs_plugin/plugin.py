from mkdocs.plugins import BasePlugin

import mkdocs
import os
import glob
import subprocess

CONFIG_KEYS = [
    'site_name',
    'site_author',
    'site_url',
    'repo_url',
    'repo_name'
]


class AutoDocumenter(BasePlugin):
    """
    Inject certain config variables into the markdown
    """
    config_scheme = (
        ('foo', mkdocs.config.config_options.Type(mkdocs.utils.string_types, default='a default value')),
        ('bar', mkdocs.config.config_options.Type(int, default=0)),
        ('baz', mkdocs.config.config_options.Type(bool, default=True))
    )

    def on_post_build(self, config):
        print("Running AutoDocumenter plugin")
        inpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_SOURCE"])
        outpath = os.path.join(os.path.dirname(config["config_file_path"]), config["auto"]["JUPYTER_BUILD"])

        for nb in glob.glob(inpath + "/*.ipynb"):
            cmd = "jupyter nbconvert --to markdown" + \
            " --template=~/mymarkdown.tpl" + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            print(cmd)
            subprocess.call(cmd, shell=True)

