#!/usr/bin/env python3
"""
HIGH PRO - Gerador de Relatório de Performance em PDF
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import json
import io

class RelatorioPerformance:
    def __init__(self, dados):
        self.dados = dados
        self.nome_colaborador = dados.get('nome', 'Sem Nome')
        self.cargo = dados.get('cargo', '')
        self.email = dados.get('email', '')
        self.telefone = dados.get('telefone', '')
        self.media = dados.get('media', 0)
        self.skills = dados.get('skills', {})
        self.avaliacao = dados.get('avaliacao', {})

    def gerar_pdf(self, filename=None):
        """Gera PDF do relatório"""
        if not filename:
            filename = f"relatorio_performance_{self.nome_colaborador.replace(' ', '_')}.pdf"

        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch,
            title=f"Relatório - {self.nome_colaborador}"
        )

        elements = []
        styles = getSampleStyleSheet()

        # Estilos personalizados
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#0564FF'),
            spaceAfter=6,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )

        subtitulo_style = ParagraphStyle(
            'SubTitle',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#5A5A5A'),
            spaceAfter=12,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )

        secao_style = ParagraphStyle(
            'Secao',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=colors.HexColor('#1A1A1A'),
            spaceBefore=12,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        )

        # Header
        header_data = [
            ['HIGH PRO', f'Relatório de Performance'],
            ['SOLUTIONS', f'{datetime.now().strftime("%d/%m/%Y")}']
        ]
        header_table = Table(header_data, colWidths=[3*inch, 2.5*inch])
        header_table.setStyle(TableStyle([
            ('FONT', (0, 0), (0, 1), 'Helvetica-Bold', 14),
            ('FONT', (1, 0), (1, 1), 'Helvetica', 10),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#0564FF')),
            ('TEXTCOLOR', (0, 1), (0, 1), colors.HexColor('#8A8A8A')),
            ('ALIGN', (1, 0), (1, 1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('LINEBELOW', (0, 1), (-1, 1), 1, colors.HexColor('#E8ECF2')),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.3*inch))

        # Dados do Colaborador
        elements.append(Paragraph('Dados do Colaborador', secao_style))
        colab_data = [
            ['Nome:', self.nome_colaborador],
            ['Cargo:', self.cargo or '—'],
            ['Email:', self.email or '—'],
            ['Telemóvel:', self.telefone or '—'],
        ]
        colab_table = Table(colab_data, colWidths=[1.2*inch, 4.3*inch])
        colab_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#5A5A5A')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1A1A1A')),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#F8F9FC'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E8ECF2')),
        ]))
        elements.append(colab_table)
        elements.append(Spacer(1, 0.2*inch))

        # Pontuação Geral
        elements.append(Paragraph('Avaliação Geral', secao_style))
        score_data = [
            ['Pontuação Geral', f'{self.media}/100', 'Status'],
            ['Performance', f'{self.media}%', self._get_status(self.media)],
        ]
        score_table = Table(score_data, colWidths=[2*inch, 1.5*inch, 2*inch])

        status_cor = colors.HexColor('#10B981') if self.media >= 67 else (
            colors.HexColor('#F59E0B') if self.media >= 33 else colors.HexColor('#EF4444')
        )

        score_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0564FF')),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 1), (1, 1), status_cor),
            ('FONTSIZE', (1, 1), (1, 1), 12),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9FC')]),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E8ECF2')),
        ]))
        elements.append(score_table)
        elements.append(Spacer(1, 0.2*inch))

        # Competências
        elements.append(Paragraph('Competências Profissionais', secao_style))
        skills_data = [['Competência', 'Pontuação', 'Status']]

        for skill, pontos in sorted(self.skills.items()):
            status = 'Crítico' if pontos < 33 else ('Em Desenv.' if pontos < 67 else 'Forte')
            skills_data.append([skill, f'{pontos}%', status])

        skills_table = Table(skills_data, colWidths=[2.5*inch, 1.2*inch, 1.8*inch])
        skills_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 9),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0564FF')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9FC'), colors.white]),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E8ECF2')),
        ]))
        elements.append(skills_table)
        elements.append(Spacer(1, 0.2*inch))

        # Matriz de Performance
        matriz = self.avaliacao.get('matrizQuadrantes', {})
        elements.append(Paragraph('Matriz de Performance', secao_style))
        matriz_data = [
            ['Aspecto', 'Valor'],
            ['Força', str(matriz.get('forca', 0))],
            ['Oportunidade', str(matriz.get('oportunidade', 0))],
            ['Fraqueza', str(matriz.get('fraqueza', 0))],
            ['Ameaça', str(matriz.get('ameaca', 0))],
        ]
        matriz_table = Table(matriz_data, colWidths=[2.5*inch, 2*inch])
        matriz_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0564FF')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F8F9FC'), colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E8ECF2')),
        ]))
        elements.append(matriz_table)
        elements.append(Spacer(1, 0.3*inch))

        # Footer
        footer_text = Paragraph(
            'HIGH PRO Solutions • Controlo de Horas © 2026 • Todos os direitos reservados',
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#8A8A8A'),
                alignment=TA_CENTER
            )
        )
        elements.append(footer_text)

        # Build PDF
        doc.build(elements)

        if filename:
            with open(filename, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            print(f"PDF gerado: {filename}")

        return pdf_buffer.getvalue()

    def _get_status(self, score):
        if score >= 67:
            return 'Excelente'
        elif score >= 33:
            return 'Bom'
        else:
            return 'Crítico'


# Para testes locais
if __name__ == '__main__':
    dados_teste = {
        'nome': 'João Silva',
        'cargo': 'Operário',
        'email': 'joao@example.com',
        'telefone': '919001234',
        'media': 78,
        'skills': {
            'Liderança': 85,
            'Organização': 72,
            'Comunicação': 90,
            'Trabalho em Equipa': 88,
        },
        'avaliacao': {
            'matrizQuadrantes': {
                'forca': 5,
                'oportunidade': 3,
                'fraqueza': 1,
                'ameaca': 1
            }
        }
    }

    relatorio = RelatorioPerformance(dados_teste)
    relatorio.gerar_pdf()
    print("Relatório gerado com sucesso!")
