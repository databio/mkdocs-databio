# MkDocs databio theme and plugin

This repository contains the [mkdocs](http://mkdocs.org) theme and plugin for the Sheffield lab. Installing this will give you access to both.

## Install

Install it with:

```{bash}
pip install --user --upgrade https://github.com/databio/mkdocs-databio/zipball/master
```

## Enabling the theme

The theme refers to the look and feel of the site. It contains the software the renders the hierarchial sidebar, the different navbar links, etc. Render your mkdocs site with it adding this to your `mkdocs.yml` file:


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
      autodoc_modules: null
      autodoc_build: "docs_build"
      usage_template: "docs/usage_template.md"
      usage_cmds:
        -"$CODEBASE/AIList/bin/AIList --help"

```

## Example

Copy/paste the contents of the `example` folder into your root repository directory.

## How to use it

Put all your `.md` files into the `docs` folder, and put all your `.ipynb` files into the `docs_jupyter` folder. With the theme and plugin enabled, you can now refer to any of these files with links. The `ipynb` files will be converted into `md` files with the same name
