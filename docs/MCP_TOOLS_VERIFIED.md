# MCP Tools - Complete Verified List (2025-01-19)

## ✅ CONFIRMED WORKING MCP Servers (All Tested)

### Core MCP Tools
1. **mcp__memory__*** ✅ WORKING
   - `create_entities`, `search_nodes`, `add_observations`, `read_graph`, `delete_entities`, etc.
   - Full memory management for SCS (Shared Context System)

2. **mcp__brave-search__*** ✅ WORKING
   - `brave_web_search`, `brave_local_search`
   - Web search for ComfyUI nodes, models, LoRAs

3. **mcp__sequential-thinking__*** ✅ WORKING
   - `sequentialthinking`
   - Complex problem solving and chain of thought

4. **mcp__filesystem__*** ✅ WORKING
   - `read_file`, `write_file`, `list_directory`, `search_files`, `list_allowed_directories`, etc.
   - Advanced file system operations

5. **mcp__desktop-commander__*** ✅ WORKING
   - Full suite of desktop/file commands
   - `get_config`, `read_file`, `write_file`, `start_process`, `interact_with_process`, etc.
   - Windows PowerShell/CMD compatible

### Browser Automation
6. **mcp__playwright-mcp__*** ✅ WORKING
   - `playwright_navigate`, `playwright_screenshot`, `playwright_click`, `playwright_fill`
   - `playwright_evaluate`, `playwright_console_logs`, `playwright_get_visible_html`
   - Advanced browser automation (different from deprecated playwright-mcp-server)

7. **mcp__puppeteer__*** ✅ WORKING
   - `puppeteer_navigate`, `puppeteer_screenshot`, `puppeteer_click`, `puppeteer_fill`
   - `puppeteer_evaluate`
   - Alternative browser automation

### Development Tools
8. **mcp__github__*** ✅ WORKING
   - `search_repositories`, `create_repository`, `get_file_contents`, `push_files`
   - `create_issue`, `create_pull_request`, `fork_repository`, `create_branch`
   - Full GitHub integration

9. **mcp__npm-search__*** ✅ WORKING
   - `search_npm_packages`
   - NPM package discovery

10. **mcp__sentry__*** ✅ WORKING
    - `whoami`, `find_organizations`, `find_projects`, `search_events`
    - `get_issue_details`, `update_issue`, `analyze_issue_with_seer`
    - Error tracking and monitoring

### AI/Search Tools
11. **mcp__perplexity__*** ✅ WORKING
    - `perplexity_ask`
    - AI-powered search and Q&A

### Microsoft Integration
12. **mcp__ms-365-mcp-server__*** ✅ AVAILABLE (requires login)
    - Full Microsoft 365 integration
    - OneDrive, Outlook, Teams, Planner, etc.
    - Currently NOT logged in but server is functional

### Installation Tools
13. **mcp__mcp-installer__*** (Available but not tested)
    - `install_repo_mcp_server`, `install_local_mcp_server`
    - For installing additional MCP servers

## ❌ NOT Available/Deprecated MCP Tools

1. **mcp__code_execution** ❌ NOT AVAILABLE
   - Use Python scripts via Bash instead

2. **mcp__web-fetch__fetch** ❌ DEPRECATED
   - Use WebFetch tool directly (standard Claude tool)

3. **mcp__playwright-mcp-server__*** ❌ DEPRECATED
   - Use mcp__playwright-mcp instead (different server)

4. **Windows-MCP** ❌ NOT A SEPARATE TOOL
   - Functionality integrated via desktop-commander

## 📊 Summary Statistics
- **Total MCP Servers Configured**: 13+
- **Confirmed Working**: 12
- **Requires Auth**: 1 (MS-365)
- **Deprecated/Removed**: 4

## 🔧 Usage Notes

### For Workflow Generation:
- Use `mcp__memory__*` for SCS state management
- Use `mcp__brave-search__*` for finding models/LoRAs
- Use `mcp__filesystem__*` or `mcp__desktop-commander__*` for file operations
- Use `mcp__sequential-thinking__*` for complex decision making

### For Browser Automation:
- Prefer `mcp__playwright-mcp__*` for modern web apps
- Use `mcp__puppeteer__*` as alternative
- Both support screenshots for visual verification

### For Development:
- Use `mcp__github__*` for version control
- Use `mcp__npm-search__*` for finding packages
- Use `mcp__sentry__*` for error tracking

## 🔍 Discovery Methods
- `ListMcpResourcesTool` - Shows all available MCP resources
- Direct testing of each tool with simple operations
- Checking server responses for availability

## ⚠️ Important Notes
- Some MCP servers may require authentication (MS-365)
- Some may need specific configuration in Claude settings
- Always test availability before relying on a tool
- Use fallback options when primary tools fail