import os
import httpx
from dotenv import load_dotenv

load_dotenv()

ALLOWED_EXTENSIONS = {
    # Programming languages
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".php",
    ".rb",
    ".swift",
    ".kt",

    # Web
    ".html",
    ".css",
    ".scss",

    # Database
    ".sql",

    # Configuration
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env.example",

    # Documentation
    ".md",
    ".rst",
    ".txt",

    # Infrastructure / DevOps
    ".sh",
    ".bash",
    ".dockerfile",
    ".tf",
    ".hcl",
    ".xml",
}


ALLOWED_FILENAMES = {
    # Build and development
    "Dockerfile",
    "Dockerfile.dev",
    "Dockerfile.prod",
    "Makefile",
    "Procfile",
    "Justfile",

    # Git
    ".gitignore",
    ".gitattributes",
    ".gitmodules",

    # Docker
    ".dockerignore",
    "docker-compose.yml",
    "docker-compose.yaml",

    # Project configuration
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "Pipfile",
    "Pipfile.lock",
    "uv.lock",
    "package.json",
    "package-lock.json",
    "tsconfig.json",

    # Documentation
    "README",
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "CHANGELOG.md",

    # Tool configuration
    ".editorconfig",
    ".pre-commit-config.yaml",
    ".python-version",
    ".nvmrc",
    ".node-version",
}
async def fetch_data(REPOSITORY_NAME: str) -> dict:



    github_token = os.environ.get("GITHUB_TOKEN")

    if not github_token:
        raise ValueError("GITHUB_TOKEN is missing")

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
    }

    base_url = f"https://api.github.com/repos/AnshuSAHA176/{REPOSITORY_NAME}"

    async with httpx.AsyncClient(timeout=15) as client:

        response = await client.get(base_url, headers=headers)
        response.raise_for_status()
        metadata = response.json()

        commit_response = await client.get(
            f"{base_url}/commits/{metadata['default_branch']}",
            headers=headers,
        )
        commit_response.raise_for_status()

        commit_data = commit_response.json()

        commit_sha = commit_data["sha"]
        tree_sha = commit_data["commit"]["tree"]["sha"]

        tree_response = await client.get(
            f"{base_url}/git/trees/{tree_sha}",
            params={"recursive": "1"},
            headers=headers,
        )
        tree_response.raise_for_status()

        tree_data = tree_response.json()

        if tree_data["truncated"]:
            raise ValueError("Repository tree response is truncated")

        files = [
            item for item in tree_data["tree"]
            if item["type"] == "blob"
        ]

    return {
        "meta_data": metadata,
        "latest_commit": commit_sha,
        "tree_sha": tree_sha,
        "files": files,
    }


from pathlib import PurePosixPath

def filter_repository_files(files: list[dict]) -> list[dict]:
    filtered_files = [
        file for file in files
        if PurePosixPath(file["path"]).suffix.lower() in ALLOWED_EXTENSIONS
        or PurePosixPath(file["path"]).name in ALLOWED_FILENAMES
    ]
    print(len(filtered_files))
    return filtered_files