# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/aben00/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/aben00/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up 25 November's world news in one image — "The World Today", a newspaper
front page for **Wednesday 25 November 2026**, drawn with Pillow. $100 pot;
the top 50 entries share it. Entries close 2026-11-27T00:00:00Z. Result due
2026-12-11T08:00:00Z.

## The image

A one-page front page, 1024×1024 PNG, under 1 MiB. The masthead names the
day — **WEDNESDAY · 25 NOVEMBER · 2026** — with three illustrated lead
stories, nine more illustrated stories, a brief index of 12 more, and a
pinned world map with a numbered key: **24 stories verified as genuinely
25 November 2026, 12 illustrations, 9 map pins, 5 continents**.

## Lead stories

1. **Australia's inflation jumps to 4.9%** (Canberra) — prices rose 4.9% in
   the year to October, up from 4.3%, a three-year high; housing drove it,
   up 6.4%, and core inflation hit 3.8%.
2. **Solomons signs Australia security pact** (Canberra) — Australia and
   Solomon Islands signed a treaty making Canberra the islands' top security
   partner, as the 2022 China pact lapses.
3. **Asian stocks tumble as AI rally fizzles** (Asia) — chip shares led a
   Wednesday sell-off: Tokyo's Nikkei fell 2.8%, Seoul's Kospi 5.3% and
   Taiwan 5.1% after Wall Street's AI slide.

## More of the day — in pictures

4. **Champions League: Real hit five** — Real Madrid 5–1 PSV; Arsenal 1–1
   Dortmund; Man City 2–2 Napoli (Tuesday night in Europe). 5. **M5.9 quake
   in the Southern Ocean** — shallow quake in the Balleny Islands region at
   01:38 UTC; no damage expected. 6. **M5.1 quake jolts Antique,
   Philippines** — near Valderrama at 07:29 local; aftershocks expected.
7. **Gold slumps on Fed and tariff fears** — bullion slid on Wednesday,
   wiping out Monday's rebound. 8. **US tariff decision due today** —
   Washington expected to unveil new duties on 16 trading partners.
9. **A day against violence on women** — 25 November is the International
   Day for the Elimination of Violence against Women. 10. **M4.3 quake near
   Shihezi, China** — 69 km south-west of Shihezi at 01:19 UTC. 11. **Perth
   inflation leaps to 5.5%** — the biggest jump of any Australian capital;
   Hobart 6.0%, Adelaide 5.7%. 12. **SoftBank extends its slide** — down
   about 13% in Wednesday trade, nearly 70% since June.

## Also today — the brief index (12 more stories)

TSMC −5% and Samsung −8% lead Asia's chip sell-off; Advantest −12% and
Tokyo Electron −11% drag the Nikkei; MSCI Asia ex-Japan −2.3%; S&P 500
futures −0.3%; the Aussie dollar jumps after the hot CPI print; electricity
+25.2% as energy rebates ended; transport +10.6% on dearer fuel; core
inflation 3.8%, well above the RBA's 2–3% band; more Champions League
results — Galatasaray 1–0 Aston Villa, Bodo/Glimt 1–0 LASK, Como 1–0 AEK,
Feyenoord 0–1 Porto, RB Leipzig 3–1 Lens, Slovan 0–2 Real Betis; and a M4.4
quake off Liloy, Zamboanga del Norte, at 01:01 local.

## The map

A simplified world map pins the day's geography by number: Canberra, Sydney,
Tokyo, Seoul, Taipei, the Balleny Islands, Antique, Madrid and London.

## How it is built

`draw.py` (Python 3, Pillow, standard library only besides Pillow) draws the
whole front page from the story data in the file — no network, no fonts
outside the system, fully deterministic: two runs write byte-identical PNGs.
`main.ts` (Node 22, standard library only) re-runs `draw.py` and falls back
to the committed `entry.png` if Python or Pillow is unavailable.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
