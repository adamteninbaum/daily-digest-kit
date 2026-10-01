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
1. Open the intake form (https://claude.ai/artifact/VHoQtYU45bG1FYuxHHZihs, once it is
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

## Daily Digest Lite (the 20-second version)

`lite/` is a no-setup version for sharing. A friend opens one link, picks topics and taps
**Make my brief**. Their own Claude (on their own plan, via the page's `sample` capability)
picks stories from a shared headline pool and writes the script; their browser reads it aloud
with word highlighting. Preferences, briefs and votes stay in their browser.

- `lite/build_pool.py OUT.json` builds the headline pool (Google News per topic, Hacker News,
  Techmeme, Hugging Face papers). A small Routine on the owner's account runs it a few times a
  day and republishes `lite/index.html` with `pool.json` to the Lite page.
- Tradeoffs vs the full kit: no newsletters, no phone alerts, no schedule (tap to make one),
  device voice instead of Edge TTS, and stories are summarized from headlines.
