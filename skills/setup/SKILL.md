---
name: setup
description: Set up the person's own Daily Digest, a private page with a new daily audio news brief made by a scheduled Routine in their Claude account. Use when someone asks to set up, create or start their daily digest, news brief or morning audio brief, or pastes a Daily Digest setup message or profile JSON from the intake form.
---

# Set up a Daily Digest

You are building one person's Daily Digest in their own Claude account: a private
Artifact page, plus a daily Routine that writes a new audio brief onto that page. Do the
steps in order. Ask questions only in steps 1 and 3.

KIT = `https://github.com/adamteninbaum/daily-digest-kit` (public; git clone needs no
login). The daily Routine clones KIT and follows its `RUNBOOK.md`, so setup and daily runs
always use the same code.

## 1. Get their profile
If the message already has a profile JSON (pasted from the intake form), use it as is and
go to step 2. Otherwise build one with them. The format and defaults are in
`PROFILE.md` in KIT (after step 2 you can read it there).

Ask these in plain chat, in one message, and say they can skip any:
- First name (the brief greets them with it).
- In their own words, what they are into (this matters most).
- Anything to leave out.
- Their city or area for local news (optional).

Then use `AskUserQuestion` for the rest, in one call:
- Topics (multiSelect): offer 4 broad ones that fit what they said, from: AI, Tech &
  gadgets, Business & markets, Startups, Personal finance, US politics, World news,
  Science, Space, Health & fitness, Climate, Sports, Film & TV, Music, Gaming, Design &
  creative, Food & cooking, Travel, Books, Local news.
- Sources: "The web" (Google News, Hacker News, Techmeme; recommended), "The web and
  my Gmail newsletters".
- Length: "About 2 minutes, 6 stories (Recommended)", "About 1 minute, 4 stories",
  "About 3 minutes, 8 stories".
- Ready by: "7:30am", "8:00am", "9:00am" (they can type another time). Time zone: use
  the one they mention; otherwise ask in the same call.

Defaults for anything not asked: `wildcards` 2 (at most `items` - 1),
`voice` "en-US-AndrewMultilingualNeural", `tone` "conversational, like a smart friend
catching you up", `newsletter_senders` [], `alerts.ntfy_topic` "", `dropbox` false.
`timezone` is an IANA name (e.g. "America/New_York"); `timezone_label` is its short label
("ET", "CT", "MT", "PT", or the usual abbreviation elsewhere). `time` is "HH:MM", 24-hour.

## 2. Get the kit
Clone KIT into your scratchpad directory (or the working directory if you have no
scratchpad): `git clone KIT <dir>/daily-digest-kit`. Work from that folder. The
Artifact tool publishes only files under the working or scratchpad directory.

## 3. Confirm once, then check the network
Tell them in a few lines what you are about to create, and wait for a yes:
- A private page, "<name>'s Daily Digest", with its own small database (their profile
  and their votes) and permission to call one tool on their Claude Code Remote
  connector, `fire_trigger`, so its "New brief now" button can start their Routine.
- A daily Routine at <time> <timezone_label> that clones KIT and follows its
  `RUNBOOK.md`, runs on their own Claude usage, and sends a push notification when done.
  Whatever is on KIT's main branch at run time is what runs.
- If they picked newsletters: the Routine reads their Gmail newsletters (read only).

Then run `curl -s -o /dev/null -w '%{http_code}' https://speech.platform.bing.com/ ; echo;
curl -s -o /dev/null -w '%{http_code}' https://news.google.com/rss ; echo`.
If either prints 000 or 403, their cloud environment blocks the voice or news services.
Carry on, and in step 9 tell them to turn on **Full** network access: in a Claude Code
session, open the session title menu, choose **Edit cloud environment**, set **Network
access** to Full, and save. Their daily Routine uses the same environment.

## 4. Publish their digest page
Read `site/index.html` from the clone in full, then publish it with the `Artifact` tool
(action `publish`): `file_path` = that file, `icon` = `audio`, `description` = "My daily
audio news brief", `capabilities` =
`{"db": {}, "mcp": {"servers": [{"server": "Claude Code Remote", "tools": ["fire_trigger"]}]}}`.
Keep the URL it returns: that is PAGE_URL.

If the publish is refused, stop and tell them what was refused and why, in plain words;
do not look for another way to publish it.

## 5. Create their daily Routine
Use `create_trigger` (Claude Code Remote tools; load with ToolSearch if deferred):
- `name`: "<name>'s Daily Digest"
- `create_new_session_on_fire`: true
- `notifications`: `{"push": true}`
- `cron_expression`: `CRON_TZ=<timezone> <MM> <HH> * * *`, where HH:MM is 8 minutes
  before the profile's `time` (so the brief is ready on time).
- `connectors`: `["Gmail"]` if `sources.newsletters` is true. If the call refuses
  connectors, create it without them and tell them in step 9 to attach Gmail to the
  Routine in claude.ai (Claude Code, Routines, their digest Routine, Connectors).
- `environment_id`: leave it out in a claude.ai/code session. Outside one (for example
  the desktop app or a local terminal), call `list_environments` and use their default
  cloud environment; ask only if there are several and none is clearly the default.
- `initiation`: `human_request`
- `prompt` (fill in the blanks):

```
You are making <name>'s daily audio news brief. Do every step; do not ask questions.
Clone https://github.com/adamteninbaum/daily-digest-kit (public; git clone needs no login)
and follow its RUNBOOK.md exactly.
PAGE_URL = <PAGE_URL>
Backup copy of the profile (the live one is saved on the page as config/profile):
<profile JSON>
```
Keep the trigger id it returns.

## 6. Save the profile on the page
Add `page_url` and `trigger_id` to the profile, then `ArtifactData` action `set`,
`url` = PAGE_URL, `collection` = `config`, `doc_id` = `profile`, `data` = the profile.
(Load ArtifactData with ToolSearch if deferred.)

## 7. Make the first brief
`fire_trigger` with the trigger id. It takes about 5 minutes.

## 8. Optional extras
- ntfy alerts: if `alerts.ntfy_topic` is set, tell them to install the free **ntfy** app
  and subscribe to that exact topic.
- Dropbox copies of the audio: only if they ask; see `dropbox_upload.py` in KIT.

## 9. Tell them, briefly
- Their page link (PAGE_URL), and that the first brief appears there in about 5 minutes.
- Any fixes from steps 3 and 5 they need to do (network access, attaching Gmail).
- How to use it: press play (each word lights up as it is read), vote "More like this" /
  "Less like this" to teach it, "New brief now" for an extra one (allow the permission
  the first time), and "All briefs" for past days.
- For a phone icon: open the page in Safari, Share, Add to Home Screen.
- To change anything later: `/daily-digest:update-profile`.
