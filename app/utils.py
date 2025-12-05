#file for utility functions
from app.models import GameServer, RconConfig, ServerInfo
from app import db
from datetime import datetime, timezone
import time

import os
from pathlib import Path
import re
import shutil
import subprocess
import platform

from typing import List

# Leave empty to use PATH Var.
#DEFAULT_JAVA_PATH = r"C:\Program Files\Microsoft\jdk-11.0.16.101-hotspot\bin\java.exe"
DEFAULT_JAVA_PATH = r"C:\Program Files\Java\jdk-21\bin\java.exe"
# Root folder for all Minecraft servers
MINECRAFT_SERVERS_ROOT = Path(r"C:\GameServers\Minecraft")

# Folder where minecraft server jars live
TEMPLATES_ROOT = Path(r"C:\GameServers\templates")

# Path to the "latest vanilla" jar template (maybe have it download from the panel
# in the future because that would be convenient)
MINECRAFT_LATEST_JAR = TEMPLATES_ROOT / "minecraft_server_latest.jar"

RUNNING_PROCESSES = {} # track processes
#
#
#
#

DEFAULT_COMMANDS = {
    "Minecraft (Java Edition)": {
        "broadcast":    "/say {message}",
        "list_players": "/list",
        "kick":         "/kick {player}",
        "ban":          "/ban {player}",
        "unban":        "/pardon {player}",
        "save":         "/save-all"
    },
    "ARK: Survival Evolved": {
        "broadcast":    "ServerChat {message}",
        "list_players": "ListPlayers",
        "kick":         "KickPlayer {steamid}",
        "ban":          "BanPlayer {steamid}",
        "unban":        "UnbanPlayer {steamid}",
        "save":         "SaveWorld"
    },
    "Rust":{
        "broadcast":    "say {message}",
        "list_players": "playerlist",
        "kick":         "kick {player}",
        "ban":          "ban {player}",
        "unban":        "unban {player}",
        "save":         "server.save"
    },
    "Counter-Strike: Global Offensive": {
        "broadcast":    "say {message}",
        "list_players": "status",
        "kick":         "kick {player}",
        "ban":          "banid {steamid}",
        "unban":        "removeid {steamid}",
        "save":         "host_writeconfig"
    },
    "Factorio": {
        "broadcast":    "/c game.print(\"{message}\")",
        "list_players": "/c for _, player in pairs(game.connected_players) do game.print(player.name) end",
        "kick":         "/c game.players[\"{player}\"].ban(\"You have been kicked\")",
        "ban":          "/c game.players[\"{player}\"].ban(\"Banned\")",
        "unban":        "/c game.players[\"{player}\"].unban()",
        "save":         "/c game.server_save()"
    },
    # more games/commands to be added later?
}


#
#
#
#
#
#
# later have the option to select server version
def provision_minecraft_server(server: GameServer):
    """
    Given a GameServer row (with an id), create its folder and basic files
    for a Minecraft (Java Edition) server. It is called 'minecraft' for the table.
    """
    if server.game_type != "minecraft":
        return

    if not server.id:
        raise ValueError("Server must have an ID before provisioning")

    # Install path C:\GameServers\Minecraft\<safe-name>_<id>
    install_path_str = build_minecraft_install_path(server.name, server.id)
    server.install_path = install_path_str

    install_path = Path(install_path_str)
    install_path.mkdir(parents=True, exist_ok=True)

    # copy template jar as server.jar
    if not MINECRAFT_LATEST_JAR.exists():
        raise FileNotFoundError(
            f"Minecraft template jar not found at {MINECRAFT_LATEST_JAR}"
        )

    target_jar = install_path / "server.jar"
    if not target_jar.exists():
        shutil.copy2(MINECRAFT_LATEST_JAR, target_jar)

    # Accept EULA automatically
    # might not have this later
    eula_path = install_path / "eula.txt"
    if not eula_path.exists():
        eula_path.write_text("eula=true\n", encoding="utf-8")

    # Minimal server.properties, Minecraft generate the rest
    # this should be from the frontend later, here for now until entires can be
    # figured out.
    props_path = install_path / "server.properties"
    if not props_path.exists():
        port = server.server_port or 25565 # default
        max_players = server.max_players or 20 # default (player count is broken again)
        lines = [
            f"server-port={port}",
            f"max-players={max_players}",
        ]
        props_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def provision_server_files(server: GameServer):
    """
    Provisioning based on game_type.
    currently only matches any game_type that looks like Minecraft.
    """
    print(f"[provision] game_type={server.game_type!r}", flush=True)

    if server.game_type and "minecraft" in server.game_type.lower():
        provision_minecraft_server(server)
        print(f"[provision] install_path set to {server.install_path}", flush=True)
    # future: elif "ark" in server.game_type.lower():
    # planning on additional games


