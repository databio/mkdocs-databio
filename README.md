# MkDocs databio theme and plugin

This repository contains the [mkdocs](http://mkdocs.org) theme and plugin for the [Sheffield lab](http://databio.org/):

- **Theme:** The theme is just a lab style so that all our documentation matches.
- **Plugin:** The plugin is a mkdocs plugin that allows us to auto-document Python code using lucidoc, which produces markdown documentation that is naturally hosted by mkdocs.

Installing this will give you access to both for your mkdocs repositories.

## Install

Install it with:

```{bash}
pip install --user --upgrade https://github.com/databio/mkdocs-databio/zipball/master
```

## Hello World example

You can run the example in the [example](/example) folder by running this after cloning this repo:

```
cd example
mkdocs serve
```

You can use this as a template; copy/paste the contents of the `example` folder into your root repository directory and then edit away!

## Enabling the theme

The theme refers to the look and feel of the site. It contains the software that renders the hierarchial sidebar, the different navbar links, etc. Use it for your site by adding this to your `mkdocs.yml` file:


```{yaml}
theme: databio
```

## Enabling the plugin

The plugin is used to autodocument python modules, to include jupyter notebooks, and to autodocument CLI usage. You can enable it with:

```
plugins:
  - databio
```

Then, there are a bunch of config options:

```{yaml}
plugins:
  - databio:
      jupyter_source: "docs_jupyter"
      jupyter_build: "docs_jupyter/build"
      autodoc_package: null
      autodoc_build: "docs_build"
      docstring_style: "rst"
      usage_template: "docs/usage_template.md"
      usage_cmds:
        -"$CODEBASE/AIList/bin/AIList --help"

```


## How to use it

Put all your `.md` files into the `docs` folder, and put all your `.ipynb` files into the `docs_jupyter` folder. With the theme and plugin enabled, you can now refer to any of these files with links. The `ipynb` files will be converted into `md` files with the same name.


## Contributing
If you'd like to contribute to development but are unfamiliar with `MkDocs` plugins, you can refer to the ["Developing Plugins" section](https://www.mkdocs.org/user-guide/plugins/#developing-plugins) of the `MkDocs` user guide.

