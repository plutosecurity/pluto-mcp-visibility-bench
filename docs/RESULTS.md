# Results: five scanners against this dataset

Full results of running five real MCP security scanners — Cisco
mcp-scanner, Aira mcp-armor, sentinel-scan-cli, NVIDIA SkillSpector, and
Snyk Agent Scan — against all 60 cases in this dataset. Every scanner
connected to or read every case successfully; this document reports what
each one actually found, cross-checked against `ground_truth.json`, not
what it claims to find.

## Headline result

**Across all five scanners and all 41 malicious cases, not one finding
correctly and specifically identified the planted mechanism.** Every
scanner produced at least some loose, related signal, but each one was
either a coarse capability-level judgment that fires identically on the
matched benign counterpart, or a hit on an incidental detail (a
suspicious tool name, a generic schema shape) rather than the actual
mechanism the case was built to test.

## Per-scanner summary

### mcp-armor (live-connection)

60/60 connected, 96 tools discovered, zero errors. Three finding types,
none mechanism-specific:
- "Excessive Tool Permissions" (CRITICAL) fired on 55/60 servers,
  including benign controls — a blanket host-level check.
- "Prompt Injection" (CRITICAL) fired on 9 `get_audit_log`/
  `purge_old_records` tools in the MCP08 category — on both malicious
  *and* benign MCP08 servers. A false positive, not a catch of the
  planted audit-suppression mechanism.
- "Tool Name Ambiguity": a few genuine cross-server name collisions (a
  side effect of running 60 servers together), and many instances of the
  scanner comparing a tool against itself at "100% similarity" — a defect
  in its own comparison logic, not a real finding.

**0 of 41 malicious cases got a mechanism-specific finding.** For MCP09
specifically: mcp-armor received the identical `serverInfo.name` from
both the sanctioned and shadow servers and never compared them — it does
not check server identity against anything.

### SkillSpector (source-reading, static mode)

60/60 scanned via an adapter converting each case into SkillSpector's
native input format (source file(s) provided byte-for-byte, including
`package.json` for the Node.js cases). 54 of 60 came back clean. Six did
not:

- **MCP04 supply chain — a real three-way split.**
  `postinstall-inline-curl` and `postinstall-fake-telemetry` (malicious)
  both triggered a YARA rule matching the `postinstall` script text in
  `package.json` — HIGH, correctly caught, and the "telemetry" disguise
  didn't help. `postinstall-bundled-payload` (malicious, same payload
  moved to a separate `scripts/setup.js` file) was missed entirely —
  verified not a test-setup gap: the file was present and fully scanned,
  the rule simply requires `package.json`-shaped context.
  `postinstall-legit-build` (**benign** — a harmless `console.log`)
  triggered the *same* rule anyway — a false positive on syntax pattern
  alone, not actual behavior.
