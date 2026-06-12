# CGP Example Session

This file shows an example conversation between a CGP server and one CGP engine.

In this example:

* `>` means the server sends a line to the engine.
* `<` means the engine sends a line to the server.

## Basic startup, setup, lexicon check, and move request

```text
>cgp
<name RandomTurtle
<author Dev
<version 0.0.1
<option CGP_Variant standard standard super custom
<option CGP_Lexicon NWL23 NWL23 CSW24 enable sowpods custom
<cgpok

>lexicons
<lexicons NWL23 CSW24 enable sowpods custom

>variants
<variants standard super custom

>setup variant standard lexicon NWL23
<setupok

>lexiconsample NWL23 5
<word AA
<word QI
<word ZA
<word CAT
<word SLATE
<endlexiconsample

>lexiconcheck NWL23 AA QI ZA CAT SLATE
<lexiconcheck ok

>tileset NWL23
<tile A 9 1
<tile B 2 3
<tile C 2 3
<tile D 4 2
<tile E 12 1
<tile F 2 4
<tile G 3 2
<tile H 2 4
<tile I 9 1
<tile J 1 8
<tile K 1 5
<tile L 4 1
<tile M 2 3
<tile N 6 1
<tile O 8 1
<tile P 2 3
<tile Q 1 10
<tile R 6 1
<tile S 4 1
<tile T 6 1
<tile U 4 1
<tile V 2 4
<tile W 2 4
<tile X 1 8
<tile Y 2 4
<tile Z 1 10
<tile ? 2 0
<endtileset

>tilesetcheck NWL23 A:9:1 B:2:3 C:2:3 ?:2:0
<tilesetcheck ok

>ready
<readyok

>position 15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
>rack CTAESR?
>unseen 5A2B1C3D8E2F1G2H6I1J1K3L2M4N5O2P1Q4R3S5T3U2V2W1X2Y1Z1?
>go movetime 1000
<bestmove H8 SLATE

>position 15/15/15/15/15/15/15/7SLATE3/15/15/15/15/15/15/15
>rack FAKIEST
>unseen 4A2B1C3D7E1F1G2H5I1J1K3L2M4N5O2P1Q4R2S4T3U2V2W1X2Y1Z1?
>go movetime 1000
<bestmove 8H FLAKIEST

>ping
<pong

>quit
```

## Board encoding example

```text
15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
```

The row `7CAT5` means 7 empty squares, then `CAT`, then 5 empty squares.

## Example unknown lexicon response

```text
>setup variant standard lexicon FAKELEX
<setupno unknown_lexicon

>lexiconsample FAKELEX 5
<error unknown_lexicon FAKELEX
```

## Example rejected word check

```text
>lexiconcheck NWL23 AA QI ZZZZZ
<lexiconcheck no ZZZZZ
```


## Unseen tile encoding example

```text
5A2B1C3D8E2F1G2H6I1J1K3L2M4N5O2P1Q4R3S5T3U2V2W1X2Y1Z1?
```

This means the engine sees the following unseen tile pool:

```text
5 A tiles
2 B tiles
1 C tile
3 D tiles
8 E tiles
...
1 blank tile
```

Counts are written before tile symbols.

Zero-count entries are allowed:

```text
6A2B1C4D6E0F
```

The `0F` entry means zero F tiles are unseen.
