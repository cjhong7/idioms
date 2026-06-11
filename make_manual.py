# -*- coding: utf-8 -*-
"""도전 四字成語 사용자 설명서 PDF 생성"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

# ── 한국어 폰트 등록 ──────────────────────────────────────────
FONT_DIR = "C:/Windows/Fonts"
pdfmetrics.registerFont(TTFont("Malgun", os.path.join(FONT_DIR, "malgun.ttf")))
pdfmetrics.registerFont(TTFont("MalgunBold", os.path.join(FONT_DIR, "malgunbd.ttf")))
pdfmetrics.registerFont(TTFont("HancomGothic", os.path.join(FONT_DIR, "Hancom Gothic Regular.ttf")))
pdfmetrics.registerFont(TTFont("HancomGothicBold", os.path.join(FONT_DIR, "Hancom Gothic Bold.ttf")))

# ── 색상 ──────────────────────────────────────────────────────
NAVY    = colors.HexColor("#07162E")
COBALT  = colors.HexColor("#1A4FBB")
COBALT2 = colors.HexColor("#102D7A")
LBLUE   = colors.HexColor("#A8C4FF")
CREAM   = colors.HexColor("#F5F2E8")
DARK    = colors.HexColor("#1A1A2E")
GRAY    = colors.HexColor("#555566")
LGRAY   = colors.HexColor("#EAECF4")
GREEN   = colors.HexColor("#2ECC71")
RED     = colors.HexColor("#C0392B")
AMBER   = colors.HexColor("#F39C12")
WHITE   = colors.white
BLACK   = colors.black

# ── 스타일 ────────────────────────────────────────────────────
def make_styles():
    return {
        "title": ParagraphStyle("title", fontName="MalgunBold", fontSize=28, textColor=WHITE,
                                 alignment=TA_CENTER, spaceAfter=6, leading=36),
        "subtitle": ParagraphStyle("subtitle", fontName="Malgun", fontSize=14, textColor=LBLUE,
                                    alignment=TA_CENTER, spaceAfter=4, leading=20),
        "h1": ParagraphStyle("h1", fontName="MalgunBold", fontSize=16, textColor=WHITE,
                              spaceBefore=14, spaceAfter=6, leading=22,
                              borderPad=6, backColor=COBALT2,
                              leftIndent=0, rightIndent=0),
        "h2": ParagraphStyle("h2", fontName="MalgunBold", fontSize=13, textColor=COBALT,
                              spaceBefore=10, spaceAfter=4, leading=18),
        "h3": ParagraphStyle("h3", fontName="MalgunBold", fontSize=11, textColor=DARK,
                              spaceBefore=8, spaceAfter=3, leading=16),
        "body": ParagraphStyle("body", fontName="Malgun", fontSize=10, textColor=DARK,
                                spaceAfter=4, leading=16, leftIndent=8),
        "body_c": ParagraphStyle("body_c", fontName="Malgun", fontSize=10, textColor=DARK,
                                  spaceAfter=4, leading=16, alignment=TA_CENTER),
        "bullet": ParagraphStyle("bullet", fontName="Malgun", fontSize=10, textColor=DARK,
                                  spaceAfter=3, leading=16, leftIndent=20, firstLineIndent=-12),
        "code": ParagraphStyle("code", fontName="Malgun", fontSize=9, textColor=COBALT2,
                                spaceAfter=3, leading=14, leftIndent=16,
                                backColor=LGRAY, borderPad=4),
        "note": ParagraphStyle("note", fontName="Malgun", fontSize=9, textColor=colors.HexColor("#885500"),
                                spaceAfter=3, leading=14, leftIndent=16,
                                backColor=colors.HexColor("#FFF8E0"), borderPad=4),
        "warn": ParagraphStyle("warn", fontName="MalgunBold", fontSize=9, textColor=RED,
                                spaceAfter=3, leading=14, leftIndent=16,
                                backColor=colors.HexColor("#FFF0F0"), borderPad=4),
        "tip": ParagraphStyle("tip", fontName="Malgun", fontSize=9, textColor=colors.HexColor("#1a5c1a"),
                               spaceAfter=3, leading=14, leftIndent=16,
                               backColor=colors.HexColor("#F0FFF0"), borderPad=4),
        "tbl_hdr": ParagraphStyle("tbl_hdr", fontName="MalgunBold", fontSize=9, textColor=WHITE,
                                   alignment=TA_CENTER, leading=14),
        "tbl_cell": ParagraphStyle("tbl_cell", fontName="Malgun", fontSize=9, textColor=DARK,
                                    leading=14, spaceAfter=2),
        "tbl_cell_c": ParagraphStyle("tbl_cell_c", fontName="Malgun", fontSize=9, textColor=DARK,
                                      leading=14, alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontName="Malgun", fontSize=8, textColor=GRAY,
                                  alignment=TA_CENTER),
        "covernum": ParagraphStyle("covernum", fontName="MalgunBold", fontSize=11, textColor=LBLUE,
                                    alignment=TA_CENTER, leading=18),
    }

S = make_styles()

W, H = A4
MARGIN = 18 * mm

# ── 헤더/푸터 콜백 ────────────────────────────────────────────
PAGE_NUM = [0]

def header_footer(canvas, doc):
    PAGE_NUM[0] += 1
    canvas.saveState()
    # 상단 헤더 바
    canvas.setFillColor(COBALT2)
    canvas.rect(0, H - 14*mm, W, 14*mm, fill=1, stroke=0)
    canvas.setFont("MalgunBold", 9)
    canvas.setFillColor(WHITE)
    canvas.drawString(MARGIN, H - 9*mm, "도전 四字成語  사용자 설명서")
    canvas.drawRightString(W - MARGIN, H - 9*mm, "v2026.06")
    # 하단 푸터
    canvas.setFillColor(LGRAY)
    canvas.rect(0, 0, W, 10*mm, fill=1, stroke=0)
    canvas.setFont("Malgun", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(W/2, 3.5*mm, f"— {PAGE_NUM[0]} —")
    canvas.restoreState()

def cover_page(canvas, doc):
    canvas.saveState()
    # 배경
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, W, H, fill=1, stroke=0)
    # 상단 장식 바
    canvas.setFillColor(COBALT)
    canvas.rect(0, H - 22*mm, W, 22*mm, fill=1, stroke=0)
    canvas.setFillColor(COBALT2)
    canvas.rect(0, H - 24*mm, W, 2*mm, fill=1, stroke=0)
    # 하단 장식 바
    canvas.setFillColor(COBALT)
    canvas.rect(0, 0, W, 18*mm, fill=1, stroke=0)
    canvas.setFont("Malgun", 9)
    canvas.setFillColor(LBLUE)
    canvas.drawCentredString(W/2, 6*mm, "초등학생 사자성어 교육용 웹게임  ·  교실 TV / 터치스크린 사용")
    canvas.restoreState()

# ── 테이블 스타일 헬퍼 ────────────────────────────────────────
def basic_table(data, col_widths, row_heights=None, hdr_color=COBALT):
    tbl = Table(data, colWidths=col_widths, rowHeights=row_heights)
    style = TableStyle([
        ("BACKGROUND", (0,0), (-1,0), hdr_color),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "MalgunBold"),
        ("FONTSIZE",   (0,0), (-1,0), 9),
        ("ALIGN",      (0,0), (-1,0), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("FONTNAME",   (0,1), (-1,-1), "Malgun"),
        ("FONTSIZE",   (0,1), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LGRAY]),
        ("GRID",       (0,0), (-1,-1), 0.5, colors.HexColor("#CCCCDD")),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
    ])
    tbl.setStyle(style)
    return tbl

def section_box(story, title_text, content_items):
    """파란 제목 박스 + 내용"""
    story.append(Paragraph(f"  {title_text}", S["h1"]))
    for item in content_items:
        story.append(item)

def bullet(text, bold_prefix=""):
    if bold_prefix:
        return Paragraph(f"<b>•  {bold_prefix}</b> {text}", S["bullet"])
    return Paragraph(f"•  {text}", S["bullet"])

def nb(text):
    return Paragraph(text, S["body"])

def h2(text):
    return Paragraph(text, S["h2"])

def h3(text):
    return Paragraph(text, S["h3"])

def sp(n=4):
    return Spacer(1, n*mm)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=COBALT, spaceAfter=4, spaceBefore=4)

# ════════════════════════════════════════════════════════════════
#   PDF 콘텐츠 생성
# ════════════════════════════════════════════════════════════════
def build_story():
    story = []

    # ── 표지 ──────────────────────────────────────────────────
    story.append(Spacer(1, 48*mm))
    story.append(Paragraph("도전  四字成語", S["title"]))
    story.append(Paragraph("사용자 설명서", S["subtitle"]))
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="70%", thickness=1.5, color=COBALT, spaceAfter=6, hAlign="CENTER"))
    story.append(Spacer(1, 6*mm))

    # 주요 수치 요약 박스
    summary_data = [
        [Paragraph("사자성어", S["tbl_hdr"]), Paragraph("게임 시간", S["tbl_hdr"]),
         Paragraph("최대 문제", S["tbl_hdr"]), Paragraph("단계", S["tbl_hdr"]),
         Paragraph("배포 주소", S["tbl_hdr"])],
        [Paragraph("166개 내장", S["tbl_cell_c"]), Paragraph("60초", S["tbl_cell_c"]),
         Paragraph("20문제", S["tbl_cell_c"]), Paragraph("3단계", S["tbl_cell_c"]),
         Paragraph("GitHub Pages", S["tbl_cell_c"])],
    ]
    t = basic_table(summary_data, [36*mm, 28*mm, 28*mm, 24*mm, 44*mm])
    story.append(t)
    story.append(Spacer(1, 6*mm))

    toc_data = [
        ["요약", "한 장 요약 (Quick Start) — 바쁘면 이 페이지만!"],
        ["1장", "게임 소개 및 특징"],
        ["2장", "실행 방법"],
        ["3장", "화면 흐름 & 게임 플레이"],
        ["4장", "점수 체계 & 게임 규칙"],
        ["5장", "관리자 환경설정 (전체)"],
        ["6장", "Google Sheets 연동 — GAS 설치 상세 안내"],
        ["7장", "엑셀로 사자성어 등록"],
        ["8장", "결과 분석 화면"],
        ["9장", "문제해결 & FAQ"],
    ]
    toc_tbl_data = [[Paragraph("장", S["tbl_hdr"]), Paragraph("내용", S["tbl_hdr"])]]
    for row in toc_data:
        toc_tbl_data.append([
            Paragraph(f"<b>{row[0]}</b>", S["tbl_cell_c"]),
            Paragraph(row[1], S["tbl_cell"]),
        ])
    t2 = basic_table(toc_tbl_data, [20*mm, 140*mm])
    story.append(t2)

    story.append(Spacer(1, 12*mm))
    story.append(Paragraph("2026년 6월  |  제작: Claude (Anthropic) × cjhong7", S["footer"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 한 장 요약 (Quick Start) — 2쪽
    # ══════════════════════════════════════════════════════
    story.append(Paragraph("  ⚡ 한 장 요약 (Quick Start)", S["h1"]))
    story.append(Paragraph("바쁘면 이 페이지만 읽어도 게임을 운영할 수 있습니다. 더 자세한 내용은 1장부터 참고하세요.", S["body"]))
    story.append(sp(2))

    story.append(h3("① 실행하기"))
    story.append(nb("폴더의 <b>「게임실행하기.bat」</b>를 더블클릭 → Chrome에서 게임이 자동으로 열립니다. (HTML 파일 직접 실행 ❌ — 카메라·음성 차단됨)"))

    story.append(h3("② 게임 방법"))
    story.append(nb("화면 <b>가운데의 '뜻'</b>을 읽고, <b>동서남북(상·우·하·좌) 4개 보기</b> 중 알맞은 사자성어를 선택합니다. 제한시간 60초, 최대 20문제."))

    story.append(h3("③ 점수 (정답 / 오답)"))
    quick_score = [
        [Paragraph("단계", S["tbl_hdr"]), Paragraph("저학년 (초1~2)", S["tbl_hdr"]),
         Paragraph("중학년 (초3~4)", S["tbl_hdr"]), Paragraph("고학년 (초5+)", S["tbl_hdr"])],
        [Paragraph("정답 / 오답", S["tbl_cell_c"]), Paragraph("+4 / -2", S["tbl_cell_c"]),
         Paragraph("+6 / -3", S["tbl_cell_c"]), Paragraph("+8 / -4", S["tbl_cell_c"])],
    ]
    story.append(basic_table(quick_score, [34*mm, 42*mm, 42*mm, 42*mm]))
    story.append(sp(2))

    story.append(h3("④ 조작 방법"))
    story.append(nb("<b>터치 · 마우스 · 손동작</b> 모두 가능합니다. 손동작은 보기/버튼 위에 손끝을 <b>0.5~0.7초</b> 올려두면 자동 선택됩니다. (틀린 문제 복습창의 [확인]도 손동작 가능)"))

    story.append(h3("⑤ 관리자 — 온라인 점수 저장 켜기 (선택)"))
    story.append(nb("학생 점수를 한 곳(Google Sheets)에 모으려면 ⚙️ 환경설정 → '구글 드라이브 연동'에서 아래 4단계를 한 번만 설정하세요:"))
    quick_gas = [
        "Google Sheets를 새로 만들고 → 메뉴 [확장 프로그램] → [Apps Script] 열기",
        "환경설정의 <b>[📋 코드 복사]</b> 버튼 → Apps Script에 붙여넣고 저장",
        "[배포] → [새 배포] → '웹 앱', <b>액세스 '모든 사용자'</b>로 배포 → 웹앱 URL 복사",
        "환경설정 칸에 URL을 붙여넣고 [저장] → 완료! (자세한 그림 설명은 <b>6장</b>)",
    ]
    for i, g in enumerate(quick_gas, 1):
        story.append(Paragraph(f"<b>{i}.</b>  {g}", S["bullet"]))
    story.append(Paragraph("💡  저장 위치는 스프레드시트의 <b>「전체점수」 탭</b>입니다. (기본 '시트1' 탭이 아님)", S["tip"]))
    story.append(sp(2))

    story.append(h3("⑥ 자주 묻는 문제 (빠른 해결)"))
    quick_faq = [
        [Paragraph("증상", S["tbl_hdr"]), Paragraph("빠른 해결", S["tbl_hdr"])],
        [Paragraph("점수가 시트에 안 보여요", S["tbl_cell_c"]),
         Paragraph("온라인 모드 + 환경설정에 GAS URL 입력 확인 → 스프레드시트 「전체점수」 탭 확인 (→6장·9장)", S["tbl_cell"])],
        [Paragraph("손동작이 안 돼요", S["tbl_cell_c"]),
         Paragraph("Chrome 카메라 권한 허용. 불편하면 환경설정에서 손동작을 끄고 터치로 사용 (→9장 Q2)", S["tbl_cell"])],
        [Paragraph("설정 비밀번호를 잊었어요", S["tbl_cell_c"]),
         Paragraph("초기값은 0000. 변경 후 분실 시 9장 Q5 방법으로 초기화", S["tbl_cell"])],
    ]
    story.append(basic_table(quick_faq, [44*mm, 116*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 1장: 게임 소개
    # ══════════════════════════════════════════════════════
    section_box(story, "1장  게임 소개 및 특징", [])

    story.append(h2("1-1  게임 개요"))
    story.append(nb("「도전 四字成語」는 초등학생이 사자성어의 뜻을 읽고 알맞은 사자성어를 4개 보기 중에서 선택하는 교육용 웹 게임입니다."))
    story.append(nb("교실 TV나 터치스크린에서 바로 사용할 수 있으며, 손동작(MediaPipe)·음성인식으로 조작할 수 있습니다."))
    story.append(sp(2))

    feat_data = [
        [Paragraph("구분", S["tbl_hdr"]), Paragraph("내용", S["tbl_hdr"])],
        [Paragraph("플랫폼", S["tbl_cell_c"]), Paragraph("단일 HTML 파일 (index.html) — 설치 불필요, 브라우저에서 바로 실행", S["tbl_cell"])],
        [Paragraph("조작 방식", S["tbl_cell_c"]), Paragraph("터치 / 마우스 클릭 / 손동작(카메라) / 키보드", S["tbl_cell"])],
        [Paragraph("사자성어 DB", S["tbl_cell_c"]), Paragraph("기본 166개 내장 (저학년 52·중학년 54·고학년 60) + 엑셀로 추가 등록 가능", S["tbl_cell"])],
        [Paragraph("데이터 저장", S["tbl_cell_c"]), Paragraph("오프라인: 기기 내 localStorage / 온라인: Google Sheets(GAS) 클라우드", S["tbl_cell"])],
        [Paragraph("결과 분석", S["tbl_cell_c"]), Paragraph("통계·필터·자주 틀리는 사자성어·성장 추이·엑셀 다운로드", S["tbl_cell"])],
        [Paragraph("배포", S["tbl_cell_c"]), Paragraph("https://cjhong7.github.io/idioms/", S["tbl_cell"])],
    ]
    story.append(basic_table(feat_data, [30*mm, 130*mm]))
    story.append(sp(3))

    story.append(h2("1-2  주요 특징"))
    features = [
        ("4지선다 퀴즈", "중앙에 사자성어의 '뜻'이 제시되면 동서남북 4방향에 배치된 보기 중 맞는 것을 선택"),
        ("3단계 난이도", "저학년(초1~2) / 중학년(초3~4) / 고학년(초5 이상) — 단계별 점수 차등"),
        ("손동작 인식", "카메라에 손을 뻗어 보기 위에 0.5초 체류하면 자동 선택 (MediaPipe Hands)"),
        ("음성 이름 입력", "Web Speech API로 이름을 말하면 자동 입력 (실패 시 키보드 직접 입력)"),
        ("콤보 시스템", "연속 정답 3개 이상 시 콤보 효과 + 화면 연출"),
        ("적응형 출제", "자주 틀린 사자성어를 가중치 부여해 반복 출제"),
        ("QR 참여 코드", "학생이 스마트폰으로 QR을 스캔해 온라인 모드 자동 진입"),
        ("Google Sheets 연동", "게임 종료 후 점수를 Google Sheets에 자동 저장"),
    ]
    for title, desc in features:
        story.append(bullet(desc, title + ":"))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 2장: 실행 방법
    # ══════════════════════════════════════════════════════
    section_box(story, "2장  실행 방법", [])

    story.append(h2("2-1  교실 TV/PC에서 로컬 실행 (권장)"))
    story.append(nb("게임 파일이 저장된 폴더에는 다음 파일들이 있습니다:"))
    story.append(sp(2))

    file_data = [
        [Paragraph("파일명", S["tbl_hdr"]), Paragraph("용도", S["tbl_hdr"])],
        [Paragraph("index.html", S["tbl_cell_c"]), Paragraph("게임 본체 (소스이자 배포본, 이 파일 하나로 모든 기능 동작)", S["tbl_cell"])],
        [Paragraph("게임실행하기.bat", S["tbl_cell_c"]), Paragraph("더블클릭 → 로컬 웹 서버(포트 8765) 자동 시작 + Chrome 자동 오픈", S["tbl_cell"])],
    ]
    story.append(basic_table(file_data, [40*mm, 120*mm]))
    story.append(sp(3))

    story.append(h3("▶ 실행 순서"))
    steps = [
        "「게임실행하기.bat」 파일을 더블클릭합니다.",
        "검은 PowerShell 창이 열리고 「서버 시작 중…」 메시지가 표시됩니다.",
        "Chrome 브라우저가 자동으로 http://localhost:8765 를 열며 게임 화면이 나타납니다.",
        "게임이 끝나면 PowerShell 창을 닫으면 서버도 종료됩니다.",
    ]
    for i, s_text in enumerate(steps, 1):
        story.append(Paragraph(f"<b>  {i}.</b>  {s_text}", S["body"]))
    story.append(sp(2))
    story.append(Paragraph("⚠️  주의: HTML 파일을 직접 더블클릭하면 카메라·음성인식이 차단됩니다. 반드시 bat 파일로 실행하세요.", S["warn"]))
    story.append(Paragraph("💡  브라우저는 Chrome을 권장합니다. (음성인식·손동작이 가장 안정적)", S["tip"]))

    story.append(sp(4))
    story.append(h2("2-2  인터넷 브라우저에서 직접 접속 (GitHub Pages)"))
    story.append(nb("인터넷이 연결된 환경이라면 아래 URL로 바로 접속할 수 있습니다:"))
    story.append(Paragraph("https://cjhong7.github.io/idioms/", S["code"]))
    story.append(Paragraph("⚠️  클라우드 저장(Google Sheets 연동)이 필요하면 관리자가 먼저 환경설정을 완료해야 합니다.", S["note"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 3장: 화면 흐름 & 게임 플레이
    # ══════════════════════════════════════════════════════
    section_box(story, "3장  화면 흐름 & 게임 플레이", [])

    story.append(h2("3-1  전체 화면 흐름"))
    story.append(sp(2))
    flow_data = [
        [Paragraph("단계", S["tbl_hdr"]), Paragraph("화면 이름", S["tbl_hdr"]),
         Paragraph("설명", S["tbl_hdr"])],
        [Paragraph("①", S["tbl_cell_c"]), Paragraph("모드 선택", S["tbl_cell_c"]),
         Paragraph("오프라인 / 온라인 중 선택", S["tbl_cell"])],
        [Paragraph("②", S["tbl_cell_c"]), Paragraph("로그인 (온라인만)", S["tbl_cell_c"]),
         Paragraph("학교이름 입력 또는 참여코드 스캔으로 입장", S["tbl_cell"])],
        [Paragraph("③", S["tbl_cell_c"]), Paragraph("데이터 범위 선택 (온라인만)", S["tbl_cell_c"]),
         Paragraph("전체 / 학년별 / 학년+반 별 명예의 전당 분리 저장", S["tbl_cell"])],
        [Paragraph("④", S["tbl_cell_c"]), Paragraph("인트로 (명예의 전당)", S["tbl_cell_c"]),
         Paragraph("상위 5명 랭킹 표시, 게임 시작 버튼", S["tbl_cell"])],
        [Paragraph("⑤", S["tbl_cell_c"]), Paragraph("이름 입력", S["tbl_cell_c"]),
         Paragraph("음성으로 이름 말하기 → 자동 인식 (실패 시 키보드 직접 입력)", S["tbl_cell"])],
        [Paragraph("⑥", S["tbl_cell_c"]), Paragraph("단계 선택", S["tbl_cell_c"]),
         Paragraph("저학년 / 중학년 / 고학년 선택, 이어서 하기 지원", S["tbl_cell"])],
        [Paragraph("⑦", S["tbl_cell_c"]), Paragraph("카운트다운", S["tbl_cell_c"]),
         Paragraph("3 - 2 - 1 - 시작! (BGM 시작)", S["tbl_cell"])],
        [Paragraph("⑧", S["tbl_cell_c"]), Paragraph("게임 진행", S["tbl_cell_c"]),
         Paragraph("60초 / 20문제 4지선다, 정답 시 다음 문제로 이동", S["tbl_cell"])],
        [Paragraph("⑨", S["tbl_cell_c"]), Paragraph("틀린 문제 복습 (오답 있을 때만)", S["tbl_cell_c"]),
         Paragraph("틀린 사자성어를 한자·뜻과 함께 표시 → [확인] 후 결과 화면으로", S["tbl_cell"])],
        [Paragraph("⑩", S["tbl_cell_c"]), Paragraph("결과 화면", S["tbl_cell_c"]),
         Paragraph("점수·정답률·클라우드 저장 상태 표시, 다음 행동 선택", S["tbl_cell"])],
    ]
    story.append(basic_table(flow_data, [14*mm, 40*mm, 106*mm]))
    story.append(sp(3))

    story.append(h2("3-2  게임 화면 구성"))
    story.append(nb("게임 화면은 3×3 격자 구조로 되어 있습니다:"))
    story.append(sp(2))

    layout_data = [
        [Paragraph("①  학수고대\n鶴首苦待", S["tbl_cell_c"]), Paragraph("", S["tbl_cell_c"]),
         Paragraph("", S["tbl_cell_c"])],
        [Paragraph("④  칠전팔기\n七顚八起", S["tbl_cell_c"]),
         Paragraph("◈ 이 뜻에 맞는\n사자성어는? ◈\n\n실력이 비슷해\n우열을 가리기 어려움\n(1 / 20)", S["tbl_cell_c"]),
         Paragraph("②  막상막하\n莫上莫下", S["tbl_cell_c"])],
        [Paragraph("", S["tbl_cell_c"]), Paragraph("③  금시초문\n今時初聞", S["tbl_cell_c"]),
         Paragraph("", S["tbl_cell_c"])],
    ]
    layout_tbl = Table(layout_data, colWidths=[54*mm, 54*mm, 54*mm], rowHeights=[26*mm, 32*mm, 26*mm])
    layout_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (2,0), (2,0), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (0,2), (0,2), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (2,2), (2,2), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (0,1), (0,1), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (2,1), (2,1), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (1,0), (1,0), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (1,2), (1,2), colors.HexColor("#EAE5D5")),
        ("BACKGROUND", (1,1), (1,1), colors.HexColor("#07162E")),
        ("TEXTCOLOR",  (1,1), (1,1), WHITE),
        ("FONTNAME",   (0,0), (-1,-1), "Malgun"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("GRID",       (0,0), (-1,-1), 1, COBALT),
        ("BOX",        (0,0), (-1,-1), 2, COBALT),
    ]))
    story.append(KeepTogether([
        layout_tbl,
        sp(2),
        nb("• 번호 ①②③④는 북(위) / 동(오른쪽) / 남(아래) / 서(왼쪽) 에 배치됩니다."),
        nb("• HUD: 왼쪽 위 = 남은 시간 | 가운데 위 = 현재 단계 | 오른쪽 위 = 이름·점수"),
    ]))
    story.append(sp(3))

    story.append(h2("3-3  틀린 문제 복습 창 (신규)"))
    story.append(nb("게임 종료 시 <b>틀린 문제가 하나라도 있으면</b> 결과 화면에 앞서 「📝 틀린 문제 복습」 창이 먼저 표시됩니다. 틀린 사자성어를 한 번 더 익힐 수 있는 복습 단계입니다."))
    story.append(sp(2))
    review_items = [
        "각 오답은 <b>① 번호 · 한글음 · 한자 · 뜻</b> 순서로 카드에 표시됩니다 (정답 복습용).",
        "오답이 많으면 카드 영역이 자동으로 스크롤됩니다.",
        "[✅ 확인] 버튼을 누르면 창이 닫히고 결과 화면으로 넘어갑니다.",
        "[확인] 버튼은 <b>터치·마우스·손바닥 모션</b> 모두로 누를 수 있습니다 (손끝 0.7초 체류 시 자동 선택).",
        "틀린 문제가 <b>없으면</b> 이 창은 나타나지 않고 곧바로 결과 화면이 표시됩니다.",
    ]
    for r in review_items:
        story.append(Paragraph(f"•  {r}", S["bullet"]))
    story.append(Paragraph("💡  여기서 틀린 사자성어는 다음 게임에서 더 자주 출제됩니다(적응형 출제).", S["tip"]))
    story.append(sp(3))

    story.append(h2("3-4  손동작(제스처) 조작 방법"))
    story.append(nb("카메라가 연결되어 있고 손동작 인식이 켜져 있으면, 손을 화면에 비춰 조작할 수 있습니다."))
    story.append(sp(2))
    gesture_data = [
        [Paragraph("상황", S["tbl_hdr"]), Paragraph("조작 방법", S["tbl_hdr"]),
         Paragraph("체류 시간", S["tbl_hdr"])],
        [Paragraph("게임 중 보기 선택", S["tbl_cell_c"]),
         Paragraph("손끝을 원하는 사자성어 카드 위에 올려 잠시 멈춤", S["tbl_cell"]),
         Paragraph("0.5초", S["tbl_cell_c"])],
        [Paragraph("메뉴·버튼 선택", S["tbl_cell_c"]),
         Paragraph("손끝을 버튼(게임 시작·단계·확인 등) 위에 올려 멈춤", S["tbl_cell"]),
         Paragraph("0.7초", S["tbl_cell_c"])],
        [Paragraph("틀린 문제 복습 [확인]", S["tbl_cell_c"]),
         Paragraph("손끝을 [✅ 확인] 버튼 위에 올려 멈춤", S["tbl_cell"]),
         Paragraph("0.7초", S["tbl_cell_c"])],
    ]
    story.append(basic_table(gesture_data, [44*mm, 92*mm, 24*mm]))
    story.append(sp(2))
    story.append(Paragraph("💡  손끝(검지)을 대상 위에 올리면 파란 원형 커서와 강조 효과가 나타나며, 잠시 멈추면 자동으로 선택됩니다.", S["tip"]))
    story.append(Paragraph("⚠️  손동작이 불편하면 ⚙️ 환경설정에서 손동작 인식을 끄고 터치/마우스로 플레이하세요.", S["note"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 4장: 점수 체계
    # ══════════════════════════════════════════════════════
    section_box(story, "4장  점수 체계 & 게임 규칙", [])

    story.append(h2("4-1  단계별 점수"))
    score_data = [
        [Paragraph("단계", S["tbl_hdr"]), Paragraph("대상", S["tbl_hdr"]),
         Paragraph("정답 점수", S["tbl_hdr"]), Paragraph("오답 감점", S["tbl_hdr"])],
        [Paragraph("저학년", S["tbl_cell_c"]), Paragraph("초등 1~2학년", S["tbl_cell_c"]),
         Paragraph("+4점", S["tbl_cell_c"]), Paragraph("-2점", S["tbl_cell_c"])],
        [Paragraph("중학년", S["tbl_cell_c"]), Paragraph("초등 3~4학년", S["tbl_cell_c"]),
         Paragraph("+6점", S["tbl_cell_c"]), Paragraph("-3점", S["tbl_cell_c"])],
        [Paragraph("고학년", S["tbl_cell_c"]), Paragraph("초등 5학년 이상", S["tbl_cell_c"]),
         Paragraph("+8점", S["tbl_cell_c"]), Paragraph("-4점", S["tbl_cell_c"])],
    ]
    story.append(basic_table(score_data, [30*mm, 50*mm, 40*mm, 40*mm]))
    story.append(sp(3))

    story.append(h2("4-2  게임 규칙"))
    rules = [
        ("시간 제한", "60초. 시간이 다 되면 남은 문제와 무관하게 게임 종료"),
        ("문제 수", "최대 20문제. 20문제를 모두 맞히면 시간이 남아도 게임 종료"),
        ("오답 처리", "오답 보기는 어둡게 비활성화됨. 정답을 고를 때까지 같은 문제 유지"),
        ("점수 하한", "점수는 0점 미만으로 내려가지 않음"),
        ("콤보", "연속 정답 3개 이상 시 화면 중앙에 콤보 횟수 표시 + 효과"),
        ("이어서 하기", "결과 화면에서 '이어서 다음 단계' 선택 시 저학년→중학년→고학년 순 진행"),
        ("적응형 출제", "이전에 자주 틀린 사자성어를 가중치 부여하여 더 자주 출제"),
    ]
    rule_data = [[Paragraph("규칙", S["tbl_hdr"]), Paragraph("설명", S["tbl_hdr"])]]
    for r, d in rules:
        rule_data.append([Paragraph(f"<b>{r}</b>", S["tbl_cell_c"]), Paragraph(d, S["tbl_cell"])])
    story.append(basic_table(rule_data, [32*mm, 128*mm]))
    story.append(sp(3))

    story.append(h2("4-3  결과 화면 버튼"))
    result_btns = [
        ("가. 이어서 다음 단계", "현재 단계 다음 단계로 바로 진행 (저→중→고 순서)"),
        ("나. 새로운 게임자 참여", "다른 학생이 처음부터 시작 (이름 입력 화면으로)"),
        ("다. 결과 분석 보기", "이번 게임의 상세 통계 화면으로 이동"),
        ("라. 홈으로", "처음 모드 선택 화면으로 돌아가기"),
    ]
    for btn, desc in result_btns:
        story.append(bullet(desc, btn + ":"))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 5장: 관리자 환경설정
    # ══════════════════════════════════════════════════════
    section_box(story, "5장  관리자 환경설정", [])

    story.append(h2("5-1  환경설정 열기"))
    story.append(nb("화면 우측 상단의 ⚙️(톱니바퀴) 버튼을 누르면 환경설정 화면이 열립니다."))
    story.append(nb("처음 접근 시 관리자 비밀번호를 입력해야 합니다. (초기값: <b>0000</b>)"))
    story.append(Paragraph("⚠️  참여코드로 입장한 학생 기기에는 환경설정 버튼이 숨겨져 있습니다.", S["warn"]))
    story.append(sp(3))

    story.append(h2("5-2  환경설정 항목 전체 목록"))
    setting_data = [
        [Paragraph("항목", S["tbl_hdr"]), Paragraph("내용", S["tbl_hdr"]),
         Paragraph("초기값", S["tbl_hdr"])],
        [Paragraph("관리자 비밀번호", S["tbl_cell_c"]),
         Paragraph("환경설정 잠금 비밀번호. 학생이 설정을 변경하지 못하도록 보호", S["tbl_cell"]),
         Paragraph("0000", S["tbl_cell_c"])],
        [Paragraph("학교 이름", S["tbl_cell_c"]),
         Paragraph("기록·랭킹 구분 단위. 학교명이 다르면 랭킹이 분리됨", S["tbl_cell"]),
         Paragraph("(빈 값)", S["tbl_cell_c"])],
        [Paragraph("데이터 범위", S["tbl_cell_c"]),
         Paragraph("전체 / 학년별 / 학년+반별 — 명예의 전당 표시 범위 결정", S["tbl_cell"]),
         Paragraph("전체", S["tbl_cell_c"])],
        [Paragraph("구글 드라이브 연동", S["tbl_cell_c"]),
         Paragraph("GAS 웹앱 URL + 저장 비밀번호 입력 → 점수가 스프레드시트에 자동 저장", S["tbl_cell"]),
         Paragraph("미설정", S["tbl_cell_c"])],
        [Paragraph("참여코드 생성", S["tbl_cell_c"]),
         Paragraph("학생이 QR 스캔으로 온라인 모드에 자동 입장하는 코드 생성", S["tbl_cell"]),
         Paragraph("—", S["tbl_cell_c"])],
        [Paragraph("BGM", S["tbl_cell_c"]),
         Paragraph("배경음악 켜기/끄기 (Web Audio API 동양풍 5음계)", S["tbl_cell"]),
         Paragraph("ON", S["tbl_cell_c"])],
        [Paragraph("손동작 인식", S["tbl_cell_c"]),
         Paragraph("카메라로 손동작 인식 켜기/끄기 (MediaPipe Hands)", S["tbl_cell"]),
         Paragraph("ON", S["tbl_cell_c"])],
        [Paragraph("엑셀로 사자성어 등록", S["tbl_cell_c"]),
         Paragraph(".xlsx 파일 업로드로 사자성어 커스텀 데이터 등록 / 초기화", S["tbl_cell"]),
         Paragraph("기본 166개", S["tbl_cell_c"])],
    ]
    story.append(basic_table(setting_data, [32*mm, 104*mm, 24*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 6장: GAS 상세 안내
    # ══════════════════════════════════════════════════════
    section_box(story, "6장  Google Sheets 연동 — GAS 설치 상세 안내", [])

    story.append(h2("6-1  연동 개요"))
    story.append(nb("Google Apps Script(GAS)를 사용해 게임 종료 시 점수를 Google Sheets에 자동 저장합니다."))
    story.append(nb("설정은 교사(관리자)가 처음 1회만 하면 되며, 이후 학생들은 자동으로 저장됩니다."))
    story.append(sp(2))

    story.append(h2("6-2  준비물"))
    story.append(bullet("Google 계정 (Gmail)"))
    story.append(bullet("Chrome 브라우저 (Google 로그인 상태)"))
    story.append(sp(3))

    story.append(h2("6-3  단계별 설치 방법"))
    story.append(sp(2))

    gas_steps = [
        ("1단계: 새 Google Sheets 생성",
         "Google Drive(drive.google.com)에서 [새로 만들기] → [Google Sheets]를 클릭하여\n새 스프레드시트를 만듭니다.\n제목을 「도전 사자성어 점수」와 같이 알아보기 쉽게 변경하세요."),
        ("2단계: Apps Script 열기",
         "스프레드시트 메뉴에서 [확장 프로그램] → [Apps Script]를 클릭합니다.\n새 탭에 코드 편집기가 열립니다."),
        ("3단계: GAS 코드 복사하기",
         "게임 → ⚙️ 환경설정 → 「구글 드라이브 연동」 섹션 → [📋 코드 복사] 버튼을 클릭합니다.\nGAS 코드가 클립보드에 복사됩니다."),
        ("4단계: 코드 붙여넣기",
         "Apps Script 편집기의 기존 코드(function myFunction(){...})를 전부 선택·삭제한 후\n복사한 코드를 붙여넣기(Ctrl+V)합니다.\n[💾 저장] 버튼(또는 Ctrl+S)을 눌러 저장합니다."),
        ("5단계: 웹앱 배포",
         "[배포] → [새 배포] 클릭\n  - 유형 선택: 「웹 앱」\n  - 다음 사용자로 실행: 「나」\n  - 액세스 권한: 「모든 사용자」  ← 반드시 이 값으로!\n[배포] 버튼을 클릭하고 Google 계정 권한 허용"),
        ("6단계: 웹앱 URL 복사",
         "배포 완료 후 표시되는 「웹 앱 URL」(https://script.google.com/macros/s/.../exec)\n을 복사합니다."),
        ("7단계: 게임에 URL 등록",
         "게임 → ⚙️ 환경설정 → 「구글 드라이브 연동」\n  - GAS URL 입력창에 복사한 URL 붙여넣기\n  - 저장 비밀번호 설정 (기본값 0000 사용 가능)\n  - [저장] 버튼 클릭\n이제 온라인 모드로 게임하면 점수가 자동 저장됩니다!"),
    ]

    for step_title, step_desc in gas_steps:
        inner = []
        inner.append(Paragraph(f"<b>{step_title}</b>", S["h3"]))
        for line in step_desc.split("\n"):
            inner.append(Paragraph(f"  {line}", S["body"]))
        inner.append(sp(1))
        story.append(KeepTogether(inner))

    story.append(sp(3))
    story.append(h2("6-4  결과 확인 위치"))
    story.append(Paragraph("⚠️  스프레드시트의 기본 「시트1」 탭이 아니라 「전체점수」 탭에서 데이터를 확인하세요!", S["warn"]))
    story.append(sp(2))

    sheet_data = [
        [Paragraph("탭 이름", S["tbl_hdr"]), Paragraph("저장 조건", S["tbl_hdr"])],
        [Paragraph("전체점수", S["tbl_cell_c"]), Paragraph("범위 = 전체 로 게임한 점수 (기본)", S["tbl_cell"])],
        [Paragraph("N학년점수", S["tbl_cell_c"]), Paragraph("범위 = 학년 (예: 3학년점수)", S["tbl_cell"])],
        [Paragraph("N-M점수", S["tbl_cell_c"]), Paragraph("범위 = 반 (예: 3-2점수)", S["tbl_cell"])],
    ]
    story.append(basic_table(sheet_data, [40*mm, 120*mm]))
    story.append(sp(3))

    story.append(h2("6-5  저장 결과 메시지 해석"))
    msg_data = [
        [Paragraph("게임 종료 후 메시지", S["tbl_hdr"]), Paragraph("원인 및 해결 방법", S["tbl_hdr"])],
        [Paragraph("✅ 클라우드 저장 완료", S["tbl_cell_c"]),
         Paragraph("정상 저장. 스프레드시트 「전체점수」 탭에서 확인", S["tbl_cell"])],
        [Paragraph("❌ GAS 응답 오류", S["tbl_cell_c"]),
         Paragraph("배포 시 「액세스: 모든 사용자」로 다시 배포 필요", S["tbl_cell"])],
        [Paragraph("❌ 저장 실패: 비밀번호 불일치", S["tbl_cell_c"]),
         Paragraph("환경설정의 저장 비밀번호와 GAS의 비밀번호가 다름 → 비밀번호 확인", S["tbl_cell"])],
        [Paragraph("❌ 연결 실패 (로컬엔 저장됨)", S["tbl_cell_c"]),
         Paragraph("네트워크 오류 또는 GAS URL이 잘못됨 → URL 재확인", S["tbl_cell"])],
        [Paragraph("⚠️ Google Sheets 미연동", S["tbl_cell_c"]),
         Paragraph("GAS URL이 입력되지 않음 → 환경설정에서 URL 등록", S["tbl_cell"])],
    ]
    story.append(basic_table(msg_data, [52*mm, 108*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 7장: 엑셀로 사자성어 등록
    # ══════════════════════════════════════════════════════
    section_box(story, "7장  엑셀 파일로 사자성어 등록 (커스텀)", [])

    story.append(h2("7-1  파일 형식"))
    story.append(nb("새 Excel 파일(.xlsx)을 만들어 다음 형식으로 작성합니다:"))
    story.append(sp(2))

    excel_ex = [
        [Paragraph("저학년", S["tbl_hdr"]), Paragraph("중학년", S["tbl_hdr"]), Paragraph("고학년", S["tbl_hdr"])],
        [Paragraph("일석이조|一石二鳥|한 번에 두 가지 이익을 얻음", S["code"]),
         Paragraph("와신상담|臥薪嘗膽|목적을 이루기 위해 온갖 고난을 참고 견딤", S["code"]),
         Paragraph("교학상장|敎學相長|가르치고 배우면서 서로 성장함", S["code"])],
        [Paragraph("가나다|假那多|예시 뜻 설명", S["code"]),
         Paragraph("", S["tbl_cell_c"]),
         Paragraph("", S["tbl_cell_c"])],
    ]
    story.append(basic_table(excel_ex, [54*mm, 68*mm, 38*mm]))
    story.append(sp(2))

    story.append(h2("7-2  작성 규칙"))
    excel_rules = [
        "첫 행(1행)이 머리글입니다: <b>저학년</b> / <b>중학년</b> / <b>고학년</b> 으로 정확히 입력",
        "각 칸 형식: <b>한글음|한자|뜻</b> (구분자: | 또는 / 또는 ,)",
        "한자는 반드시 4글자여야 합니다. (4글자 아니면 등록 건너뜀)",
        "각 단계는 서로 다른 열(A, B, C 열)에 작성합니다",
        "빈 칸은 건너뜁니다 (오류 없이 처리)",
    ]
    for r in excel_rules:
        story.append(Paragraph(f"•  {r}", S["bullet"]))
    story.append(sp(3))

    story.append(h2("7-3  업로드 방법"))
    story.append(nb("⚙️ 환경설정 → 「📂 엑셀 파일로 단어 등록」 섹션 → [클릭하여 엑셀 파일 업로드] 버튼"))
    story.append(nb("✅ 성공적으로 등록되었습니다! 메시지가 뜨면 완료"))
    story.append(nb("기본값으로 되돌리려면 [기본값으로 초기화] 버튼을 클릭"))
    story.append(Paragraph("💡  커스텀 데이터는 기기 내(localStorage)에 저장됩니다. 다른 기기에서는 별도로 업로드해야 합니다.", S["tip"]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 8장: 결과 분석
    # ══════════════════════════════════════════════════════
    section_box(story, "8장  결과 분석 화면", [])

    story.append(h2("8-1  분석 화면 항목"))
    story.append(nb("게임 결과 화면에서 「다. 결과 분석 보기」를 누르면 상세 분석 화면이 열립니다."))
    story.append(sp(2))

    analysis_data = [
        [Paragraph("항목", S["tbl_hdr"]), Paragraph("설명", S["tbl_hdr"])],
        [Paragraph("통계 카드", S["tbl_cell_c"]),
         Paragraph("총 점수 / 맞힌 문제 수 / 정답률 / 속도(문제당 초) 요약", S["tbl_cell"])],
        [Paragraph("필터", S["tbl_cell_c"]),
         Paragraph("이름·단계·날짜 기준으로 기록 필터링 가능", S["tbl_cell"])],
        [Paragraph("상세 기록표", S["tbl_cell_c"]),
         Paragraph("학교·이름·점수·단계·날짜 등 행별로 모든 기록 열람", S["tbl_cell"])],
        [Paragraph("자주 틀리는 단어", S["tbl_cell_c"]),
         Paragraph("오답 횟수 상위 15개 사자성어를 카드로 표시 (적응형 출제에 활용됨)", S["tbl_cell"])],
        [Paragraph("성장 추이 차트", S["tbl_cell_c"]),
         Paragraph("특정 학생을 필터 시 날짜별 정답률 꺾은선 그래프 표시", S["tbl_cell"])],
        [Paragraph("엑셀 다운로드", S["tbl_cell_c"]),
         Paragraph("[📥 엑셀 다운로드] 버튼으로 현재 기록 전체를 .xlsx 파일로 내려받기", S["tbl_cell"])],
    ]
    story.append(basic_table(analysis_data, [36*mm, 124*mm]))
    story.append(sp(3))

    story.append(h2("8-2  온라인 모드 클라우드 분석"))
    story.append(nb("온라인 모드 + Google Sheets 연동 시 게임 종료 후 자동으로 클라우드 기록을 불러옵니다."))
    story.append(nb("스프레드시트에서 직접 데이터를 관리하거나 추출할 수도 있습니다."))
    story.append(sp(2))

    col_data = [
        [Paragraph("열 이름", S["tbl_hdr"]), Paragraph("설명", S["tbl_hdr"])],
        [Paragraph("학교", S["tbl_cell_c"]), Paragraph("등록된 학교 이름", S["tbl_cell"])],
        [Paragraph("이름", S["tbl_cell_c"]), Paragraph("학생이 입력한 이름", S["tbl_cell"])],
        [Paragraph("점수", S["tbl_cell_c"]), Paragraph("최종 점수", S["tbl_cell"])],
        [Paragraph("학년 / 반", S["tbl_cell_c"]), Paragraph("범위 설정 시 입력된 학년·반 (0이면 전체 모드)", S["tbl_cell"])],
        [Paragraph("단계", S["tbl_cell_c"]), Paragraph("1=저학년 / 2=중학년 / 3=고학년", S["tbl_cell"])],
        [Paragraph("속도", S["tbl_cell_c"]), Paragraph("문제당 평균 소요 초(속도 지표)", S["tbl_cell"])],
        [Paragraph("정답률", S["tbl_cell_c"]), Paragraph("전체 시도 대비 정답 비율(%)", S["tbl_cell"])],
        [Paragraph("날짜", S["tbl_cell_c"]), Paragraph("게임 플레이 날짜·시간", S["tbl_cell"])],
    ]
    story.append(basic_table(col_data, [30*mm, 130*mm]))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════
    # 9장: 문제해결 FAQ
    # ══════════════════════════════════════════════════════
    section_box(story, "9장  문제해결 & FAQ", [])
    story.append(sp(2))

    faqs = [
        ("Q1. 게임이 열리지 않아요.",
         "A. 「게임실행하기.bat」 파일을 더블클릭했는지 확인하세요. HTML 파일을 직접 열면 안 됩니다.\n   PowerShell 창에서 오류가 보이면 포트 8765가 이미 사용 중인지 확인하세요."),
        ("Q2. 손동작이 인식이 안 돼요.",
         "A. Chrome에서 카메라 권한을 허용했는지 확인하세요 (주소창 왼쪽 자물쇠 아이콘 클릭).\n   카메라가 연결되지 않았거나 다른 앱에서 사용 중이면 인식되지 않습니다.\n   환경설정에서 손동작을 OFF로 하고 터치/마우스로 플레이할 수 있습니다."),
        ("Q3. 이름 음성 입력이 안 돼요.",
         "A. Chrome에서 마이크 권한을 허용했는지 확인하세요.\n   음성 인식 실패 시 자동으로 키보드 직접 입력 화면이 나타납니다."),
        ("Q4. 구글 점수가 저장이 안 돼요.",
         "A. 다음 순서로 확인하세요:\n   1) 온라인 모드로 플레이했는가?\n   2) 환경설정 → GAS URL이 입력되어 있는가?\n   3) 종료 화면에 ✅ 클라우드 저장 완료 가 떴는가?\n   4) 스프레드시트에서 「전체점수」 탭을 열었는가? (기본 시트1 탭 아님)\n   5) GAS 배포 시 액세스 = 「모든 사용자」로 설정했는가?"),
        ("Q5. 환경설정 비밀번호를 잊었어요.",
         "A. 브라우저 개발자 도구(F12) → Console 탭에서\n   localStorage.removeItem('scj_pw_admin_학교이름') 입력 후 Enter → 초기값 0000으로 재설정됩니다."),
        ("Q6. 사자성어를 추가/수정하고 싶어요.",
         "A. 환경설정 → 「📂 엑셀 파일로 단어 등록」에서 .xlsx 파일로 커스텀 데이터를 등록하세요.\n   7장의 형식을 참고하세요."),
        ("Q7. 다른 기기에서도 같은 기록을 보려면?",
         "A. Google Sheets 연동(6장)을 완료하고 온라인 모드로 같은 학교명으로 접속하면\n   모든 기기에서 동일한 클라우드 기록을 공유합니다."),
        ("Q8. 참여코드(QR)는 어떻게 사용하나요?",
         "A. ⚙️ 환경설정 → 「참여코드 생성」 섹션 → 전체/학년/반 단위로 코드 생성 → QR 이미지 표시\n   학생이 스마트폰 카메라로 QR을 스캔하면 해당 범위로 온라인 모드 자동 진입됩니다."),
        ("Q9. BGM을 끄고 싶어요.",
         "A. ⚙️ 환경설정 → 「🎵 배경음악 (BGM)」 → 체크박스 해제\n   또는 결과 화면에서도 개별적으로 조절할 수 있습니다."),
    ]

    for q, a in faqs:
        inner = [
            Paragraph(f"<b>{q}</b>", S["h3"]),
        ]
        for line in a.split("\n"):
            inner.append(Paragraph(f"  {line}", S["body"]))
        inner.append(sp(2))
        story.append(KeepTogether(inner))

    story.append(hr())
    story.append(sp(3))
    story.append(Paragraph("도전 四字成語  사용자 설명서  |  2026년 6월", S["footer"]))
    story.append(Paragraph("제작: Claude (Anthropic) × cjhong7  |  배포: https://cjhong7.github.io/idioms/", S["footer"]))

    return story


# ── PDF 빌드 ──────────────────────────────────────────────────
OUT = r"C:\Users\user\Desktop\2026 연구학교 관련\warp-project\four-character idiom\도전_四字成語_사용자설명서.pdf"

doc = BaseDocTemplate(
    OUT, pagesize=A4,
    leftMargin=MARGIN, rightMargin=MARGIN,
    topMargin=26*mm, bottomMargin=16*mm,
    title="도전 四字成語 사용자 설명서",
    author="cjhong7",
    subject="초등학생 사자성어 교육용 웹게임 사용 설명서",
)

# 표지 프레임 (헤더/푸터 없음)
cover_frame = Frame(0, 0, W, H, leftPadding=MARGIN, rightPadding=MARGIN,
                    topPadding=28*mm, bottomPadding=16*mm)
# 본문 프레임
body_frame = Frame(MARGIN, 14*mm, W - 2*MARGIN, H - 14*mm - 14*mm,
                   leftPadding=0, rightPadding=0, topPadding=6*mm, bottomPadding=0)

doc.addPageTemplates([
    PageTemplate(id="Cover", frames=[cover_frame], onPage=cover_page),
    PageTemplate(id="Body",  frames=[body_frame],  onPage=header_footer),
])

story = build_story()
# 표지는 Cover 템플릿, 이후는 Body
from reportlab.platypus import NextPageTemplate
story.insert(0, NextPageTemplate("Cover"))
# 표지 PageBreak 다음부터 Body 적용
# PageBreak 위치 찾아서 NextPageTemplate 삽입
for i, item in enumerate(story):
    if isinstance(item, PageBreak):
        story.insert(i, NextPageTemplate("Body"))
        break

doc.build(story)
print(f"PDF 생성 완료: {OUT}")
