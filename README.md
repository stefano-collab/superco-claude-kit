# Superco Claude kit

## Install

You need Claude Code. If you have the Claude desktop app then you already have it, on the
third tab along the top, next to Chat and Cowork. You don't need a terminal.

Make an empty folder for your work somewhere. Open the Code tab and point it at that folder.
Then type these 2 lines into the chat box:

```
/plugin marketplace add https://github.com/stefano-collab/superco-claude-kit.git
/plugin install superco-kit@superco
```

Use the full address rather than the short `owner/repo` form, which connects over SSH and
needs keys set up. Restart Claude Code when it asks.

## Then run this

```
/setup
```

It asks you about 15 questions on how you actually work, and then builds your setup out of
your answers. You get a folder structure, the CLAUDE.md it reads at the start of every
session, a place to keep API keys and one skill for whatever you said you repeat most.

It won't build anything until you've answered the questions. Give it 10 minutes.
