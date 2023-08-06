import email.parser
import io
import os
import sys
import tempfile
import unittest
from distutils.core import run_setup
from email.message import Message
from pathlib import Path
from typing import Dict, Tuple

import setuptools  # noqa: F401 patchers gotta patch

from dowsing.setuptools import SetuptoolsReader
from dowsing.setuptools.setup_and_metadata import SETUP_ARGS
from dowsing.types import Distribution


def egg_info(files: Dict[str, str]) -> Tuple[Message, Distribution]:
    # TODO consider
    # https://docs.python.org/3/distutils/apiref.html#distutils.core.run_setup
    # and whether that gives a Distribution that knows setuptools-only options
    with tempfile.TemporaryDirectory() as d:
        for relname, contents in files.items():
            Path(d, relname).parent.mkdir(exist_ok=True, parents=True)
            Path(d, relname).write_text(contents)

        try:
            cwd = os.getcwd()
            stdout = sys.stdout

            os.chdir(d)
            sys.stdout = io.StringIO()
            dist = run_setup(f"setup.py", ["egg_info"])
        finally:
            os.chdir(cwd)
            sys.stdout = stdout

        sources = list(Path(d).rglob("PKG-INFO"))
        assert len(sources) == 1

        with open(sources[0]) as f:
            parser = email.parser.Parser()
            info = parser.parse(f)
        reader = SetuptoolsReader(Path(d))
        dist = reader.get_metadata()
        return info, dist


# These tests do not increase coverage, and just verify that we have the right
# static data.
class SetupArgsTest(unittest.TestCase):
    def test_arg_mapping(self) -> None:
        for field in SETUP_ARGS:
            if field.sample_value is None:
                continue
            with self.subTest(field.keyword):
                # Tests that the same arg from setup.py or setup.cfg makes it into
                # metadata in the same way.
                foo = field.sample_value
                setup_py_info, setup_py_dist = egg_info(
                    {
                        "setup.py": "from setuptools import setup\n"
                        f"setup({field.keyword}={foo!r})\n",
                        "a/__init__.py": "",
                        "b/__init__.py": "",
                    }
                )

                cfg_format_foo = field.cfg.writer_cls().to_ini(foo)
                setup_cfg_info, setup_cfg_dist = egg_info(
                    {
                        "setup.cfg": f"[{field.cfg.section}]\n"
                        f"{field.cfg.key} = {cfg_format_foo}\n",
                        "setup.py": "from setuptools import setup\n" "setup()\n",
                        "a/__init__.py": "",
                        "b/__init__.py": "",
                    }
                )

                name = field.get_distribution_key()
                self.assertNotEqual(
                    getattr(setup_py_dist, name), None,
                )
                self.assertEqual(
                    foo, getattr(setup_py_dist, name),
                )
                self.assertEqual(
                    foo, getattr(setup_cfg_dist, name),
                )

                if field.metadata:
                    a = setup_py_info.get_all(field.metadata.key)
                    b = setup_cfg_info.get_all(field.metadata.key)

                    # install_requires gets written out to *.egg-info/requires.txt
                    # instead
                    if field.keyword != "install_requires":
                        self.assertEqual(a, b)
                        self.assertNotEqual(a, None)
