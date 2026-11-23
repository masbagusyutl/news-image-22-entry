# MODEL.md — "The Sunday Globe": Sunday 22 November 2026 in one image

Entry for make.fun competition **news-image-20261122** ("Sum up 22 November's
world news in one image", $100 total, top 50 paid). A retro-newspaper front
page: masthead + lead story (COP31 collapse) with a flat globe illustration,
50 verified stories in three columns across 9 regions, a UTC timeline strip,
an explicit date-check footer and a sources line.

## Selection rationale

The lead is the day's most consequential story by every wire's own
judgement: COP31 collapsed with no agreement (CNN: "the first major
breakdown since COP15 in Copenhagen in 2009"; the longest COP in history).
The other 49 stories are the day's most consequential items across regions
and fields as reported on 22 November 2026: Gulf/Iran tensions, the Ukraine
war's widening geography (Libya, Poland, the Baltic), West Bank violence and
Israel's coalition deadlock, the Mexico cartel capture, the Indonesia factory
fire, the Nigeria boat sinking, BepiColombo at Mercury, the FBI breach, and
the day's sport. No story is from before 22 November as its news event;
items whose underlying event was 20–21 November (UK–EU deal, Signal's
announcement, autonomous-weapons talks) are included only as reported and
developed on 22 November, and the Shenzhen trilateral summit (19–20 Nov) was
deliberately excluded as a 22 November story.

## The 50 stories and their sources

All were verified against reporting dated 22 November 2026 (AP, Reuters,
CNN, Al Jazeera, Le Monde, WSJ, ESA, UN, UKMTO, NEMA, NBC, UK government).
Numbers are the numbers as first reported that day; where wires disagreed
during the day (e.g. the Indonesia factory toll), the AP figure carried in
the morning reporting is used.

| # | Story | Source |
|---|-------|--------|
| 1 | COP31 collapses, no deal on fossil fuels (Antalya) | CNN, Le Monde, WSJ |
| 2 | Longest COP ever; first big breakdown since 2009 | CNN |
| 3 | Guterres: "deeply disappointing" | UN |
| 4 | Iran hits Bahrain civilian plant, Sitra; 2 hurt | Reuters / AFP |
| 5 | Two tankers struck near Strait of Hormuz | UKMTO / Reuters |
| 6 | Day 130 of the US naval blockade of Iran | AP (via OneTurn) |
| 7 | Trump: Tehran seeks a deal; he wants it permanent | AP |
| 8 | Gaza airstrike leaves one critically hurt | AP |
| 9 | Settlers burn 12 cars in 4 West Bank villages | AP |
| 10 | Eisenkot calls settler attacks "Jewish terrorism" | AP |
| 11 | Eisenkot invites Likud into coalition talks | AP |
| 12 | Saudis and Houthis trade fire; 149 Houthis hit | AP |
| 13 | Suspected Ukrainian sea drones hit Russian corvette | AP |
| 14 | Drone hits Dymer flats; 2 killed, 4 hurt, 14 missing | AP / OneTurn |
| 15 | Missile hits Kryvyi Rih; two killed, 60 hurt | AP / CNN |
| 16 | Sanctioned ship Sparta II still burning, Gulf of Finland | Reuters |
| 17 | Russian missiles land in Poland amid drills | AP |
| 18 | Russia revives old demands on European security | AP |
| 19 | Drones damage UN building in Khartoum | Reuters |
| 20 | UK–EU closer-ties deal: food trade, youth mobility | UK government |
| 21 | Denmark expels Russian official over murder plot | AP |
| 22 | Poland: Russia twice tried to kill a rapper | AP |
| 23 | Spain heads for uncertainty before 29 Nov vote | AP |
| 24 | France wage strikes enter sixth week | AP |
| 25 | Cikande candy factory fire kills 3; 37 missing | AP |
| 26 | 7.2-magnitude quake hits Indonesia, no tsunami warning | AP |
| 27 | Lahore tops world pollution ranking, AQI over 500 | AP |
| 28 | Nepal PM Shah to raise border issues in Delhi | AP |
| 29 | China–Japan ties fray over Taiwan, minerals | AP |
| 30 | EU–Indonesia trade deal; tariffs cut on 98.5% of goods | AP |
| 31 | Nigeria boat capsizes; at least 24 dead | Al Jazeera / NEMA |
| 32 | Rohingya welcome UN court genocide ruling | AP |
| 33 | Burhan vows to fight on in Blue Nile | AP |
| 34 | Phumzile Mlambo-Ngcuka dies at 71 | AP |
| 35 | "El Chapo Isidro" seized in Sinaloa; 11 killed | AP |
| 36 | FBI probes hack of crime database, second in months | AP |
| 37 | Trump on FBI hack: "not good" but may offer benefits | AP |
| 38 | Salvadorans killed in Haiti; first mission deaths | AP |
| 39 | Lebanon arrests three over 264 kg of explosives | AP |
| 40 | Pakistan forest feud kills 7 | AP |
| 41 | BepiColombo enters Mercury orbit; thruster glitch | Reuters / ESA |
| 42 | Signal blocks AI assistants reading private chats | Reuters |
| 43 | UN talks on robot weapons end with no binding rules | AP |
| 44 | Afghan women turn to online work | AP |
| 45 | Liverpool 4–0 Man Utd | NBC |
| 46 | Boca Juniors win Copa Sudamericana 2–0 | AP |
| 47 | Atalanta 4–4 Inter | AP |
| 48 | Georgia into SEC final, 34–6 | AP |
| 49 | Indiana stunned 27–24 in OT at Washington | AP |
| 50 | TCU fires coach Sonny Dykes | AP |

## Timeline entries (UTC, approximate first-report times)

~03:00 drones hit UN building, Khartoum · ~07:00 BepiColombo burn cut short
· 09:31 ESA confirms Mercury orbit (QNA timestamp) · ~11:00 drone hits Dymer
flats · ~13:00 "El Chapo Isidro" capture confirmed · ~15:00 COP31 collapses
· 15:24 Nigeria boat toll hits 24 (Al Jazeera) · ~18:30 Liverpool 4–0 Man Utd.

## Exclusions

- Shenzhen Trump–Xi–Putin trilateral summit (19–20 Nov): not a 22 Nov story.
- ICJ Rohingya genocide verdict itself (19 Nov): only the refugees' welcome
  of it, reported 22 Nov, is used.
- Unverified competition-chat claims: none used; every story traces to a
  named outlet's 22 November reporting.

## Build

`render.py` (Pillow, local build time only) draws the 1024×1024 PNG from the
story list above; `main.py` (stdlib only) copies the rendered `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` and verifies its PNG magic, byte size and
sha256. Rendering twice produces byte-identical output (verified sha256
e6d4b4094613e94fc2b6f56b883b158288963aabb922eee378b38a283ee68cc1, 238,013
bytes, under the 1 MiB cap). Type auto-fits: 10 pt story type was selected
by the renderer's fit loop. No network at run time; no vendored dependencies.
