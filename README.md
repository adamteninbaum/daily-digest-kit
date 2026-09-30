# Daily Digest kit

A personal daily audio news brief that runs in **your own** Claude account. Pick your
topics, and every morning you get a private page with a 1 to 3 minute audio brief, the
full transcript with each word lighting up as it's read, direct links, and thumbs up/down
buttons that teach it what you like.

Sources: the web (Google News for your topics, Hacker News and Techmeme for tech, and a
few targeted searches) and, if you want, the newsletters already in your Gmail.

## Get started (about 10 minutes)
You need a paid Claude plan that includes Claude Code and Routines.

**With the plugin (easiest):** install the `daily-digest` plugin, then in Claude Code
type `/daily-digest:setup`. Claude asks a few questions, builds your page and daily
schedule, and makes your first brief. Later, `/daily-digest:update-profile` changes
topics, length, time and so on.

To try the plugin before it is in a marketplace:
`/plugin marketplace add adamteninbaum/daily-digest-kit`, then
`/plugin install daily-digest@daily-digest-kit`.

**Without the plugin:**
1. Open the intake form (https://claude.ai/artifact/TQZW7vQwws8rkmU7nkgCHi, once it is
   shared with you), answer the questions, and
   copy the setup message it gives you.
2. Go to claude.ai/code, start a new session, paste the message, and let Claude set
   everything up. It will tell you if you need to flip any settings (usually: turn on
   full network access for your cloud environment, and attach Gmail if you want your
   newsletters included).

## What's in here
- `.claude-plugin/`: the plugin manifest (and a one-plugin marketplace for testing).
- `skills/setup/SKILL.md`: what Claude does to set you up (the plugin command and the
  intake form's pasted message both follow it). `skills/update-profile/SKILL.md`: changes.
- `RUNBOOK.md`: what your daily run does, step by step.
- `SETUP.md`: entry point for the pasted setup message; points to the setup skill.
- `PROFILE.md`: your preferences format.
- `site/index.html`: your digest page. `intake/index.html`: the intake form.
- `discover.py` (web news), `resolve_links.py` (clean links), `tts.py` (audio + word
  timings), `build_digest.py` (page files), `notify.py` and `dropbox_upload.py` (optional).

Everything runs on free services: Edge TTS for the voice and public news feeds. Your
brief runs on your own Claude usage.
