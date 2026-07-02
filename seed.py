#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人案件管理系统 - 示例数据填充脚本
运行此脚本可在数据库中插入演示案例数据，方便快速体验系统功能。
"""

import os
import sys

# 确保当前目录在 path 中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db, get_db

def seed():
    """填充示例数据"""
    # 先初始化数据库
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # 检查是否已有数据
    existing = cursor.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    if existing > 0:
        print("数据库中已有案件数据，跳过填充（如需重新填充请先删除 data/cases.db）")
        conn.close()
        return

    # ===================== 客户 =====================
    cursor.execute("""
        INSERT INTO clients (name, type, phone, email, address, id_number, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        'A科技股份有限公司',
        '企业',
        '010-87654321',
        'legal@a-tech.com',
        '某市滨湖区太湖大道 88 号',
        '91310000MA1XX12345',
        '长期合作客户，主营智能制造设备出口。法务联系人：王经理 13900001111'
    ))
    client_id = cursor.lastrowid

    # ===================== 案例一：买卖合同纠纷 =====================
    cursor.execute("""
        INSERT INTO cases (case_number, case_name, case_type, court, judge, status,
                           client_id, opposing_party, opposing_counsel,
                           claim_amount, fee_amount, fee_status, description,
                           create_date, client_name, client_contact, invoice_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        '(2026)某0211民初字第1234号',
        'A科技股份有限公司诉B贸易有限公司买卖合同纠纷',
        '合同纠纷',
        '某市滨湖区人民法院',
        '张法官',
        '进行中',
        client_id,
        'B贸易有限公司',
        '某律师事务所 刘律师',
        2580000.00,
        120000.00,
        '部分收费',
        '委托人A科技股份有限公司与B贸易有限公司于2025年3月签订设备采购合同，总价款258万元。委托人已按约交付全部设备，但对方至今仅支付首款50万元，余款208万元逾期未付。委托人多次催款无果，现委托我所代理诉讼。',
        '2026-03-15',
        'A科技股份有限公司',
        '王经理 13900001111',
        '未开票'
    ))
    case1_id = cursor.lastrowid

    # 案例一时间线
    timeline_events_case1 = [
        ('2026-03-15', '接受委托', '与委托人签订委托代理合同，正式接受本案代理', '立案'),
        ('2026-03-25', '立案', '向某市滨湖区人民法院提交起诉状及证据材料，正式立案', '立案'),
        ('2026-04-10', '送达起诉状副本', '法院向被告B贸易有限公司送达起诉状副本', '其他'),
        ('2026-05-08', '证据交换', '双方在法院组织下进行庭前证据交换，我方提交合同、交付单、催款函等12份证据', '其他'),
        ('2026-06-18', '开庭', '第一次开庭审理，双方进行举证质证及法庭辩论', '开庭'),
        ('2026-07-15', '补充证据', '根据法庭要求补充提交第三方物流签收记录', '其他'),
    ]
    for date, title, desc, etype in timeline_events_case1:
        cursor.execute("""
            INSERT INTO timeline_events (case_id, date, title, description, event_type)
            VALUES (?, ?, ?, ?, ?)
        """, (case1_id, date, title, desc, etype))

    # 案例一跟进记录
    followups_case1 = [
        ('2026-03-15', '与王经理初次会面，了解案情基本情况，查阅合同及往来函件，初步评估胜诉可能性较大', '王经理', '13900001111', '已全面了解案情', '草拟起诉状及证据清单'),
        ('2026-04-20', '与被告方律师电话沟通和解可能性，对方表示需请示公司领导', '刘律师（对方）', '13800002222', '对方未明确表态，诉讼继续进行', '关注对方是否在期限内提交答辩状'),
        ('2026-06-15', '开庭前与委托人确认证据原件，进行模拟庭审演练，委托人配合度良好', '王经理', '13900001111', '庭审准备充分', '准时出庭'),
    ]
    for date, content, person, phone, result, next_action in followups_case1:
        cursor.execute("""
            INSERT INTO case_followups (case_id, date, content, contact_person, contact_phone, result, next_action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (case1_id, date, content, person, phone, result, next_action))

    # 案例一工作记录
    work_records_case1 = [
        ('2026-03-16', '查阅买卖合同纠纷相关司法解释及类案裁判文书', 3.0, '调研'),
        ('2026-03-18', '起草民事起诉状及证据目录', 4.0, '起草'),
        ('2026-03-22', '整理证据材料：合同、付款凭证、交付单、催款函等', 2.5, '阅卷'),
        ('2026-05-06', '准备证据交换材料，编制证据清单', 3.0, '起草'),
        ('2026-06-10', '庭前准备：撰写代理词、质证提纲、辩论要点', 5.0, '起草'),
        ('2026-06-18', '参加开庭审理，进行法庭调查、举证质证、法庭辩论', 4.5, '出庭'),
    ]
    for date, content, hours, category in work_records_case1:
        cursor.execute("""
            INSERT INTO work_records (case_id, date, content, hours, category)
            VALUES (?, ?, ?, ?, ?)
        """, (case1_id, date, content, hours, category))

    # 案例一待办
    todos_case1 = [
        ('提交补充证据材料', '根据6月18日开庭要求，补充提交第三方物流签收记录原件', '2026-07-15', '紧急', '待办', None),
        ('草拟代理词补充意见', '针对庭审中对方提出的新抗辩观点进行补充论证', '2026-07-10', '重要', '待办', None),
        ('跟进法院判决进度', '联系承办法官了解判决出具进展', '2026-08-01', '普通', '待办', None),
    ]
    for title, desc, deadline, priority, status, _ in todos_case1:
        cursor.execute("""
            INSERT INTO todo_items (case_id, title, description, deadline, priority, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (case1_id, title, desc, deadline, priority, status))

    # 案例一传票信息（无实际文件，仅信息录入演示）
    cursor.execute("""
        INSERT INTO case_documents (case_id, doc_type, category, file_name, file_path, file_size,
                                    hearing_date, hearing_time, hearing_location, hearing_court,
                                    hearing_judge, hearing_case_number, case_cause, summons_cause,
                                    summoned_party, summoned_address, contact_phone, clerk)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case1_id, '传票', '',
        '开庭传票（示例记录）.pdf', '', 0,
        '2026-06-18', '09:30',
        '某市滨湖区人民法院 第二审判庭',
        '某市滨湖区人民法院',
        '张法官',
        '(2026)某0211民初字第1234号',
        '买卖合同纠纷',
        '案件承办',
        'B贸易有限公司',
        '某市南山区科技园南路1号',
        '010-12345678',
        '李书记员'
    ))

    # ===================== 案例二：侵害商标权纠纷（已结案）=====================
    cursor.execute("""
        INSERT INTO cases (case_number, case_name, case_type, court, judge, status,
                           client_id, opposing_party, opposing_counsel,
                           claim_amount, fee_amount, fee_status, description,
                           create_date, close_date, client_name, client_contact, invoice_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        '(2025)某02民初字第567号',
        'A科技股份有限公司诉C精密机械有限公司侵害商标权纠纷',
        '知识产权',
        '某市中级人民法院',
        '陈法官',
        '已结案',
        client_id,
        'C精密机械有限公司',
        '某律师事务所 李律师',
        500000.00,
        80000.00,
        '已收费',
        '委托人发现C精密机械有限公司未经许可在其产品及宣传材料中使用与委托人注册商标近似的标识，涉嫌侵害注册商标专用权。经公证取证后提起诉讼。本案经中院主持调解，双方达成和解协议，被告停止侵权并赔偿损失。',
        '2025-08-01',
        '2025-12-20',
        'A科技股份有限公司',
        '王经理 13900001111',
        '已开票'
    ))
    case2_id = cursor.lastrowid

    # 案例二时间线
    timeline_events_case2 = [
        ('2025-08-01', '接受委托', '委托人发现侵权行为，委托我所代理维权', '立案'),
        ('2025-08-10', '证据保全公证', '对被告侵权网页及产品进行公证取证', '其他'),
        ('2025-09-01', '立案', '向某市中级人民法院提交起诉状，正式立案', '立案'),
        ('2025-10-20', '证据交换', '双方在法院主持下进行证据交换', '其他'),
        ('2025-11-15', '开庭', '第一次开庭审理，被告当庭承认部分侵权事实', '开庭'),
        ('2025-12-15', '调解', '在法院主持下达成调解协议', '调解'),
        ('2025-12-20', '结案', '法院出具调解书，被告支付赔偿款到位', '其他'),
    ]
    for date, title, desc, etype in timeline_events_case2:
        cursor.execute("""
            INSERT INTO timeline_events (case_id, date, title, description, event_type)
            VALUES (?, ?, ?, ?, ?)
        """, (case2_id, date, title, desc, etype))

    # 案例二跟进记录
    followups_case2 = [
        ('2025-08-05', '与委托人收集商标注册证书、荣誉证书等权利证据，核实侵权范围', '王经理', '13900001111', '权利基础扎实', '尽快完成公证取证'),
        ('2025-11-15', '开庭后被告主动联系和解，提出50万元赔偿方案，征求委托人意见', '李律师（对方）', '13600003333', '谈判空间较大', '草拟和解方案'),
    ]
    for date, content, person, phone, result, next_action in followups_case2:
        cursor.execute("""
            INSERT INTO case_followups (case_id, date, content, contact_person, contact_phone, result, next_action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (case2_id, date, content, person, phone, result, next_action))

    # 案例二工作记录
    work_records_case2 = [
        ('2025-08-02', '商标近似对比分析：制作侵权对比表', 3.5, '调研'),
        ('2025-08-08', '起草起诉状及证据清单', 3.0, '起草'),
        ('2025-10-15', '撰写开庭代理词', 4.0, '起草'),
        ('2025-11-15', '参加开庭审理', 3.0, '出庭'),
        ('2025-12-15', '参与法院调解，协助起草调解协议', 2.5, '调研'),
    ]
    for date, content, hours, category in work_records_case2:
        cursor.execute("""
            INSERT INTO work_records (case_id, date, content, hours, category)
            VALUES (?, ?, ?, ?, ?)
        """, (case2_id, date, content, hours, category))

    # 通用待办（不关联具体案件）
    cursor.execute("""
        INSERT INTO todo_items (case_id, title, description, deadline, priority, status)
        VALUES
        (NULL, '更新案件管理系统', '完成开源版本发布前的功能检查和文档编写', '2026-07-01', '重要', '进行中'),
        (NULL, '准备半年度工作汇报', '整理2026年上半年案件数据和工作总结', '2026-06-30', '紧急', '待办')
    """)

    conn.commit()
    conn.close()
    print("✅ 示例数据填充完成！")
    print(f"  - 客户: 1")
    print(f"  - 案件: 2（1件进行中 + 1件已结案）")
    print(f"  - 时间线事件: {len(timeline_events_case1) + len(timeline_events_case2)}")
    print(f"  - 跟进记录: {len(followups_case1) + len(followups_case2)}")
    print(f"  - 工作记录: {len(work_records_case1) + len(work_records_case2)}")
    print(f"  - 待办事项: 5")
    print(f"  - 传票记录: 1")

if __name__ == '__main__':
    seed()
