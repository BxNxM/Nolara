import os
import shutil
from pathlib import Path


NOLARA_USER_CONFIG = Path.home() / ".nolara"


def get_symlink_targets():
    """
    Returns a dictionary of {user-facing link path: project source path},
    using the directory of this file (not installed package location).
    """
    # Get directory where this script resides
    project_root = Path(__file__).parent.resolve()

    user_configs = project_root / "configuration"
    system_prompts_dir = project_root / "lib" / "system_prompts"
    agent_tools_dir = project_root / "lib" / "tools"

    return {
        NOLARA_USER_CONFIG / "configs": user_configs,
        NOLARA_USER_CONFIG / "system_prompts": system_prompts_dir,
        NOLARA_USER_CONFIG / "tools": agent_tools_dir,
    }


def ensure_directory(path: Path):
    """Ensure a directory exists"""
    path.mkdir(parents=True, exist_ok=True)


def is_symlink_correct(link: Path, target: Path) -> bool:
    """Return True if the link exists and points to the correct target"""
    return link.is_symlink() and link.resolve() == target.resolve()


def ensure_symlink(link: Path, target: Path):
    """Ensure a single symlink is correct, fixing or creating it if needed"""
    try:
        if link.exists() or link.is_symlink():
            # Remove incorrect or broken link/folder/file
            if not is_symlink_correct(link, target):
                if link.is_symlink() or link.is_file():
                    link.unlink()
                else:
                    shutil.rmtree(link)
        if not link.exists():
            link.symlink_to(target, target_is_directory=target.is_dir())
            print(f"[nolara] Linked: {link} → {target}")
        else:
            print(f"[nolara] Valid link exists: {link}")
    except Exception as e:
        print(f"[nolara] Failed to ensure link {link} → {target}: {e}")


def setup_nolara_user_config_links():
    """Main function to set up ~/.nolara and symlinks"""
    print(f"USER CONFIG: {NOLARA_USER_CONFIG}")

    ensure_directory(NOLARA_USER_CONFIG)
    links = get_symlink_targets()
    for link, target in links.items():
        ensure_symlink(link, target)


