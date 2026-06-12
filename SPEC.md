# CGP: Crossword Game Protocol

Version: 0.1 draft

## 1. Purpose

CGP is a line-based text protocol for communication between crossword-game engines and GUIs, match runners, or validators.

The server controls the game flow. The engine receives game state and returns a move.

CGP uses a server/engine architecture. Engines do not communicate with each other directly.

The server is responsible for sending each engine only the public and private information that engine is allowed to know.

## 2. Transport

Engines communicate through standard input and standard output.

Each command is one line.

Each response is one line unless the command explicitly defines a multiline response.

Engines must flush stdout after every response.

Lines should be UTF-8 text.

## 3. Notation used in this document

`>` means the server sends a line to the engine.

`<` means the engine sends a line to the server.

`[]` means a required placeholder.

`[x...]` means one or more values.

`[x?]` means an optional value.

Example:

```text
>cgp
<cgpok
```

## 4. Required startup sequence

The server starts by sending:

```text
>cgp
```

The engine must respond with zero or more identification or option lines, followed by:

```text
<cgpok
```

Example:

```text
>cgp
<name RandomTurtle
<author Dev
<version 0.0.1
<option CGP_Variant standard standard super custom
<option CGP_Lexicon NWL23 NWL23 CSW24 custom
<cgpok
```

Required final response:

```text
<cgpok
```

Optional startup responses:

```text
<name [engine name]
<author [author name]
<version [version string]
<option [option name] [default value] [allowed value...]
```

## 5. Readiness

The server may ask whether the engine is ready:

```text
>ready
```

The engine must respond:

```text
<readyok
```

or:

```text
<readyno [reason]
```

`ready` should be sent after setup and before asking the engine to move.

## 6. Setup

The server sends game settings using:

```text
>setup variant [variant] lexicon [lexicon]
```

Example:

```text
>setup variant standard lexicon NWL23
```

The engine responds:

```text
<setupok
```

or:

```text
<setupno [reason]
```

Examples:

```text
<setupno unknown_lexicon
<setupno unknown_variant
```

## 7. Lexicon list

The server may ask which lexicons the engine supports:

```text
>lexicons
```

The engine responds:

```text
<lexicons [lexicon...]
```

Example:

```text
>lexicons
<lexicons NWL23 CSW24 enable sowpods
```

## 8. Variant list

The server may ask which variants the engine supports:

```text
>variants
```

The engine responds:

```text
<variants [variant...]
```

Example:

```text
>variants
<variants standard super custom
```

## 9. Lexicon compatibility check

The server may ask an engine for a sample of words from a lexicon:

```text
>lexiconsample [lexicon] [count]
```

The engine responds with one or more word lines, followed by:

```text
<endlexiconsample
```

Example:

```text
>lexiconsample NWL23 5
<word AA
<word QI
<word ZA
<word CAT
<word SLATE
<endlexiconsample
```

If the engine does not know the lexicon:

```text
<error unknown_lexicon [lexicon]
```

The server may ask an engine whether words are legal in a lexicon:

```text
>lexiconcheck [lexicon] [word...]
```

The engine responds:

```text
<lexiconcheck ok
```

or:

```text
<lexiconcheck no [bad word...]
```

Example:

```text
>lexiconcheck NWL23 AA QI ZZZZZ
<lexiconcheck no ZZZZZ
```

## 10. Tileset check

The server may ask for the tile distribution used with a lexicon:

```text
>tileset [lexicon]
```

The engine responds with tile lines, followed by:

```text
<endtileset
```

Format:

```text
<tile [letter] [count] [score]
```

Example:

```text
>tileset NWL23
<tile A 9 1
<tile B 2 3
<tile C 2 3
<tile ? 2 0
<endtileset
```

The server may ask an engine to verify a tileset:

```text
>tilesetcheck [lexicon] [tile spec...]
```

Tile specs use:

```text
[letter]:[count]:[score]
```

Example:

```text
>tilesetcheck NWL23 A:9:1 B:2:3 ?:2:0
<tilesetcheck ok
```

or:

```text
<tilesetcheck no [bad tile...]
```

Example:

```text
<tilesetcheck no Z ?
```

## 11. Board encoding

CGP positions use a compact board encoding inspired by FEN.

A standard board has 15 rows and 15 columns.

