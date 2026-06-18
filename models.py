#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人案件管理系统 - 数据库初始化与模型
本地部署，数据不上云，隐私优先
"""

import sqlite3
import os
import sys

def get_data_dir():
    """获取数据目录路径（兼容 PyInstaller 打包）"""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

DB_PATH = os.path.join(get_data_dir(), 'cases.db')

# 字段注释映射（SQLite不支持COMMENT，用字典记录）
FIELD_COMMENTS = {
    'cases': {
        'id': '主键', 'case_number': '案号', 'case_name': '案件名称',
        'case_type': '案件类型', 'court': '受理法院', 'judge': '法官',
        'status': '案件状态(进行中/已结案/暂停)', 'client_id': '关联客户ID',
        'client_name': '客户名称', 'client_contact': '客户联系方式',
        'opposing_party': '对方当事人', 'opposing_counsel': '对方律师',
        'claim_amount': '诉求金额', 'fee_amount': '律师费',
        'fee_status': '收费状态(未收费/部分收费/已收费)', 'description': '案件描述',
        'create_date': '立案日期', 'close_date': '结案日期',
    },
    'clients': {
        'id': '主键', 'name': '客户姓名/名称', 'type': '客户类型(个人/企业)',
        'phone': '电话', 'email': '邮箱', 'address': '地址',
        'id_number': '身份证号/统一社会信用代码', 'notes': '备注',
    },
    'work_records': {
        'id': '主键', 'case_id': '关联案件ID', 'date': '工作日期',
        'content': '工作内容', 'hours': '工时(小时)',
        'category': '工作类别(出庭/阅卷/起草/沟通/调研)',
    },
    'todo_items': {
        'id': '主键', 'case_id': '关联案件ID(可为空=通用待办)',
        'title': '待办标题', 'description': '待办描述',
        'deadline': '截止日期', 'priority': '优先级(紧急/重要/普通)',
        'status': '状态(待办/进行中/已完成)', 'reminder_date': '提醒日期',
    },
    'case_followups': {
        'id': '主键', 'case_id': '关联案件ID', 'date': '跟进日期',
        'content': '跟进内容', 'contact_person': '联系人', 'contact_phone': '联系电话',
        'result': '跟进结果', 'next_action': '下一步行动',
    },
    'doc_templates': {
        'id': '主键', 'name': '模板名称',
        'category': '模板分类(起诉状/答辩状/律师函/合同/备忘录)',
        'content': '模板内容', 'notes': '使用说明',
    },
    'timeline_events': {
        'id': '主键', 'case_id': '关联案件ID', 'date': '事件日期',
        'title': '事件标题', 'description': '事件描述',
        'event_type': '事件类型(立案/开庭/判决/调解/执行/其他)',
    },
}

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """初始化数据库，创建所有表"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    cursor = conn.cursor()

    # 案件表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_number TEXT NOT NULL,
        case_name TEXT NOT NULL,
        case_type TEXT NOT NULL,
        court TEXT,
        judge TEXT,
        status TEXT DEFAULT '进行中',
        client_id INTEGER,
        opposing_party TEXT,
        opposing_counsel TEXT,
        claim_amount REAL,
        fee_amount REAL,
        fee_status TEXT DEFAULT '未收费',
        description TEXT,
        create_date DATE,
        close_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 客户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT DEFAULT '个人',
        phone TEXT,
        email TEXT,
        address TEXT,
        id_number TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 工作记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS work_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        date DATE NOT NULL,
        content TEXT NOT NULL,
        hours REAL,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
    )
    """)

    # 待办事项表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        deadline DATE,
        priority TEXT DEFAULT '普通',
        status TEXT DEFAULT '待办',
        reminder_date DATE,
        source_doc_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE SET NULL
    )
    """)

    # 迁移：若 todo_items 表缺少 source_doc_id 列则添加
    try:
        cursor.execute("ALTER TABLE todo_items ADD COLUMN source_doc_id INTEGER")
    except:
        pass

    # 案件跟进记录表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_followups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        date DATE NOT NULL,
        content TEXT NOT NULL,
        contact_person TEXT DEFAULT '',
        contact_phone TEXT DEFAULT '',
        result TEXT,
        next_action TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
    )
    """)

    # 文书模板表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doc_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        category TEXT,
        content TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 时间线事件表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        date DATE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        event_type TEXT,
        source_doc_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
    )
    """)

    # 迁移：若 timeline_events 表缺少 source_doc_id 列则添加
    try:
        cursor.execute("ALTER TABLE timeline_events ADD COLUMN source_doc_id INTEGER")
    except:
        pass

    # 案件文档表（上传文件，含传票字段）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER NOT NULL,
        doc_type TEXT DEFAULT '文档',
        category TEXT DEFAULT '',
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER,
        folder_path TEXT DEFAULT '',
        hearing_date DATE,
        hearing_time TEXT,
        hearing_location TEXT,
        hearing_court TEXT,
        hearing_judge TEXT,
        hearing_case_number TEXT,
        case_cause TEXT,
        summons_cause TEXT,
        summoned_party TEXT,
        summoned_address TEXT,
        contact_phone TEXT,
        clerk TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (case_id) REFERENCES cases(id) ON DELETE CASCADE
    )
    """)

    # 案件类型预设数据
    case_types = [
        '民事诉讼', '知识产权', '公司纠纷', '合同纠纷', '劳动争议',
        '建设工程', '证券虚假陈述', '私募纠纷', '破产清算', '股权转让',
        '产品质量', '不动产买卖', '刑事辩护', '行政诉讼', '仲裁', '其他'
    ]

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS case_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """)

    for ct in case_types:
        cursor.execute("INSERT OR IGNORE INTO case_types (name) VALUES (?)", (ct,))

    # 预设文书模板
    default_templates = [
        ('民事起诉状', '起诉状', '原告：{原告}\n被告：{被告}\n\n诉讼请求：\n1. {诉讼请求1}\n2. {诉讼请求2}\n\n事实与理由：\n{事实与理由}\n\n此致\n{法院}\n\n原告：{原告签名}\n日期：{日期}', '通用民事起诉状模板，需替换花括号中的变量'),
        ('答辩状', '答辩状', '答辩人：{答辩人}\n针对{案号}案件，答辩如下：\n\n答辩意见：\n{答辩意见}\n\n证据：\n{证据清单}\n\n答辩人：{答辩人签名}\n日期：{日期}', '通用答辩状模板'),
        ('律师函', '律师函', '{律师事务所名称}\n\n致：{收函人}\n\n关于：{事由}\n\n{函件正文}\n\n特此函告。\n\n{律师姓名}\n{日期}', '通用律师函模板'),
    ]

    for name, cat, content, notes in default_templates:
        cursor.execute("INSERT OR IGNORE INTO doc_templates (name, category, content, notes) VALUES (?, ?, ?, ?)",
                       (name, cat, content, notes))

    conn.commit()

    # 兼容已有数据库 - 添加新字段
    try:
        cursor.execute("ALTER TABLE case_documents ADD COLUMN category TEXT DEFAULT ''")
    except Exception:
        pass  # 字段已存在
    try:
        cursor.execute("ALTER TABLE case_followups ADD COLUMN contact_person TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE case_followups ADD COLUMN contact_phone TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE cases ADD COLUMN client_name TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE cases ADD COLUMN client_contact TEXT DEFAULT ''")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE case_documents ADD COLUMN folder_path TEXT DEFAULT ''")
    except Exception:
        pass
    # 传票字段迁移
    for col, col_def in [
        ('hearing_date', 'DATE'),
        ('hearing_time', "TEXT DEFAULT ''"),
        ('hearing_location', "TEXT DEFAULT ''"),
        ('hearing_court', "TEXT DEFAULT ''"),
        ('hearing_judge', "TEXT DEFAULT ''"),
        ('hearing_case_number', "TEXT DEFAULT ''"),
        ('case_cause', "TEXT DEFAULT ''"),
        ('summons_cause', "TEXT DEFAULT ''"),
        ('summoned_party', "TEXT DEFAULT ''"),
        ('summoned_address', "TEXT DEFAULT ''"),
        ('contact_phone', "TEXT DEFAULT ''"),
        ('clerk', "TEXT DEFAULT ''"),
    ]:
        try:
            cursor.execute(f"ALTER TABLE case_documents ADD COLUMN {col} {col_def}")
        except Exception:
            pass
    try:
        cursor.execute("ALTER TABLE cases ADD COLUMN invoice_status TEXT DEFAULT '未开票'")
    except Exception:
        pass
    try:
        cursor.execute("ALTER TABLE doc_templates ADD COLUMN file_path TEXT DEFAULT ''")
    except Exception:
        pass

    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")

if __name__ == '__main__':
    init_db()