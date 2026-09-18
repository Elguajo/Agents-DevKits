#!/usr/bin/env bash
set -euo pipefail

adopt_existing=false
copy_codex=false
linked_count=0
copied_count=0
migrated_count=0
already_linked_count=0
skipped_count=0
removed_stale_count=0
backed_up_count=0

while (($#)); do
  case "$1" in
    --adopt) adopt_existing=true ;;
    --copy-codex) copy_codex=true ;;
    *)
      echo "Usage: $0 [--adopt] [--copy-codex]" >&2
      exit 2
      ;;
  esac
  shift
done

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
source_root="$repo_root/skills"
backup_root="${HOME}/.agent-skills-backups/$(date +%Y%m%d-%H%M%S)"

for target_root in "${HOME}/.codex/skills" "${HOME}/.claude/skills"; do
  runtime="$(basename "$(dirname "$target_root")")"
  copy_to_target=false
  if [[ "$runtime" == ".codex" && "$copy_codex" == true ]]; then
    copy_to_target=true
  fi
  mkdir -p "$target_root"

  # Remove only broken symlinks previously managed by this repository.
  # This makes skill renames safe without touching unrelated local skills.
  for existing_link in "$target_root"/*; do
    [[ -L "$existing_link" ]] || continue
    link_target="$(readlink "$existing_link")"
    if [[ "$link_target" == "$source_root/"* && ! -e "$existing_link" ]]; then
      rm "$existing_link"
      removed_stale_count=$((removed_stale_count + 1))
      echo "Removed stale managed link: $existing_link"
    fi
  done

  for source_skill in "$source_root"/*; do
    [[ -d "$source_skill" && -f "$source_skill/SKILL.md" ]] || continue

    skill_name="$(basename "$source_skill")"
    target_skill="$target_root/$skill_name"

    if [[ -L "$target_skill" && "$(readlink "$target_skill")" == "$source_skill" && "$copy_to_target" != true ]]; then
      already_linked_count=$((already_linked_count + 1))
      echo "Already linked: $runtime/$skill_name"
      continue
    fi

    # A managed Codex link can be converted without --adopt: it is known to
    # belong to this repository, and the prior link is retained in the backup.
    if [[ -L "$target_skill" && "$(readlink "$target_skill")" == "$source_skill" && "$copy_to_target" == true ]]; then
      backup_skill="$backup_root/$runtime/$skill_name"
      mkdir -p "$(dirname "$backup_skill")"
      mv "$target_skill" "$backup_skill"
      cp -a "$source_skill" "$target_skill"
      copied_count=$((copied_count + 1))
      migrated_count=$((migrated_count + 1))
      echo "Copied Codex skill (migrated managed link): $runtime/$skill_name"
      continue
    fi

    if [[ -e "$target_skill" || -L "$target_skill" ]]; then
      if [[ "$adopt_existing" != true ]]; then
        skipped_count=$((skipped_count + 1))
        echo "Skipped existing skill: $target_skill (run with --adopt to replace it safely)" >&2
        continue
      fi

      backup_skill="$backup_root/$runtime/$skill_name"
      mkdir -p "$(dirname "$backup_skill")"
      mv "$target_skill" "$backup_skill"
      backed_up_count=$((backed_up_count + 1))
      echo "Backed up: $target_skill -> $backup_skill"
    fi

    if [[ "$copy_to_target" == true ]]; then
      cp -a "$source_skill" "$target_skill"
      copied_count=$((copied_count + 1))
      echo "Copied Codex skill: $runtime/$skill_name"
    else
      ln -s "$source_skill" "$target_skill"
      linked_count=$((linked_count + 1))
      echo "Linked: $runtime/$skill_name"
    fi
  done
done

echo "Installation summary: linked=$linked_count copied=$copied_count migrated=$migrated_count already-linked=$already_linked_count skipped=$skipped_count backed-up=$backed_up_count stale-links-removed=$removed_stale_count"
