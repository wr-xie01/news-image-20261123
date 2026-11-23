# The World in One Day — 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/wr-xie01/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/wr-xie01/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page that sums up Monday 23 November 2026 in a
single 1024×1024 image. Every story on the page happened or was first
reported on 23 November 2026.

## The six stories

1. **Seoul — KOSPI slides 5.8% as AI sell-off deepens.** Seoul readies
   a 10 trillion won stabilisation fund after the Nasdaq's worst week
   since 2020; US futures rebound. *(AP, Seeking Alpha)*
2. **Wellington — India denied as New Zealand bat out a draw.**
   Mitchell and Phillips hold firm on day five; New Zealand finish
   239 for 5 after India's record 720 for 9. *(ESPNcricinfo)*
3. **London — NHS launches world's biggest AI cancer trial.** The
   EDITH trial will test AI reading of mammograms for nearly 700,000
   women at 30 sites across the UK. *(BBC, Sky News)*
4. **New Delhi — Nepal's PM meets Modi in Delhi.** Balen Shah's first
   visit as PM brings talks, a joint vision, and a new
   Ayodhya–Janakpur train service. *(IANS, ANI)*
5. **Zurich — FIFA confirms UK as 2035 World Cup host.** The first
   World Cup in Britain since 1966: 48 teams, 104 matches and 19
   venues across four nations. *(BBC Sport)*
6. **Vanuatu — Deep M6.5 quake shakes the Pacific.** The tremor struck
   600 km down at 02:40 UTC; no damage was reported and there was no
   tsunami threat. *(USGS, Xinhua)*

## How it was made

`generate_image.py` draws the front page with Pillow: the masthead
"THE WORLD IN ONE DAY", a navy date band for Monday 23 November
2026, and a 2×3 grid of story cards, each with a small hand-drawn
icon. Run it to regenerate the image:

```sh
python3 generate_image.py   # writes entry.png (1024x1024, < 1 MiB)
```

`main.py` copies `entry.png` to the output directory
(`$MAKEFUN_OUTPUT_DIR`, or `/output` by default), refusing to run if
the image is not a 1024×1024 PNG under 1 MiB.

## Bounty

[Sum up 23 November's world news in one image](https://make.fun/bounty/news-image-20261123)
— $100 in prizes across 50 places, paid in USDC on Solana.
