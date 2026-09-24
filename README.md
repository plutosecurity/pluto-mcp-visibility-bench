# pluto-mcp-visibility-bench

benchmark of 60 MCP (Model Context Protocol) test
servers, covering 8 categories from the OWASP MCP Top 10 that existing
public MCP security benchmarks do not test.

Published by [Pluto Security](https://pluto.security).

## Why this exists

Existing public MCP security benchmarks (MCPTox, MCPSecBench, MSB) give
solid coverage of two OWASP MCP Top 10 categories: **MCP03 (Tool
Poisoning)** and **MCP05 (Command Injection & Execution)**. The other
eight categories — token/secret mismanagement, privilege escalation,
supply-chain tampering, intent-flow subversion, insufficient
authentication, lack of audit/telemetry, shadow servers, and context
over-sharing — were untested by anything publicly available at the time
this was built. This dataset fills that gap.

Every case also states which MCP evidence location its planted mechanism
lives in (description, schema, source, runtime response, multi-call
state, server identity, or install-time script) — so it's checkable
whether a given scanner architecture could ever see it, before any
scanner is run.

## What's here

- **60 cases**: 41 malicious, 19 benign, across 8 categories.
- `ground_truth.json`: one entry per case — the exact planted mechanism
  (or, for benign cases, confirmation nothing is planted), which MCP
  evidence location it lives in (description, schema, source, runtime
  response, multi-call state, server identity, install-time script), and
  the matching benign counterpart's ID where one exists.
- `cases/<owasp-category>/malicious/<case-id>/` and
  `cases/<owasp-category>/benign/<case-id>/`: the actual runnable MCP
  servers (Python via the official `mcp` SDK, or Node.js via
  `@modelcontextprotocol/sdk` for the supply-chain cases), each paired
  with an `mcp.json` client config.

## Categories

| OWASP category | What's tested | Malicious | Benign |
|---|---|---|---|
| MCP01: Token Mismanagement & Secret Exposure | A secret registered in one tool call leaks in a *later, unrelated* call's response | 6 | 2 |
| MCP02: Privilege Escalation via Scope Creep | A tool declares `readOnlyHint: true` but its code mutates state | 6 | 2 |
| MCP04: Software Supply Chain Attacks | An install-time `postinstall` script, and a matched legitimate/typosquatted server pair | 5 | 4 |
| MCP06: Intent Flow Subversion | A tool gives a correct, honest answer while smuggling in a redirect for the agent's next action | 5 | 2 |
| MCP07: Insufficient Authentication & Authorization | A sensitive tool with no real role check, and cross-session data reuse via a guessable session ID | 7 | 3 |
| MCP08: Lack of Audit and Telemetry | A destructive action whose code silently discards any record of it (see caveat below) | 5 | 2 |
| MCP09: Shadow MCP Servers | A server that spoofs another server's declared identity during the MCP handshake (see caveat below) | 2 | 2 |
| MCP10: Context Injection & Over-Sharing | A tool's response returns materially more data than its own description promises | 5 | 2 |

**Two explicit caveats.** MCP08 (Lack of Audit and Telemetry) and MCP09
(Shadow MCP Servers) describe organizational, fleet-wide properties in
the original OWASP taxonomy — whether an organization has centralized
logging, and whether it can discover unauthorized servers. No single test
server can fully represent either property. The cases here are narrow,
honest **proxies**: a single server that suppresses its own audit trail,
and a matched pair where one server impersonates another's declared
identity. Useful signal, not a full representation of the OWASP category
— stated here rather than overclaimed.

## Methodology

Every case follows the same discipline used to build MCPTox, MCPSecBench,
and MSB in the first place:

1. **One planted mechanism per case**, stated as a single precise
   sentence in `ground_truth.json`.
2. **Ground truth by direct inspection.** Every mechanism was verified by
   actually launching the server and connecting a real MCP client — not
   assumed from the code, and never inferred from any scanner's output.
3. **A benign counterpart for every mechanism family**, structurally
   comparable to its malicious counterpart, not an unrelated real-world
   server bolted on afterward.
4. **No overlap with MCPTox, MCPSecBench, MSB**, or other MCP security
   benchmarks — each category was checked against existing public
   datasets before being added.

## Using this dataset

Each case is a self-contained MCP server. To run one:

```bash
# Python cases
pip install "mcp<2"
python3 cases/<category>/<malicious-or-benign>/<case-id>/server.py

# Node.js cases (MCP04 only)
cd cases/mcp04-supply-chain/<malicious-or-benign>/<case-id>
npm install --ignore-scripts   # deliberately skip postinstall; see the case's own notes
node server.mjs
```

Point any MCP client or scanner at the case's `mcp.json`, or launch it
directly via stdio and compare its behavior against the mechanism
described in `ground_truth.json`.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). We welcome additional cases
that follow the same ground-truth discipline, especially for OWASP
categories not yet well represented here.

## License

Apache-2.0 — see [`LICENSE`](LICENSE). All cases are synthetic, built for
defensive security research, and contain no real credentials, real
target infrastructure, or functioning exploit payloads (network calls in
the supply-chain cases point at a non-resolving `.test` domain and are
inert by design).
