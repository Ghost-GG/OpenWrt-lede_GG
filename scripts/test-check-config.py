"""校验丢失依赖、模块状态和分区参数变化都能被识别。"""
import runpy
from pathlib import Path

check = runpy.run_path(str(Path(__file__).with_name("check-config.py")))["changed_selections"]
requested = {"CONFIG_PACKAGE_demo": "y", "CONFIG_TARGET_x86": "y", "CONFIG_TARGET_ROOTFS_PARTSIZE": "512"}
assert check(requested, dict(requested)) == []
assert len(check(requested, {**requested, "CONFIG_PACKAGE_demo": "m"})) == 1
assert len(check(requested, {"CONFIG_TARGET_x86": "y"})) == 2
assert len(check(requested, {**requested, "CONFIG_TARGET_ROOTFS_PARTSIZE": "256"})) == 1
assert check(requested, {**requested, "CONFIG_PACKAGE_dependency": "y"}) == []
print("配置校验自检通过。")
