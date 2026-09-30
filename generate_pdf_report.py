"""
PDF Generator for Customer Churn Prediction Project Report.
Uses ReportLab to generate a clean, publication-ready PDF document.
"""

from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, KeepTogether
)

def build_pdf():
    base_dir = Path(__file__).parent
    pdf_path = base_dir / "Customer_Churn_Project_Report.pdf"
    chart_image = base_dir / "outputs" / "evaluation_dashboard.png"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    bold_body = ParagraphStyle(
        'DocBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=1
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    td_center = ParagraphStyle(
        'TDCenter',
        parent=td_style,
        alignment=1
    )

    story = []

    # Title & Header
    story.append(Paragraph("Customer Churn Prediction & Risk Intelligence", title_style))
    story.append(Paragraph("Technical Whitepaper & Project Documentation | Tech Stack: Python, Scikit-Learn, Pandas, Flask", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=12))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Customer churn is a critical problem for subscription and service-based organizations. "
        "This project implements a lightweight, high-performance Data Science pipeline capable of predicting "
        "customer churn with <b>79.7% ROC-AUC</b>, isolating primary attrition drivers, and prescribing actionable "
        "retention workflows. The entire system executes on CPU in <b>under 2 seconds</b> without external dependencies.",
        body_style
    ))

    # 2. Dataset Overview
    story.append(Paragraph("2. Dataset Specifications", h1_style))
    story.append(Paragraph(
        "The model was trained on 1,200 customer profiles using an 80/20 stratified train/test split. "
        "The positive churn rate is 33.2%, providing a realistic class distribution.",
        body_style
    ))

    data_table_content = [
        [Paragraph("Feature", th_style), Paragraph("Type", th_style), Paragraph("Description", th_style), Paragraph("Sample Values", th_style)],
        [Paragraph("TenureMonths", td_style), Paragraph("Integer", td_style), Paragraph("Subscription duration in months", td_style), Paragraph("1 to 72 months", td_style)],
        [Paragraph("Contract", td_style), Paragraph("Categorical", td_style), Paragraph("Customer contract duration", td_style), Paragraph("Month-to-month, 1-yr, 2-yr", td_style)],
        [Paragraph("InternetService", td_style), Paragraph("Categorical", td_style), Paragraph("Connection infrastructure", td_style), Paragraph("Fiber optic, DSL, None", td_style)],
        [Paragraph("TechSupport", td_style), Paragraph("Categorical", td_style), Paragraph("Technical support status", td_style), Paragraph("Yes, No", td_style)],
        [Paragraph("MonthlyCharges", td_style), Paragraph("Float", td_style), Paragraph("Monthly billing amount", td_style), Paragraph("$18.00 - $120.00", td_style)],
        [Paragraph("TotalCharges", td_style), Paragraph("Float", td_style), Paragraph("Cumulative charges to date", td_style), Paragraph("$20.00 - $8,000.00", td_style)],
        [Paragraph("Churn", td_style), Paragraph("Binary (Target)", td_style), Paragraph("Target label (1 = Left, 0 = Stayed)", td_style), Paragraph("0 or 1", td_style)]
    ]

    t_data = Table(data_table_content, colWidths=[90, 85, 220, 140])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_data)
    story.append(Spacer(1, 10))

    # 3. Model Benchmark
    story.append(Paragraph("3. Machine Learning Model Benchmarking", h1_style))
    story.append(Paragraph(
        "Three distinct classification paradigms were trained using identical preprocessing via ColumnTransformer (StandardScaler for numerics, OneHotEncoder for categoricals):",
        body_style
    ))

    benchmark_content = [
        [Paragraph("Model", th_style), Paragraph("Type", th_style), Paragraph("Accuracy", th_style), Paragraph("Precision", th_style), Paragraph("Recall", th_style), Paragraph("ROC-AUC", th_style)],
        [Paragraph("<b>Logistic Regression ★</b>", td_style), Paragraph("Linear Log-Odds", td_style), Paragraph("76.7%", td_center), Paragraph("71.4%", td_center), Paragraph("50.0%", td_center), Paragraph("<b>0.797</b>", td_center)],
        [Paragraph("Random Forest", td_style), Paragraph("Ensemble Bagging", td_style), Paragraph("74.2%", td_center), Paragraph("70.5%", td_center), Paragraph("38.8%", td_center), Paragraph("0.761", td_center)],
        [Paragraph("Gradient Boosting", td_style), Paragraph("Ensemble Boosting", td_style), Paragraph("72.9%", td_center), Paragraph("60.9%", td_center), Paragraph("52.5%", td_center), Paragraph("0.760", td_center)]
    ]

    t_bench = Table(benchmark_content, colWidths=[120, 105, 75, 75, 75, 85])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # 4. Diagnostics & Visuals
    if chart_image.exists():
        story.append(KeepTogether([
            Paragraph("4. Performance Diagnostics & Driver Analysis", h1_style),
            Image(str(chart_image), width=520, height=360),
            Spacer(1, 8),
            Paragraph("<i>Figure 1: (Clockwise from top left) Model comparison, confusion matrix, ROC curves, and top statistical drivers of customer churn.</i>", ParagraphStyle('Cap', parent=body_style, fontSize=8, textColor=colors.HexColor('#64748b')))
        ]))

    # 5. Risk Tiers & Business Strategy
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. Prescriptive Retention Strategy", h1_style))
    tier_content = [
        [Paragraph("Risk Tier", th_style), Paragraph("Probability", th_style), Paragraph("Typical Profile", th_style), Paragraph("Prescribed Action", th_style)],
        [Paragraph("<b>LOW RISK</b>", td_style), Paragraph("< 35%", td_center), Paragraph("Tenure > 24m, 2-Yr contract", td_style), Paragraph("Standard engagement, loyalty perks", td_style)],
        [Paragraph("<b>MODERATE</b>", td_style), Paragraph("35% - 65%", td_center), Paragraph("Tenure 6-18m, 1-Yr contract", td_style), Paragraph("Proactive check-in, tech support trial", td_style)],
        [Paragraph("<b>HIGH RISK</b>", td_style), Paragraph("> 65%", td_center), Paragraph("Month-to-month, < 4m tenure", td_style), Paragraph("Immediate outreach, annual contract discount", td_style)]
    ]
    t_tier = Table(tier_content, colWidths=[90, 75, 170, 200])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f0fdf4'), colors.HexColor('#fefce8'), colors.HexColor('#fef2f2')]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_tier)

    doc.build(story)
    print(f"[+] Successfully generated PDF document at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()
