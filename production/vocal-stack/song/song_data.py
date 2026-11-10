#!/usr/bin/env python3
"""Cape Jones dance song — data: Japanese lyrics (mora-tokenised), melody, structure.
Anime-intro / digicore hyperpop. Key C major, 152 BPM (same as the Tamagotchi loop).
Canon basis: cape-jones docs/SHOW-BIBLE-SEED.md (owner tone text, PR #265 branch) —
deadpan caped hero, mundane + wild card, world/lighting changes around him,
the dance never changes, Tamagotchi digital-pet music.
Every phrase: morae list and notes list MUST be equal length (asserted).
notes = (midi, dur_beats). Phrases are 2 bars = 8 beats unless noted.
"""
BPM = 152
BAR_BEATS = 4
BEAT_SEC = 60.0 / BPM
BAR_SEC = BAR_BEATS * BEAT_SEC
TOTAL_BARS = 48

# duration patterns (sum = 8 beats)
P12 = [0.5, 0.5, 1.0] * 4
P13 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0]
P14 = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0]
P12L = [1.0, 0.5, 0.5] * 4
P10 = [1.0, 0.5, 0.5, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0]

def ph(section, start_bar, morae, midis, durs, romaji, english):
    assert len(morae) == len(midis) == len(durs), (section, len(morae), len(midis), len(durs))
    assert abs(sum(durs) - 8.0) < 1e-6, (section, sum(durs))
    return dict(section=section, start_bar=start_bar, morae=morae,
                notes=list(zip(midis, durs)), romaji=romaji, english=english)

PHRASES = [
 # ---- VERSE A (bars 4-11) ----
 ph("verseA", 4,
    "a sa no ni wa de hi to ri o do ru".split(),
    [76,79,81, 79,76,74, 76,79,81, 84,81,79], P12,
    "Asa no niwa de hitori odoru",
    "In the morning yard, he dances alone"),
 ph("verseA", 6,
    "ma n to hi ra ri ka o wa ma ji me".split(),
    [81,84,83, 81,79,76, 81,79,76, 74,76,76], P12,
    "Manto hirari, kao wa majime",
    "Cape fluttering — his face dead serious"),
 ph("verseA", 8,
    "se ka i ga ka wa xtu te mo ka wa ra na i".split(),
    [76,79,81,84, 81,79,76,74, 79,81,79, 76,74,72], P14,
    "Sekai ga kawattemo kawaranai",
    "Even if the world changes, he never does"),
 ph("verseA", 10,
    "a shi mo to da ke ga bi i to wo ki za mu".split(),
    [74,76,79,81, 79,76,74, 76,79,81, 79,76,74,76], P14,
    "Ashimoto dake ga biito wo kizamu",
    "Only his feet keep the beat"),
 # ---- CHORUS A (bars 12-19) ----
 ph("chorusA", 12,
    "ke e pu jo o n zu o do re o do re".split(),
    [84,83,81,79, 81,83,84, 86,84,83, 81,79,76], P13,
    "Keepu Joonzu, odore odore!",
    "Cape Jones, dance, dance!"),
 ph("chorusA", 14,
    "i ro ga ka wa re ba so ra mo ka wa ru".split(),
    [81,79,76,74, 76,79,81, 79,81,84, 83,81,79], P13,
    "Iro ga kawareba sora mo kawaru",
    "When the colors change, the sky changes too"),
 ph("chorusA", 16,
    "ke e pu jo o n zu ma wa re ma wa re".split(),
    [84,83,81,79, 81,83,84, 86,84,83, 81,79,76], P13,
    "Keepu Joonzu, maware maware!",
    "Cape Jones, spin, spin!"),
 ph("chorusA", 18,
    "a shi ta mo ko ko de o na ji da n su".split(),
    [79,81,83,84, 86,84,83, 81,83,81, 79,76,79], P13,
    "Ashita mo koko de onaji dansu",
    "Tomorrow, same place, same dance"),
 # ---- VERSE B (bars 20-27) ----
 ph("verseB", 20,
    "po ke xtu to no na ka pi pi xtu to na i te".split(),
    [76,79,81,79, 76,74,76, 79,81,83, 81,79,76,74], P14,
    "Poketto no naka, pipitto naite",
    "In his pocket, a little pet beeps"),
 ph("verseB", 22,
    "de n chi ga he xtu te mo ki ni shi na i".split(),
    [74,76,79,76, 81,79,76, 74,72,74, 76,79,76], P13,
    "Denchi ga hettemo ki ni shinai",
    "Battery running low — he doesn't care"),
 ph("verseB", 24,
    "yu u go ha n no ma e mo so no a to mo".split(),
    [81,79,76,74, 76,79, 81,79,76, 74,76,79,81,79], P14,
    "Yuugohan no mae mo, sono ato mo",
    "Before dinner, and after dinner too"),
 ph("verseB", 26,
    "o na ji su te xtu pu yu me no su te xtu pu".split(),
    [84,83,81, 79,81,83,84, 86,84,83, 81,79,76,74], P14,
    "Onaji suteppu, yume no suteppu",
    "The same step, the dream step"),
 # ---- BRIDGE (bars 28-33) ----
 ph("bridge", 28,
    "hi ru ga yo ru ni yo ru ga a sa ni".split(),
    [76,79,81, 79,76,74, 76,79,81, 83,81,79], P12L,
    "Hiru ga yoru ni, yoru ga asa ni",
    "Day into night, night into morning"),
 ph("bridge", 30,
    "e ru i i di i a o pi n ku mi do ri".split(),
    [72,74,76,79, 81,84,83, 81,79,81, 79,76,74,76], P14,
    "Eru-ii-dii, ao, pinku, midori",
    "LED — blue, pink, green"),
 ph("bridge", 32,
    "ka wa ru no wa se ka i da ke".split(),
    [79,81,83,84,81, 79,76,74, 76,79], P10,
    "Kawaru no wa sekai dake",
    "The only thing that changes is the world"),
 # ---- CHORUS B (bars 34-41) = chorus A repeat ----
 ph("chorusB", 34,
    "ke e pu jo o n zu o do re o do re".split(),
    [84,83,81,79, 81,83,84, 86,84,83, 81,79,76], P13,
    "Keepu Joonzu, odore odore!",
    "Cape Jones, dance, dance!"),
 ph("chorusB", 36,
    "i ro ga ka wa re ba so ra mo ka wa ru".split(),
    [81,79,76,74, 76,79,81, 79,81,84, 83,81,79], P13,
    "Iro ga kawareba sora mo kawaru",
    "When the colors change, the sky changes too"),
 ph("chorusB", 38,
    "ke e pu jo o n zu ma wa re ma wa re".split(),
    [84,83,81,79, 81,83,84, 86,84,83, 81,79,76], P13,
    "Keepu Joonzu, maware maware!",
    "Cape Jones, spin, spin!"),
 ph("chorusB", 40,
    "a shi ta mo ko ko de o na ji da n su".split(),
    [79,81,83,84, 86,84,83, 81,83,81, 79,76,79], P13,
    "Ashita mo koko de onaji dansu",
    "Tomorrow, same place, same dance"),
 # ---- OUTRO (bars 40-43) ----
 ph("outro", 42,
    "ka re wa zu xtu to ko ko".split(),
    [76,79,84,81, 79,76,74,72], [1.0]*8,
    "Kare wa zutto koko",
    "He is always right here"),
 ph("outro", 44,
    "ke e pu jo o n zu o do re".split(),
    [84,83,81, 79,81,83, 84,86,84,83], P10,
    "Keepu Joonzu, odore",
    "Cape Jones, dance"),
 ph("outro", 46,
    "la la la la la la laa".split(),
    [81,79,76,79,81,79,84], [1,1,1,1,1,1,2],
    "La la la la la la laa",
    "La la la la la la laa"),
]