Rows are separated by `/`.

Letters represent occupied squares.

Numbers represent runs of empty squares.

For a 15×15 board, the largest possible empty run is `15`.

Each row must expand to exactly 15 squares.

A standard board position must contain exactly 15 rows.

Example empty board:

```text
15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
```

Example board with `CAT` on row 8 starting at column H:

```text
15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
```

The row `7CAT5` means:

```text
7 empty squares, then C A T, then 5 empty squares
```

Lowercase letters on the board represent blank tiles.

## 12. Position

The server sends the public board position using:

```text
>position [board]
```

Example:

```text
>position 15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
```

The empty board may be sent as:

```text
>position 15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
```

A server may also support this shorthand:

```text
>position startpos
```

`startpos` means the empty board for the current variant.

## 13. Private player state

The server may send private player state to an engine.

Private state is information known to the player represented by that engine, but not necessarily known to other players or engines.

Examples include the engine's rack and unseen tile pool.

The server is responsible for only sending private state to the engine that is allowed to know it.

Engines do not communicate with each other through CGP.

## 14. Rack

The server may send the engine's current rack using:

```text
>rack [tiles]
```

Example:

```text
>rack CTAESR?
```

The blank tile is represented by `?`.

The engine should treat `rack` as replacing its previous rack state.

## 15. Unseen tiles

The server may send the tile pool not visible to the engine using:

```text
>unseen [tile count...]
```

Tile counts use:

```text
[letter]:[count]
```

Example:

```text
>unseen 5A2B1C3D8E1?
```

The unseen pool usually includes the bag plus unknown opponent rack tiles.

The server may omit `unseen` if the variant or server does not support unseen-tile tracking.

The engine should treat `unseen` as replacing its previous unseen state.

## 16. Move notation

Placement moves use basic crossword notation:

```text
[column][row] [word]
```

for horizontal moves.

```text
[row][column] [word]
```

for vertical moves.

Examples:

```text
H8 SLATE
```

means play `SLATE` horizontally starting at column H, row 8.

```text
8H SLATE
```

means play `SLATE` vertically starting at row 8, column H.

Columns use letters.

Rows use numbers.

Rows are 1-indexed.

Columns are A-indexed.

Lowercase letters in a word represent blank tiles.

Example:

```text
H8 SLaTE
```

means the lowercase `a` is a blank tile assigned as A.

## 17. Asking for a move

The server sends:

```text
>go
```

or:

```text
>go movetime [milliseconds]
```

Example:

```text
>go movetime 1000
```

The engine responds with exactly one move:

```text
<bestmove [move]
```

or:

```text
<bestmove pass
```

Examples:

```text
<bestmove H8 SLATE
<bestmove 8H FLAKIEST
<bestmove pass
```

A normal turn may look like this:

```text
>position 15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
>rack SLATE??
>unseen 5A2B1C3D8E1?
>go movetime 1000
<bestmove 8H SLATE
```

## 18. Move validity

The engine should only return legal moves.

The server or match runner may reject illegal moves.

Illegal moves may cause the engine to lose the game, depending on the server or tournament rules.

## 19. Ping

The server may test whether the engine is alive:

```text
>ping
```

The engine should respond:

```text
<pong
```

## 20. Quit

The server may end the engine process:

```text
>quit
```

The engine should exit.

The engine does not need to respond to `quit`.

## 21. Errors

Engines may respond with:

```text
<error [code] [details?]
```

Examples:

```text
<error unknown_command banana
<error unknown_lexicon NWL23
<error bad_position
<error not_ready
```

For multiline commands, an `error` response ends the response immediately.

## 22. Required commands

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

A recommended CGP engine should also support:

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

## 23. Minimal legal session

```text
>cgp
<name PassTurtle
<author Dev
<version 0.0.1
<option CGP_Variant standard standard custom
<option CGP_Lexicon NWL23 NWL23 custom
<cgpok
>setup variant standard lexicon NWL23
<setupok
>ready
<readyok
>position 15/15/15/15/15/15/15/15/15/15/15/15/15/15/15
>rack CTAESR?
>go movetime 1000
<bestmove pass
>quit
```

## 24. Draft notes

This document describes CGP draft version 0.1.

Command names and response formats may change before version 1.0.

Implementations should treat unknown commands as non-fatal unless the command is required for the current session.
