#!/usr/bin/env bash
# 在 LEDE 构建目录运行，补回上游迁移到 QWRT 后缺失的两个包。
set -euo pipefail

restore_package() {
  local feed=$1 package=$2 revision=$3
  if [[ -f "feeds/$feed/$package/Makefile" ]]; then
    echo "$feed/$package 已存在，使用当前版本。"
    return
  fi

  # shortcut: 仅缺失目录使用迁移前版本，上游恢复或 LEDE 接入替代包后移除此补丁。
  git -C "feeds/$feed" fetch --depth 1 origin "$revision"
  git -C "feeds/$feed" restore --source="$revision" --staged --worktree -- "$package"
  test -f "feeds/$feed/$package/Makefile"
  echo "$feed/$package restored-from=$revision"
}

restore_package luci modules/luci-mod-network e881fed794a36dd18f282a4e227b7a1ced5679e5
restore_package packages utils/hwdata bdb45ca0f4b1cb38605098021012967425dcf95d
