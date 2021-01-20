#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging

ENV_VAR_ROOT = "IG_SERVICE"
CONFIG_FILE_NAME = "trading_ig_config.py"

logger = logging.getLogger(__name__)


class ConfigEnvVar(object):
    def __init__(self, env_var_base):
        self.ENV_VAR_BASE = env_var_base

    def _env_var(self, key):
        return self.ENV_VAR_BASE + "_" + key.upper()

    def get(self, key, default_value=None):
        env_var = self._env_var(key)
        return os.environ.get(env_var, default_value)

    def __getattr__(self, key):
        env_var = self._env_var(key)
        try:
            return os.environ[env_var]
        except KeyError:
            raise Exception("Environment variable '%s' doesn't exist" % env_var)


try:
    src_text = '#!/usr/bin/env python\n#-*- coding:utf-8 -*-\n\n\nclass config(object):\n    username = "YOUR_USERNAME"\n    password = "YOUR_PASSWORD"\n    api_key = "YOUR_API_KEY"\n    acc_type = "DEMO"  # LIVE / DEMO\n    acc_number = "ABC123"\n'

    dst = os.path.join(os.getcwd(), "trading_ig_config.py")

    if not os.path.exists(dst):
        logger.info('Creating a new {} file.'.format(dst))
        with open(dst, 'wt') as f:
            f.write(src_text)

    with open(dst, 'rt') as f:
        dst_text = f.read()

    if src_text == dst_text:
        logger.error("API key is not configured yet. "
                     "If you want to set the auth info from file, add the auth info to {}".format(dst))
        raise IOError("Config is not set.")

    from trading_ig_config import config

    logger.info("import config from %s" % CONFIG_FILE_NAME)
except Exception:
    logger.warning("can't import config from config file")
    try:
        config = ConfigEnvVar(ENV_VAR_ROOT)
        logger.info("import config from environment variables '%s_...'" % ENV_VAR_ROOT)
    except Exception:
        logger.warning("can't import config from environment variables")
        raise (
            """Can't import config - you might create a '%s' filename or use
environment variables such as '%s_...'"""
            % (CONFIG_FILE_NAME, ENV_VAR_ROOT)
        )