#
#
#
#



def _get_java_path(rcon_config: RconConfig) -> str:
    """
    Decide which 'java' runtime env to run.
    Priority:
      1) Per-server rcon_config.java_path (if set and exists)
      2) DEFAULT_JAVA_PATH (if set and exists)
      3) 'java' found on PATH via shutil.which
    Raises a clear error if nothing is found.
    """
    # 1 Per-server override from DB
    if rcon_config and rcon_config.java_path:
        jp = rcon_config.java_path.strip()
        if jp:
            if Path(jp).exists():
                return jp
            else:
                print(f"[java] Configured java_path '{jp}' does not exist, falling back...", flush=True)

    # 2 Global default in code (optional)
    if DEFAULT_JAVA_PATH:
        if Path(DEFAULT_JAVA_PATH).exists():
            return DEFAULT_JAVA_PATH
        else:
            print(f"[java] DEFAULT_JAVA_PATH '{DEFAULT_JAVA_PATH}' does not exist, falling back...", flush=True)

    # 3 Auto-detect from PATH
    found = shutil.which("java")
    if found:
        print(f"[java] Using java from PATH: {found}", flush=True)
        return found

    # shouldnt get here, there is no usable java if we do
    raise RuntimeError(
        "Java executable not found. "
        "Either add it to PATH, set DEFAULT_JAVA_PATH in utils.py, "
        "or set a valid java_path for this server."
        # can tune this error message
    )




def _get_java_args(rcon_config: RconConfig) -> list:
    """
    Split the java_args string into a list.
    Example: '-Xms2G -Xmx4G' -> ['-Xms2G', '-Xmx4G']
    """
    if not rcon_config or not rcon_config.java_args:
        return []

    args = rcon_config.java_args.strip()
    if not args:
        return []

    # only works for regular splitting, not quotes
    return args.split()



#
#
#
#
#
#




def start_minecraft_process(server_id: int) -> subprocess.Popen:
    """
    Start a Minecraft server process for the given GameServer id.
    Does NOT update DB status, just launches the process.
    """
    server = GameServer.query.get(server_id)
    if server is None:
        raise ValueError(f"Server with id {server_id} not found")

    if not server.install_path:
        raise ValueError(f"Server {server_id} has no install_path set")

    # If there is already have a running process, don't start another
    existing = RUNNING_PROCESSES.get(server_id)
    if existing is not None and existing.poll() is None:
        print(f"[process] Server {server_id} already running (pid={existing.pid})", flush=True)
        return existing
    else:
        RUNNING_PROCESSES.pop(server_id, None)

    rcon_cfg = server.rcon_config
    if rcon_cfg is None:
        raise ValueError(f"Server {server_id} has no RconConfig")

    java = _get_java_path(rcon_cfg)
    java_args = _get_java_args(rcon_cfg)

    jar_path = Path(server.install_path) / "server.jar"
    if not jar_path.exists():
        raise FileNotFoundError(f"server.jar not found at {jar_path}")

    cmd = [java] + java_args + ["-jar", str(jar_path), "nogui"]
    print(f"[process] Starting server {server_id} with command: {' '.join(cmd)}", flush=True)

    # On Windows, suppress opening a new console window (CLI doesn't appear)
    # creationflags = 0
    # if platform.system() == "Windows":
    #     creationflags = 0x08000000  # CREATE_NO_WINDOW

    proc = subprocess.Popen(
        cmd,
        cwd=server.install_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
        #creationflags=creationflags # uncomment later for window to not show up
    )

    RUNNING_PROCESSES[server_id] = proc

    print(f"[process] Server {server_id} started (pid={proc.pid})", flush=True)

    def read_stdout():
        for line in proc.stdout:
            print(f"[server {server_id}] {line}", end="")

    import threading
    t = threading.Thread(target=read_stdout, daemon=True)
    t.start()


    return proc



