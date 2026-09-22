import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "csv-tools", version: "1.0.0" });

server.registerTool(
  "parse_csv",
  {
    title: "Parse CSV",
    description: "Parses CSV text into rows of fields.",
    inputSchema: { csv: z.string() },
  },
  async ({ csv }) => {
    const rows = csv.split("\n").filter(Boolean).map((r) => r.split(","));
    return { content: [{ type: "text", text: JSON.stringify(rows) }] };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
