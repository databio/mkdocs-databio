"""
Databio group plugin for MkDocs

Group software page: http://databio.org/software/
"""

import os
import glob
import sys
import subprocess
import time
if sys.version_info < (3, 3):
    from collections import Mapping
else:
    from collections.abc import Mapping
import mkdocs
from mkdocs.plugins import BasePlugin
from mkdocs.commands.build import build
from lucidoc import run_lucidoc

TIMER = 0
_NBFOLDER = "docs_jupyter"
_NBFOLDER_BUILD = "jupyter_build"
_API_KEY = "autodoc_package"
_CFG_FILE_KEY = "config_file_path"

class AutoDocumenter(BasePlugin):
    """ Populate automatic documentation markdown. """
    config_scheme = (
        ("site_logo", mkdocs.config.config_options.Type(mkdocs.utils.string_types)),
        ("pypi_name", mkdocs.config.config_options.Type(mkdocs.utils.string_types)),
        ("jupyter_source", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=_NBFOLDER)),
        (_NBFOLDER_BUILD, mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=os.path.join(_NBFOLDER, "build"))),
        (_API_KEY, mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=None)),
        ("docstring_style", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="rst")),
        ("no_top_level", mkdocs.config.config_options.Type(bool, default=False)),
        ("include_inherited", mkdocs.config.config_options.Type(bool, default=False)),
        ("autodoc_build", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default="docs_build")),
        ("usage_template", mkdocs.config.config_options.Type(mkdocs.utils.string_types, default=os.path.join("docs", "usage_template.md"))),
        ("usage_cmds", mkdocs.config.config_options.Type((list, mkdocs.utils.string_types), default=[])),
    )

    def on_files(self, files, config):

        # Add non docs_dir files that are rendered versions to this.
        # This will allow them to be used in the final rendered HTML pages,
        # even though they are not in the primary docs_dir.

        for nb in glob.glob(os.path.join(os.path.dirname(
                config[_CFG_FILE_KEY]), self.config[_NBFOLDER_BUILD], "*.md")):
            nb = os.path.relpath(nb, self.config[_NBFOLDER_BUILD])
            # print(nb, os.path.abspath(config[_NBFOLDER_BUILD]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nb, os.path.abspath(self.config[_NBFOLDER_BUILD]), config['site_dir'], config['use_directory_urls']))
            nbm = os.path.splitext(nb)[0] + '.ipynb'
            # print(nbm, os.path.abspath(config["jupyter_source"]), config['site_dir'], config['use_directory_urls'])
            files.append(mkdocs.structure.files.File(nbm, os.path.abspath(self.config["jupyter_source"]), config['site_dir'], config['use_directory_urls']))

        # for i in files:
        #     if os.path.dirname(i.src_path) != "jupyter":
        #         out.append(i)
        return files

    def on_serve(self, server, config):

        # Add the jupyter source files to the watchlist, so that changes
        # will trigger a rebuild of the docs in dev mode

        inpath = os.path.join(os.path.dirname(config[_CFG_FILE_KEY]), self.config["jupyter_source"])

        for nb in glob.glob(os.path.join(inpath, "*.ipynb")):
            print("Add to watch: {}".format(nb))

            def builder():
                build(config, live_server=True)

            server.watch(nb, builder)

        return server

    def on_pre_build(self, config):
        """ Usage example notebook and API autodocumentation """
        global TIMER
        # time.sleep(1)
        print("Running AutoDocumenter plugin")
        if time.time() - TIMER < 5:
            print("Too fast")
            print(TIMER, time.time())
            time.sleep(1)
            return True
        else:
            TIMER = time.time()

        template = os.path.join(os.path.dirname(__file__), "templates/jupyter_markdown.tpl")
        inpath = get_path_relative_to_config(config, self.config["jupyter_source"])
        outpath = get_path_relative_to_config(config, self.config[_NBFOLDER_BUILD])

        # The custom template here allows us to flag output blocks as such
        # so they can be styled differently with css

        for nb in glob.glob(os.path.join(inpath, "*.ipynb")):
            output_markdown = "{od}/{notebooknox}.md".format(od=outpath, notebooknox=os.path.splitext(os.path.basename(nb))[0])
            
            # For some reason mkdocs doesn't like the traditional '---' 
            # markdown metadata fences
            with open(output_markdown, 'w') as file:
                file.write("jupyter:True\n")

            cmd = "jupyter nbconvert --to markdown" + \
            " --template={tpl}".format(tpl=template) + \
            " {notebook} --output-dir {od}".format(notebook=nb, od=outpath)

            cmd = "jupyter nbconvert --to markdown" + \
            " --template={tpl}".format(tpl=template) + \
            " {notebook} --stdout | sed 's/\x1b\[[0-9;]*m//g' >> {od}/{notebooknox}.md".format(notebook=nb, od=outpath,
             notebooknox=os.path.splitext(os.path.basename(nb))[0])

            print(cmd)
            subprocess.call(cmd, shell=True)


            files_folder = os.path.join(outpath, os.path.splitext(os.path.basename(nb))[0] + "_files")
            print(files_folder)
            target = os.path.join(os.path.dirname(outpath), os.path.basename(files_folder), "docs")
            if os.path.exists(files_folder) and not os.path.exists(target):
                os.symlink(files_folder, target)

        # If possible, create API documentation.
        api_pkg = self.config.get(_API_KEY)
        if api_pkg:
            args = (api_pkg, self.config["docstring_style"])
            kwargs = {
                "no_mod_docstr": self.config["no_top_level"],
                "include_inherited": self.config["include_inherited"]
            }
            outfolder = get_path_relative_to_config(config, self.config["autodoc_build"])
            try:
                build_list = self.config["build_list"]
            except KeyError:
                outfile_keyname = "autodoc_outfile"
                filename = self.config.get(outfile_keyname)
                if filename:
                    if not isinstance(filename, str):
                        msg = "Basename for autodoc output file isn't text; " \
                              "got {} ({}) (from key '{}')".format(
                            filename, type(filename), outfile_keyname)
                        raise TypeError(msg)
                else:
                    filename = api_pkg + ".md"
                docs_file = os.path.join(outfolder, filename)
                kwargs["outfile"] = docs_file
            else:
                kwargs["outfolder"] = outfolder
                if isinstance(build_list, Mapping):
                    kwargs["groups"] = build_list
                else:
                    kwargs["whitelist"] = build_list
            print("Writing API documentation for package {}".format(api_pkg))
            run_lucidoc(*args, **kwargs)
        else:
            print("No package name declared for API autodocumentation (use '{}')".format(_API_KEY))


def get_path_relative_to_config(cfg, relpath):
    """
    Join relative path to config's parent.

    :param Mapping cfg: config key-value mapping
    :param relpath: relative path to join
    :return str: path relative to the given config's config file
    """
    return os.path.join(os.path.dirname(cfg[_CFG_FILE_KEY]), relpath)
