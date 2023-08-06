import json
import sys
from pathlib import Path
from typing import List

import click
from honesty.archive import extract_and_get_names
from honesty.cache import Cache
from honesty.cmdline import select_versions, wrap_async
from honesty.releases import FileType, async_parse_index
from moreorless.click import echo_color_unified_diff

from dowsing.pep517 import get_metadata


@click.command()
@click.argument("packages", nargs=-1)
@wrap_async
async def main(packages: List[str]) -> None:
    # Much of this code mirrors the methods in honesty/cmdline.py
    async with Cache(fresh_index=True) as cache:
        for package_name in packages:
            package_name, operator, version = package_name.partition("==")
            try:
                package = await async_parse_index(package_name, cache, use_json=True)
            except Exception as e:
                continue

            selected_versions = select_versions(package, operator, version)
            rel = package.releases[selected_versions[0]]

            sdists = [f for f in rel.files if f.file_type == FileType.SDIST]
            wheels = [f for f in rel.files if f.file_type == FileType.BDIST_WHEEL]

            if not sdists or not wheels:
                continue

            sdist_path = await cache.async_fetch(pkg=package_name, url=sdists[0].url)
            # wheel_path = await cache.async_fetch(pkg=package_name, url=wheels[0].url)

            sdist_root, sdist_filenames = extract_and_get_names(
                sdist_path, strip_top_level=True, patterns=("*.*")
            )
            # wheel_root, wheel_filenames = extract_and_get_names(
            #     wheel_path, strip_top_level=True, patterns=("*.*")
            # )

            try:
                subdirs = tuple(Path(sdist_root).iterdir())
                metadata = get_metadata(Path(sdist_root, subdirs[0]))
                assert metadata.source_mapping is not None, "no source_mapping"
            except Exception as e:
                continue

            names = set(n.split("/")[0] for n in metadata.source_mapping.keys())
            for n in names:
                print(n)
            with open("log.jsonlines", "a") as f:
                f.write(
                    json.dumps({"project": package_name, "top_level": sorted(names)})
                    + "\n"
                )


if __name__ == "__main__":
    main()
