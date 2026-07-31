# 版本历史

## v1.3.1 (2026-07-31)

### 问题修复
- 修复 macOS APP「不支持此应用程序」错误（v1.3.0 为 arm64 架构，Intel Mac 无法运行）
- 改用 `macos-latest` + `arch -x86_64` 交叉编译，生成 x86_64 架构 APP
- 兼容 Intel Mac（原生运行）和 Apple Silicon Mac（通过 Rosetta 2）

---

## v1.3.0 (2026-07-31)

### 新功能
- macOS DMG 安装包，拖拽安装体验（.app + /Applications 快捷方式）
- GitHub Actions 自动构建 macOS DMG（macos-latest + PyInstaller + hdiutil）
- 同时提供 DMG 和 ZIP 两种格式下载

---

## v1.2.1 (2026-07-30)

### 新功能
- EXE 改为后台运行模式，无控制台窗口，启动后浏览器自动打开
- 新增 `/shutdown` 端点，可通过浏览器优雅关闭服务
- GitHub Actions 自动构建 Windows 独立 EXE（PyInstaller --onefile）

### 问题修复
- 修复关闭程序后无法重新打开的问题（端口 TIME_WAIT 导致绑定失败）
- 启动时自动检测端口占用，如已被旧进程占用则自动释放
- 修正 `启动.bat` 中 EXE 名称错误（案件管理系统.exe → case-manager.exe）

---

## v1.1.2 (2026-07-03)

### 新功能
- 图文版 Windows 安装指南 PDF（含系统截图）
- 通过 GitHub Actions 自动构建和发布

---

## v1.1.1 (2026-07-02)

### 新功能
- Windows 和 macOS 用户使用指南（Markdown + PDF）
- macOS 安装脚本和启动脚本

### 问题修复
- 修复 Windows 批处理文件编码问题（UTF-8 → GBK，适配 CMD 代码页 936）
- 修复 PowerShell 安装脚本编码问题

---

## v1.1.0 (2026-06-18)

### 新功能
- 初版发布：个人案件管理系统
- 案件增删改查、文书模板、待办事项管理
- 数据统计仪表盘
- 本地部署，数据不上云，隐私优先
- Flask + SQLite 架构
