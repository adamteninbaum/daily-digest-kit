---
name: update-profile
description: Change an existing Daily Digest, such as its topics, interests, sources, length, voice, tone, delivery time or time zone. Use when someone asks to update, change or tweak their daily digest or news brief, or pastes a new setup message with "Update my Daily Digest profile".
---

# Update a Daily Digest profile

The person already has a Daily Digest page and a daily Routine (made by
`/daily-digest:setup`). The profile format is `PROFILE.md` in
`https://github.com/adamteninbaum/daily-digest-kit`.

## 1. Find their digest
- If they gave the page link, that is PAGE_URL. Otherwise `Artifact` action `list` and
  pick the one titled "<name>'s Daily Digest"; ask only if there are several or none.
- Load `ArtifactData` (ToolSearch `select:ArtifactData` if deferred) and `get` collection
  `config`, doc_id `profile`. Keep its `version`; `trigger_id` is their Routine.
- If the profile has no `trigger_id`, find the Routine with `list_triggers` (named
  "<name>'s Daily Digest").

## 2. Work out the change
- If they pasted a new profile JSON, use it, keeping the saved `page_url` and `trigger_id`.
- Otherwise apply what they asked to the saved profile. Ask only if the request is
  unclear. Show the fields you will change, old and new, in a short list.

## 3. Save it
- `ArtifactData` `set`, collection `config`, doc_id `profile`, `if_version` = the version
  from step 1, `data` = the new profile.
- `update_trigger` on `trigger_id`:
  - `prompt`: the same prompt `/daily-digest:setup` writes (step 5 of its SKILL.md), with
    the new profile JSON as the backup copy.
  - `cron_expression`, only if `time` or `timezone` changed:
    `CRON_TZ=<timezone> <MM> <HH> * * *`, HH:MM being 8 minutes before `time`.
- If they turned on newsletters, tell them to attach Gmail to the Routine in claude.ai
  (Claude Code, Routines, their digest Routine, Connectors) unless it already has it.

## 4. Tell them
One or two lines: what changed, and that the next brief (at <time> <timezone_label>, or
"New brief now" on the page) uses it. Votes and past briefs are kept.
