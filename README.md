# CGP — Crossword Game Protocol

CGP is a line-based protocol for connecting crossword-game engines to GUIs, match runners, and validators.

It borrows the idea of a text-based engine protocol from chess protocols like UCI, but it is designed for Scrabble-like games: boards, racks, lexicons, tile sets, variants, passes, exchanges, and word validation.

## Status

CGP is currently a draft protocol.

Current draft version: `0.1`

Expect command names and response formats to change before `1.0`.

## What CGP is

CGP defines how a server talks to a word-game engine through standard input and standard output.

The server controls the game flow.

The engine receives:

- setup information
- public board position information
- private player information, such as rack and unseen tiles
- time/search limits

The engine returns:

- metadata
- supported variants and lexicons
- lexicon/tile compatibility info
- one chosen move

## What CGP is not

CGP is not a Scrabble engine.

CGP does not generate moves by itself.

CGP does not require engines to be written in any specific language.

A CGP engine can be written in Python, C++, C#, Rust, Go, or anything else that can read stdin and write stdout.

## Server / engine model

CGP uses a server-controlled architecture.

The server sends each engine only the information that engine is allowed to know.

Engines do not talk to each other directly.

This means the server may safely send private data, such as the engine's own rack and unseen tile pool, to one engine without revealing that information to the opponent engine.

## Example

```text
>cgp
<name Scuttler
<author Dev
<version 0.0.1
<option CGP_Variant standard standard super custom
<option CGP_Lexicon NWL23 NWL23 CSW24 enable sowpods custom
<cgpok

>setup variant standard lexicon NWL23
<setupok

>ready
<readyok

>position 15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
>rack CTAESR?
>unseen 5A2B1C3D8E2F1G2H6I1J1K3L2M4N5O2P1Q4R3S5T3U2V2W1X2Y1Z1?
>go movetime 1000
<bestmove H8 SLATE

>quit
```

In the example above:

- `>` means the server sends a line to the engine.
- `<` means the engine sends a line to the server.

## Board encoding

CGP uses a compact board encoding inspired by FEN.

A standard board has 15 rows and 15 columns.

Rows are separated by `/`.

Letters represent occupied squares.

Numbers represent runs of empty squares.

For a 15×15 board, the largest possible empty run is `15`.

Example empty board:

```text
15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
```

Example board with `CAT` on row 8 starting at column H:

```text
15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
```

The row `7CAT5` means:

- 7 empty squares
- C A T
- 5 empty squares

Lowercase letters on the board represent blank tiles.

## Private player data

The server may send private player data before `go`.

Example:

```text
>position 15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
>rack SLATE??
>unseen 5A2B1C3D8E1?
>go movetime 1000
<bestmove 8H SLATE
```

`rack` gives the engine's current rack.

`unseen` gives the tile pool not visible to that engine. This usually includes the bag plus unknown opponent rack tiles.

Unseen tiles use Tile-FEN notation: each count is written before its tile symbol, and entries are concatenated without spaces.

```text
[count][tile][count][tile]...
```

Example:

```text
5A2B1C3D8E1?
```

means 5 A tiles, 2 B tiles, 1 C tile, 3 D tiles, 8 E tiles, and 1 blank tile are unseen.

Zero-count entries are allowed when a server wants to be explicit:

```text
6A2B1C4D6E0F
```

## Move notation

CGP uses compact crossword-style move notation.

```text
H8 SLATE
```

means play `SLATE` horizontally starting at column H, row 8.

```text
8H SLATE
```

means play `SLATE` vertically starting at row 8, column H.

Rows are numbered starting at 1.

Columns are lettered starting at A.

Lowercase letters in a word represent blank tiles.

Example:

```text
H8 SLaTE
```

means the lowercase `a` is a blank assigned as A.

## Basic engine flow

A normal CGP session looks like this:

1. Server sends `cgp`.
2. Engine responds with metadata and `cgpok`.
3. Server sends `setup`.
4. Engine responds with `setupok`.
5. Server sends `ready`.
6. Engine responds with `readyok`.
7. Server sends `position`.
8. Server sends private state such as `rack` and `unseen`.
9. Server sends `go`.
10. Engine responds with `bestmove`.
11. Server eventually sends `quit`.

## Required commands

A minimal CGP engine must support:

```text
cgp
setup
ready
position
rack
go
quit
```

Recommended commands:

```text
name
author
version
lexicons
variants
lexiconsample
lexiconcheck
tileset
tilesetcheck
unseen
ping
```

## Lexicons and variants

Engines may report supported lexicons:

```text
>lexicons
<lexicons NWL23 CSW24 enable sowpods custom
```

Engines may report supported variants:

```text
>variants
<variants standard super custom
```

A server should choose a lexicon and variant supported by the engine before starting a match.

In engine-vs-engine matches, the server should choose a lexicon and variant supported by both engines.

## Error handling

Engines may respond with:

```text
<error [code] [details?]
```

Example:

```text
<error unknown_lexicon FAKELEX
```

For multiline responses, an `error` line ends the response immediately.

## Current goals

The first goals for CGP are:

- define a stable draft protocol
- support one-engine communication
- support engine-vs-engine match runners
- allow bots written in different languages to play through the same interface
- make lexicon and tileset compatibility checkable
- allow servers to send private player state safely to individual engines

## Related project ideas

`Scuteboard` is a planned GUI / tournament runner that speaks CGP.

A CGP engine should be launchable by Scuteboard as a separate process.

## License

This project is licensed under the **Apache License, Version 2.0** - see the [LICENSE](LICENSE) file for details.
