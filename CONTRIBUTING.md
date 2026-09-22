# Contributing

This dataset follows a strict ground-truth discipline: every case's
planted mechanism (or, for benign cases, absence of one) must be
independently verifiable by inspection, not just plausible.

## Adding a case

1. **Pick a real gap.** Check `README.md`'s category table and
   `ground_truth.json` first — a new case should test a mechanism not
   already covered, not a variant that duplicates an existing one's
   evidence location and shape.
2. **One mechanism per case**, stated as a single precise sentence.
3. **Build a benign counterpart** that is structurally comparable (same
   tool shape, same complexity) — not an unrelated real-world server.
4. **Verify it yourself before opening a PR.** Launch the server, connect
   a real MCP client (the official `mcp` Python SDK or
   `@modelcontextprotocol/sdk` for Node.js), and confirm the mechanism
   manifests exactly as your ground-truth entry describes. Paste that
   verification output in your PR description.
5. **Add a `ground_truth.json` entry** following the existing schema:
   `id`, `owasp_category`, `malicious`, `mechanism`, `evidence_location`,
   `benign_pair_id`, `verified_by`, `date`.
6. **No real payloads.** Any network call in a case must point at a
   non-resolving `.test`/`.invalid` domain and fail harmlessly. No real
   credentials, no functioning exploits, no destructive behavior against
   anything outside the case's own in-memory state.

## Reporting scanner results

If you run a scanner against this dataset, we'd like to hear about it —
open an issue with the scanner name/version and what it did or didn't
catch, ideally with the raw output. Findings that contradict or refine
anything in `docs/RESULTS.md` are especially welcome.
