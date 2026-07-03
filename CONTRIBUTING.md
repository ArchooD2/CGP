# Contributing to CGP

Thanks for helping with CGP — the Crossword Game Protocol.

CGP is currently a draft protocol. Contributions are welcome, especially if they make the protocol clearer, easier to implement, or easier to test across engines written in different languages.

## Project goals

CGP should be:

- simple to parse
- easy to implement in any language
- usable through stdin/stdout
- friendly to GUI apps, match runners, validators, and engines
- flexible enough for Scrabble-like variants
- explicit about public and private game information

CGP should not require engines to use any specific move generator, dictionary format, GUI library, or programming language.

## Repository files

The main files are:

```text
README.md
SPEC.md
EXAMPLE.md
CONTRIBUTING.md
```

`README.md` explains the project.

`SPEC.md` defines the protocol.

`EXAMPLE.md` shows example server/engine conversations.

`CONTRIBUTING.md` explains how to suggest or make changes.

Reference implementations may be added later under:

```text
reference/
```

## Types of contributions

Useful contributions include:

- clarifying unclear protocol wording
- adding examples
- fixing contradictions between `README.md`, `SPEC.md`, and `EXAMPLE.md`
- proposing commands or response formats
- writing validators
- writing sample engines
- testing engines written in different languages
- documenting edge cases

## Before changing the protocol

Before changing command names, response formats, or notation, check whether the change affects:

- existing examples
- required commands
- recommended commands
- move notation
- board encoding
- Tile-FEN encoding
- lexicon compatibility checks
- private player state such as `rack` and `unseen`

Protocol changes should update all relevant docs together.

If you change `SPEC.md`, check whether `README.md` and `EXAMPLE.md` also need updates.

## Protocol design rules

Prefer simple line-based commands.

Prefer one obvious way to do something.

Avoid commands that require complex parsing unless they provide a clear benefit.

Keep engine responses easy to read from stdout.

For multiline responses, define a clear terminator line.

For errors during multiline responses, engines may send:

```text
<error [code] [details?]
```

An error line ends the multiline response immediately.

## Required vs recommended commands

Be careful when adding required commands.

A command should only become required if a minimal engine cannot reasonably function without it.

Recommended commands are better for metadata, validation, diagnostics, and compatibility checks.

Required commands should stay small.

## Public and private state

CGP uses a server/engine architecture.

Engines do not communicate directly with each other.

The server is responsible for sending each engine only the information that engine is allowed to know.

Public state includes the board position.

Private state may include:

```text
rack
unseen
```

Do not design protocol features that require one engine to trust another engine directly.

## Board encoding

Board state uses a compact 15-row encoding inspired by FEN.

Example:

```text
15/15/15/15/15/15/15/7CAT5/15/15/15/15/15/15/15
```

Digits represent runs of empty squares.

Letters represent tiles on the board.

Rows are separated by `/`.

For a standard board, there should be 15 rows, and each row should expand to 15 squares.

Changes to board encoding should be treated as major protocol changes.

## Tile-FEN encoding

Unseen tile pools use Tile-FEN notation.

Example:

```text
5A2B1C3D8E1?
```

This means:

```text
5 A tiles
2 B tiles
1 C tile
3 D tiles
8 E tiles
1 blank tile
```

Zero-count entries are allowed when a server wants to be explicit:

```text
6A2B1C4D6E0F
```

Changes to Tile-FEN encoding should update `SPEC.md` and `EXAMPLE.md`.

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

Lowercase letters in words represent blanks.

Do not change move notation casually. Move notation is one of the easiest places to break every engine.

## Lexicons and tilesets

Lexicon-related changes should consider:

- how engines report supported lexicons
- how a server chooses a shared lexicon
- how `lexiconsample` works
- how `lexiconcheck` works
- how `tileset` works
- how `tilesetcheck` works

The protocol should not require engines to reveal an entire word list.

Sampling and checking are for compatibility, not proof of full lexicon equality.

Static resources such as lexicons, tile sets, and rule variants should be negotiated by identity during setup. Do not require a server to transmit a full dictionary every move.

## Compatibility expectations

A CGP engine should be able to:

1. receive `cgp`
2. respond with metadata and `cgpok`
3. receive `setup`
4. respond with `setupok` or `error`
5. receive `ready`
6. respond with `readyok` or `error`
7. receive `position`
8. receive private state such as `rack` and `unseen`
9. receive `go`
10. respond with exactly one `bestmove` line
11. receive `quit`
12. exit cleanly

Reference validators should test these basics first.

## Adding examples

Examples may show one server talking to one engine, or one server managing multiple independent engine sessions.

Do not show two engines talking directly to each other. In engine-vs-engine examples, each engine has its own stdin/stdout session with the server.

Use:

```text
>
```

for server-to-engine lines.

Use:

```text
<
```

for engine-to-server lines.

Example sessions should be valid according to `SPEC.md`.

## Error handling

When adding errors, prefer short stable codes.

Good:

```text
<error unknown_lexicon FAKELEX
<error bad_position
<error not_ready
```

Less good:

```text
<error I have no idea what that lexicon is lol
```

Human-readable details can come after the stable error code.

## Style

Keep docs readable.

Use short sections.

Use examples for every non-obvious format.

Avoid overexplaining implementation details in the spec.

Implementation advice belongs in README files, examples, or reference-code comments.

## Versioning

CGP is currently draft `0.2`.

Before `1.0`, breaking changes are allowed with reasoning explaining them.

After `1.0`, breaking changes should require a new major version or clearly named protocol version.

If a change breaks existing engines, call it out clearly.

## Suggested pull request checklist

Before submitting a change, check and include:

- [ ] Does this change affect `SPEC.md`?
- [ ] Does this change affect `README.md`?
- [ ] Does this change affect `EXAMPLE.md`?
- [ ] Does this change introduce or change a required command?
- [ ] Does this change affect board encoding?
- [ ] Does this change affect Tile-FEN encoding?
- [ ] Does this change affect move notation?
- [ ] Does this change affect private state like `rack` or `unseen`?
- [ ] Does this change keep stdin/stdout communication simple?

## Current priorities

Current useful work:

- stabilize the draft protocol
- write a basic validator
- write simple sample engines
- test Python engines against compiled engines
- test lexicon and tileset compatibility
- document edge cases
- build Scuteboard or another CGP-compatible runner

## Name note

CGP stands for Crossword Game Protocol.

Scuteboard is a planned GUI or match runner that speaks CGP.
