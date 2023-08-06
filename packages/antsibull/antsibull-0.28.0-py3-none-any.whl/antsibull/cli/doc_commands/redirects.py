# coding: utf-8
# Author: Toshio Kuratomi <tkuratom@redhat.com>
# License: GPLv3+
# Copyright: Ansible Project, 2020
"""Subcommand to generate apache redirects for 2.9 vs 2.10 docsite."""

import os
import os.path
import typing as t
from collections import defaultdict
from ...logging import log


mlog = log.fields(mod=__name__)


def generate_redirects() -> int:
    """
    Create apache redirects for the documentation.

    Stable documentation creates documentation for a built version of Ansible.  It uses the exact
    versions of collections included in the last Ansible release to generate rst files documenting
    those collections.

    :returns: A return code for the program.  See :func:`antsibull.cli.antsibull_docs.main` for
        details on what each code means.
    """
    flog = mlog.fields(func='generate_redirects')
    flog.notice('Begin generating redirects')

    app_ctx = app_context.app_ctx.get()
    deps_file = ctx.get(deps_file)
    dependencies = parse_deps_file(deps_file)
    filepath = download(dependencies)
    ansible_base_install = filepath['ansible-base']
    base_runtime_yml = os.path.join(ansible_base_install, 'ansible/config/runtime.yml')
    with open(base_runtime_yml) as f:
        base_data = yaml.safe_load(f.read())

    old_to_new = defaultdict(dict)
    new_to_old = defaultdict(dict)
    for (plugin_type, plugin), record in base_data.items():
        if 'redirect' in record:
            old_to_new[plugin_type][plugin] = record['redirect']
            new_to_old[plugin_type][record['redirect']] = plugin

    htaccess_contents = template.render(old_to_new, new_to_old)
    htaccess = os.path.join(destdir, '.htaccess')
    with open(htaccess, 'w') as f:
        f.write(htaccess_contents)
    #
    # From nitzmahone: yeah, so it sounds like you might want a hybrid approach- load all the raw
    # data to get all the things you want to resolve, then call find_plugin_with_context on all of
    # them and inspect the `redirected_names` in the result and keep a running map of source
    # names->final_targets, then generate stubs at the end for all of those
    #
    # Retrieve all of the collections and ansible-base (or use them from a cache).
    #
    # Set up os.environ so that the ansible variables only point at the places that we've installed
    # collections.
    #
    # import collection_loader
    #
    # use collection_loader to retrieve the ansible-base version of runtime.yml
    # assemble a mapping of redirects from fqcn to ansible-base short name
    #
    # use collection_loader to retrieve the runtime.yml of all the collections
    # assemble an additional mapping of redirects from fqcn to other fqcn's
    #
    # Find the beginning and end of all the redirect chains.
    #
        # For docs-build, we'd then need to add all of the redirects as aliases to the end of the
        # chain.
        #
        # If the end of the chain is not within the collections known to ansible, emit a stub that
        # says that the content has moved with the new collection name.
        #
    # For redirects, emit a redirect from each step along the chain that points to the last link in
    # the chain.  This is the end of creating the redirects from any old names to the new names.
    #
    #
    # For backredirects, for any entry on the chain, link backwards to the start of the chain.  If
    # there isn't a file at the beginning of the chain, create a stub page that says the plugin was
    # not present in ansible-2.9.


    # parse runtime.yml file from ansible-base
    # for every redirect, generate a redirect from 2.9 pattern to 2.10 pattern
    # for the backredirect, could we just look backwards?

    # find runtime.yml
    #
    # parse runtime.yml


