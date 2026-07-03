# 个人案件管理系统 — Windows 安装指南

---

## 一、系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 10（64位） | Windows 11（64位） |
| Python | 3.10+ | 3.12+ |
| 内存 | 4 GB | 8 GB+ |
| 磁盘空间 | 500 MB | 1 GB+ |
| 浏览器 | Chrome / Edge（最新版） | Chrome |

---

## 二、下载项目

从 GitHub 下载最新版源码：

> https://github.com/vincent9306/law-case-manager

点击页面上的绿色 **「Code」** 按钮 → **「Download ZIP」**，将 ZIP 文件解压到方便访问的位置（建议放在桌面或 D 盘根目录，**路径中不要包含中文或空格**）。

---

## 三、安装 Python

如果电脑尚未安装 Python，请按以下步骤操作：

1. 访问 https://www.python.org/downloads/ 下载最新版 Python 安装包。
2. 双击运行安装程序。

> ⚠️ **关键步骤**：安装界面的第一页，**务必勾选底部「Add Python to PATH」**（将 Python 添加到系统环境变量），否则后续命令将无法执行。

3. 安装完成后，按 `Win + R` 输入 `cmd` 回车，在命令提示符中输入以下命令验证：
   ```
   python --version
   ```
   如果显示版本号（如 `Python 3.12.0`），说明安装成功。

> 💡 **如果之前安装过 Python 但没有勾选 PATH**：
> 在 Windows 搜索框中输入「环境变量」→「编辑系统环境变量」→「环境变量」→ 在「系统变量」中找到 `Path` →「编辑」→ 添加两个路径：
> - `C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\`
> - `C:\Users\你的用户名\AppData\Local\Programs\Python\Python312\Scripts\`

---

## 四、安装系统

### 方式 A：自动安装（推荐）

1. 进入解压后的项目文件夹。
2. 找到文件 `install_windows.ps1`。
3. 右键点击该文件，选择 **「使用 PowerShell 运行」**。

> ⚠️ **如果提示「无法加载，因为在此系统上禁止运行脚本」**，请先执行以下操作：
> 1. 在 Windows 搜索框中输入 `PowerShell`。
> 2. 右键点击 Windows PowerShell → **「以管理员身份运行」**。
> 3. 在 PowerShell 窗口中粘贴以下命令并回车：
>    ```powershell
>    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
>    ```
> 4. 出现确认提示时输入 `Y` 并回车。
> 5. 关闭管理员 PowerShell，重新右键运行 `install_windows.ps1`。

脚本会自动完成：
- 检查 Python 环境
- 安装所需依赖包（Flask、PyPDF2、openpyxl 等）
- 创建数据目录和数据库
- 生成 `start.bat` 启动文件

### 方式 B：手动安装

如果自动脚本无法运行，请手动执行以下步骤：

1. 按 `Win + R`，输入 `cmd`，回车打开命令提示符。
2. 进入项目目录（将下面路径替换成你的实际路径）：
   ```
   cd /d D:\你的项目路径\law-case-manager
   ```
3. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```
4. 初始化数据库：
   ```
   python -c "from app import app; from models import init_db; init_db()"
   ```
5. 启动程序：
   ```
   python app.py
   ```
6. 浏览器自动打开后，或手动访问 **http://127.0.0.1:5066**。

### 方式 C：打包为独立 EXE（无需 Python 环境）

如果你希望分发给没有安装 Python 的同事使用，可以将项目打包为独立的 `.exe` 文件：

1. 确保 Python 已安装（打包过程需要 Python 环境）。
2. 在项目文件夹中找到 **`Windows一键打包.bat`**，双击运行。
3. 脚本会自动完成打包，等待提示完成。
4. 打包完成后，可执行文件位于 `dist\案件管理系统\` 目录下。
5. 将整个 `dist\案件管理系统\` 文件夹复制到任意电脑使用，**无需安装 Python**。

> ⚠️ **重要提示**：如果双击 `.bat` 文件后出现乱码或奇怪报错（如 `'cho' 不是内部或外部命令`、`'PDF2' 不是内部或外部命令`），这是文件编码问题。解决方法：
> - **方法 1（推荐）**：改用 `install_windows.ps1`（方式 A）。
> - **方法 2**：用记事本打开 `.bat` 文件，点击「文件 → 另存为」，底部编码选择 **「ANSI」**，保存替换原文件。
> - **方法 3**：在命令提示符中先输入 `chcp 65001` 回车，然后再运行 bat 文件。

---

## 五、启动系统

安装完成后，双击项目文件夹中的 **`start.bat`** 即可启动。

启动成功后，命令提示符窗口会显示：

```
========================================
  个人案件管理系统
  Developed by Yizhen Li
========================================

  正在启动服务...
```

浏览器将自动打开系统首页。若未自动打开，请手动访问 **http://127.0.0.1:5066**。

> ⚠️ **请勿关闭命令提示符窗口** — 关闭窗口即停止服务。

---

## 六、常见安装问题

### Q1：提示「python 不是内部或外部命令」

**原因**：Python 未安装，或未添加到系统 PATH。

**解决**：重新运行 Python 安装程序，安装时务必勾选「Add Python to PATH」。或参照上文第三章中的手动添加 PATH 方法。

### Q2：端口 5066 被占用

**解决**：
在命令提示符中输入：
```
netstat -ano | findstr :5066
```
记下最后一列的 PID 数字，然后输入：
```
taskkill /PID 进程号 /F
```
之后重新启动即可。或者修改 `app.py` 最后一行的端口号（搜索 `5066` 替换为其他端口如 `5088`）。

### Q3：防火墙弹出拦截提示

首次启动时 Windows 防火墙可能弹出提示，请点击 **「允许访问」**，否则浏览器无法连接。

### Q4：浏览器打开后页面空白

1. 确认命令提示符窗口没有报错信息。
2. 确认地址栏是 `http://127.0.0.1:5066`（注意是 **http** 不是 https）。
3. 尝试使用 Chrome 浏览器。
4. 关闭代理 / VPN 后重试。

---

## 七、创建桌面快捷方式

1. 在项目文件夹中找到 `start.bat`。
2. 右键点击 →「发送到」→「桌面快捷方式」。
3. 以后双击桌面快捷方式即可快速启动。

---

## 附录：完全卸载

直接删除项目文件夹即可。系统不会在注册表或其他位置留下痕迹。

如需保留数据，删除前请先备份 `data\` 文件夹。

---

> *Developed by Yizhen Li — Beijing Dacheng Law Offices, LLP (Wuxi)*
> *项目主页：https://github.com/vincent9306/law-case-manager*
