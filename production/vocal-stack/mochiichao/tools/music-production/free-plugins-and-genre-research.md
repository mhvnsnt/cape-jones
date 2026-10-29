# Free / open-source plugins + genre research for the Mochiichao vocal chain

## Genre: what we're actually making
- **Hyperpop, specifically digicore.** Hyperpop is a loosely-defined movement:
  an exaggerated take on popular music drawing on electronic, hip hop, and dance.
  The NTS Guide to Digicore lists Deko's PHANTASY STAR ONLINE ft. Yameii
  alongside Jane Remover, 100 gecs, Glaive, ericdoa, midwxst, and SEBii.
- **Yameii Online** is a virtual musician / digital rapper conceived by Osean and
  Deko, built on Vocaloid software (AVANNA), with an anime / metaverse presentation.
  That's why our game track targets: hip-hop + pop + hyperpop + anime-opening,
  dreamy, pitched-up, vocaloid-crisp.
- **Rulebook break (measured, not guessed):** AVANNA's recommended top is G4
  (392 Hz), but neptune babii's outro measures 394 Hz median with D5 per-second
  notes. V15's lead median is 394 Hz — it matches the reference song, not the
  spec sheet. Music theory guides the key (D major); the reference overrides the
  ceiling.

## Free plugins researched (functions wired in open-source, binaries NOT redistributed)
| Plugin | Free? | What it does | Our open-source equivalent in this repo |
|---|---|---|---|
| Xfer OTT | Free | Multiband upward + downward compression. Lead vocals: Depth 7-20%, 15% typical, de-esser after it | Parallel heavily-compressed copy (0.05/10:1) mixed at 0.15 depth, de-esser kept (v15) |
| Valhalla Supermassive | Free | Huge evolving delay/reverb, 18 modes, dreamy space | Tempo-synced dotted-eighth delay 321.4 ms + 642 ms tap + chorus + echo taps |
| Graillon 3 Free / MAutoPitch | Free | Pitch correction + formant shift | pyworld autotune scripts (avanna_style_autotune_v*.py) |
| TDR Nova | Free | Dynamic EQ | Dual-EQ chain: EQ1 on vocal, EQ2 (different curve) on bus |
| Cableguys PanCake | Free | Auto-pan LFO | Python equal-power pan LFO 0.4 Hz on the low overdub (v14+) |
| Vital / Surge XT | Free, open | Synths | For future game tracks, not this vocal mix |
| Little AlterBoy / Fruity Chorus style | Paid / DAW | Formant/pitch vocal FX, chorus | Rubberband pitch/formant layers + ffmpeg chorus |

## Why VST binaries are not in the public repo
Free download does not mean free redistribution. The plugin installers stay as
download notes (get them from the makers' own sites). What IS in the repo is
our own code that performs the same functions, so the chain is reproducible
without any proprietary binary.
