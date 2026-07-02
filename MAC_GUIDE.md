# 个人案件管理系统 - macOS 使用指南

---

## 一、系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | macOS 12 Monterey | macOS 14 Sonoma+ |
| 架构 | Intel（x86_64）/ Apple Silicon（M1/M2/M3/M4） | Apple Silicon |
| 内存 | 4 GB | 8 GB+ |
| 磁盘空间 | 500 MB | 1 GB+ |
| 浏览器 | Chrome / Safari（最新版） | Chrome |

---

## 二、下载与安装

### 方式 A：使用预打包版（推荐，无需安装 Python）

1. 从 GitHub Releases 下载 `case-manager-macOS.zip`：
   > https://github.com/vincent9306/law-case-manager/releases

2. 解压到任意位置（建议放在 `/Applications` 或 `~/Desktop`）。

3. 进入解压后的文件夹，双击 `启动.command`。

4. **重要：首次运行需要绕过 Gatekeeper**

   如果出现以下提示：
   > 「启动.command」无法打开，因为无法验证开发者

   请按以下步骤操作：

   ```
   系统设置 → 隐私与安全性 → 安全性 → 点击「仍要打开」
   ```

   或者使用终端命令：
   ```bash
   # 进入解压后的目录
   cd ~/Desktop/案件管理系统-macOS

   # 移除隔离属性
   xattr -d com.apple.quarantine 启动.command
   xattr -cr 案件管理系统
   ```

5. 浏览器将自动打开，访问 **http://127.0.0.1:5066**。

### 方式 B：从源码运行（需要 Python）

1. 从 GitHub 下载源代码：
   > https://github.com/vincent9306/law-case-manager

2. 解压到任意目录。

3. 打开终端（Terminal），进入项目目录：
   ```bash
   cd ~/Downloads/law-case-manager
   ```

4. 运行安装脚本：
   ```bash
   bash install_mac.sh
   ```

5. 启动程序：
   ```bash
   bash start.sh
   ```

6. 浏览器访问 **http://127.0.0.1:5066**。

### 方式 C：手动安装

1. 确保已安装 Python 3.10+：
   ```bash
   python3 --version
   ```
   如未安装，从 https://www.python.org/downloads/ 下载安装。

2. 进入项目目录，创建虚拟环境（推荐）：
   ```bash
   cd law-case-manager
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行：
   ```bash
   python3 app.py
   ```

5. 浏览器访问 **http://127.0.0.1:5066**。

---

## 三、首次启动

第一次启动时，系统会自动：

1. 在 `data/` 目录下创建 SQLite 数据库（`cases.db`）。
2. 在 `data/uploads/` 目录下创建文件上传目录。
3. 启动 Flask Web 服务器（默认端口 **5066**）。

启动成功后，终端会显示类似以下信息：

```
========================================
  个人案件管理系统
  Developed by Yizhen Li
  Beijing Dacheng Law Offices, LLP (Wuxi)
========================================

  * Running on http://127.0.0.1:5066
```

浏览器将自动打开首页。若未自动打开，请手动访问 http://127.0.0.1:5066。

---

## 四、功能概览

启动后，在浏览器中打开 **http://127.0.0.1:5066**，你将看到以下页面：

| 功能模块 | 说明 |
|---------|------|
| 📊 **仪表盘** | 案件总览、状态分布统计、近期待办提醒 |
| 📋 **案件列表** | 全部案件浏览、搜索、筛选、排序、导出 Excel |
| 📝 **案件详情** | 基本信息、当事人、进度跟踪、文档管理、时间线 |
| ⏱️ **时间线** | 案件关键事件节点的可视化记录 |
| 📄 **传票管理** | 庭审传票的录入、提醒与跟踪 |
| 📈 **数据统计** | 案件类型、状态、收费等维度的统计分析 |

---

## 五、常见问题排查

### Q1：双击「启动.command」后提示"无法验证开发者"

这是 macOS 的 Gatekeeper 安全机制。请执行：

```bash
# 方法 1：终端命令（推荐）
xattr -d com.apple.quarantine 启动.command
xattr -cr ./

# 方法 2：系统设置
# 系统设置 → 隐私与安全性 → 找到拦截记录 → 点击「仍要打开」
```

### Q2：提示"无法打开，因为 Apple 无法检查其是否包含恶意软件"

同样执行 Q1 中的 `xattr -cr` 命令移除整个文件夹的隔离属性。

### Q3：提示"zsh: bad CPU type in executable"

这通常出现在 Apple Silicon（M1/M2/M3/M4）Mac 上运行 Intel 版可执行文件时。

**解决方法**：
- 安装 Rosetta 2：`softwareupdate --install-rosetta`
- 或从源码运行（方式 B）。

### Q4：端口 5066 被占用

**解决方法**：
```bash
# 查找占用端口的进程
lsof -i :5066

# 终止进程（替换 PID 为实际进程号）
kill -9 <PID>
```

或修改 `app.py` 中的端口号（搜索 `5066` 替换为其他端口）。

### Q5：浏览器打开后页面空白 / 加载失败

**解决方法**：
1. 确认终端窗口没有报错信息。
2. 检查浏览器是否开启了代理（VPN），尝试关闭。
3. 尝试使用 Chrome 无痕模式打开。
4. 清除浏览器缓存后重试。

### Q6：如何备份数据？

数据库文件和上传文件位于 `data/` 目录下：

```
data/
├── cases.db          ← 数据库文件（所有案件数据）
└── uploads/          ← 上传的文件
```

**备份方法**：直接复制整个 `data/` 目录即可。

---

## 六、数据导出

系统支持将案件列表导出为 Excel 文件：

1. 进入「案件列表」页面。
2. 点击「导出 Excel」按钮。
3. 浏览器会自动下载 `.xlsx` 文件。

---

## 七、停止与重启

- **停止**：在终端窗口按 `Control + C`，或直接关闭终端窗口。
- **重启**：重新双击 `启动.command`。

---

## 八、创建桌面快捷方式（可选）

### 方法 1：使用 Automator 创建 .app

1. 打开「自动操作」（Automator）。
2. 新建「应用程序」。
3. 搜索并添加「运行 Shell 脚本」。
4. 输入：
   ```bash
   cd /Applications/案件管理系统-macOS
   ./启动.command
   ```
5. 保存为 `案件管理系统.app`，放在桌面。

### 方法 2：添加至程序坞

将 `启动.command` 拖入程序坞右侧即可快速启动。

---

## 九、技术支持

- GitHub Issues：https://github.com/vincent9306/law-case-manager/issues
- 项目主页：https://github.com/vincent9306/law-case-manager

---

> *Developed by Yizhen Li — Beijing Dacheng Law Offices, LLP (Wuxi)*
