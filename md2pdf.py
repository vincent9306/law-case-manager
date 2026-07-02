#!/usr/bin/env python3
"""使用 reportlab 将 Markdown 用户指南转换为 PDF（支持中文）"""

import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# 注册中文字体
def register_chinese_font():
    """注册系统中文字体"""
    font_paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/Users/yizhenli/Library/Fonts/方正小标宋简.TTF",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont("ChineseFont", font_path))
                print(f"✅ 已加载中文字体: {font_path}")
                return "ChineseFont"
            except Exception as e:
                print(f"⚠️ 字体加载失败 {font_path}: {e}")
                continue
    
    print("⚠️ 未找到中文字体，使用默认字体")
    return "Helvetica"

def parse_markdown(md_file):
    """解析 Markdown 文件，返回内容块列表"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    blocks = []
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].rstrip()
        
        # 空行
        if not line:
            i += 1
            continue
        
        # 标题
        if line.startswith('#'):
            level = len(line) - len(line.lstrip('#'))
            text = line.lstrip('#').strip()
            blocks.append(('heading', level, text))
            i += 1
            continue
        
        # 分隔线
        if re.match(r'^---+$', line):
            blocks.append(('hr', None, None))
            i += 1
            continue
        
        # 表格
        if '|' in line and i + 1 < len(lines) and re.match(r'^\|?[\s\-:]+\|?$', lines[i+1].strip()):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            blocks.append(('table', None, table_lines))
            continue
        
        # 代码块
        if line.startswith('```'):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # 跳过结束的 ```
            blocks.append(('code', None, '\n'.join(code_lines)))
            continue
        
        # 列表项
        if re.match(r'^[\s]*[-*+] ', line) or re.match(r'^\d+\. ', line):
            list_items = [line.strip()]
            i += 1
            while i < len(lines) and (re.match(r'^[\s]*[-*+] ', lines[i].strip()) or re.match(r'^\d+\. ', lines[i].strip())):
                list_items.append(lines[i].strip())
                i += 1
            blocks.append(('list', None, list_items))
            continue
        
        # 普通段落
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#'):
            if '|' in lines[i] and lines[i].strip().startswith('|'):
                break
            para_lines.append(lines[i])
            i += 1
        
        text = ' '.join(para_lines).strip()
        # 移除 Markdown 格式标记（简化版）
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        text = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', text)
        blocks.append(('paragraph', None, text))
    
    return blocks

def create_pdf(md_path, pdf_path, font_name):
    """创建 PDF 文件"""
    blocks = parse_markdown(md_path)
    
    # 创建 PDF 文档
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    
    # 定义样式
    styles = getSampleStyleSheet()
    
    # 标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=font_name,
        fontSize=20,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=12,
        alignment=TA_CENTER,
    )
    
    # H1 样式
    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        textColor=HexColor('#1a1a1a'),
        spaceAfter=8,
        spaceBefore=16,
        borderPadding=5,
        borderColor=HexColor('#4a90d9'),
        borderWidth=0,
    )
    
    # H2 样式
    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=14,
        textColor=HexColor('#2c3e50'),
        spaceAfter=6,
        spaceBefore=12,
    )
    
    # H3 样式
    h3_style = ParagraphStyle(
        'CustomH3',
        parent=styles['Heading3'],
        fontName=font_name,
        fontSize=12,
        textColor=HexColor('#34495e'),
        spaceAfter=4,
        spaceBefore=8,
    )
    
    # 正文样式
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=16,
        textColor=colors.black,
    )
    
    # 代码样式
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8,
        leading=12,
        textColor=colors.black,
        backColor=HexColor('#f4f4f4'),
    )
    
    # 构建内容
    story = []
    
    for block_type, level, content in blocks:
        if block_type == 'heading':
            if level == 1:
                story.append(Paragraph(content, h1_style))
            elif level == 2:
                story.append(Paragraph(content, h2_style))
            elif level == 3:
                story.append(Paragraph(content, h3_style))
        elif block_type == 'hr':
            story.append(Spacer(1, 0.2*cm))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
            story.append(Spacer(1, 0.2*cm))
        elif block_type == 'paragraph':
            if content:
                story.append(Paragraph(content, body_style))
                story.append(Spacer(1, 0.3*cm))
        elif block_type == 'table':
            # 解析表格
            table_data = []
            for row in content:
                cells = [c.strip() for c in row.split('|')[1:-1]]
                table_data.append(cells)
            
            if len(table_data) >= 2:
                # 跳过分隔行
                if re.match(r'^[\s\-:]+$', table_data[1][0]):
                    table_data = [table_data[0]] + table_data[2:]
                
                # 创建表格
                t = Table(table_data)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4a90d9')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, 0), 9),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(t)
                story.append(Spacer(1, 0.5*cm))
        elif block_type == 'code':
            # 代码块
            for line in content.split('\n'):
                story.append(Paragraph(line.replace(' ', '    '), code_style))
            story.append(Spacer(1, 0.3*cm))
        elif block_type == 'list':
            for item in content:
                # 移除列表标记
                text = re.sub(r'^[\s]*[-*+.]\s*', '• ', item)
                text = re.sub(r'^\d+\.\s*', '• ', text)
                story.append(Paragraph(text, body_style))
            story.append(Spacer(1, 0.3*cm))
    
    # 生成 PDF
    doc.build(story)
    print(f"✅ 已生成: {pdf_path}")


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 注册中文字体
    font_name = register_chinese_font()
    
    # 转换 Windows 指南
    create_pdf(
        os.path.join(base_dir, "WINDOWS_GUIDE.md"),
        os.path.join(base_dir, "Windows使用指南.pdf"),
        font_name
    )
    
    # 转换 macOS 指南
    create_pdf(
        os.path.join(base_dir, "MAC_GUIDE.md"),
        os.path.join(base_dir, "macOS使用指南.pdf"),
        font_name
    )
    
    print("\n🎉 所有 PDF 生成完成！")
