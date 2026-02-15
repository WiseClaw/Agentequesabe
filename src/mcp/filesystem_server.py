import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WiseClaw Filesystem")

@mcp.tool()
def list_directory(path: str = ".") -> list:
    """Lista o conteúdo de uma diretoria."""
    try:
        return os.listdir(path)
    except Exception as e:
        return [str(e)]

@mcp.tool()
def read_file(path: str) -> str:
    """Lê o conteúdo de um ficheiro."""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Escreve conteúdo num ficheiro."""
    try:
        with open(path, 'w') as f:
            f.write(content)
        return f"File {path} written successfully."
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    mcp.run()
