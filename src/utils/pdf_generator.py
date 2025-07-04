from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
from collections import Counter # Necessário para design2

# Remova: import sys; sys.stdout.reconfigure(encoding='utf-8')

def criar_pdf_design1(cursos, titulo="Relatório de Cursos"):
    """Cria PDF com design corporativo (Design 1)"""
    try:
        # Criar buffer em memória
        buffer = io.BytesIO()
        
        # Configurar documento
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        titulo_style = ParagraphStyle(
            'TituloCustom',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.Color(0.545, 0, 0)  # Cor Unyleya
        )
        
        # Estilo para subtítulo
        subtitulo_style = ParagraphStyle(
            'SubtituloCustom',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        # Elementos do PDF
        elementos = []
        
        # Cabeçalho
        elementos.append(Paragraph("UNYLEYA", titulo_style))
        elementos.append(Paragraph(titulo, subtitulo_style))
        elementos.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}", 
                                  styles['Normal']))
        elementos.append(Spacer(1, 20))
        
        # Estatísticas
        total_cursos = len(cursos)
        areas_unicas = len(set(curso['area'] for curso in cursos if curso['area']))
        metodologias_unicas = len(set(curso['metodologia'] for curso in cursos))
        
        stats_data = [
            ['Estatísticas do Relatório', ''],
            ['Total de Cursos:', str(total_cursos)],
            ['Áreas Diferentes:', str(areas_unicas)],
            ['Metodologias Diferentes:', str(metodologias_unicas)]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 1*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.545, 0, 0)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elementos.append(stats_table)
        elementos.append(Spacer(1, 30))
        
        # Tabela de cursos
        elementos.append(Paragraph("Lista de Cursos", styles['Heading2']))
        elementos.append(Spacer(1, 10))
        
        # Cabeçalhos da tabela
        dados_tabela = [['#', 'Nome do Curso', 'Área', 'Metodologia', 'Faixa']]
        
        # Adicionar cursos
        for i, curso in enumerate(cursos, 1):
            dados_tabela.append([
                str(i),
                curso['nome'][:40] + '...' if len(curso['nome']) > 40 else curso['nome'],
                curso['area'] or 'N/A',
                curso['metodologia'],
                curso['faixa']
            ])
        
        # Criar tabela
        tabela = Table(dados_tabela, colWidths=[0.5*inch, 3*inch, 1.2*inch, 1*inch, 1*inch])
        tabela.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.545, 0, 0)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Dados
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            
            # Zebra striping
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))
        
        # Aplicar zebra striping manualmente
        for i in range(1, len(dados_tabela)):
            if i % 2 == 0:
                tabela.setStyle(TableStyle([
                    ('BACKGROUND', (0, i), (-1, i), colors.lightgrey)
                ]))
        
        elementos.append(tabela)
        
        # Rodapé
        elementos.append(Spacer(1, 30))
        elementos.append(Paragraph("Sistema de Gestão de Cursos - Unyleya", 
                                  styles['Normal']))
        
        # Gerar PDF
        doc.build(elementos)
        
        # Retornar buffer
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF (Design 1): {e}")
        raise # Re-lança a exceção para ser capturada na rota

def criar_pdf_design2(cursos, titulo="Relatório Avançado de Cursos"):
    """Cria PDF com design moderno (Design 2)"""
    try:
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        titulo_principal = ParagraphStyle(
            'TituloPrincipal',
            parent=styles['Title'],
            fontSize=28,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=colors.Color(0.2, 0.2, 0.8)
        )
        
        subtitulo_moderno = ParagraphStyle(
            'SubtituloModerno',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=25,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        
        elementos = []
        
        # Cabeçalho moderno
        elementos.append(Paragraph("📚 UNYLEYA ANALYTICS", titulo_principal))
        elementos.append(Paragraph(titulo, subtitulo_moderno))
        
        # Linha decorativa
        linha_data = [['', '', '', '', '']]
        linha_table = Table(linha_data, colWidths=[1*inch]*5)
        linha_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (-1, 0), 3, colors.Color(0.2, 0.2, 0.8)),
        ]))
        elementos.append(linha_table)
        elementos.append(Spacer(1, 20))
        
        # Dashboard de estatísticas
        total_cursos = len(cursos)
        areas = [curso['area'] for curso in cursos if curso['area']]
        metodologias = [curso['metodologia'] for curso in cursos]
        faixas = [curso['faixa'] for curso in cursos]
        
        # Contar ocorrências
        
        contador_areas = Counter(areas)
        contador_metodologias = Counter(metodologias)
        contador_faixas = Counter(faixas)
        
        # Dashboard em formato de cards
        dashboard_data = [
            ['📊 DASHBOARD EXECUTIVO', '', '', ''],
            ['Total de Cursos', str(total_cursos), 'Áreas Únicas', str(len(contador_areas))],
            ['Metodologias', str(len(contador_metodologias)), 'Faixas Diferentes', str(len(contador_faixas))],
        ]
        
        dashboard_table = Table(dashboard_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch])
        dashboard_table.setStyle(TableStyle([
            # Título
            ('SPAN', (0, 0), (-1, 0)),
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.2, 0.8)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            
            # Dados
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.darkblue),
        ]))
        
        elementos.append(dashboard_table)
        elementos.append(Spacer(1, 30))
        
        # Análise por metodologia
        elementos.append(Paragraph("📈 Distribuição por Metodologia", styles['Heading2']))
        elementos.append(Spacer(1, 10))
        
        metodologia_data = [['Metodologia', 'Quantidade', 'Percentual']]
        for metodologia, count in contador_metodologias.most_common():
            percentual = (count / total_cursos) * 100
            metodologia_data.append([metodologia, str(count), f"{percentual:.1f}%"])
        
        metodologia_table = Table(metodologia_data, colWidths=[2*inch, 1*inch, 1*inch])
        metodologia_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elementos.append(metodologia_table)
        elementos.append(PageBreak())
        
        # Lista detalhada de cursos
        elementos.append(Paragraph("📋 Lista Completa de Cursos", styles['Heading2']))
        elementos.append(Spacer(1, 15))
        
        # Tabela principal
        cursos_data = [['ID', 'Nome do Curso', 'Área', 'Metodologia', 'Faixa']]
        
        for i, curso in enumerate(cursos, 1):
            nome_curso = curso['nome']
            if len(nome_curso) > 35:
                nome_curso = nome_curso[:35] + '...'
            
            cursos_data.append([
                str(i),
                nome_curso,
                curso['area'] or 'Não definida',
                curso['metodologia'],
                curso['faixa']
            ])
        
        cursos_table = Table(cursos_data, colWidths=[0.4*inch, 2.8*inch, 1.3*inch, 0.8*inch, 0.8*inch])
        cursos_table.setStyle(TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.2, 0.2, 0.8)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            
            # Dados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternating colors
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))
        
        # Aplicar cores alternadas
        for i in range(1, len(cursos_data)):
            if i % 2 == 0:
                cursos_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, i), (-1, i), colors.Color(0.95, 0.95, 1))
                ]))
        
        elementos.append(cursos_table)
        
        # Rodapé
        elementos.append(Spacer(1, 30))
        rodape_data = [[f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')} | Sistema Unyleya"]]
        rodape_table = Table(rodape_data, colWidths=[6*inch])
        rodape_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ]))
        elementos.append(rodape_table)
        
        doc.build(elementos)
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Erro ao gerar PDF (Design 2): {e}")
        raise # Re-lança a exceção para ser capturada na rota