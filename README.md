# Ghost 的 LEDE 云编译

使用 GitHub Actions 编译 x86_64 固件，源码来自 [coolsnowwolf/lede](https://github.com/coolsnowwolf/lede)。

## 开始编译

1. 打开仓库的 **Actions**。
2. 选择 **编译 LEDE x86_64**。
3. 点击 **Run workflow**，选择 `main`，再次点击运行。
4. 成功后在运行详情的 **Artifacts** 下载 `LEDE-x86_64-运行编号`。

仅手动触发，不会因为修改文件自动启动编译，不会定时反复编译。

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

清理运行器中不需要的 Android、.NET、GHC、CodeQL 文件和 Docker 镜像，保留 swap，并记录磁盘容量、inode 和目录占用。下载目录和 ccache 根据实际拉取的源码、feeds 提交及配置生成缓存键，仅在版本一致时复用；ccache 上限 3 GiB。上游版本变化后可能没有缓存加速。

通过 make 命令参数 `CONFIG_CCACHE=y` 启用编译缓存，不改写用户 `.config`。不缓存整套工具链和 build_dir，避免复用不兼容的构建状态。

失败时优先下载 `LEDE-buildinfo-运行编号`，查看下载日志、编译日志、空间记录和 `resolved.config`。若配置项被 defconfig 丢弃，工作流会在正式编译前停止并列出变化。

单个 GitHub 托管 Job 最长 6 小时；当前编译步骤最多 300 分钟，为其他步骤预留时间。首次运行若仍然超时，应根据日志再决定拆分工具链构建或使用其他运行器。

产物保留 14 天，请及时下载。当前仅制作固件，不自动发布 Release 或刷写设备。