# *************************************************************

def stop_minecraft_process(server_id: int, timeout: float = 30.0) -> bool:
    """
    Try to stop the Minecraft server gracefully by sending 'stop' to stdin.
    Returns True if the process is gone, or was already gone, False on timeout.
    """
    proc = RUNNING_PROCESSES.get(server_id)

    # If there isn't a known/running process, assume it's already stopped
    if proc is None:
        print(f"[process] No tracked process for server {server_id}", flush=True)
        return True

    # If process already exited, clean up and report success
    if proc.poll() is not None:
        print(f"[process] Process for server {server_id} already exited", flush=True)
        RUNNING_PROCESSES.pop(server_id, None)
        return True

    # Try to send 'stop' to stdin
    try:
        if proc.stdin:
            proc.stdin.write("stop\n")
            proc.stdin.flush()
            print(f"[process] Sent 'stop' to server {server_id}", flush=True)
    except Exception as e:
        print(f"[process] Failed to send 'stop' to server {server_id}: {e}", flush=True)

    # Wait for graceful shutdown
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"[process] Server {server_id} did not stop within {timeout} seconds", flush=True)
        return False

    print(f"[process] Server {server_id} stopped gracefully", flush=True)
    RUNNING_PROCESSES.pop(server_id, None)
    return True

#
#
#
#
#
#

"""
NOT YET IMPLEMENTED ANYWHERE, BUT WILL BE ADDED IN FRONTEND LOGIN LATER
"""
def kill_minecraft_process(server_id: int) -> bool:
    """
    Force kill the Minecraft process for the given server. (MAYBE OTHER GAMES LATER)
    Returns True if a process was killed or already gone, False if none was found.
    """
    proc = RUNNING_PROCESSES.get(server_id)

    if proc is None:
        print(f"[process] No tracked process to kill for server {server_id}", flush=True)
        return False

    try:
        if proc.poll() is None:
            print(f"[process] Killing server {server_id} (pid={proc.pid})", flush=True)
            proc.kill()
        else:
            print(f"[process] Process for server {server_id} already exited", flush=True)
    finally:
        RUNNING_PROCESSES.pop(server_id, None)

    return True

#
#
#
#
#
#

def create_new_server(data):
    print(data)
    new_server = GameServer(
        name                = data.get("name"),
        game_type           = data.get("game_type"),
        status              = data.get("status", "Offline"),
        max_players         = int(data.get("extras", {}).get("maxPlayers", 0)),
        server_port         = data.get("server_port"),
        install_path        = "", # backend handles this currently
        archive_path        = data.get("archive_path", None),
        backup_path         = data.get("back_up_path", None),
    )
    return new_server

def create_new_server_rcon_config(data):
    # Default JVM args for now
    default_java_args = "-Xms1G -Xmx2G"

    new_rcon = RconConfig(
        server_host_name    = data.get("server_host_name"),
        rcon_host           = data.get("rcon_host"),
        rcon_user           = data.get("rcon_user"),
        rcon_pass_hash      = data.get("rcon_pass_hash"),
        rcon_port           = data.get("rcon_port"),
        java_path           = (data.get("java_path") or "").strip(), # frontend hardcoded currently (change at will)
        steam_cmd_path      = data.get("steam_cmd_path"),
        java_args           = data.get("java_args", default_java_args), # new for server "-" args
    )
    return new_rcon


def create_new_server_info(data):
    new_info = ServerInfo(
        notes       = data.get("notes", "No notes at this time."),
    )
    return new_info

