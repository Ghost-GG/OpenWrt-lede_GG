"""发现 feeds 或依赖不匹配导致用户选择丢失时，终止编译。"""
from pathlib import Path
import sys


def read_config(path):
    return dict(
        line.split("=", 1)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.startswith("CONFIG_") and "=" in line
    )


def changed_selections(requested, resolved):
    # 软件包及镜像选项影响最终固件，不能让 defconfig 静默替换。
    image_keys = {
        "CONFIG_GRUB_IMAGES", "CONFIG_GRUB_EFI_IMAGES", "CONFIG_QCOW2_IMAGES",
        "CONFIG_VMDK_IMAGES", "CONFIG_VDI_IMAGES", "CONFIG_VHDX_IMAGES",
        "CONFIG_ISO_IMAGES", "CONFIG_TARGET_KERNEL_PARTSIZE",
        "CONFIG_TARGET_ROOTFS_PARTSIZE", "CONFIG_TARGET_IMAGES_GZIP",
    }
    changes = []
    for key, value in requested.items():
        selected = key.startswith(("CONFIG_PACKAGE_", "CONFIG_TARGET_")) and value in ("y", "m")
        if (selected or key in image_keys) and resolved.get(key, "n") != value:
            changes.append(f"{key}: {value} -> {resolved.get(key, 'n')}")
    return changes


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("用法：python3 scripts/check-config.py 原始配置 解析后配置")
    changes = changed_selections(read_config(sys.argv[1]), read_config(sys.argv[2]))
    if changes:
        raise SystemExit("配置发生变化，请检查源码及 feeds：\n" + "\n".join(changes))
    print("配置检查通过：所选软件包、目标平台和镜像参数均保留。")
