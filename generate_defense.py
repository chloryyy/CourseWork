#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор доклада (Word) и презентации (PPTX) для защиты курсовой работы.
Тема: «Современные протоколы динамической маршрутизации для обеспечения
киберустойчивости беспроводных сенсорных сетей»
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

from pptx import Presentation
from pptx.util import Inches as PptxInches, Pt as PptxPt, Emu as PptxEmu
from pptx.dml.color import RGBColor as PptxRGB
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


# =====================================================================
#                          ДОКЛАД (WORD)
# =====================================================================

def generate_report():
    doc = Document()

    # Стили
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    font.color.rgb = RGBColor(0, 0, 0)
    pf = style.paragraph_format
    pf.line_spacing = 1.5
    pf.space_after = Pt(0)
    pf.space_before = Pt(0)

    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(3)
        section.right_margin = Cm(1.5)

    def add_text(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, indent=True):
        p = doc.add_paragraph()
        p.alignment = align
        if indent:
            p.paragraph_format.first_line_indent = Cm(1.25)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = bold
        run.font.italic = italic
        return p

    def add_slide_mark(n):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(f'[Слайд {n}]')
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0, 0, 200)
        return p

    # ===== Заголовок =====
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('ДОКЛАД')
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(
        'к курсовой работе на тему:\n'
        '«Современные протоколы динамической маршрутизации\n'
        'для обеспечения киберустойчивости беспроводных сенсорных сетей»'
    )
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.italic = True

    doc.add_paragraph()

    # ===== Слайд 1 — Титульный =====
    add_slide_mark(1)

    add_text(
        'Уважаемые члены комиссии, вашему вниманию представляется курсовая '
        'работа на тему «Современные протоколы динамической маршрутизации '
        'для обеспечения киберустойчивости беспроводных сенсорных сетей».'
    )

    # ===== Слайд 2 — Актуальность и цель =====
    add_slide_mark(2)

    add_text(
        'Беспроводные сенсорные сети находят всё более широкое применение: '
        'от промышленного мониторинга и умного города до систем видеонаблюдения '
        'и здравоохранения. По прогнозам, к 2027 году количество IoT-устройств '
        'превысит 29 миллиардов, значительную часть которых составляют '
        'сенсорные узлы.'
    )

    add_text(
        'Ключевая проблема БСС — ограниченность ресурсов узлов: малая '
        'вычислительная мощность, небольшая память и, главное, ограниченный '
        'запас энергии. Эти ограничения непосредственно влияют на протоколы '
        'маршрутизации, от которых зависит надёжность и эффективность передачи данных.'
    )

    add_text(
        'Целью работы является исследование современных протоколов динамической '
        'маршрутизации для БСС с точки зрения обеспечения киберустойчивости, '
        'а также анализ подходов к многокритериальной маршрутизации и обнаружению '
        'вторжений в сенсорных сетях.'
    )

    # ===== Слайд 3 — Задачи =====
    add_slide_mark(3)

    add_text('Для достижения цели были поставлены следующие задачи:')

    tasks = [
        'исследовать роль динамической маршрутизации в БСС и специфику её '
        'реализации в условиях ресурсных ограничений;',
        'проанализировать проблемы безопасности и киберустойчивости, '
        'связанные с энергетическим дефицитом, типами трафика и перегрузкой узлов;',
        'рассмотреть подходы к многокритериальной маршрутизации;',
        'исследовать возможности адаптации систем обнаружения вторжений для БСС;',
        'провести сравнительный анализ существующих протоколов маршрутизации.'
    ]
    for i, t in enumerate(tasks, 1):
        add_text(f'{i}) {t}')

    # ===== Слайд 4 — Архитектура БСС и энергетические ограничения =====
    add_slide_mark(4)

    add_text(
        'Беспроводная сенсорная сеть — это распределённая самоорганизующаяся '
        'система из множества автономных узлов с датчиками, микроконтроллером, '
        'приёмопередатчиком и батареей. Основной поток данных направлен от '
        'сенсорных узлов к базовой станции через промежуточные узлы.'
    )

    add_text(
        'Энергопотребление узла определяется тремя компонентами: работа '
        'датчиков, обработка данных и передача по радиоканалу. Передача одного '
        'бита потребляет в 1000–3000 раз больше энергии, чем одна операция '
        'процессора. Поэтому время жизни маршрута становится критическим '
        'параметром и определяется двумя факторами: остаточной энергией узлов '
        'и типом передаваемого трафика.'
    )

    # ===== Слайд 5 — Проблемы безопасности =====
    add_slide_mark(5)

    add_text(
        'БСС подвержены широкому спектру атак. На сетевом уровне выделяются: '
        'атака «чёрная дыра» — скомпрометированный узел привлекает и отбрасывает '
        'трафик; «червоточина» — два удалённых узла создают скрытый канал, '
        'искажая топологию; Sybil-атака — узел выдаёт себя за множество узлов; '
        'а также атаки на истощение энергии, которые эксплуатируют протоколы '
        'маршрутизации для создания циклических маршрутов.'
    )

    add_text(
        'Эволюция угроз приводит к появлению комбинированных атак, '
        'одновременно воздействующих на несколько уровней сетевого стека. '
        'Атаки с использованием машинного обучения способны адаптироваться '
        'к работе систем защиты, минимизируя вероятность обнаружения.'
    )

    # ===== Слайд 6 — QoS и балансировка нагрузки =====
    add_slide_mark(6)

    add_text(
        'Современные приложения БСС, особенно видеонаблюдение, требуют '
        'обеспечения качества обслуживания: допустимой задержки, минимальных '
        'потерь пакетов, гарантированной пропускной способности. При этом '
        'маршрутизация должна одновременно максимизировать время жизни сети, '
        'что создаёт конфликт критериев.'
    )

    add_text(
        'Проблема перегрузки узлов вблизи базовой станции — так называемый '
        '«эффект воронки» — решается через многопутевую маршрутизацию, '
        'использование избыточных шлюзов и адаптивную балансировку нагрузки. '
        'Связь с киберустойчивостью: равномерное распределение нагрузки '
        'повышает устойчивость к отказам, а перегрузка может быть целью '
        'целенаправленных атак типа flooding.'
    )

    # ===== Слайд 7 — Многокритериальная маршрутизация =====
    add_slide_mark(7)

    add_text(
        'Задача маршрутизации в БСС является многокритериальной: необходимо '
        'одновременно оптимизировать время жизни маршрута, задержку, '
        'надёжность, энергоэффективность и безопасность. Основные подходы:'
    )

    add_text(
        'Первый — свёртка критериев: из вектора критериев формируется '
        'единый скалярный показатель через взвешенное суммирование, после чего '
        'применяются классические алгоритмы Дейкстры или Флойда-Уоршелла.'
    )

    add_text(
        'Второй — эволюционные алгоритмы: NSGA-II, муравьиной колонии, '
        'роя частиц — позволяют находить множество Парето-оптимальных решений.'
    )

    add_text(
        'Третий — методы машинного обучения: обучение с подкреплением '
        'позволяет узлам адаптивно выбирать маршруты, а федеративное обучение '
        'обеспечивает распределённое обучение без централизованного сбора данных.'
    )

    # ===== Слайд 8 — IDS для БСС =====
    add_slide_mark(8)

    add_text(
        'Классические системы обнаружения вторжений не могут быть напрямую '
        'перенесены в БСС из-за ресурсных ограничений. Для сенсорных сетей '
        'разработаны специализированные облегчённые архитектуры: распределённая '
        '(агенты на каждом узле), иерархическая (анализ на уровне кластера) '
        'и мобильная (перемещающиеся агенты).'
    )

    add_text(
        'Обнаружение аномалий является предпочтительным подходом для БСС. '
        'Оно основано на двух принципах: анализ поведения и сравнение с моделью '
        'нормы. Ключевые метрики: объём трафика, паттерн передачи, скорость '
        'расходования энергии, стабильность маршрутов. Применяются облегчённые '
        'статистические тесты — CUSUM и EWMA — способные работать на '
        'микроконтроллерах с минимальными затратами.'
    )

    # ===== Слайд 9 — Сравнительный анализ протоколов =====
    add_slide_mark(9)

    add_text(
        'В работе проведён сравнительный анализ протоколов маршрутизации БСС '
        'по шести критериям: энергоэффективность, масштабируемость, поддержка '
        'QoS, устойчивость к атакам, адаптивность и сложность реализации.'
    )

    add_text(
        'Классические протоколы — SPIN, LEACH, PEGASIS — оптимизируют '
        'энергоэффективность, но не обеспечивают защиту от атак. Протоколы '
        'с поддержкой QoS — SPEED — гарантируют задержку, но без механизмов '
        'безопасности. Специализированные протоколы — INSENS, SecRoute — '
        'обеспечивают устойчивость к атакам за счёт дополнительных накладных '
        'расходов. Ни один протокол не обеспечивает одновременно высокие '
        'показатели по всем критериям.'
    )

    # ===== Слайд 10 — Заключение =====
    add_slide_mark(10)

    add_text(
        'Подводя итоги, можно выделить следующие основные результаты работы.'
    )

    add_text(
        'Установлено, что время жизни маршрута является критическим параметром, '
        'определяемым остаточной энергией узлов и типом трафика. Для '
        'мультимедийных приложений необходим одновременный учёт QoS и '
        'времени жизни, что формирует задачу многокритериальной оптимизации.'
    )

    add_text(
        'Показано, что обнаружение аномалий на основе анализа поведения '
        'является наиболее перспективным подходом к обеспечению безопасности '
        'БСС, поскольку не требует значительных ресурсов и способно выявлять '
        'ранее неизвестные атаки.'
    )

    add_text(
        'Перспективным направлением является разработка гибридных протоколов, '
        'интегрирующих иерархическую организацию, многокритериальную '
        'оптимизацию, механизмы доверия и облегчённые IDS.'
    )

    # ===== Слайд 11 — Спасибо за внимание =====
    add_slide_mark(11)

    add_text(
        'Доклад окончен. Спасибо за внимание. Готов ответить на ваши вопросы.'
    )

    output = '/home/ubuntu/repos/CourseWork/Доклад_защита_курсовой.docx'
    doc.save(output)
    print(f'Доклад сохранён: {output}')


