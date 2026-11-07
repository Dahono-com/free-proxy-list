#!/usr/bin/env python3
"""Fetch live-tested free proxies from the Dahono free proxy API and write plain-text lists.

API docs: https://router.dahono.com/proxy/free
The API returns at most 100 proxies per page and allows 30 requests per minute,
so pages are fetched with a short pause between them.
"""
import json
import os
import re
import time
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

API = "https://router.dahono.com/api/proxy/free"
PAUSE_S = 2.2
MAX_PAGES = 200
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = "dahono-free-proxy-list/1.0 (+https://github.com/Dahono-com/free-proxy-list)"


def fetch(page):
    url = f"{API}?limit=100&page={page}&sortBy=latency"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # rate limit or transient error: back off and retry
            if attempt == 3:
                raise
            time.sleep(15 * (attempt + 1))


def main():
    first = fetch(1)
    proxies = list(first["proxies"])
    pages = min(first.get("totalPages", 1), MAX_PAGES)
    for page in range(2, pages + 1):
        time.sleep(PAUSE_S)
        proxies.extend(fetch(page)["proxies"])

    seen, alive = set(), []
    for p in proxies:
        if p.get("alive") and p["proxy"] not in seen:
            seen.add(p["proxy"])
            alive.append(p)
    alive.sort(key=lambda p: p.get("latency_ms") or 10**9)

    by_proto, by_country = defaultdict(list), defaultdict(list)
    for p in alive:
        for proto in p.get("protocols") or []:
            by_proto[proto].append(p["proxy"])
        if p.get("country"):
            by_country[p["country"]].append(p["proxy"])

    def write(path, lines):
        with open(os.path.join(ROOT, path), "w") as f:
            f.write("\n".join(lines) + ("\n" if lines else ""))

    write("proxies/all.txt", [p["proxy"] for p in alive])
    for proto in ("http", "https", "socks4", "socks5"):
        write(f"proxies/{proto}.txt", by_proto.get(proto, []))
    for f in os.listdir(os.path.join(ROOT, "countries")):
        if f.endswith(".txt"):
            os.remove(os.path.join(ROOT, "countries", f))
    for cc, lines in by_country.items():
        write(f"countries/{cc}.txt", lines)
    keep = ("proxy", "protocols", "anonymity", "country", "latency_ms", "uptime_24h", "reliability")
    with open(os.path.join(ROOT, "proxies/proxies.json"), "w") as f:
        json.dump([{k: p.get(k) for k in keep} for p in alive], f, separators=(",", ":"))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    top = sorted(by_country.items(), key=lambda kv: -len(kv[1]))[:10]
    stats = [
        f"_Last update: **{now}** · **{len(alive):,}** live proxies · **{len(by_country)}** countries_",
        "",
        "| Protocol | Proxies | Raw list |",
        "| --- | ---: | --- |",
    ]
    for proto in ("http", "https", "socks4", "socks5"):
        stats.append(f"| {proto.upper()} | {len(by_proto.get(proto, [])):,} | [`proxies/{proto}.txt`](proxies/{proto}.txt) |")
    stats.append(f"| All | {len(alive):,} | [`proxies/all.txt`](proxies/all.txt) |")
    stats += ["", "Top countries: " + " · ".join(f"[{cc}](countries/{cc}.txt) {len(v):,}" for cc, v in top)]
    readme_path = os.path.join(ROOT, "README.md")
    readme = open(readme_path).read()
    readme = re.sub(r"<!-- stats:start -->.*<!-- stats:end -->",
                    "<!-- stats:start -->\n" + "\n".join(stats) + "\n<!-- stats:end -->", readme, flags=re.S)
    open(readme_path, "w").write(readme)
    print(f"{len(alive)} live proxies, {len(by_country)} countries")


if __name__ == "__main__":
    main()
