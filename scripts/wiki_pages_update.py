import asyncio
import gzip
import re
from asyncio import Semaphore, TaskGroup
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote_plus

import orjson

from app.lib.retry import retry
from app.utils import HTTP

_download_limiter = Semaphore(6)  # max concurrent downloads
_wiki_pages_path = Path('config/wiki_pages.json')


class WikiPageInfo(NamedTuple):
    key: str
    value: str
    locale: str


async def discover_sitemap_urls() -> list[str]:
    r = await HTTP.get('https://wiki.openstreetmap.org/sitemap-index-wiki.xml')
    r.raise_for_status()
    matches = re.finditer(
        r'https://wiki\.openstreetmap\.org/sitemap-wiki-NS_\d+-\d+.xml.gz', r.text
    )
    result = [match[0] for match in matches]
    print(f'[🔍] Discovered {len(result)} sitemaps')
    return result


@retry(timedelta(minutes=1))
async def fetch_and_parse_sitemap(url: str) -> list[WikiPageInfo]:
    async with _download_limiter:
        r = await HTTP.get(url)
        r.raise_for_status()

    text = gzip.decompress(r.content).decode()
    result: list[WikiPageInfo] = []

    for match in re.finditer(
        r'/(?:(?P<locale>[\w-]+):)?(?P<page>(?:Key|Tag):.*?)</loc>', text
    ):
        locale = match['locale'] or ''
        locale = unquote_plus(locale)

        # skip talk pages
        if (
            locale.startswith(('Talk', 'Proposal'))  #
            or locale.endswith(('_talk', '_proposal'))
        ):
            continue

        page = match['page']
        page = unquote_plus(page)

        if page.startswith('Key:'):
            # skip key pages with values
            if '=' in page:
                continue
            key, value = page[4:], '*'
        else:
            # skip tag pages without values
            if '=' not in page:
                continue
            key, value = page[4:].split('=', 1)

        result.append(WikiPageInfo(key, value, locale))

    print(f'[✅] {url!r}: {len(result)} pages')
    return result


async def main():
    urls = await discover_sitemap_urls()

    async with TaskGroup() as tg:
        tasks = [tg.create_task(fetch_and_parse_sitemap(url)) for url in urls]

    key_values_locales: defaultdict[str, defaultdict[str | None, set[str]]]
    key_values_locales = defaultdict(lambda: defaultdict(set))
    for info in (info for task in tasks for info in task.result()):
        key_values_locales[info.key][info.value].add(info.locale)

    result = {
        key: {value: sorted(locales) for value, locales in values.items()}
        for key, values in key_values_locales.items()
    }
    buffer = orjson.dumps(
        result,
        option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS | orjson.OPT_APPEND_NEWLINE,
    )
    _wiki_pages_path.write_bytes(buffer)


if __name__ == '__main__':
    asyncio.run(main())
