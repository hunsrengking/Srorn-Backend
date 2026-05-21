from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import datetime
from typing import Literal

# PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics

from app.config.db import get_db
from app.services import report_service

router = APIRouter()

COMPANY_NAME = "PRINCE TUFU SUPPORT SYSTEM"
REPORT_TITLE = "REPORT DATA"


# ===================== HELPER =====================
def format_date(value):
    if value is None or pd.isna(value):
        return ""
    try:
        return pd.to_datetime(value).strftime("%d-%b-%Y")  # dd-MMM-yyyy
    except Exception:
        return str(value)


def calc_col_widths(
    df: pd.DataFrame, max_width: float, font="Helvetica", font_size=9, padding=16
):
    # Calculate minimum required widths based on header texts
    min_widths = []
    for col in df.columns:
        header_text = str(col).replace("_", " ").title()
        w = pdfmetrics.stringWidth(header_text, "Helvetica-Bold", 10)
        # Ensure an absolute minimum width of 35 so tiny headers like "Id" don't get squished
        min_widths.append(max(w + padding, 35))
    
    # Calculate ideal maximum widths based on longest data in cells
    data_widths = []
    for col in df.columns:
        max_w = 0
        for val in df[col].astype(str):
            # Limit the characters checked to avoid ridiculously long string scaling
            val_str = val if len(val) < 100 else val[:100] + "..." 
            w = pdfmetrics.stringWidth(val_str, font, font_size)
            if w > max_w:
                max_w = w
        data_widths.append(max_w + padding)
        
    ideal_widths = [max(m, d) for m, d in zip(min_widths, data_widths)]
    total_ideal = sum(ideal_widths)
    
    # If it fits perfectly, use ideal widths
    if total_ideal <= max_width:
        return ideal_widths
        
    # Otherwise, it needs to shrink, but we shouldn't shrink below min_widths (headers)
    allocated = list(min_widths)
    remaining = max_width - sum(allocated)
    
    # Distribute the remaining space to columns that need more than their min_width
    if remaining > 0:
        extra_needed = [max(0, ideal - min_w) for ideal, min_w in zip(ideal_widths, min_widths)]
        total_extra = sum(extra_needed)
        if total_extra > 0:
            for i in range(len(allocated)):
                allocated[i] += (extra_needed[i] / total_extra) * remaining
    else:
        # Extremely rare: if max_width is somehow smaller than all headers combined
        scale = max_width / sum(min_widths)
        allocated = [w * scale for w in min_widths]
        
    return allocated


# ===================== ROUTES =====================
@router.get("/reports-testing")
def get_reports_testing(db: Session = Depends(get_db)):
    return db.execute(text("SELECT * FROM v_ticket_reports")).mappings().all()


@router.get("/reports")
def get_reports(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    return report_service.getReports(db, from_date, to_date, status)


@router.get("/reports/export")
def export_reports(
    from_date: str | None = Query(None),
    to_date: str | None = Query(None),
    status: str | None = Query(None),
    export_type: Literal["csv", "excel", "pdf"] = Query("csv", alias="type"),
    db: Session = Depends(get_db),
):
    reports = report_service.getReports(db, from_date, to_date, status)

    if not reports:
        raise HTTPException(status_code=404, detail="No report data found")

    df = pd.DataFrame(reports)

    # rename columns to standard
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

    # enforce column order
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
    if export_type == "pdf":
        return _export_pdf(df, from_date, to_date)


# ===================== CSV =====================
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


# ===================== EXCEL =====================
def _export_excel(df: pd.DataFrame, from_date: str | None, to_date: str | None):
    stream = io.BytesIO()

    with pd.ExcelWriter(stream, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Reports")  # type: ignore
        writer.sheets["Reports"] = worksheet

        header = workbook.add_format( # type: ignore
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
        sub_header = workbook.add_format( # type: ignore
            {
                "align": "center", 
                "font_size": 11, 
                "bg_color": "#F1F5F9",
                "font_color": "#475569",
                "border": 1,
                "border_color": "#CBD5E1",
            }
        )
        col_header = workbook.add_format( # type: ignore
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
        cell = workbook.add_format( # type: ignore
            {
                "border": 1, 
                "border_color": "#E2E8F0", 
                "valign": "vcenter"
            }
        )
        cell_right = workbook.add_format( # type: ignore
            {
                "border": 1, 
                "border_color": "#E2E8F0", 
                "align": "right", 
                "valign": "vcenter"
            }
        )
        date_cell = workbook.add_format( # type: ignore
            {
                "border": 1, 
                "border_color": "#E2E8F0", 
                "num_format": "dd-mmm-yyyy", 
                "valign": "vcenter"
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
                len(header_name), *(len(str(val)) for val in df[col_name].astype(str))
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


# ===================== PDF =====================
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
        "Meta", parent=styles["Normal"], alignment=1, fontSize=10, textColor=colors.HexColor("#475569"), spaceAfter=2
    )
    cell_style = ParagraphStyle(
        "Cell", parent=styles["Normal"], fontSize=9, leading=12, textColor=colors.HexColor("#334155")
    )
    header_style = ParagraphStyle(
        "Header",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.white,
        alignment=1,
        fontName="Helvetica-Bold",
    )

    # Header & Title
    elements.append(Paragraph(COMPANY_NAME, title_style))
    elements.append(Paragraph(REPORT_TITLE, subtitle_style))
    
    # Meta
    period = f"Period: {from_date or 'All time'} → {to_date or 'Present'}"
    generated = f"Generated: {datetime.datetime.now():%d-%b-%Y %H:%M:%S}"
    elements.append(Paragraph(period, meta_style))
    elements.append(Paragraph(generated, meta_style))
    elements.append(Spacer(1, 15))

    # Table data
    table_data = [[Paragraph(str(col).replace("_", " ").title(), header_style) for col in df.columns]]
    for _, row in df.iterrows():
        table_data.append([Paragraph(str(val), cell_style) for val in row])

    # Column widths responsive to header & body
    col_widths = calc_col_widths(df, doc.width)

    # Create table
    table = Table(table_data, colWidths=col_widths, repeatRows=1, hAlign="LEFT")

    # Table style
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
    for i, col in enumerate(df.columns):
        if pd.api.types.is_numeric_dtype(df[col]):
            style.add("ALIGN", (i, 1), (i, -1), "RIGHT")
    table.setStyle(style)
    elements.append(table)

    # Footer
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
