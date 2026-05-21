import datetime
import io
from typing import Literal

import pandas as pd
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.features.reports import service as report_service

COMPANY_NAME = "PRINCE TUFU SUPPORT SYSTEM"
REPORT_TITLE = "REPORT DATA"


class ReportController:
    @staticmethod
    def get_reports_testing(db: Session):
        return db.execute(text("SELECT * FROM v_ticket_reports")).mappings().all()

    @staticmethod
    def get_reports(
        db: Session,
        from_date: str | None = None,
        to_date: str | None = None,
        status: str | None = None,
    ):
        return report_service.getReports(db, from_date, to_date, status)

    @staticmethod
    def export_reports(
        db: Session,
        from_date: str | None,
        to_date: str | None,
        status: str | None,
        export_type: Literal["csv", "excel", "pdf"],
    ):
        reports = report_service.getReports(db, from_date, to_date, status)

        if not reports:
            raise HTTPException(status_code=404, detail="No report data found")

        df = pd.DataFrame(reports)
        df = df.rename(
            columns={
                "ID": "id",
                "Title": "title",
                "Department": "department",
                "Category": "category",
                "Priority": "priority",
                "Status": "status",
                "Assigned To": "assigned_to",
                "Created At": "create_date",
            }
        )
        df = df[
            [
                "id",
                "title",
                "department",
                "category",
                "priority",
                "status",
                "assigned_to",
                "create_date",
            ]
        ]

        if export_type == "csv":
            return _export_csv(df)
        if export_type == "excel":
            return _export_excel(df, from_date, to_date)
        return _export_pdf(df, from_date, to_date)


def format_date(value):
    if value is None or pd.isna(value):
        return ""
    try:
        return pd.to_datetime(value).strftime("%d-%b-%Y")
    except Exception:
        return str(value)


def calc_col_widths(
    df: pd.DataFrame,
    max_width: float,
    font="Helvetica",
    font_size=9,
    padding=16,
):
    min_widths = []
    for col in df.columns:
        header_text = str(col).replace("_", " ").title()
        width = pdfmetrics.stringWidth(header_text, "Helvetica-Bold", 10)
        min_widths.append(max(width + padding, 35))

    data_widths = []
    for col in df.columns:
        max_data_width = 0
        for value in df[col].astype(str):
            value_text = value if len(value) < 100 else value[:100] + "..."
            width = pdfmetrics.stringWidth(value_text, font, font_size)
            if width > max_data_width:
                max_data_width = width
        data_widths.append(max_data_width + padding)

    ideal_widths = [max(min_width, data_width) for min_width, data_width in zip(min_widths, data_widths)]
    total_ideal_width = sum(ideal_widths)

    if total_ideal_width <= max_width:
        return ideal_widths

    allocated = list(min_widths)
    remaining = max_width - sum(allocated)

    if remaining > 0:
        extra_needed = [
            max(0, ideal_width - min_width)
            for ideal_width, min_width in zip(ideal_widths, min_widths)
        ]
        total_extra = sum(extra_needed)
        if total_extra > 0:
            for index in range(len(allocated)):
                allocated[index] += (extra_needed[index] / total_extra) * remaining
    else:
        scale = max_width / sum(min_widths)
        allocated = [width * scale for width in min_widths]

    return allocated


def _export_csv(df: pd.DataFrame) -> StreamingResponse:
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(format_date)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=report.csv"
    return response