# romaji mora -> kana (xtu = small tsu, 'n' = ん, long vowels as separate morae)
KANA = {
 "a":"あ","i":"い","u":"う","e":"え","o":"お",
 "ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
 "sa":"さ","shi":"し","su":"す","se":"せ","so":"そ",
 "ta":"た","chi":"ち","tsu":"つ","te":"て","to":"と",
 "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
 "ha":"は","hi":"ひ","fu":"ふ","he":"へ","ho":"ほ",
 "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
 "ya":"や","yu":"ゆ","yo":"よ",
 "ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
 "wa":"わ","wo":"を","n":"ん","xtu":"っ",
 "ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
 "za":"ざ","ji":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
 "da":"だ","de":"で","do":"ど",
 "ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
 "pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
 "jo":"じょ","di":"でぃ","la":"ら","laa":"らあ",
}
for p in PHRASES:
    p["kana"] = "".join(KANA[m] for m in p["morae"])
    for m in p["morae"]:
        assert m in KANA, m

SECTIONS = [  # (name, start_bar, end_bar_exclusive)
    ("intro", 0, 4), ("verseA", 4, 12), ("chorusA", 12, 20),
    ("verseB", 20, 28), ("bridge", 28, 34), ("chorusB", 34, 42),
    ("outro", 42, 48),
]
CHORDS = [(48, [60, 64, 67]), (43, [59, 62, 67]), (45, [57, 60, 64]), (41, [57, 60, 65])]  # C G Am F

if __name__ == "__main__":
    tot = sum(len(p["morae"]) for p in PHRASES)
    print(f"phrases={len(PHRASES)} morae={tot} total={TOTAL_BARS*BAR_SEC:.2f}s")
    for p in PHRASES:
        print(p["start_bar"], p["kana"], "|", p["romaji"])
