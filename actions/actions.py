#!/usr/bin/python

import os
import sys

sys.path.append('hooks/')

from charmhelpers.core.hookenv import action_fail
from pg_dir_utils import (
    restart_pg,
    sapi_post_zone_info,
    sapi_post_license,
    sapi_post_ips
)


def restart_pg(args):
    """
    Restart PLUMgrid services.
    """
    restart_pg()


def post_ips(args):
    """
    POST plumgrid nodes IPs to solutions api server.
    """
    sapi_post_ips()


def post_zone_info(args):
    """
    POST zone information to solutions api server
    """
    sapi_post_zone_info()


def post_license(args):
    """
    POST PLUMgrid License to solutions api server
    """
    sapi_post_license()


# A dictionary of all the defined actions to callables (which take
# parsed arguments).
ACTIONS = {"restart-pg": restart_pg, "post-ips": post_ips, "post-zone-info": post_zone_info,
           "post-license": post_license}


def main(args):
    action_name = os.path.basename(args[0])
    try:
        action = ACTIONS[action_name]
    except KeyError:
        return "Action %s undefined" % action_name
    else:
        try:
            action(args)
        except Exception as e:
            action_fail(str(e))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
