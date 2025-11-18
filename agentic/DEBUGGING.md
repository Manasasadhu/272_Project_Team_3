# Debugging Guide for Agentic Server

## Setup Complete! 🎉

Your debugging environment is now configured. Here's how to use it:

## How to Debug

### Step 1: Start the Application
```bash
cd /Users/samvedjoshi/Documents/GitHub/272_Project_Team_3/agentic
docker-compose up --build
```

**Important:** The application will wait for the debugger to attach before starting. You'll see a message like:
```
agentic_server  | Waiting for debugger to attach on port 5678...
```

### Step 2: Attach VS Code Debugger

1. Open VS Code in the `agentic` folder
2. Press `F5` or go to **Run and Debug** panel (Cmd+Shift+D)
3. Select **"Python: Attach to Docker"** from the dropdown
4. Click the green play button (▶️)

Once attached, you'll see:
- Debug toolbar at the top of VS Code
- Variables, Watch, Call Stack panels on the left
- The application will continue running

### Step 3: Set Breakpoints

1. Open any file in the `src/` directory
2. Click in the gutter (left of line numbers) to set a red breakpoint dot
3. Recommended places to set breakpoints:
   - `src/api/routes.py` - Line 18: `async def execute_agent(request: ExecuteAgentRequest):`
   - `src/services/agent_orchestrator.py` - Line 43: `async def execute_research_goal(...)`
   - `src/agent/react_agent.py` - Wherever the main execution logic is
   - `src/tools/search_tool.py` - Line 19: `def execute(self, params: Dict[str, Any])`
   - `src/tools/extraction_tool.py` - Line 19: `def execute(self, params: Dict[str, Any])`

### Step 4: Make an API Request

Now run your curl command:
```bash
curl -X POST "http://localhost:8000/api/agent/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "research_goal": "Analyze emerging trends in artificial intelligence and machine learning",
    "scope_parameters": {
      "discovery_depth": "comprehensive",
      "temporal_boundary": {
        "publication_window_years": 2
      },
      "quality_threshold": {
        "impact_level": "high_impact"
      }
    }
  }'
```

### Step 5: Debug Controls

When execution stops at a breakpoint:

- **Continue (F5)**: Resume execution until next breakpoint
- **Step Over (F10)**: Execute current line, don't enter functions
- **Step Into (F11)**: Enter into function calls
- **Step Out (Shift+F11)**: Exit current function
- **Restart (Cmd+Shift+F5)**: Restart debugging session

### Inspect Variables

While paused at a breakpoint:
- Hover over variables to see their values
- Use the **Variables** panel to explore objects
- Use the **Watch** panel to monitor specific expressions
- Use the **Debug Console** to execute Python commands

## Alternative: Run Without Waiting for Debugger

If you want the server to start immediately without waiting:

Edit `Dockerfile` and change:
```dockerfile
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

To:
```dockerfile
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

(Remove `--wait-for-client`)

Then you can attach the debugger at any time, even after the server has started.

## Troubleshooting

### Debugger Won't Attach
- Make sure Docker containers are running: `docker-compose ps`
- Check port 5678 is exposed: `docker port agentic_server`
- Restart containers: `docker-compose restart`

### Breakpoints Not Hitting
- Make sure you're using the correct configuration: "Python: Attach to Docker"
- Check pathMappings in `.vscode/launch.json` are correct
- Verify breakpoints are in the mounted `src/` directory

### Code Changes Not Reflecting
- The `src/` directory is mounted as a volume
- Changes should reflect immediately with `--reload`
- If not, restart: `docker-compose restart agentic_server`

## Tips

1. **Conditional Breakpoints**: Right-click on a breakpoint → Edit Breakpoint → Add condition
2. **Logpoints**: Right-click in gutter → Add Logpoint (logs without stopping)
3. **Exception Breakpoints**: In Debug panel, check "Raised Exceptions" to stop on errors
4. **Multiple Sessions**: You can debug multiple requests simultaneously

## What's Been Configured

✅ Docker container exposes debugpy on port 5678  
✅ VS Code launch configuration for remote debugging  
✅ Source code is mounted for live reloading  
✅ Path mappings configured for local ↔ container paths  
✅ debugpy installed in container

Happy Debugging! 🐛🔍
