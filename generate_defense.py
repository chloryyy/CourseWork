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

    # Цветовая схема
    BG_COLOR = PptxRGB(0x1B, 0x2A, 0x4A)       # тёмно-синий фон
    TITLE_COLOR = PptxRGB(0xFF, 0xFF, 0xFF)     # белый
    TEXT_COLOR = PptxRGB(0xE8, 0xE8, 0xE8)      # светло-серый
    ACCENT_COLOR = PptxRGB(0x4E, 0xC9, 0xB0)    # бирюзовый акцент
    LIGHT_BG = PptxRGB(0x22, 0x3A, 0x5E)        # чуть светлее фон для полос

    def add_bg(slide):
        """Заполнить фон слайда тёмно-синим."""
        bg = slide.background
        fill = bg.fill
        fill.solid()
        fill.fore_color.rgb = BG_COLOR

    def add_textbox(slide, left, top, width, height, text, font_size=20,
                    bold=False, color=TEXT_COLOR, alignment=PP_ALIGN.LEFT,
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

    def add_paragraph_to_tf(tf, text, font_size=20, bold=False,
                            color=TEXT_COLOR, alignment=PP_ALIGN.LEFT,
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

    def add_accent_line(slide, top):
        shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            PptxInches(0.8), PptxInches(top),
            PptxInches(2.0), PptxPt(4)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = ACCENT_COLOR
        shape.line.fill.background()

    def add_slide_number(slide, num):
        txBox = slide.shapes.add_textbox(
            PptxInches(12.5), PptxInches(7.0),
            PptxInches(0.7), PptxInches(0.4)
        )
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = str(num)
        p.font.size = PptxPt(12)
        p.font.color.rgb = PptxRGB(0x88, 0x88, 0xAA)
        p.font.name = 'Calibri'
        p.alignment = PP_ALIGN.RIGHT

    # ===== СЛАЙД 1 — Титульный =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    add_bg(slide)

    add_textbox(slide, 1.0, 0.8, 11.3, 0.6,
                'БЕЛОРУССКИЙ ГОСУДАРСТВЕННЫЙ УНИВЕРСИТЕТ ИНФОРМАТИКИ И РАДИОЭЛЕКТРОНИКИ',
                font_size=16, bold=False, color=PptxRGB(0x99, 0xAA, 0xCC),
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 1.0, 1.3, 11.3, 0.4,
                'Кафедра телекоммуникаций и информационных технологий',
                font_size=14, color=PptxRGB(0x99, 0xAA, 0xCC),
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 1.0, 2.0, 11.3, 0.5, 'КУРСОВАЯ РАБОТА',
                font_size=24, bold=True, color=ACCENT_COLOR,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 1.5, 3.0, 10.3, 1.8,
                'Современные протоколы динамической\nмаршрутизации для обеспечения\n'
                'киберустойчивости беспроводных\nсенсорных сетей',
                font_size=30, bold=True, color=TITLE_COLOR,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, 6.5, 5.5, 5.5, 1.2,
                'Выполнил: студент группы ______\n'
                'Проверил: ________________',
                font_size=16, color=TEXT_COLOR,
                alignment=PP_ALIGN.LEFT)

    add_textbox(slide, 5.0, 6.8, 3.3, 0.5, 'Минск 2025',
                font_size=16, color=PptxRGB(0x99, 0xAA, 0xCC),
                alignment=PP_ALIGN.CENTER)

    # ===== СЛАЙД 2 — Актуальность и цель =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7, 'Актуальность и цель работы',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 11.7, 5.5, '', font_size=20)
    tf.paragraphs[0].text = ''

    items = [
        ('Актуальность:', True, ACCENT_COLOR),
        ('• БСС — одна из ключевых технологий IoT (>29 млрд устройств к 2027 г.)', False, TEXT_COLOR),
        ('• Ресурсные ограничения узлов: энергия, память, вычислительная мощность', False, TEXT_COLOR),
        ('• Новые требования: мультимедийный трафик (видеонаблюдение) → QoS', False, TEXT_COLOR),
        ('• Рост киберугроз, нацеленных на протоколы маршрутизации', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Цель:', True, ACCENT_COLOR),
        ('Исследование современных протоколов динамической маршрутизации для БСС', False, TEXT_COLOR),
        ('с точки зрения обеспечения киберустойчивости', False, TEXT_COLOR),
    ]
    for text, bold, color in items:
        add_paragraph_to_tf(tf, text, font_size=20, bold=bold, color=color)

    add_slide_number(slide, 2)

    # ===== СЛАЙД 3 — Задачи =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7, 'Задачи исследования',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 11.7, 5.5, '', font_size=20)
    tf.paragraphs[0].text = ''

    tasks = [
        '1. Исследовать роль динамической маршрутизации в БСС\n'
        '   и специфику реализации в условиях ресурсных ограничений',
        '2. Проанализировать проблемы безопасности и киберустойчивости:\n'
        '   энергетический дефицит, типы трафика, перегрузка узлов',
        '3. Рассмотреть подходы к многокритериальной маршрутизации\n'
        '   (свёртка критериев, эволюционные алгоритмы, машинное обучение)',
        '4. Исследовать адаптацию IDS/IPS для сенсорных сетей',
        '5. Провести сравнительный анализ существующих протоколов\n'
        '   маршрутизации с точки зрения киберустойчивости',
    ]
    for t in tasks:
        add_paragraph_to_tf(tf, t, font_size=19, color=TEXT_COLOR,
                           space_before=PptxPt(12))

    add_slide_number(slide, 3)

    # ===== СЛАЙД 4 — Архитектура БСС =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'Архитектура БСС и энергетические ограничения',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 5.8, 5.5, '', font_size=18)
    tf.paragraphs[0].text = ''

    items_left = [
        ('Компоненты сенсорного узла:', True, ACCENT_COLOR),
        ('• Датчики (температура, влажность, видео)', False, TEXT_COLOR),
        ('• Микроконтроллер (4–100 МГц)', False, TEXT_COLOR),
        ('• Приёмопередатчик', False, TEXT_COLOR),
        ('• Батарея (1000–3000 мА·ч)', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Ключевой факт:', True, ACCENT_COLOR),
        ('Передача 1 бита ≈ 1000–3000×', False, TEXT_COLOR),
        ('энергии по сравнению с 1 операцией CPU', False, TEXT_COLOR),
    ]
    for text, bold, color in items_left:
        add_paragraph_to_tf(tf, text, font_size=18, bold=bold, color=color)

    _, tf2 = add_textbox(slide, 7.0, 1.5, 5.8, 5.5, '', font_size=18)
    tf2.paragraphs[0].text = ''

    items_right = [
        ('Время жизни маршрута:', True, ACCENT_COLOR),
        ('T = min(Eᵢ / rᵢ), i = 1..k', False, PptxRGB(0xFF, 0xD7, 0x00)),
        ('', False, TEXT_COLOR),
        ('где Eᵢ — остаточная энергия узла', False, TEXT_COLOR),
        ('      rᵢ — скорость расхода (зависит от трафика)', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Типы трафика:', True, ACCENT_COLOR),
        ('• Телеметрия → низкая нагрузка', False, TEXT_COLOR),
        ('• Видеопоток → в 50–100× больше энергии', False, TEXT_COLOR),
    ]
    for text, bold, color in items_right:
        add_paragraph_to_tf(tf2, text, font_size=18, bold=bold, color=color)

    add_slide_number(slide, 4)

    # ===== СЛАЙД 5 — Угрозы безопасности =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'Угрозы безопасности БСС',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 5.8, 5.5, '', font_size=18)
    tf.paragraphs[0].text = ''

    items_left = [
        ('Атаки на маршрутизацию:', True, ACCENT_COLOR),
        ('', False, TEXT_COLOR),
        ('⬥ Чёрная дыра — привлечение', False, TEXT_COLOR),
        ('  и отбрасывание трафика', False, TEXT_COLOR),
        ('⬥ Червоточина — скрытый канал', False, TEXT_COLOR),
        ('  между удалёнными узлами', False, TEXT_COLOR),
        ('⬥ Sybil — узел выдаёт себя', False, TEXT_COLOR),
        ('  за множество узлов', False, TEXT_COLOR),
        ('⬥ Sinkhole — создание «воронки»', False, TEXT_COLOR),
        ('  для перехвата данных', False, TEXT_COLOR),
    ]
    for text, bold, color in items_left:
        add_paragraph_to_tf(tf, text, font_size=18, bold=bold, color=color,
                           space_before=PptxPt(3))

    _, tf2 = add_textbox(slide, 7.0, 1.5, 5.8, 5.5, '', font_size=18)
    tf2.paragraphs[0].text = ''

    items_right = [
        ('Энергетические атаки:', True, ACCENT_COLOR),
        ('', False, TEXT_COLOR),
        ('⬥ Vampire attacks — создание', False, TEXT_COLOR),
        ('  циклических маршрутов', False, TEXT_COLOR),
        ('⬥ Denial-of-sleep — не дают', False, TEXT_COLOR),
        ('  узлам войти в спящий режим', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Эволюция угроз:', True, ACCENT_COLOR),
        ('⬥ Комбинированные атаки', False, TEXT_COLOR),
        ('⬥ Атаки с использованием ML', False, TEXT_COLOR),
        ('⬥ Атаки на цепочку поставок', False, TEXT_COLOR),
    ]
    for text, bold, color in items_right:
        add_paragraph_to_tf(tf2, text, font_size=18, bold=bold, color=color,
                           space_before=PptxPt(3))

    add_slide_number(slide, 5)

    # ===== СЛАЙД 6 — QoS и балансировка =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'QoS-маршрутизация и балансировка нагрузки',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 5.8, 5.5, '', font_size=18)
    tf.paragraphs[0].text = ''

    items = [
        ('Параметры QoS:', True, ACCENT_COLOR),
        ('• Сквозная задержка (delay)', False, TEXT_COLOR),
        ('• Джиттер', False, TEXT_COLOR),
        ('• Потери пакетов (loss ratio)', False, TEXT_COLOR),
        ('• Пропускная способность', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Конфликт критериев:', True, ACCENT_COLOR),
        ('QoS ↔ Время жизни сети', False, PptxRGB(0xFF, 0xD7, 0x00)),
        ('→ Многокритериальная оптимизация', False, TEXT_COLOR),
    ]
    for text, bold, color in items:
        add_paragraph_to_tf(tf, text, font_size=18, bold=bold, color=color)

    _, tf2 = add_textbox(slide, 7.0, 1.5, 5.8, 5.5, '', font_size=18)
    tf2.paragraphs[0].text = ''

    items2 = [
        ('Балансировка нагрузки:', True, ACCENT_COLOR),
        ('• «Эффект воронки» — перегрузка', False, TEXT_COLOR),
        ('  узлов вблизи базовой станции', False, TEXT_COLOR),
        ('• Многопутевая маршрутизация', False, TEXT_COLOR),
        ('• Избыточные шлюзы', False, TEXT_COLOR),
        ('• Адаптивное перераспределение', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Протоколы QoS:', True, ACCENT_COLOR),
        ('SPEED, MMSPEED, SAR', False, PptxRGB(0xFF, 0xD7, 0x00)),
    ]
    for text, bold, color in items2:
        add_paragraph_to_tf(tf2, text, font_size=18, bold=bold, color=color)

    add_slide_number(slide, 6)

    # ===== СЛАЙД 7 — Многокритериальная маршрутизация =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'Подходы к многокритериальной маршрутизации',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    # Три блока
    blocks = [
        ('Свёртка критериев', [
            'F(P) = Σ wₖ·fₖ(P)',
            'Алгоритмы Дейкстры, Флойда',
            'Метод ε-ограничений',
            'Анализ иерархий (AHP)',
        ]),
        ('Эволюционные методы', [
            'NSGA-II (Парето-фронт)',
            'ACO (муравьиная колония)',
            'PSO (рой частиц)',
            'Распределённое выполнение',
        ]),
        ('Машинное обучение', [
            'Q-обучение / DQN',
            'Адаптация к динамике',
            'Федеративное обучение',
            'Обнаружение аномалий',
        ]),
    ]

    for i, (title, items) in enumerate(blocks):
        left = 0.8 + i * 4.2
        # Заголовок блока
        add_textbox(slide, left, 1.5, 3.8, 0.5, title,
                    font_size=22, bold=True, color=ACCENT_COLOR,
                    alignment=PP_ALIGN.CENTER)
        # Пункты
        _, tf = add_textbox(slide, left, 2.2, 3.8, 4.5, '', font_size=17)
        tf.paragraphs[0].text = ''
        for item in items:
            add_paragraph_to_tf(tf, f'• {item}', font_size=17, color=TEXT_COLOR,
                               space_before=PptxPt(8))

    add_slide_number(slide, 7)

    # ===== СЛАЙД 8 — IDS для БСС =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'Системы обнаружения вторжений для БСС',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 5.8, 5.5, '', font_size=18)
    tf.paragraphs[0].text = ''

    items = [
        ('Архитектуры IDS для БСС:', True, ACCENT_COLOR),
        ('• Распределённая — агенты на узлах', False, TEXT_COLOR),
        ('• Иерархическая — анализ на кластере', False, TEXT_COLOR),
        ('• Мобильная — перемещающиеся агенты', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Обнаружение аномалий:', True, ACCENT_COLOR),
        ('• Модель нормального поведения', False, TEXT_COLOR),
        ('• Не требует базы сигнатур', False, TEXT_COLOR),
        ('• Выявляет zero-day атаки', False, TEXT_COLOR),
    ]
    for text, bold, color in items:
        add_paragraph_to_tf(tf, text, font_size=18, bold=bold, color=color)

    _, tf2 = add_textbox(slide, 7.0, 1.5, 5.8, 5.5, '', font_size=18)
    tf2.paragraphs[0].text = ''

    items2 = [
        ('Метрики аномальности:', True, ACCENT_COLOR),
        ('• Объём трафика', False, TEXT_COLOR),
        ('• Паттерн передачи', False, TEXT_COLOR),
        ('• Скорость расхода энергии', False, TEXT_COLOR),
        ('• Стабильность маршрутов', False, TEXT_COLOR),
        ('', False, TEXT_COLOR),
        ('Лёгкие алгоритмы:', True, ACCENT_COLOR),
        ('CUSUM, EWMA, TinyML', False, PptxRGB(0xFF, 0xD7, 0x00)),
    ]
    for text, bold, color in items2:
        add_paragraph_to_tf(tf2, text, font_size=18, bold=bold, color=color)

    add_slide_number(slide, 8)

    # ===== СЛАЙД 9 — Сравнительный анализ =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7,
                'Сравнительный анализ протоколов',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    # Таблица
    rows, cols = 8, 7
    tbl_left = PptxInches(0.8)
    tbl_top = PptxInches(1.5)
    tbl_w = PptxInches(11.7)
    tbl_h = PptxInches(5.0)
    table_shape = slide.shapes.add_table(rows, cols, tbl_left, tbl_top, tbl_w, tbl_h)
    table = table_shape.table

    headers = ['Протокол', 'Тип', 'Энерго-\nэффект.', 'Масшт.', 'QoS',
               'Устойч.\nк атакам', 'Адаптивн.']
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
            p.font.color.rgb = PptxRGB(0x1B, 0x2A, 0x4A)
            p.font.name = 'Calibri'
            p.alignment = PP_ALIGN.CENTER
        cell.fill.solid()
        cell.fill.fore_color.rgb = ACCENT_COLOR

    for i, row_data in enumerate(data):
        for j, val in enumerate(row_data):
            cell = table.cell(i + 1, j)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = PptxPt(14)
                p.font.color.rgb = TEXT_COLOR
                p.font.name = 'Calibri'
                p.alignment = PP_ALIGN.CENTER
            cell.fill.solid()
            if i % 2 == 0:
                cell.fill.fore_color.rgb = PptxRGB(0x1F, 0x33, 0x55)
            else:
                cell.fill.fore_color.rgb = LIGHT_BG

    add_textbox(slide, 0.8, 6.7, 11.7, 0.5,
                'Н — низкая    С — средняя    В — высокая',
                font_size=14, color=PptxRGB(0x88, 0x88, 0xAA),
                alignment=PP_ALIGN.CENTER)

    add_slide_number(slide, 9)

    # ===== СЛАЙД 10 — Заключение =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)
    add_textbox(slide, 0.8, 0.4, 11.7, 0.7, 'Заключение',
                font_size=32, bold=True, color=TITLE_COLOR)
    add_accent_line(slide, 1.1)

    _, tf = add_textbox(slide, 0.8, 1.5, 11.7, 5.5, '', font_size=19)
    tf.paragraphs[0].text = ''

    conclusions = [
        '1. Время жизни маршрута — критический параметр, определяемый\n'
        '   остаточной энергией узлов и типом трафика',
        '2. Для мультимедийных приложений необходим одновременный учёт\n'
        '   QoS и времени жизни → многокритериальная оптимизация',
        '3. Обнаружение аномалий на основе анализа поведения — наиболее\n'
        '   перспективный подход к безопасности БСС',
        '4. Ни один протокол не обеспечивает высокие показатели по всем\n'
        '   критериям одновременно',
        '5. Перспективное направление — гибридные протоколы,\n'
        '   интегрирующие иерархическую организацию, многокритериальную\n'
        '   оптимизацию, механизмы доверия и облегчённые IDS',
    ]
    for c in conclusions:
        add_paragraph_to_tf(tf, c, font_size=19, color=TEXT_COLOR,
                           space_before=PptxPt(14))

    add_slide_number(slide, 10)

    # ===== СЛАЙД 11 — Спасибо за внимание =====
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_bg(slide)

    add_textbox(slide, 1.0, 2.5, 11.3, 1.5,
                'Спасибо за внимание!',
                font_size=44, bold=True, color=TITLE_COLOR,
                alignment=PP_ALIGN.CENTER)

    # Акцентная линия
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        PptxInches(5.0), PptxInches(4.0),
        PptxInches(3.3), PptxPt(4)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT_COLOR
    shape.line.fill.background()

    add_textbox(slide, 1.0, 4.5, 11.3, 0.8,
                'Готов ответить на ваши вопросы',
                font_size=24, color=TEXT_COLOR,
                alignment=PP_ALIGN.CENTER)

    add_slide_number(slide, 11)

    output = '/home/ubuntu/repos/CourseWork/Презентация_защита_курсовой.pptx'
    prs.save(output)
    print(f'Презентация сохранена: {output}')


if __name__ == '__main__':
    generate_report()
    generate_presentation()
