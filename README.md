# Ghost 的 LEDE 云编译

使用 GitHub Actions 编译 x86_64 固件，源码来自 [coolsnowwolf/lede](https://github.com/coolsnowwolf/lede)。

## 开始编译

1. 打开仓库的 **Actions**。
2. 选择 **编译 LEDE x86_64**。
3. 点击 **Run workflow**，选择 `main`，再次点击运行。
4. 成功后在运行详情的 **Artifacts** 下载 `LEDE-x86_64-运行编号`。

每周日北京时间 03:00 自动编译（UTC 周六 19:00），同时保留手动触发；修改文件不会立即启动编译。定时任务使用默认分支的最新工作流及配置。

GitHub 定时任务可能延迟；公开仓库连续 60 天没有活动时，定时工作流会自动停用，届时需在 Actions 中重新启用。

## 当前配置

- 目标：x86_64 Generic。
- 启动：UEFI；当前未启用传统 BIOS 镜像。
- 根文件系统：SquashFS。
- 镜像：压缩磁盘镜像、QCOW2（PVE/KVM）、VMDK（VMware）。
- 内核分区 256 MiB，根文件系统分区 512 MiB。
- `.config` 保留用户选择，具体应用及驱动以该文件为准。
- 保留 PassWall 的额外 feeds 以及用户原来的 feeds 配置顺序。

## 配置文件

| 文件 | 用途 |
| --- | --- |
| `.config` | 从用户已完成选择的配置复制，云端执行 defconfig 后检查选择是否丢失 |
| `feeds.conf.default` | 每次编译按此文件拉取各 feeds 分支的最新提交 |

每次编译拉取 LEDE `master` 最新提交。两个 PassWall feeds 跟随 `main`，LuCI 跟随 `openwrt-25.12`，其余未指定分支的 feeds 跟随各仓库默认分支。仓库中的 `.config` 保持原样，在构建目录内执行 `defconfig` 并检查所选配置是否变化。

实际拉取的源码提交和 feeds 版本记录在日志产物的 `buildinfo/source.version` 和 `buildinfo/feeds.lock` 中，不再从仓库读取固定版本。跟随上游不代表所有软件都是作者发布的最新版本；上游变更可能导致配置检查或编译失败。

## 缓存与日志

借鉴 kenzok8 的 Lean 工作流，使用 `ubuntu-latest`，清理 Android、.NET、GHC、大型预装软件、CodeQL 和 Docker 镜像，并按用户选择禁用 swap、删除 `/mnt/swapfile`。这会增加可用磁盘空间，也会降低内存不足时的缓冲能力。

将 `dl`、`bin`、`staging_dir` 放在 `/mnt/openwrt` 下，通过软链接连接源码目录；是否增加可用容量取决于运行器的实际挂载布局。记录 `/`、`/mnt` 和工作区的磁盘容量、inode，以及源码和 `/mnt/openwrt` 的目录占用。

feeds 分两步更新后安装，保留用户原 feeds 来源，不套用他人的插件替换和 `.config`。下载并发为 CPU 核数加 1，随后清理小于 1 KiB 的下载文件；如误删有效小文件，编译时可能重新下载。

下载完成后通过 `stupidloud/cachewrtbuild` 恢复工具链和 ccache，任务成功后由 Action 自动保存。缓存键包含实际 Ubuntu 版本、用户配置和 Action 计算的工具链提交；浅克隆下上游提交变化可能导致缓存未命中。保留 Make 依赖检查，不采用缓存命中后修改 Makefile 强制跳过工具链的做法。不再使用原下载目录缓存。

通过 make 命令参数 `CONFIG_CCACHE=y` 启用编译缓存，ccache 上限 3 GiB，不改写用户 `.config`。第三方清理和缓存 Action 固定为已检查的提交。空间检查保留只读诊断，不复制依赖未定义 `MTARGET` 的构建目录删除代码。

失败时优先下载 `LEDE-buildinfo-运行编号`，查看下载日志、编译日志、空间记录和 `resolved.config`。若配置项被 defconfig 丢弃，工作流会在正式编译前停止并列出变化。

单个 GitHub 托管 Job 最长 6 小时；当前编译步骤最多 300 分钟，为其他步骤预留时间。首次运行若仍然超时，应根据日志再决定拆分工具链构建或使用其他运行器。

产物保留 14 天，请及时下载。当前仅制作固件，不自动发布 Release 或刷写设备。
