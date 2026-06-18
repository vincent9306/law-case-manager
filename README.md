# 个人案件管理系统

一个**完全离线**的个人案件管理系统，适合律师、法务等专业人士使用。所有数据存储在本地，隐私优先，断网可用。

## 核心功能

- **案件管理** — CRUD、8阶段状态流转、一键推进/结案
- **客户管理** — 客户信息维护，支持 Excel 一键导出
- **工作记录** — 按案件记录工作内容与工时
- **待办事项** — 按优先级/截止日期排序，支持开庭自动生成提醒
- **跟进记录** — 记录每次沟通的联系人、结果、下一步行动
- **文书模板** — 支持上传 Word/PDF，占位符高亮，一键生成文档
- **时间线** — 案件全生命周期事件可视化
- **数据统计** — 状态分布、收费情况、工时统计
- **iCloud 日历集成** — 开庭日期自动添加到 macOS 日历（仅 macOS）

## 案件状态体系

```
一审进行中 → 一审已结案 → 二审进行中 → 二审已结案
→ 执行进行中 → 执行已终本 → 执行完毕
```

另支持"已结案"快捷标记按钮。

## 隐私优势

- **完全离线** — 所有数据存储在本地 SQLite 数据库
- **无网络依赖** — 断网也能完整使用
- **无第三方服务** — 不依赖任何云服务或外部 API
- **自主可控** — 数据完全在您掌控中

---

## 快速开始

### 方式一：独立可执行文件（推荐，无需安装 Python）

#### Mac
1. [下载 `案件管理系统-mac.zip`](https://github.com/vincent9306/law-case-manager/releases) 并解压
2. 双击 `启动.command` 即可运行
3. 首次运行可能需要在「系统设置 → 隐私与安全性」中允许

#### Windows
1. [下载 `案件管理系统-windows.zip`](https://github.com/vincent9306/law-case-manager/releases) 并解压
2. 双击 `启动.bat` 即可运行
3. 如被杀毒软件拦截，请添加信任

### 方式二：源码运行（需要 Python）

#### Mac

```bash
git clone https://github.com/vincent9306/law-case-manager.git
cd law-case-manager
bash install_mac.sh    # 一键安装
bash start.sh          # 启动系统
```

#### Windows

1. 克隆项目并进入目录
2. 右键点击 `install_windows.ps1`，选择"使用 PowerShell 运行"
3. 安装完成后双击 `start.bat` 启动

浏览器访问 `http://127.0.0.1:5066`

### 方式三：手动安装（通用）

```bash
pip install -r requirements.txt
python3 app.py
```

---

### 自行打包

如需自行打包为独立可执行文件：

```bash
# Mac
bash build_mac.sh

# Windows
双击运行 Windows一键打包.bat
```

> 打包输出在 `dist/案件管理系统/` 目录下，将该文件夹分发给其他人即可直接使用，**无需安装 Python**。

---

## 系统要求

| 平台 | 要求 |
|------|------|
| Mac | macOS 10.15+，Homebrew |
| Windows | Windows 10+，Python 3.8+ |
| Linux | Python 3.8+ |

### 依赖组件

- Python 3.8+
- Python 依赖：Flask、PyPDF2、openpyxl、python-docx

---

## 使用方法

> 📖 **详细使用说明请参阅 [USAGE.md](USAGE.md)**，涵盖案件管理、传票、文档、时间线、待办、模板、统计等全部功能的图文说明。

### 启动

```bash
bash start.sh    # Mac/Linux
start.bat        # Windows
python3 app.py   # 通用
```

### 访问

浏览器打开 `http://127.0.0.1:5066`

### 示例数据

系统首次启动已内置演示案件（合同纠纷 + 知识产权），含客户、时间线、传票、跟进记录、工作记录、待办等完整数据。如需重新填充：

```bash
rm data/cases.db && python seed.py && python app.py
```

### 停止

终端按 `Ctrl + C`

---

## 数据位置

| 数据类型 | 位置 |
|----------|------|
| 数据库 | `data/cases.db`（SQLite） |
| 上传文件 | `data/uploads/` |

### 数据备份

定期备份 `data/` 目录即可。

### 数据迁移

将 `data/` 目录完整复制到新机器即可。

---

## 常见问题

### 端口 5066 被占用

```bash
# Mac/Linux
lsof -ti:5066 | xargs kill -9

# 然后重新运行
bash start.sh
```

### iCloud 日历添加失败（macOS）

- 系统设置 → 隐私与安全性 → 自动化
- 确认 Terminal / Python 有权控制"日历"

### 数据库被锁定

- 确保只有一个 Flask 进程在运行
- 删除 `data/cases.db-journal` 文件（如果存在）

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python Flask + SQLite |
| 前端 | Bootstrap 5 + JavaScript + Axios |
| 日历 | AppleScript（macOS） |
| 导出 | openpyxl（Excel）、python-docx（Word） |

## 项目结构

```
law-case-manager/
├── app.py                 # Flask 后端主应用
├── models.py              # 数据库模型与初始化
├── seed.py                # 示例数据填充脚本
├── requirements.txt       # Python 依赖
├── start.sh               # Mac/Linux 启动脚本
├── 启动.bat               # Windows 启动脚本（打包后使用）
├── 启动.command           # Mac 启动脚本（打包后使用）
├── install_mac.sh         # Mac 一键安装脚本
├── install_windows.ps1    # Windows 安装脚本
├── build_mac.sh           # Mac 打包脚本
├── Windows一键打包.bat    # Windows 打包脚本
├── law-case-manager.spec  # PyInstaller 配置
├── templates/             # HTML 模板
├── static/                # 静态资源
└── data/                  # 运行时数据（自动创建）
    ├── cases.db           # SQLite 数据库
    └── uploads/           # 上传文件
```

---

## 卸载

直接删除整个文件夹即可。如需保留数据，请先备份 `data/` 目录。

## 许可证

本项目基于 [MIT License](LICENSE) 开源，可自由使用、修改、分发。

## 贡献

欢迎提交 Issue 和 Pull Request。
