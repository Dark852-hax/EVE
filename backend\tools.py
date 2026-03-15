"""
EVE AI Tool System
Tools that give EVE the ability to actually DO things on the computer and web.
"""

import os
import asyncio
import subprocess
import json
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
import bs4

class ToolCategory(Enum):
    """Categories of tools"""
    WEB = "web"
    COMPUTER = "computer"
    CODE = "code"
    SYSTEM = "system"
    UTILITY = "utility"

@dataclass
class ToolResult:
    """Result from tool execution"""
    success: bool
    output: Optional[str] = None
    error: Optional[str] = None
    data: Optional[Any] = None
    tool_name: str = ""
    
    def to_dict(self) -> Dict:
        return {
            'success': self.success,
            'output': self.output,
            'error': self.error,
            'data': self.data,
            'tool_name': self.tool_name
        }

class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str, category: ToolCategory):
        self.name = name
        self.description = description
        self.category = category
        self.enabled = True
    
    async def execute(self, **kwargs) -> ToolResult:
        """Execute the tool"""
        raise NotImplementedError
    
    def validate_params(self, params: Dict, required: List[str]) -> Optional[str]:
        """Validate required parameters"""
        for param in required:
            if param not in params:
                return f"Missing required parameter: {param}"
        return None


class WebSearchTool(BaseTool):
    """Tool for searching the web"""
    
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information",
            category=ToolCategory.WEB
        )
    
    async def execute(self, query: str, num_results: int = 5, **kwargs) -> ToolResult:
        """Search the web"""
        try:
            # Using DuckDuckGo as it's free and doesn't require API key
            url = "https://html.duckduckgo.com/html/"
            data = {
                'q': query,
                'b': str((num_results - 1) * 10)
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data) as response:
                    if response.status != 200:
                        return ToolResult(
                            success=False,
                            error=f"Search failed with status {response.status}",
                            tool_name=self.name
                        )
                    
                    html = await response.text()
                    soup = bs4.BeautifulSoup(html, 'html.parser')
                    
                    results = []
                    for result in soup.select('.result')[:num_results]:
                        title_elem = result.select_one('.result__title')
                        link_elem = result.select_one('.result__url')
                        snippet_elem = result.select_one('.result__snippet')
                        
                        if title_elem:
                            results.append({
                                'title': title_elem.get_text(strip=True),
                                'url': link_elem.get_text(strip=True) if link_elem else '',
                                'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                            })
                    
                    return ToolResult(
                        success=True,
                        output=f"Found {len(results)} results for '{query}'",
                        data=results,
                        tool_name=self.name
                    )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class WebBrowseTool(BaseTool):
    """Tool for browsing websites"""
    
    def __init__(self):
        super().__init__(
            name="web_browse",
            description="Navigate and extract data from websites",
            category=ToolCategory.WEB
        )
    
    async def execute(self, url: str, action: str = "get", selector: str = "", **kwargs) -> ToolResult:
        """Browse a website"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status != 200:
                        return ToolResult(
                            success=False,
                            error=f"Failed to fetch URL: status {response.status}",
                            tool_name=self.name
                        )
                    
                    html = await response.text()
                    
                    if action == "get":
                        # Return basic info
                        return ToolResult(
                            success=True,
                            output=f"Successfully fetched {url}",
                            data={
                                'url': str(response.url),
                                'status': response.status,
                                'content_length': len(html),
                                'html_preview': html[:500] + "..." if len(html) > 500 else html
                            },
                            tool_name=self.name
                        )
                    
                    elif action == "extract" and selector:
                        # Extract specific content
                        soup = bs4.BeautifulSoup(html, 'html.parser')
                        elements = soup.select(selector)
                        
                        extracted = []
                        for elem in elements:
                            extracted.append(elem.get_text(strip=True))
                        
                        return ToolResult(
                            success=True,
                            output=f"Extracted {len(extracted)} elements matching '{selector}'",
                            data=extracted,
                            tool_name=self.name
                        )
                    
                    return ToolResult(
                        success=True,
                        output=f"Fetched {len(html)} bytes from {url}",
                        data={'html_length': len(html)},
                        tool_name=self.name
                    )
                    
        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                error="Request timed out",
                tool_name=self.name
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class FileReadTool(BaseTool):
    """Tool for reading files"""
    
    def __init__(self):
        super().__init__(
            name="file_read",
            description="Read contents of a file",
            category=ToolCategory.COMPUTER
        )
    
    async def execute(self, path: str, encoding: str = "utf-8", lines: int = 0, **kwargs) -> ToolResult:
        """Read a file"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    error=f"File not found: {path}",
                    tool_name=self.name
                )
            
            if not os.path.isfile(path):
                return ToolResult(
                    success=False,
                    error=f"Path is not a file: {path}",
                    tool_name=self.name
                )
            
            with open(path, 'r', encoding=encoding, errors='replace') as f:
                if lines > 0:
                    content = ''.join(f.readlines()[:lines])
                else:
                    content = f.read()
            
            return ToolResult(
                success=True,
                output=f"Successfully read {len(content)} characters from {path}",
                data={'content': content, 'path': path, 'size': os.path.getsize(path)},
                tool_name=self.name
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class FileWriteTool(BaseTool):
    """Tool for writing files"""
    
    def __init__(self):
        super().__init__(
            name="file_write",
            description="Create or modify a file",
            category=ToolCategory.COMPUTER
        )
    
    async def execute(self, path: str, content: str, encoding: str = "utf-8", append: bool = False, **kwargs) -> ToolResult:
        """Write to a file"""
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            mode = 'a' if append else 'w'
            
            with open(path, mode, encoding=encoding) as f:
                f.write(content)
            
            return ToolResult(
                success=True,
                output=f"Successfully wrote {len(content)} characters to {path}",
                data={'path': path, 'bytes_written': len(content.encode(encoding))},
                tool_name=self.name
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class FileListTool(BaseTool):
    """Tool for listing directories"""
    
    def __init__(self):
        super().__init__(
            name="file_list",
            description="List files in a directory",
            category=ToolCategory.COMPUTER
        )
    
    async def execute(self, path: str = ".", pattern: str = "*", recursive: bool = False, **kwargs) -> ToolResult:
        """List files in a directory"""
        try:
            if not os.path.exists(path):
                return ToolResult(
                    success=False,
                    error=f"Path does not exist: {path}",
                    tool_name=self.name
                )
            
            if not os.path.isdir(path):
                return ToolResult(
                    success=False,
                    error=f"Path is not a directory: {path}",
                    tool_name=self.name
                )
            
            import fnmatch
            
            files = []
            dirs = []
            
            if recursive:
                for root, directories, filenames in os.walk(path):
                    for filename in filenames:
                        if fnmatch.fnmatch(filename, pattern):
                            full_path = os.path.join(root, filename)
                            files.append({
                                'name': filename,
                                'path': full_path,
                                'size': os.path.getsize(full_path)
                            })
                    for dirname in directories:
                        if fnmatch.fnmatch(dirname, pattern):
                            dirs.append({
                                'name': dirname,
                                'path': os.path.join(root, dirname)
                            })
            else:
                entries = os.listdir(path)
                for entry in entries:
                    full_path = os.path.join(path, entry)
                    if fnmatch.fnmatch(entry, pattern):
                        if os.path.isfile(full_path):
                            files.append({
                                'name': entry,
                                'path': full_path,
                                'size': os.path.getsize(full_path)
                            })
                        elif os.path.isdir(full_path):
                            dirs.append({
                                'name': entry,
                                'path': full_path
                            })
            
            return ToolResult(
                success=True,
                output=f"Found {len(files)} files and {len(dirs)} directories",
                data={'files': files, 'directories': dirs},
                tool_name=self.name
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class CommandExecuteTool(BaseTool):
    """Tool for executing system commands"""
    
    def __init__(self):
        super().__init__(
            name="execute_command",
            description="Run a terminal command",
            category=ToolCategory.SYSTEM
        )
    
    async def execute(self, command: str, shell: bool = True, timeout: int = 30, cwd: str = "", **kwargs) -> ToolResult:
        """Execute a command"""
        try:
            # Security: whitelist allowed commands or add more validation
            dangerous_patterns = ['rm -rf', 'del /f', 'format', 'mkfs']
            for pattern in dangerous_patterns:
                if pattern.lower() in command.lower():
                    return ToolResult(
                        success=False,
                        error=f"Command blocked for safety: {pattern}",
                        tool_name=self.name
                    )
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd or None
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), 
                    timeout=timeout
                )
                
                output = stdout.decode('utf-8', errors='replace')
                error = stderr.decode('utf-8', errors='replace')
                
                return ToolResult(
                    success=process.returncode == 0,
                    output=output if output else "(no output)",
                    error=error if error else None,
                    data={
                        'returncode': process.returncode,
                        'command': command
                    },
                    tool_name=self.name
                )
                
            except asyncio.TimeoutError:
                process.kill()
                return ToolResult(
                    success=False,
                    error=f"Command timed out after {timeout} seconds",
                    tool_name=self.name
                )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class CodeExecuteTool(BaseTool):
    """Tool for executing code"""
    
    def __init__(self):
        super().__init__(
            name="code_execute",
            description="Run code in a sandbox",
            category=ToolCategory.CODE
        )
    
    async def execute(self, code: str, language: str = "python", **kwargs) -> ToolResult:
        """Execute code"""
        try:
            if language.lower() == "python":
                return await self._execute_python(code)
            elif language.lower() in ["javascript", "js"]:
                return await self._execute_javascript(code)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unsupported language: {language}",
                    tool_name=self.name
                )
                
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )
    
    async def _execute_python(self, code: str) -> ToolResult:
        """Execute Python code"""
        try:
            # Capture output
            output_lines = []
            
            # Create a restricted environment
            import sys
            from io import StringIO
            
            # Save original stdout
            old_stdout = sys.stdout
            
            # Create custom stdout to capture print
            captured_output = StringIO()
            sys.stdout = captured_output
            
            try:
                # Execute the code
                exec(code, {'__builtins__': __builtins__})
            except Exception as e:
                sys.stdout = old_stdout
                return ToolResult(
                    success=False,
                    error=f"Error executing code: {str(e)}",
                    tool_name=self.name
                )
            
            # Get captured output
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            return ToolResult(
                success=True,
                output=output if output else "(no output)",
                data={'language': 'python'},
                tool_name=self.name
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )
    
    async def _execute_javascript(self, code: str) -> ToolResult:
        """Execute JavaScript code (requires Node.js)"""
        try:
            # Write code to temp file
            temp_file = "__temp_js.js"
            with open(temp_file, 'w') as f:
                f.write(code)
            
            process = await asyncio.create_subprocess_exec(
                'node', temp_file,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=30
            )
            
            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass
            
            output = stdout.decode('utf-8', errors='replace')
            error = stderr.decode('utf-8', errors='replace')
            
            return ToolResult(
                success=process.returncode == 0,
                output=output if output else "(no output)",
                error=error if error else None,
                tool_name=self.name
            )
            
        except FileNotFoundError:
            return ToolResult(
                success=False,
                error="Node.js not found. Please install Node.js to run JavaScript.",
                tool_name=self.name
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                tool_name=self.name
            )


