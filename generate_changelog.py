import subprocess
import re

log = subprocess.check_output(['git', 'log', '-p', 'config.yaml']).decode('utf-8')
commits = log.split('commit ')[1:]

version_map = {}
for c in commits:
    lines = c.split('\n')
    commit_hash = lines[0].strip()
    for line in lines:
        if line.startswith('+version:'):
            match = re.search(r'\+version:\s*"([^"]+)"', line)
            if match and "localdev" not in match.group(1).lower():
                version_map[commit_hash] = match.group(1)
        elif line.startswith('+  version:'): # just in case
            match = re.search(r'\+  version:\s*"([^"]+)"', line)
            if match and "localdev" not in match.group(1).lower():
                version_map[commit_hash] = match.group(1)

log_output = subprocess.check_output(['git', 'log', '--date=short', '--format=%H|%s']).decode('utf-8').strip().split('\n')

changelog = ["# Changelog\n", "All notable changes to the Antigravity CLI Home Assistant Add-on will be documented in this file.\n"]
current_version = "1.7.7"
commits_in_version = []

for entry in log_output:
    if not entry: continue
    parts = entry.split('|', 1)
    if len(parts) != 2: continue
    commit_hash, msg = parts
    
    if commit_hash in version_map:
        if commits_in_version:
            changelog.append(f"## [{current_version}]")
            for c in commits_in_version:
                changelog.append(f"- {c}")
            changelog.append("")
            commits_in_version = []
        current_version = version_map[commit_hash]
    
    commits_in_version.append(msg)

if commits_in_version:
    changelog.append(f"## [{current_version}]")
    for c in commits_in_version:
        changelog.append(f"- {c}")

with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(changelog))
