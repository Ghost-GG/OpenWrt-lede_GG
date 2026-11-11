# Ghost 的 LEDE 云编译

使用 GitHub Actions 编译 x86_64 固件，源码来自 [coolsnowwolf/lede](https://github.com/coolsnowwolf/lede)。每周日北京时间 03:00 自动编译，也可以在 Actions 页面手动运行。

## 编译与下载

1. 打开仓库的 [Actions](https://github.com/Ghost-GG/OpenWrt-lede_GG/actions)。
2. 选择“编译 LEDE x86_64”，点击“Run workflow”。
3. 选择 `main` 分支，再次点击运行。
4. 编译成功后，在运行详情的 Artifacts 中下载 `LEDE-x86_64-运行编号`。

固件和日志保留 14 天。仓库只生成编译产物，不自动发布 Release 或刷写设备。

定时任务使用默认分支的最新工作流和配置，运行时间为北京时间周日 03:00（UTC 周六 19:00）。修改仓库文件不会立即触发编译。GitHub 调度可能延迟；公开仓库连续 60 天没有活动时，定时工作流会自动停用，需要到 Actions 页面重新启用。

## 固件配置

| 项目 | 当前选择 |
| --- | --- |
| 目标平台 | x86_64 Generic |
| 启动方式 | UEFI，未启用传统 BIOS 镜像 |
| 根文件系统 | SquashFS |
| 镜像格式 | 压缩磁盘镜像、QCOW2（PVE/KVM）、VMDK（VMware） |
| 分区大小 | 内核分区 256 MiB，根文件系统分区 512 MiB |
| 配置来源 | 仓库中的 `.config` |

## LuCI 应用

当前 `.config` 选中了以下 23 个 LuCI 应用，均为 `=y`，计划编入固件。最终安装的软件包以对应构建产物中的 `.manifest` 为准；编入固件不代表服务已启用或配置完成。

| 软件包 | 名称 | 用途 |
| --- | --- | --- |
| `luci-app-argon-config` | Argon 主题设置 | 调整 Argon 主题外观 |
| `luci-app-arpbind` | IP/MAC 绑定 | 配置静态 ARP 绑定 |
| `luci-app-autoreboot` | 定时重启 | 设置路由器自动重启时间 |
| `luci-app-cifs-mount` | SMB/CIFS 挂载 | 将网络共享目录挂载到路由器 |
| `luci-app-ddns` | 动态 DNS | 在公网 IP 变化时更新域名解析 |
| `luci-app-design-config` | Design 主题设置 | 调整 Design 主题外观 |
| `luci-app-diskman` | 磁盘管理 | 查看和管理磁盘、分区；已选中 lsblk 支持 |
| `luci-app-filemanager` | 文件管理 | 在网页中管理路由器文件 |
| `luci-app-filetransfer` | 文件传输 | 提供文件及 IPK 安装包上传页面 |
| `luci-app-firewall` | 防火墙 | 配置防火墙规则和端口转发 |
| `luci-app-netdata` | Netdata 监控 | 查看系统资源和运行状态 |
| `luci-app-nfs` | NFS 共享 | 配置 NFS 文件共享 |
| `luci-app-nlbwmon` | 流量统计 | 统计局域网设备的网络流量 |
| `luci-app-openclash` | OpenClash | 管理 Clash 配置、订阅和分流规则 |
| `luci-app-oui` | 设备厂商标识 | 为 DHCP 租约列表提供本地 OUI 厂商图标 |
| `luci-app-package-manager` | 软件包管理 | 在网页中管理软件包 |
| `luci-app-passwall` | PassWall | 管理代理节点、订阅和分流规则 |
| `luci-app-smartdns` | SmartDNS | 配置 SmartDNS 的上游解析、缓存和解析策略 |
| `luci-app-ssr-plus` | SSR Plus+ | 管理代理节点和访问控制规则 |
| `luci-app-upnp` | UPnP | 管理 UPnP、NAT-PMP/PCP 自动端口映射 |
| `luci-app-vlmcsd` | KMS 服务 | 管理 vlmcsd KMS 服务 |
| `luci-app-vsftpd` | FTP 服务 | 配置 vsftpd 文件传输服务 |
| `luci-app-wol` | 网络唤醒 | 向支持 Wake-on-LAN 的设备发送唤醒报文 |

应用说明可查阅 [LuCI 源码](https://github.com/coolsnowwolf/luci/tree/openwrt-25.12/applications)、[PassWall 源码](https://github.com/Openwrt-Passwall/openwrt-passwall/tree/main/luci-app-passwall)和 [SSR Plus+ 源码](https://github.com/fw876/helloworld/tree/master/luci-app-ssr-plus)。

### 主题与基础组件

| 类别 | 已选内容 |
| --- | --- |
| 主题 | `luci-theme-argon`、`luci-theme-bootstrap`、`luci-theme-design` |
| 管理页面 | 网络、状态、系统，以及完整管理界面 |
| 协议支持 | `luci-proto-ipv6`、`luci-proto-ppp` |
| 兼容组件 | `luci-compat`、`luci-lua-runtime` |
| 界面语言 | LuCI 基础界面及配置中选中的应用简体中文语言包 |

### 代理相关组件

PassWall 和 SSR Plus+ 均选择了 nftables 透明代理支持。

| 配置位置 | 已选组件 |
| --- | --- |
| PassWall | Geoview、SmartDNS、HAProxy、Hysteria、Shadowsocks Rust 客户端、ShadowsocksR Libev 客户端、Simple Obfs、Sing-box、V2Ray Plugin、Xray |
| SSR Plus+ | HTTP 代理、Mihomo、GeoData |

SSR Plus+ 自身的 Shadowsocks 客户端、服务端和 V2Ray/Xray 选择项为 None；PassWall 选中的相关组件仍会编入同一固件。具体功能以各插件的配置和运行状态为准。

`luci-app-rclone` 没有启用，配置中残留的 rclone WebUI 子选项不计入应用清单。

## 源码与配置更新

| 文件 | 用途 |
| --- | --- |
| `.config` | 保存设备、驱动和应用选择 |
| `feeds.conf.default` | 指定各 feeds 的来源和分支 |

每次编译拉取 LEDE `master` 的最新提交。两个 PassWall feeds 跟随 `main`，LuCI 跟随 `openwrt-25.12`，其余未指定分支的 feeds 跟随各仓库默认分支。feeds 来源及顺序保持仓库配置，连续更新两次后安装。

工作流将 `.config` 复制到构建目录，执行 `defconfig` 并核对所选配置，不回写仓库中的原文件。如果所选配置被丢弃，任务会在正式编译前停止并列出差异。

实际使用的版本记录在日志产物的 `buildinfo/source.version` 和 `buildinfo/feeds.lock` 中。软件版本取决于 feeds 的维护进度，可能落后于软件作者发布的版本；上游更新也可能导致配置检查或编译失败。

## 构建环境与缓存

工作流参考了 [kenzok8 的 Lean 工作流](https://github.com/kenzok8/openwrt_Build/blob/master/.github/workflows/Lean.yml)，使用 `ubuntu-latest` 运行器。

编译前清理 Android、.NET、GHC、大型预装软件、CodeQL 和 Docker 镜像，同时禁用 swap 并删除 `/mnt/swapfile`。释放空间后，内存不足时可用的缓冲也会减少。

`dl`、`bin` 和 `staging_dir` 放在 `/mnt/openwrt` 下，通过软链接连接源码目录。`/mnt` 是否提供额外容量取决于运行器的磁盘挂载情况。工作流记录 `/`、`/mnt` 和工作区的容量、inode，以及源码和构建目录占用，空间检查本身只读取信息。

源码下载并发为 CPU 核数加 1。下载后清理小于 1 KiB 的文件；如果其中有有效源码文件，编译时可能重新下载。下载目录不做缓存。

下载完成后，`stupidloud/cachewrtbuild` 恢复工具链和 ccache，任务成功后保存缓存。缓存键包含实际 Ubuntu 版本、用户配置和 Action 计算的工具链提交；浅克隆下，上游提交变化可能导致缓存未命中。Make 仍会检查依赖，必要时重新编译。

编译命令通过 `CONFIG_CCACHE=y` 启用缓存，ccache 上限为 3 GiB，不改写固件配置。第三方清理和缓存 Action 均固定到指定提交。工作流还为主机端 libtirpc 添加 GNU C17 编译参数，以兼容其旧式函数声明。

## 日志与故障排查

失败时下载 `LEDE-buildinfo-运行编号`，查看下载日志、编译日志、空间记录和 `resolved.config`。多线程编译失败后，工作流会自动改用单线程输出详细错误。

单个 GitHub 托管 Job 最长运行 6 小时；当前编译步骤最多 300 分钟，两次编译尝试共用这一限额，其余时间留给准备和上传。如果超时，先根据日志确认耗时阶段，再考虑拆分工具链构建或更换运行器。