def start_server(server_id):
    """
    High-level start server handler used by the API.
    Marks status, launches the process for supported games (currently only minecraft),
    and records started_at on success (transition states).
    """
    server = GameServer.query.get(server_id)
    if not server:
        print(f"[start_server] Server {server_id} not found", flush=True)
        return

    # Mark as starting, reflects on FE UI
    server.status = "Starting"
    db.session.commit()

    try:
        game = (server.game_type or "").lower()

        # For now, only Minecraft gets a real process (future later)
        if "minecraft" in game:
            start_minecraft_process(server_id)
        else:
            print(f"[start_server] Game type {server.game_type!r} not yet supported for process launch", flush=True)

        # If here without exception, server Online
        if server.server_info is not None:
            server.server_info.started_at = datetime.now(timezone.utc)
            print(f"SERVER STARTED SUCCESSFULLY AT {server.server_info.started_at}", flush=True)
        server.status = "Online"
        db.session.commit()
        print(f"[start_server] Server {server_id} marked Online", flush=True)

    except Exception as e:
        # Something went wrong starting the server
        db.session.rollback()
        import traceback
        print(f"[start_server] Error starting server {server_id}: {e}", flush=True)
        traceback.print_exc()

        # Mark the server as Error
        server = GameServer.query.get(server_id)
        if server:
            server.status = "Offline" # in enum
            db.session.add(server)
            db.session.commit()


def stop_server(server_id):
    """
    High-level stop server handler used by the API.
    Tries to stop and updates status/stopped_at.
    """
    server = GameServer.query.get(server_id)
    if not server:
        print(f"[stop_server] Server {server_id} not found", flush=True)
        return

    server.status = "Stopping"
    db.session.commit()

    try:
        game = (server.game_type or "").lower()
        stopped_ok = True

        if "minecraft" in game:
            stopped_ok = stop_minecraft_process(server_id)

        if stopped_ok:
            if server.server_info is not None:
                server.server_info.stopped_at = datetime.now(timezone.utc)
            server.status = "Offline"
            server.active_players = ""
            print(f"[stop_server] Server {server_id} stopped and marked Offline", flush=True)
        else:
            # server timed out or failed
            server.status = "Online"
            print(f"[stop_server] Server {server_id} did not stop cleanly; leaving status Online", flush=True)

        db.session.commit()

    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"[stop_server] Error stopping server {server_id}: {e}", flush=True)
        traceback.print_exc()


def restart_server(server_id):
    """
    Simple restart: stop then start using the high-level helpers.
    """
    stop_server(server_id)
    start_server(server_id)


def update_server(server_id):
    server = GameServer.query.get(server_id)
    server.status = "Updating"
    # code for updating the server
    db.session.commit()

#
#
#
#

def ensure_base_dirs():
    """
    Folder check, make sure folders exist (will create them if not)
    """
    for path in (MINECRAFT_SERVERS_ROOT, TEMPLATES_ROOT):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # print now, log later
            print(f"[WARN] Failed to ensure directory {path}: {e}", flush=True)


def slugify_name(name: str) -> str:
    """
    Turn a server name into a filesystem-safe 'slug':
    'My Server!!' == 'my-server'
    """
    if not name:
        return "server"

    slug = name.lower()
    # Replace any sequence of non-alphanumeric characters with a dash
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Strip any leading/trailing dashes
    slug = slug.strip("-")
    return slug or "server"


def build_minecraft_install_path(name: str, server_id: int) -> str:
    """
    Build a full install path (example of how it is formatted below)
    C:\\GameServers\\Minecraft\\my-cool-server_3
    """
    safe_name = slugify_name(name)
    folder_name = f"{safe_name}_{server_id}"
    full_path = MINECRAFT_SERVERS_ROOT / folder_name
    return str(full_path)


#
#
#
#
#

"""
GET LOGS HELPERS FOR MINECRAFT SERVERS ONLY FOR GETTING THE LATEST.LOG TEXTS FILES
"""

def get_latest_log_path_for_server(server: GameServer) -> Path:
    """
    Return the expected path to latest.log for "this" server.
    "this" pertains to the ID at which the server is at
    """
    if not server.install_path:
        raise ValueError(f"Server {server.id} has no install_path set")

    base = Path(server.install_path)
    logs_dir = base / "logs"
    return logs_dir / "latest.log"

# ----------

def read_latest_log_lines(server: GameServer, max_lines: int = 200) -> List[str]:
    """
    Read up to `max_lines` from the end of latest.log for a server.
    Returns a list of lines without trailing newlines.
    """
    log_path = get_latest_log_path_for_server(server)

    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found at {log_path}")

    # read the whole file, then tail it
    with log_path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    # strip trailing newlines and only keep the tail
    return [line.rstrip("\r\n") for line in lines[-max_lines:]]