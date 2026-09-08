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

Use the full address. The short `owner/repo` form connects over SSH, which needs keys set up.
Restart Claude Code when it asks.

## Then run this

```
/setup
```

It asks which job is closest to yours, then about 12 questions on how you actually work, and
builds the setup out of your answers. Delivery and marketing get different folder shapes. A
marketing setup has no clients directory in it.

You get the folder structure, the CLAUDE.md it reads at the start of every session and a
place to keep API keys. The knowledge base arrives with your own material already in it. It
pulls the current documentation for whatever platform you live in. It reads whatever real
work you point it at. Then it writes one skill for the thing you said you repeat most, and
runs that skill once on something real of yours, in front of you.

Point it at a folder of your own notes or paste a few in. If you have an API key for a tool
you use it can read from there instead. Most people haven't got one.

It won't build anything until you've answered the questions. Give it 15 minutes.
