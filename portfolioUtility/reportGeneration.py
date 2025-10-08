# portfolio_utils/report_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

class ReportGenerator:
    def __init__(self, output_path="portfolio_report.pdf"):
        self.output_path = output_path
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "TitleStyle",
            parent=self.styles["Heading1"],
            fontSize=20,
            alignment=1,  # center
            textColor=colors.darkblue,
            spaceAfter=20
        )
        self.section_title = ParagraphStyle(
            "SectionTitle",
            parent=self.styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#003366"),
            spaceAfter=10
        )
        self.normal = self.styles["Normal"]

    def generate(self, metrics, holdings):
        """
        metrics: dict from PortfolioCalculator
        holdings: dict {symbol: quantity}
        """
        doc = SimpleDocTemplate(self.output_path, pagesize=A4)
        elements = []

        # Title
        title = Paragraph(f"📊 Portfolio Performance Report", self.title_style)
        elements.append(title)

        # Date
        date_str = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        elements.append(Paragraph(f"Generated on: {date_str}", self.normal))
        elements.append(Spacer(1, 12))

        # Portfolio Summary
        elements.append(Paragraph("Portfolio Summary", self.section_title))
        summary_data = [
            ["Metric", "Value"],
            ["Total Value", f"${metrics['portfolio_value']:.2f}"],
            ["Profit / Loss", f"${metrics['profit_loss']:.2f}"],
            ["Growth", f"{metrics['growth']*100:.2f}%"],
            ["Volatility (annualized)", f"{metrics['volatility']*100:.2f}%"],
        ]
        table = Table(summary_data, hAlign="LEFT", colWidths=[200, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('BOX', (0, 0), (-1, -1), 1, colors.gray),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

        # Per-stock details
        elements.append(Paragraph("Per-Stock Metrics", self.section_title))
        stock_table_data = [["Symbol", "Quantity", "Max Drawdown", "Value at Risk (95%)"]]
        for symbol in holdings:
            dd = metrics["max_drawdown"].get(symbol, 0)
            var = metrics["value_at_risk"].get(symbol, 0)
            qty = holdings[symbol]
            stock_table_data.append([
                symbol,
                str(qty),
                f"{dd*100:.2f}%",
                f"{var*100:.2f}%"
            ])

        stock_table = Table(stock_table_data, hAlign="LEFT", colWidths=[120, 120, 150, 150])
        stock_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ]))
        elements.append(stock_table)
        elements.append(Spacer(1, 30))

        # Footer
        footer = Paragraph(
            "Report generated automatically by Portfolio Analyzer System.",
            ParagraphStyle("Footer", parent=self.normal, fontSize=8, textColor=colors.gray)
        )
        elements.append(footer)

        # Build the PDF
        doc.build(elements)
        print(f"✅ Report generated successfully: {self.output_path}")