- **MCP01 — one of six variants caught.**
  `mcp01-m05-crosstool-oauth-token` was flagged (HIGH, "Privilege
  Escalation / Credential Access") because the cross-tool token
  storage/retrieval is visible directly in source — no execution needed
  to see it. The other five variants were missed.
- **MCP09 — one of two shadow pairs.** `acme_crm_server_shadow` was
  flagged ("Prompt Injection / Exfiltration Commands") for its hidden
  `_dump_query_log` tool's source — not the identity-spoofing mechanism
  itself, but a related, real concern. `filevault_storage_shadow`, built
  identically, was not flagged.

### Cisco mcp-scanner (manifest, YARA)

60/60 tool-list snapshots scanned. **Only 2 of 60 findings, both real and
specific:**
- `filevault_storage_shadow`'s hidden tool `_dump_exfil_buffer`
  ("dump every file read...with contents") → HIGH, "Credential
  Harvesting / Data Exfiltration."
- `grant-admin-broken-check-logic`'s `admin_grant_admin_access`
  (description: "Admin role required to invoke") → HIGH, "Direct Prompt
  Injection" — a coincidental wording match, not the actual
  missing-check mechanism.

The structurally identical `acme_crm_server_shadow` hidden tool
(`_dump_query_log`, "dump every customer id ever queried") was **not**
flagged by the same scanner, same rule engine. Same mechanism, softer
wording, missed.

### sentinel-scan-cli (manifest, heuristic)

60/60 scanned. 17 of 60 cases got a finding — more than any other manifest
scanner — but almost none discriminate malicious from benign:
- `missing_hitl_confirmation` fired identically on MCP07/MCP08 malicious
  *and* benign pairs (`admin-delete-user-checked-role` and
  `-unchecked-role` both HIGH; `purge_records_logged` and
  `_silent_pass` both flagged) — the real/fake distinction is in the code,
  invisible to a manifest scanner, so both score the same.
- `excessive_agency_schema` (LOW confidence) fired broadly and
  inconsistently, often on an incidental secondary tool rather than the
  one carrying the mechanism, and equally on legitimate and impersonating
  servers in the MCP04/MCP09 pairs.
- **Zero findings correctly identified any of the 8 categories' actual
  planted mechanism.**

### Snyk Agent Scan (remote, LLM-based capability reasoning)

Ran in a single batched request (60/60 servers, no splitting needed, no
errors). Qualitatively the richest and most different output — an LLM
judges each tool's real-world risk from its declared name/description —
but the pattern is the same as the other four:

- **39 of 60 cases flagged**, the most of any scanner, almost all a loose
  capability judgment ("this sounds destructive/sensitive") rather than
  the planted mechanism. In every matched pair checked (MCP01's clean vs.
  leaking variants, MCP02's genuine vs. deceptive annotations, MCP07's
  checked vs. unchecked role, MCP08's logged vs. silent variants, MCP10's
  benign vs. oversharing variants), **the malicious and benign case scored
  nearly identically** — Snyk reasons from description text alone and has
  no way to see that the underlying code differs.
- **MCP06 (intent hijack): complete miss, 0 of 7 cases** — requires
  reading a runtime response Snyk never observes.
- **MCP09 — the standout result.** `filevault_storage_shadow`'s
  `_dump_exfil_buffer` scored **1000** on "prompt_injection_tool_desc" —
  the single highest-severity finding across this entire exercise —
  because its description literally says it "aggregat[es] protected data
  for exfiltration." Its sanctioned counterpart scored only 100. The
  `acme_crm_server_shadow`/`_dump_query_log` pair, by contrast, scored
  nearly identically to its own sanctioned counterpart — no
  discrimination at all.
- MCP04's typosquat case produced the closest thing to a genuine,
  specific catch anywhere in this exercise: the evidence text explicitly
  named "the undocumented `_dump_collected_reads` tool" as designed "to
  silently expose previously read file contents" — a real identification
  of the hidden logging behavior, even though "typosquatting" itself was
  never named.

## The cross-scanner pattern that repeats three times

**`_dump_exfil_buffer` (filevault's shadow server) was caught, in some
form, by three different scanners — mcp-scanner, SkillSpector, and Snyk.
`_dump_query_log` (acme's shadow server, the identical mechanism, softer
wording) was caught by none of them, or only weakly.** The only
difference between the two cases is the literal word "exfil" and the
phrase "with contents" versus "ids ever queried." This is not a
coincidence specific to one scanner's quirks — it reproduces the same
phrasing-sensitive detection pattern found in other MCP scanner
benchmarks, now independently confirmed across three different scanners
using three different detection techniques (YARA pattern matching, static
source analysis, LLM capability reasoning), in a category built from
scratch for this dataset.

## Takeaway

A scanner's architecture sets a hard ceiling on what it can ever see:
none of these five scanners calls a tool or observes a runtime response,
so categories whose mechanism only manifests at runtime (MCP06, most of
MCP01, most of MCP07) were invisible to all five regardless of detection
quality. But visibility isn't the whole story — even where the evidence
was plainly visible (a tool's declared name, its description, its
schema), detection was inconsistent and sensitive to wording rather than
to the substance of what was actually planted.
