# Free Proxy List

Free, auto-updated list of **live-tested** HTTP, HTTPS, SOCKS4 and SOCKS5 proxies, sorted by latency. Updated every 3 hours by GitHub Actions from the [Dahono free proxy feed](https://router.dahono.com/proxy/free).

<!-- stats:start -->
_Last update: **2026-11-11 21:59 UTC** · **5,280** live proxies · **113** countries_

| Protocol | Proxies | Raw list |
| --- | ---: | --- |
| HTTP | 2,544 | [`proxies/http.txt`](proxies/http.txt) |
| HTTPS | 2,361 | [`proxies/https.txt`](proxies/https.txt) |
| SOCKS4 | 590 | [`proxies/socks4.txt`](proxies/socks4.txt) |
| SOCKS5 | 917 | [`proxies/socks5.txt`](proxies/socks5.txt) |
| All | 5,280 | [`proxies/all.txt`](proxies/all.txt) |

Top countries: [ID](countries/ID.txt) 1,258 · [US](countries/US.txt) 980 · [CN](countries/CN.txt) 212 · [IN](countries/IN.txt) 184 · [PH](countries/PH.txt) 173 · [TH](countries/TH.txt) 161 · [CO](countries/CO.txt) 156 · [BR](countries/BR.txt) 144 · [MX](countries/MX.txt) 139 · [BD](countries/BD.txt) 107
<!-- stats:end -->

## Raw lists

Use the raw URLs directly in your scripts. Each line is `ip:port`, fastest first.

```
https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/proxies/http.txt
https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/proxies/https.txt
https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/proxies/socks4.txt
https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/proxies/socks5.txt
https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/countries/ID.txt
```

`proxies/proxies.json` has the same proxies with protocol, anonymity, country, latency and 24-hour uptime.

## Usage

**curl**

```bash
curl -x "http://$(head -1 proxies/http.txt)" https://api.ipify.org
```

**Python**

```python
import requests

proxies = requests.get(
    "https://raw.githubusercontent.com/Dahono-com/free-proxy-list/main/proxies/http.txt"
).text.split()

for p in proxies[:10]:
    try:
        r = requests.get("https://api.ipify.org", proxies={"http": f"http://{p}", "https": f"http://{p}"}, timeout=8)
        print(p, r.text)
        break
    except requests.RequestException:
        continue
```

## Live API

Need filters (country, protocol, anonymity, latency, uptime)? Query the API directly. No key needed, 30 requests per minute:

```bash
curl "https://router.dahono.com/api/proxy/free?country=ID&protocol=socks5&format=txt&limit=100"
```

Parameters and examples: [router.dahono.com/proxy/free](https://router.dahono.com/proxy/free).

## Notes

- Free public proxies are unreliable, slow, and can disappear at any time. They are fine for testing and learning, not for production.
- Proxies on this list are public servers we found and tested; we do not run them. Do not send passwords or other sensitive data through them.
- Use them only for lawful purposes and respect the terms of the sites you access.

For stable residential IPs from 190+ countries with rotation and sticky sessions, see [Dahono Residential Proxy](https://router.dahono.com/proxy).

## License

MIT. The list data is provided as is, without warranty.