class ToolRegistry:
    """Registry of all available tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register all default tools"""
        tools = [
            WebSearchTool(),
            WebBrowseTool(),
            FileReadTool(),
            FileWriteTool(),
            FileListTool(),
            CommandExecuteTool(),
            CodeExecuteTool(),
        ]
        
        for tool in tools:
            self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self, category: Optional[ToolCategory] = None) -> List[Dict]:
        """List all tools, optionally filtered by category"""
        result = []
        for tool in self.tools.values():
            if tool.enabled:
                if category is None or tool.category == category:
                    result.append({
                        'name': tool.name,
                        'description': tool.description,
                        'category': tool.category.value,
                        'enabled': tool.enabled
                    })
        return result
    
    async def execute_tool(self, tool_name: str, **params) -> ToolResult:
        """Execute a tool by name"""
        tool = self.get_tool(tool_name)
        
        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool not found: {tool_name}",
                tool_name=tool_name
            )
        
        if not tool.enabled:
            return ToolResult(
                success=False,
                error=f"Tool is disabled: {tool_name}",
                tool_name=tool_name
            )
        
        return await tool.execute(**params)


# Example usage
async def main():
    """Test the tool system"""
    registry = ToolRegistry()
    
    # List available tools
    print("Available tools:")
    for tool in registry.list_tools():
        print(f"  - {tool['name']} ({tool['category']}): {tool['description']}")
    
    # Test web search
    print("\n--- Testing Web Search ---")
    result = await registry.execute_tool("web_search", query="Python AI assistants")
    print(f"Success: {result.success}")
    print(f"Output: {result.output}")
    if result.data:
        print(f"Results: {json.dumps(result.data[:2], indent=2)}")
    
    # Test file listing
    print("\n--- Testing File List ---")
    result = await registry.execute_tool("file_list", path=".")
    print(f"Success: {result.success}")
    print(f"Output: {result.output}")
    
    # Test code execution
    print("\n--- Testing Code Execution ---")
    result = await registry.execute_tool(
        "code_execute",
        code="print('Hello from EVE!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')",
        language="python"
    )
    print(f"Success: {result.success}")
    print(f"Output: {result.output}")

if __name__ == "__main__":
    asyncio.run(main())
