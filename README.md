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
| `source.version` | LEDE master 的固定提交，首次使用 `80122feac964889bc69b62420cedfefaaf701eb0` |
| `feeds.conf.default` | 用户原始 feeds 配置，保留分支信息供更新时参考 |
| `feeds.lock` | 当前实际使用的 feeds 提交，工作流以此文件拉取依赖 |

首次固定版本用于匹配生成 `.config` 时的源码环境。以后升级源码时同步更新 `source.version`、`feeds.lock` 和 `.config`，避免混用不兼容版本。

## 缓存与日志

清理运行器中不需要的 Android、.NET、GHC 文件，保留 swap。下载目录和 ccache 在相同源码、feeds 和配置间复用，ccache 上限 3 GiB；首次编译没有缓存加速。

通过 make 命令参数 `CONFIG_CCACHE=y` 启用编译缓存，不改写用户 `.config`。不缓存整套工具链和 build_dir，避免复用不兼容的构建状态。

失败时优先下载 `LEDE-buildinfo-运行编号`，查看下载日志、编译日志、空间记录和 `resolved.config`。若配置项被 defconfig 丢弃，工作流会在正式编译前停止并列出变化。

单个 GitHub 托管 Job 最长 6 小时；当前编译步骤最多 300 分钟，为其他步骤预留时间。首次运行若仍然超时，应根据日志再决定拆分工具链构建或使用其他运行器。

产物保留 14 天，请及时下载。当前仅制作固件，不自动发布 Release 或刷写设备。