def _export_excel(df: pd.DataFrame, from_date: str | None, to_date: str | None):
    stream = io.BytesIO()

    with pd.ExcelWriter(stream, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Reports")  # type: ignore
        writer.sheets["Reports"] = worksheet

        header = workbook.add_format(  # type: ignore
            {
                "bold": True,
                "font_size": 16,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#1A365D",
                "font_color": "white",
                "border": 1,
                "border_color": "#1A365D",
            }
        )
        sub_header = workbook.add_format(  # type: ignore
            {
                "align": "center",
                "font_size": 11,
                "bg_color": "#F1F5F9",
                "font_color": "#475569",
                "border": 1,
                "border_color": "#CBD5E1",
            }
        )
        col_header = workbook.add_format(  # type: ignore
            {
                "bold": True,
                "align": "center",
                "valign": "vcenter",
                "bg_color": "#2563EB",
                "font_color": "white",
                "border": 1,
                "border_color": "#1E40AF",
            }
        )
        cell = workbook.add_format(  # type: ignore
            {
                "border": 1,
                "border_color": "#E2E8F0",
                "valign": "vcenter",
            }
        )
        cell_right = workbook.add_format(  # type: ignore
            {
                "border": 1,
                "border_color": "#E2E8F0",
                "align": "right",
                "valign": "vcenter",
            }
        )
        date_cell = workbook.add_format(  # type: ignore
            {
                "border": 1,
                "border_color": "#E2E8F0",
                "num_format": "dd-mmm-yyyy",
                "valign": "vcenter",
            }
        )

        last_col = len(df.columns) - 1
        worksheet.merge_range(0, 0, 0, last_col, f"{COMPANY_NAME} - REPORT", header)
        period = f"From: {from_date or 'All time'} | To: {to_date or 'Present'}"
        worksheet.merge_range(1, 0, 1, last_col, period, sub_header)

        for col, name in enumerate(df.columns):
            header_name = str(name).replace("_", " ").title()
            worksheet.write(3, col, header_name, col_header)

        for row_idx, row in enumerate(df.itertuples(index=False), start=4):
            for col_idx, value in enumerate(row):
                if isinstance(value, (pd.Timestamp, datetime.date, datetime.datetime)):
                    worksheet.write_datetime(row_idx, col_idx, value, date_cell)
                elif isinstance(value, (int, float)):
                    worksheet.write(row_idx, col_idx, value, cell_right)
                else:
                    worksheet.write(row_idx, col_idx, value, cell)

        for col_idx, col_name in enumerate(df.columns):
            header_name = str(col_name).replace("_", " ").title()
            max_length = max(
                len(header_name),
                *(len(str(value)) for value in df[col_name].astype(str)),
            )
            worksheet.set_column(col_idx, col_idx, min(max_length + 4, 40))

        worksheet.freeze_panes(4, 0)

    stream.seek(0)
    response = StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response.headers["Content-Disposition"] = "attachment; filename=report.xlsx"
    return response


def _export_pdf(df: pd.DataFrame, from_date: str | None, to_date: str | None):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].apply(format_date)

    stream = io.BytesIO()
    doc = SimpleDocTemplate(
        stream,
        pagesize=landscape(A4),
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
    )

    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=1,
        fontSize=22,
        textColor=colors.HexColor("#1A365D"),
        fontName="Helvetica-Bold",
        spaceAfter=6,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Heading2"],
        alignment=1,
        fontSize=14,
        textColor=colors.HexColor("#2563EB"),
        fontName="Helvetica-Bold",
        spaceAfter=12,
    )
    meta_style = ParagraphStyle(
        "Meta",
        parent=styles["Normal"],
        alignment=1,
        fontSize=10,
        textColor=colors.HexColor("#475569"),
        spaceAfter=2,
    )
    cell_style = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#334155"),
    )
    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.white,
        alignment=1,
        fontName="Helvetica-Bold",
    )

    elements.append(Paragraph(COMPANY_NAME, title_style))
    elements.append(Paragraph(REPORT_TITLE, subtitle_style))
    period = f"Period: {from_date or 'All time'} -> {to_date or 'Present'}"
    generated = f"Generated: {datetime.datetime.now():%d-%b-%Y %H:%M:%S}"
    elements.append(Paragraph(period, meta_style))
    elements.append(Paragraph(generated, meta_style))
    elements.append(Spacer(1, 15))

    table_data = [
        [
            Paragraph(str(col).replace("_", " ").title(), header_style)
            for col in df.columns
        ]
    ]
    for _, row in df.iterrows():
        table_data.append([Paragraph(str(value), cell_style) for value in row])

    col_widths = calc_col_widths(df, doc.width)
    table = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")

    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [colors.white, colors.HexColor("#F8FAFC")],
            ),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("WORDWRAP", (0, 0), (-1, -1), "CJK"),
        ]
    )
    for index, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            style.add("ALIGN", (index, 1), (index, -1), "RIGHT")
    table.setStyle(style)
    elements.append(table)

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(
            doc.pagesize[0] - doc.rightMargin,
            0.4 * inch,
            f"Page {canvas.getPageNumber()}",
        )

    doc.build(elements, onFirstPage=footer, onLaterPages=footer)

    stream.seek(0)
    response = StreamingResponse(stream, media_type="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=report.pdf"
    return response