# =====================================================================
#                       ПРЕЗЕНТАЦИЯ (PPTX)
# =====================================================================

def generate_presentation():
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)

    # Цвета — белый фон, классический академический стиль
    DARK = PptxRGB(0x2D, 0x2D, 0x2D)            # основной текст
    BLUE = PptxRGB(0x1A, 0x47, 0x8A)            # заголовки
    ACCENT = PptxRGB(0xC0, 0x39, 0x2B)           # акцент (красноватый)
    GRAY = PptxRGB(0x66, 0x66, 0x66)             # подписи
    LIGHT_GRAY = PptxRGB(0xF2, 0xF2, 0xF2)      # фон блоков
    WHITE = PptxRGB(0xFF, 0xFF, 0xFF)
    TEAL = PptxRGB(0x16, 0x7F, 0x72)            # дополнительный акцент
    NODE_GREEN = PptxRGB(0x27, 0xAE, 0x60)
    NODE_ORANGE = PptxRGB(0xE6, 0x7E, 0x22)
    NODE_RED = PptxRGB(0xE7, 0x4C, 0x3C)
    LIGHT_BLUE_BG = PptxRGB(0xEB, 0xF5, 0xFB)

    def add_textbox(slide, left, top, width, height, text, font_size=20,
                    bold=False, color=DARK, alignment=PP_ALIGN.LEFT,
                    font_name='Calibri'):
        txBox = slide.shapes.add_textbox(
            PptxInches(left), PptxInches(top),
            PptxInches(width), PptxInches(height)
        )
        tf = txBox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = PptxPt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = alignment
        return txBox, tf

    def add_para(tf, text, font_size=20, bold=False,
                 color=DARK, alignment=PP_ALIGN.LEFT,
                 font_name='Calibri', space_before=PptxPt(6)):
        p = tf.add_paragraph()
        p.text = text
        p.font.size = PptxPt(font_size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = alignment
        p.space_before = space_before
        return p

    def add_header_bar(slide):
        """Тонкая синяя полоса сверху слайда."""
        bar = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            PptxInches(0), PptxInches(0),
            PptxInches(13.333), PptxPt(6)
        )
        bar.fill.solid()
        bar.fill.fore_color.rgb = BLUE
        bar.line.fill.background()

    def add_footer(slide, num):
        """Номер слайда и линия внизу."""
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            PptxInches(0.8), PptxInches(7.05),
            PptxInches(11.7), PptxPt(1)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = PptxRGB(0xCC, 0xCC, 0xCC)
        line.line.fill.background()
        add_textbox(slide, 12.2, 7.05, 0.8, 0.35, str(num),
                    font_size=11, color=GRAY, alignment=PP_ALIGN.RIGHT)

    def add_title(slide, text):
        add_textbox(slide, 0.8, 0.3, 11.7, 0.8, text,
                    font_size=28, bold=True, color=BLUE)

    def draw_circle(slide, left, top, size, fill_color, text='', text_size=10):
        """Нарисовать кружок (узел сети)."""
        shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            PptxInches(left), PptxInches(top),
            PptxInches(size), PptxInches(size)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        shape.line.color.rgb = PptxRGB(0x99, 0x99, 0x99)
        shape.line.width = PptxPt(1)
        if text:
            tf = shape.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = PptxPt(text_size)
            p.font.color.rgb = WHITE
            p.font.bold = True
            p.alignment = PP_ALIGN.CENTER
        return shape

    def draw_arrow(slide, x1, y1, x2, y2, color=PptxRGB(0x99, 0x99, 0x99)):
        """Нарисовать соединительную линию."""
        connector = slide.shapes.add_connector(
            1,  # straight connector
            PptxInches(x1), PptxInches(y1),
            PptxInches(x2), PptxInches(y2)
        )
        connector.line.color.rgb = color
        connector.line.width = PptxPt(1.5)
        return connector

    def draw_rounded_rect(slide, left, top, width, height, fill_color,
                          text='', text_size=14, text_color=DARK):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            PptxInches(left), PptxInches(top),
            PptxInches(width), PptxInches(height)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
        shape.line.color.rgb = PptxRGB(0xDD, 0xDD, 0xDD)
        shape.line.width = PptxPt(1)
        if text:
            tf = shape.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = text
            p.font.size = PptxPt(text_size)
            p.font.color.rgb = text_color
            p.font.bold = False
            p.alignment = PP_ALIGN.CENTER
            tf.paragraphs[0].space_before = PptxPt(0)
            tf.paragraphs[0].space_after = PptxPt(0)
        return shape

    # ================================================================
    #  СЛАЙД 1 — Титульный
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Верхняя синяя полоса (побольше для титульного)
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        PptxInches(0), PptxInches(0),
        PptxInches(13.333), PptxInches(2.3)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    add_textbox(slide, 0.8, 0.3, 11.7, 0.5,
                'БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ '
                'ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ',
                font_size=15, color=PptxRGB(0xBB, 0xCC, 0xDD),
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 0.8, 0.75, 11.7, 0.4,
                'Кафедра телекоммуникаций и информационных технологий',
                font_size=13, color=PptxRGB(0xBB, 0xCC, 0xDD),
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 0.8, 1.35, 11.7, 0.5, 'Курсовая работа',
                font_size=22, bold=True, color=WHITE,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 1.2, 2.8, 10.9, 1.6,
                'Современные протоколы динамической маршрутизации\n'
                'для обеспечения киберустойчивости\n'
                'беспроводных сенсорных сетей',
                font_size=28, bold=True, color=BLUE,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 7.0, 5.0, 5.5, 1.2,
                'Выполнил: студент группы ______\n'
                'Проверил: ________________',
                font_size=15, color=DARK)

    add_textbox(slide, 5.0, 6.7, 3.3, 0.5, 'Минск, 2025',
                font_size=14, color=GRAY, alignment=PP_ALIGN.CENTER)

    # ================================================================
    #  СЛАЙД 2 — Актуальность и цель
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Актуальность и цель работы')
    add_footer(slide, 2)

    _, tf = add_textbox(slide, 0.8, 1.3, 11.7, 5.5, '', font_size=19)
    tf.paragraphs[0].text = ''

    add_para(tf, 'Актуальность', font_size=21, bold=True, color=BLUE,
             space_before=PptxPt(4))
    add_para(tf, '- БСС (беспроводные сенсорные сети) — основа технологий '
             'IoT, более 29 млрд устройств к 2027 г.',
             font_size=18, space_before=PptxPt(8))
    add_para(tf, '- Ограниченные ресурсы узлов: энергия батареи, малая '
             'вычислительная мощность, небольшой объём памяти',
             font_size=18, space_before=PptxPt(6))
    add_para(tf, '- Новые применения (видеонаблюдение, промышленный '
             'мониторинг) требуют учёта качества обслуживания (QoS)',
             font_size=18, space_before=PptxPt(6))
    add_para(tf, '- Растущие киберугрозы, нацеленные именно на протоколы '
             'маршрутизации',
             font_size=18, space_before=PptxPt(6))

    add_para(tf, '', font_size=10, space_before=PptxPt(12))
    add_para(tf, 'Цель работы', font_size=21, bold=True, color=BLUE,
             space_before=PptxPt(4))
    add_para(tf, 'Исследование современных протоколов динамической '
             'маршрутизации для БСС с точки зрения обеспечения '
             'киберустойчивости, анализ подходов к многокритериальной '
             'маршрутизации и обнаружению вторжений.',
             font_size=18, space_before=PptxPt(8))

    # ================================================================
    #  СЛАЙД 3 — Задачи
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Задачи исследования')
    add_footer(slide, 3)

    tasks = [
        'Исследовать роль динамической маршрутизации в БСС '
        'и специфику реализации в условиях ресурсных ограничений',
        'Проанализировать проблемы безопасности и киберустойчивости: '
        'энергодефицит, типы трафика, перегрузка узлов',
        'Рассмотреть подходы к многокритериальной маршрутизации '
        '(свёртка критериев, эволюционные алгоритмы, машинное обучение)',
        'Исследовать адаптацию систем обнаружения вторжений (IDS) '
        'для сенсорных сетей',
        'Провести сравнительный анализ существующих протоколов '
        'маршрутизации БСС',
    ]
    for i, t in enumerate(tasks):
        top = 1.4 + i * 1.1
        # Номер в кружке
        num_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            PptxInches(0.8), PptxInches(top),
            PptxInches(0.45), PptxInches(0.45)
        )
        num_shape.fill.solid()
        num_shape.fill.fore_color.rgb = BLUE
        num_shape.line.fill.background()
        ntf = num_shape.text_frame
        ntf.paragraphs[0].text = str(i + 1)
        ntf.paragraphs[0].font.size = PptxPt(16)
        ntf.paragraphs[0].font.color.rgb = WHITE
        ntf.paragraphs[0].font.bold = True
        ntf.paragraphs[0].alignment = PP_ALIGN.CENTER

        add_textbox(slide, 1.5, top + 0.02, 10.5, 0.5, t,
                    font_size=18, color=DARK)

    # ================================================================
    #  СЛАЙД 4 — Архитектура БСС (с диаграммой сети)
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Архитектура БСС и энергоограничения')
    add_footer(slide, 4)

    # Левая часть — текст
    _, tf = add_textbox(slide, 0.8, 1.3, 5.5, 5.5, '', font_size=17)
    tf.paragraphs[0].text = ''

    add_para(tf, 'Сенсорный узел:', font_size=18, bold=True, color=BLUE,
             space_before=PptxPt(2))
    add_para(tf, '  Датчики + МК + радио + батарея', font_size=16,
             space_before=PptxPt(4))
    add_para(tf, '', font_size=8, space_before=PptxPt(4))
    add_para(tf, 'Передача 1 бита = 1000-3000x', font_size=16,
             bold=True, color=ACCENT, space_before=PptxPt(4))
    add_para(tf, 'энергии по сравнению с 1 операцией CPU', font_size=16,
             space_before=PptxPt(2))
    add_para(tf, '', font_size=8, space_before=PptxPt(8))
    add_para(tf, 'Время жизни маршрута:', font_size=18, bold=True,
             color=BLUE, space_before=PptxPt(4))
    add_para(tf, 'T = min(Ei / ri),  i = 1..k', font_size=17,
             bold=True, color=TEAL, space_before=PptxPt(6))
    add_para(tf, 'Ei - остаточная энергия узла', font_size=15,
             color=GRAY, space_before=PptxPt(4))
    add_para(tf, 'ri - скорость расхода (зависит от трафика)', font_size=15,
             color=GRAY, space_before=PptxPt(2))
    add_para(tf, '', font_size=8, space_before=PptxPt(8))
    add_para(tf, 'Видеопоток потребляет в 50-100 раз', font_size=16,
             space_before=PptxPt(4))
    add_para(tf, 'больше энергии, чем телеметрия', font_size=16,
             space_before=PptxPt(2))

    # Правая часть — схема топологии БСС
    # Фон для схемы
    bg_rect = draw_rounded_rect(slide, 6.8, 1.3, 5.8, 5.5, LIGHT_BLUE_BG)
    bg_rect.line.fill.background()

    add_textbox(slide, 7.0, 1.4, 5.4, 0.4,
                'Топология БСС (кластерная)', font_size=14,
                bold=True, color=BLUE, alignment=PP_ALIGN.CENTER)

    # Базовая станция (большой)
    draw_circle(slide, 9.3, 2.0, 0.6, ACCENT, 'БС', 12)

    # Кластерные головы
    ch_positions = [(7.6, 3.4), (9.3, 4.0), (11.0, 3.2)]
    for x, y in ch_positions:
        draw_circle(slide, x, y, 0.45, NODE_ORANGE, 'КГ', 10)
        draw_arrow(slide, x + 0.22, y, 9.6, 2.55, PptxRGB(0xBB, 0xBB, 0xBB))

    # Сенсорные узлы вокруг каждой КГ
    sensor_groups = [
        # Вокруг КГ1 (7.6, 3.4)
        [(7.1, 4.3), (7.8, 4.6), (7.0, 5.0), (8.2, 4.2)],
        # Вокруг КГ2 (9.3, 4.0)
        [(8.8, 5.0), (9.5, 5.2), (10.0, 4.8), (9.0, 5.5)],
        # Вокруг КГ3 (11.0, 3.2)
        [(11.4, 4.0), (10.6, 4.4), (11.6, 4.6), (11.0, 4.9)],
    ]
    for gi, group in enumerate(sensor_groups):
        ch_x, ch_y = ch_positions[gi]
        for sx, sy in group:
            draw_circle(slide, sx, sy, 0.3, NODE_GREEN, 'У', 8)
            draw_arrow(slide, sx + 0.15, sy,
                       ch_x + 0.22, ch_y + 0.45,
                       PptxRGB(0xCC, 0xCC, 0xCC))

    # Легенда
    draw_circle(slide, 7.2, 6.1, 0.22, ACCENT, '', 1)
    add_textbox(slide, 7.5, 6.08, 1.5, 0.3, 'Базовая станция',
                font_size=11, color=GRAY)
    draw_circle(slide, 9.0, 6.1, 0.22, NODE_ORANGE, '', 1)
    add_textbox(slide, 9.3, 6.08, 1.5, 0.3, 'Кластерная голова',
                font_size=11, color=GRAY)
    draw_circle(slide, 10.9, 6.1, 0.22, NODE_GREEN, '', 1)
    add_textbox(slide, 11.2, 6.08, 1.5, 0.3, 'Сенсорный узел',
                font_size=11, color=GRAY)

    # ================================================================
    #  СЛАЙД 5 — Угрозы безопасности (со схемой классификации)
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Угрозы безопасности маршрутизации в БСС')
    add_footer(slide, 5)

    # Визуальная классификация атак через цветные карточки
    # Строка 1 — Атаки на маршрутизацию
    add_textbox(slide, 0.8, 1.2, 5.0, 0.45, 'Атаки на маршрутизацию',
                font_size=18, bold=True, color=BLUE)

    attack_cards_row1 = [
        ('Чёрная дыра', 'Привлечение и\nотбрасывание трафика'),
        ('Червоточина', 'Скрытый туннель между\nудалёнными узлами'),
        ('Sybil-атака', 'Один узел выдаёт\nсебя за множество'),
        ('Sinkhole', 'Создание «воронки»\nдля перехвата данных'),
    ]
    for i, (title, desc) in enumerate(attack_cards_row1):
        left = 0.8 + i * 3.1
        card = draw_rounded_rect(slide, left, 1.8, 2.8, 1.6,
                                 PptxRGB(0xFD, 0xED, 0xED))
        tf = card.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = title
        tf.paragraphs[0].font.size = PptxPt(15)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = ACCENT
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = PptxPt(12)
        p.font.color.rgb = DARK
        p.alignment = PP_ALIGN.CENTER
        p.space_before = PptxPt(6)

    # Строка 2 — Энергетические атаки
    add_textbox(slide, 0.8, 3.7, 5.0, 0.45, 'Энергетические атаки',
                font_size=18, bold=True, color=BLUE)

    attack_cards_row2 = [
        ('Vampire attacks', 'Создание циклических\nмаршрутов для истощения'),
        ('Denial-of-sleep', 'Не позволяют узлам\nвойти в спящий режим'),
    ]
    for i, (title, desc) in enumerate(attack_cards_row2):
        left = 0.8 + i * 3.1
        card = draw_rounded_rect(slide, left, 4.3, 2.8, 1.6,
                                 PptxRGB(0xFE, 0xF5, 0xE7))
        tf = card.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = title
        tf.paragraphs[0].font.size = PptxPt(15)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = NODE_ORANGE
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = PptxPt(12)
        p.font.color.rgb = DARK
        p.alignment = PP_ALIGN.CENTER
        p.space_before = PptxPt(6)

    # Правый блок — эволюция угроз
    add_textbox(slide, 7.5, 3.7, 5.0, 0.45, 'Эволюция угроз',
                font_size=18, bold=True, color=BLUE)

    _, tf_evo = add_textbox(slide, 7.5, 4.3, 5.2, 2.5, '', font_size=16)
    tf_evo.paragraphs[0].text = ''
    add_para(tf_evo, '- Комбинированные атаки на несколько '
             'уровней стека', font_size=16, space_before=PptxPt(6))
    add_para(tf_evo, '- Атаки с использованием машинного '
             'обучения', font_size=16, space_before=PptxPt(6))
    add_para(tf_evo, '- FOTA-атаки через обновление '
             'прошивки', font_size=16, space_before=PptxPt(6))
    add_para(tf_evo, '- Атаки через IoT-инфраструктуру',
             font_size=16, space_before=PptxPt(6))

    # ================================================================
    #  СЛАЙД 6 — QoS и балансировка
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'QoS-маршрутизация и балансировка нагрузки')
    add_footer(slide, 6)

    # Левая часть
    _, tf = add_textbox(slide, 0.8, 1.3, 5.8, 3.0, '', font_size=17)
    tf.paragraphs[0].text = ''
    add_para(tf, 'Параметры QoS', font_size=19, bold=True, color=BLUE,
             space_before=PptxPt(2))
    add_para(tf, '- Сквозная задержка (end-to-end delay)', font_size=17,
             space_before=PptxPt(8))
    add_para(tf, '- Джиттер (вариация задержки)', font_size=17,
             space_before=PptxPt(5))
    add_para(tf, '- Коэффициент потерь пакетов', font_size=17,
             space_before=PptxPt(5))
    add_para(tf, '- Пропускная способность', font_size=17,
             space_before=PptxPt(5))

    # Правая часть
    _, tf2 = add_textbox(slide, 7.0, 1.3, 5.8, 3.0, '', font_size=17)
    tf2.paragraphs[0].text = ''
    add_para(tf2, 'Балансировка нагрузки', font_size=19, bold=True,
             color=BLUE, space_before=PptxPt(2))
    add_para(tf2, '- «Эффект воронки» — перегрузка узлов', font_size=17,
             space_before=PptxPt(8))
    add_para(tf2, '   вблизи базовой станции', font_size=17,
             space_before=PptxPt(2))
    add_para(tf2, '- Многопутевая маршрутизация', font_size=17,
             space_before=PptxPt(5))
    add_para(tf2, '- Использование избыточных шлюзов', font_size=17,
             space_before=PptxPt(5))

    # Ключевая мысль в рамке
    key_box = draw_rounded_rect(slide, 1.5, 4.8, 10.3, 1.2, LIGHT_BLUE_BG)
    key_box.line.color.rgb = BLUE
    key_box.line.width = PptxPt(1.5)
    tf_key = key_box.text_frame
    tf_key.word_wrap = True
    tf_key.paragraphs[0].text = ('Конфликт: обеспечение QoS требует лучших '
                                  'каналов, но их интенсивное использование '
                                  'ускоряет расход энергии.')
    tf_key.paragraphs[0].font.size = PptxPt(17)
    tf_key.paragraphs[0].font.color.rgb = BLUE
    tf_key.paragraphs[0].alignment = PP_ALIGN.CENTER
    p2 = tf_key.add_paragraph()
    p2.text = 'Протоколы: SPEED, MMSPEED, SAR'
    p2.font.size = PptxPt(16)
    p2.font.color.rgb = TEAL
    p2.font.bold = True
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = PptxPt(4)

    # ================================================================
    #  СЛАЙД 7 — Многокритериальная маршрутизация
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Подходы к многокритериальной маршрутизации')
    add_footer(slide, 7)

    blocks = [
        ('Свёртка критериев', LIGHT_BLUE_BG, BLUE, [
            'F(P) = sum(wk * fk(P))',
            'Алгоритмы Дейкстры, Флойда',
            'Метод анализа иерархий',
        ]),
        ('Эволюционные методы', PptxRGB(0xE8, 0xF8, 0xF5), TEAL, [
            'NSGA-II (Парето-фронт)',
            'ACO (муравьиная колония)',
            'PSO (рой частиц)',
        ]),
        ('Машинное обучение', PptxRGB(0xFD, 0xED, 0xED), ACCENT, [
            'Q-обучение / DQN',
            'Федеративное обучение',
            'Адаптация в реальном времени',
        ]),
    ]

    for i, (title, bg_color, title_color, items) in enumerate(blocks):
        left = 0.8 + i * 4.1
        # Карточка
        card = draw_rounded_rect(slide, left, 1.3, 3.7, 4.8, bg_color)
        card.line.color.rgb = PptxRGB(0xDD, 0xDD, 0xDD)

        # Заголовок внутри карточки
        add_textbox(slide, left + 0.2, 1.5, 3.3, 0.5, title,
                    font_size=20, bold=True, color=title_color,
                    alignment=PP_ALIGN.CENTER)

        # Пункты
        _, tf = add_textbox(slide, left + 0.3, 2.3, 3.1, 3.5, '',
                            font_size=16)
        tf.paragraphs[0].text = ''
        for item in items:
            add_para(tf, '- ' + item, font_size=16, color=DARK,
                     space_before=PptxPt(10))

    # ================================================================
    #  СЛАЙД 8 — IDS для БСС
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Системы обнаружения вторжений для БСС')
    add_footer(slide, 8)

    # Левая часть — архитектуры
    _, tf = add_textbox(slide, 0.8, 1.3, 5.8, 3.0, '', font_size=17)
    tf.paragraphs[0].text = ''
    add_para(tf, 'Архитектуры IDS', font_size=19, bold=True, color=BLUE,
             space_before=PptxPt(2))
    add_para(tf, '- Распределённая — лёгкие агенты на каждом узле',
             font_size=17, space_before=PptxPt(8))
    add_para(tf, '- Иерархическая — анализ на уровне кластерной головы',
             font_size=17, space_before=PptxPt(5))
    add_para(tf, '- Мобильная — перемещающиеся агенты-мониторы',
             font_size=17, space_before=PptxPt(5))
    add_para(tf, '', font_size=8, space_before=PptxPt(8))
    add_para(tf, 'Почему обнаружение аномалий?', font_size=19,
             bold=True, color=BLUE, space_before=PptxPt(2))
    add_para(tf, '- Не требует базы сигнатур (экономия памяти)',
             font_size=17, space_before=PptxPt(6))
    add_para(tf, '- Способно выявлять zero-day атаки',
             font_size=17, space_before=PptxPt(5))
    add_para(tf, '- Использует предсказуемость поведения БСС',
             font_size=17, space_before=PptxPt(5))

    # Правая часть — метрики в карточках
    add_textbox(slide, 7.2, 1.3, 5.3, 0.45, 'Метрики аномальности',
                font_size=19, bold=True, color=BLUE)

    metrics = [
        ('Объём трафика', 'Резкий рост — flooding'),
        ('Паттерн передачи', 'Нетипичная активность'),
        ('Расход энергии', 'Ускоренный — denial-of-sleep'),
        ('Стабильность маршрутов', 'Частые изменения — sinkhole'),
    ]
    for i, (metric, hint) in enumerate(metrics):
        top = 2.0 + i * 1.15
        card = draw_rounded_rect(slide, 7.2, top, 5.3, 0.95, LIGHT_BLUE_BG)
        tf = card.text_frame
        tf.word_wrap = True
        tf.paragraphs[0].text = metric
        tf.paragraphs[0].font.size = PptxPt(16)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = BLUE
        tf.paragraphs[0].alignment = PP_ALIGN.LEFT
        p = tf.add_paragraph()
        p.text = hint
        p.font.size = PptxPt(13)
        p.font.color.rgb = GRAY
        p.alignment = PP_ALIGN.LEFT
        p.space_before = PptxPt(2)

    # Внизу — лёгкие алгоритмы
    add_textbox(slide, 7.2, 6.3, 5.3, 0.45,
                'Лёгкие алгоритмы: CUSUM, EWMA, TinyML',
                font_size=16, bold=True, color=TEAL)

    # ================================================================
    #  СЛАЙД 9 — Сравнительный анализ (таблица)
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Сравнительный анализ протоколов')
    add_footer(slide, 9)

    rows, cols = 8, 7
    tbl_left = PptxInches(0.8)
    tbl_top = PptxInches(1.3)
    tbl_w = PptxInches(11.7)
    tbl_h = PptxInches(5.2)
    table_shape = slide.shapes.add_table(
        rows, cols, tbl_left, tbl_top, tbl_w, tbl_h
    )
    table = table_shape.table

    headers = ['Протокол', 'Тип', 'Энерго-\nэффект.',
               'Масшт.', 'QoS', 'Устойч.\nк атакам', 'Адаптивн.']
    data = [
        ['SPIN', 'Плоский', 'С', 'Н', 'Н', 'Н', 'С'],
        ['LEACH', 'Иерарх.', 'В', 'С', 'Н', 'Н', 'С'],
        ['PEGASIS', 'Иерарх.', 'В', 'Н', 'Н', 'Н', 'Н'],
        ['GPSR', 'Геогр.', 'С', 'В', 'Н', 'Н', 'В'],
        ['SPEED', 'QoS', 'С', 'С', 'В', 'Н', 'В'],
        ['INSENS', 'Безоп.', 'С', 'С', 'Н', 'В', 'С'],
        ['SecRoute', 'Безоп.', 'С', 'С', 'С', 'В', 'В'],
    ]

    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.text = h
        for p in cell.text_frame.paragraphs:
            p.font.size = PptxPt(14)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.font.name = 'Calibri'
            p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE

    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = PptxPt(14)
                p.font.color.rgb = DARK
                p.font.name = 'Calibri'
                p.alignment = PP_ALIGN.CENTER
            cell.fill.solid()
            if i % 2 == 0:
                cell.fill.fore_color.rgb = LIGHT_GRAY
            else:
                cell.fill.fore_color.rgb = WHITE

    add_textbox(slide, 0.8, 6.65, 11.7, 0.35,
                'Н — низкая    С — средняя    В — высокая',
                font_size=13, color=GRAY, alignment=PP_ALIGN.CENTER)

    # ================================================================
    #  СЛАЙД 10 — Заключение
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_header_bar(slide)
    add_title(slide, 'Заключение')
    add_footer(slide, 10)

    conclusions = [
        'Время жизни маршрута — критический параметр, определяемый '
        'остаточной энергией узлов и типом передаваемого трафика.',
        'Для мультимедийных приложений необходим одновременный учёт '
        'QoS и времени жизни сети, что формирует задачу '
        'многокритериальной оптимизации.',
        'Обнаружение аномалий на основе анализа поведения — наиболее '
        'перспективный подход к обеспечению безопасности БСС.',
        'Ни один из существующих протоколов не обеспечивает высокие '
        'показатели по всем критериям одновременно.',
        'Перспективное направление — гибридные протоколы, '
        'интегрирующие иерархическую организацию, многокритериальную '
        'оптимизацию, механизмы доверия и облегчённые IDS.',
    ]
    for i, c in enumerate(conclusions):
        top = 1.3 + i * 1.1
        # Номер
        num_shape = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            PptxInches(0.8), PptxInches(top),
            PptxInches(0.4), PptxInches(0.4)
        )
        num_shape.fill.solid()
        num_shape.fill.fore_color.rgb = TEAL
        num_shape.line.fill.background()
        ntf = num_shape.text_frame
        ntf.paragraphs[0].text = str(i + 1)
        ntf.paragraphs[0].font.size = PptxPt(15)
        ntf.paragraphs[0].font.color.rgb = WHITE
        ntf.paragraphs[0].font.bold = True
        ntf.paragraphs[0].alignment = PP_ALIGN.CENTER

        add_textbox(slide, 1.4, top, 11.0, 0.6, c,
                    font_size=17, color=DARK)

    # ================================================================
    #  СЛАЙД 11 — Спасибо за внимание
    # ================================================================
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    # Синяя полоса сверху
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        PptxInches(0), PptxInches(0),
        PptxInches(13.333), PptxInches(2.0)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    add_textbox(slide, 1.0, 0.5, 11.3, 1.0,
                'Спасибо за внимание!',
                font_size=40, bold=True, color=WHITE,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 1.0, 3.0, 11.3, 0.8,
                'Готов ответить на ваши вопросы',
                font_size=22, color=GRAY,
                alignment=PP_ALIGN.CENTER)

    output = '/home/ubuntu/repos/CourseWork/Презентация_защита_курсовой.pptx'
    prs.save(output)
    print(f'Презентация сохранена: {output}')


if __name__ == '__main__':
    generate_report()
    generate_presentation()
