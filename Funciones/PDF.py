from flask import Blueprint, Response, flash, redirect, session
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io
from Funciones.Conexion import get_connection, login_requerido

recibos_bp = Blueprint('recibos', __name__)

def generar_recibo_pdf(abono_data):
    """
    Genera un PDF del recibo de abono
    abono_data debe contener:
    - id_abono, monto_abonado, fecha, saldo_pendiente
    - cliente_nombre, total_factura, cobrador_nombre
    """
    
    # Crear buffer en memoria
    buffer = io.BytesIO()
    
    # Configurar documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=70,
        bottomMargin=50
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    titulo_style = ParagraphStyle(
        'TituloRecibo',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=10,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica-Bold'
    )
    
    # Estilo para subtítulo
    subtitulo_style = ParagraphStyle(
        'SubtituloRecibo',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#7f8c8d'),
        fontName='Helvetica'
    )
    
    # Estilo para información principal
    info_style = ParagraphStyle(
        'InfoRecibo',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=8,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#2c3e50'),
        fontName='Helvetica'
    )
    
    # Estilo para nota
    nota_style = ParagraphStyle(
        'NotaRecibo',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4,
        alignment=TA_LEFT,
        textColor=colors.HexColor('#7f8c8d'),
        fontName='Helvetica'
    )
    
    # Contenido del PDF
    story = []
    
    # Título
    titulo = Paragraph("RECIBO DE CONTROL", titulo_style)
    story.append(titulo)
    
    # Subtítulo
    subtitulo = Paragraph("ESPERA PUNTUALIDAD EN SUS ABONOS PARA SERVIRLE MEJOR", subtitulo_style)
    story.append(subtitulo)
    
    # Espaciado
    story.append(Spacer(1, 20))
    
    # Información principal en tabla para mejor formato
    data = [
        [f"No. {abono_data['id_abono']}", "", f"POR $ {abono_data['total_factura']:.2f}"],
        ["", "", ""],
        [f"Recibí de {abono_data['cliente_nombre']}", "", ""],
        ["", "", ""],
        [f"La suma de $ {abono_data['monto_abonado']:.2f}", "", f"Resta $ {abono_data['saldo_pendiente']:.2f}"],
        ["", "", ""],
    ]
    
    # Crear tabla principal
    tabla_principal = Table(data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
    tabla_principal.setStyle(TableStyle([
        # Bordes inferiores para campos a llenar
        ('LINEBELOW', (0,0), (0,0), 2, colors.black),  # No.
        ('LINEBELOW', (2,0), (2,0), 2, colors.black),  # POR $
        ('LINEBELOW', (0,2), (2,2), 2, colors.black),  # Recibí de
        ('LINEBELOW', (0,4), (0,4), 2, colors.black),  # La suma de
        ('LINEBELOW', (2,4), (2,4), 2, colors.black),  # Resta
        
        # Alineación
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        # Fuente
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 14),
        
        # Espaciado
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 10),
    ]))
    
    story.append(tabla_principal)
    story.append(Spacer(1, 30))
    
    # Fecha y lugar
    fecha_obj = datetime.strptime(abono_data['fecha'], '%Y-%m-%d') if isinstance(abono_data['fecha'], str) else abono_data['fecha']
    
    meses = [
        "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    
    fecha_texto = f"San Salvador, {fecha_obj.day} de {meses[fecha_obj.month]} del {fecha_obj.year}"
    
    fecha_para = Paragraph(fecha_texto, info_style)
    story.append(fecha_para)
    story.append(Spacer(1, 40))
    
    # Línea para firma del cobrador
    cobrador_data = [
        ["_" * 50],
        [f"COBRADOR: {abono_data['cobrador_nombre']}"]
    ]
    
    tabla_cobrador = Table(cobrador_data, colWidths=[4*inch])
    tabla_cobrador.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,1), (0,1), 'Helvetica-Bold'),
        ('FONTNAME', (0,0), (0,0), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (0,0), 5),
        ('TOPPADDING', (0,1), (0,1), 5),
    ]))
    
    story.append(tabla_cobrador)
    story.append(Spacer(1, 30))
    
    # Nota final
    nota_titulo = Paragraph("<b>NOTA:</b>", nota_style)
    story.append(nota_titulo)
    
    notas_texto = [
        "Si cambia de dirección avise al cobrador o a nuestra dirección",
        "No se devuelven abonos al recoger la mercadería por estar en",
        "Mora. No se abre otra cuenta sin cancelar la anterior.",
        "",
        "<b>CUANDO HAGA SU ABONO RECLAME SU RECIBO</b>"
    ]
    
    for nota in notas_texto:
        if nota:  # Si no está vacía
            nota_para = Paragraph(nota, nota_style)
            story.append(nota_para)
        else:
            story.append(Spacer(1, 6))
    
    # Construir PDF
    doc.build(story)
    
    # Obtener el PDF del buffer
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

@recibos_bp.route('/generar_recibo/<int:abono_id>')
@login_requerido
def generar_recibo(abono_id):
    """Genera y descarga el recibo PDF de un abono específico"""
    if session.get('rango') not in [2, 4]:  # Cliente o cobrador
        flash("Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Obtener información del abono
        cursor.execute("""
            SELECT 
                av.id_abono,
                av.monto_abonado,
                av.fecha,
                av.saldo_pendiente,
                av.mes_correspondiente,
                av.año_correspondiente,
                fv.total,
                fv.id_factura_venta,
                cli.nombre AS cliente_nombre,
                cli.apellido AS cliente_apellido,
                cob.nombre AS cobrador_nombre,
                cob.apellido AS cobrador_apellido
            FROM abono_venta av
            JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
            JOIN usuarios cli ON fv.id_cliente = cli.id
            LEFT JOIN usuarios cob ON fv.id_cobrador = cob.id
            WHERE av.id_abono = %s
        """, (abono_id,))
        
        abono = cursor.fetchone()
        
        if not abono:
            flash("Abono no encontrado.", "danger")
            return redirect('/home')
        
        # Verificar permisos
        if session.get('rango') == 2:  # Cliente
            # Verificar que el abono pertenece al cliente logueado
            cursor.execute("""
                SELECT COUNT(*) as count FROM abono_venta av
                JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
                WHERE av.id_abono = %s AND fv.id_cliente = %s
            """, (abono_id, session['user_id']))
            
            if cursor.fetchone()['count'] == 0:
                flash("No tienes acceso a este recibo.", "danger")
                return redirect('/mis_compras')
                
        elif session.get('rango') == 4:  # Cobrador
            # Verificar que el abono pertenece a una venta del cobrador
            cursor.execute("""
                SELECT COUNT(*) as count FROM abono_venta av
                JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
                WHERE av.id_abono = %s AND fv.id_cobrador = %s
            """, (abono_id, session['user_id']))
            
            if cursor.fetchone()['count'] == 0:
                flash("No tienes acceso a este recibo.", "danger")
                return redirect('/cobros')
        
        # Preparar datos para el PDF
        abono_data = {
            'id_abono': abono['id_abono'],
            'monto_abonado': float(abono['monto_abonado']),
            'fecha': abono['fecha'],
            'saldo_pendiente': float(abono['saldo_pendiente']),
            'total_factura': float(abono['total']),
            'cliente_nombre': f"{abono['cliente_nombre']} {abono['cliente_apellido'] or ''}".strip(),
            'cobrador_nombre': f"{abono['cobrador_nombre'] or 'Sin asignar'} {abono['cobrador_apellido'] or ''}".strip()
        }
        
        # Generar PDF
        pdf_data = generar_recibo_pdf(abono_data)
        
        # Crear respuesta HTTP
        
        response = Response(pdf_data, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename=recibo_abono_{abono_id}.pdf'
        
        return response
        
    except Exception as e:
        print(f"ERROR en generar_recibo: {str(e)}")
        flash(f"Error al generar recibo: {str(e)}", "danger")
        return redirect('/home')
        
    finally:
        cursor.close()
        conn.close()


# ================================
# TAMBIÉN AGREGA ESTA RUTA PARA VER EL PDF EN EL NAVEGADOR
# ================================

@recibos_bp.route('/ver_recibo/<int:abono_id>')
@login_requerido  
def ver_recibo(abono_id):
    """Muestra el recibo PDF en el navegador sin descargar"""
    if session.get('rango') not in [2, 4]:
        flash("Acceso denegado.", "danger")
        return redirect('/home')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Misma lógica de verificación que generar_recibo
        cursor.execute("""
            SELECT 
                av.id_abono,
                av.monto_abonado,
                av.fecha,
                av.saldo_pendiente,
                fv.total,
                cli.nombre AS cliente_nombre,
                cli.apellido AS cliente_apellido,
                cob.nombre AS cobrador_nombre,
                cob.apellido AS cobrador_apellido
            FROM abono_venta av
            JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
            JOIN usuarios cli ON fv.id_cliente = cli.id
            LEFT JOIN usuarios cob ON fv.id_cobrador = cob.id
            WHERE av.id_abono = %s
        """, (abono_id,))
        
        abono = cursor.fetchone()
        if not abono:
            flash("Abono no encontrado.", "danger")
            return redirect('/home')
        
        # Verificar permisos (misma lógica que generar_recibo)
        if session.get('rango') == 2:
            cursor.execute("""
                SELECT COUNT(*) as count FROM abono_venta av
                JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
                WHERE av.id_abono = %s AND fv.id_cliente = %s
            """, (abono_id, session['user_id']))
            
            if cursor.fetchone()['count'] == 0:
                flash("No tienes acceso a este recibo.", "danger")
                return redirect('/mis_compras')
                
        elif session.get('rango') == 4:
            cursor.execute("""
                SELECT COUNT(*) as count FROM abono_venta av
                JOIN factura_venta fv ON av.id_factura_venta = fv.id_factura_venta
                WHERE av.id_abono = %s AND fv.id_cobrador = %s
            """, (abono_id, session['user_id']))
            
            if cursor.fetchone()['count'] == 0:
                flash("No tienes acceso a este recibo.", "danger")
                return redirect('/cobros')
        
        # Preparar datos y generar PDF
        abono_data = {
            'id_abono': abono['id_abono'],
            'monto_abonado': float(abono['monto_abonado']),
            'fecha': abono['fecha'],
            'saldo_pendiente': float(abono['saldo_pendiente']),
            'total_factura': float(abono['total']),
            'cliente_nombre': f"{abono['cliente_nombre']} {abono['cliente_apellido'] or ''}".strip(),
            'cobrador_nombre': f"{abono['cobrador_nombre'] or 'Sin asignar'} {abono['cobrador_apellido'] or ''}".strip()
        }
        
        pdf_data = generar_recibo_pdf(abono_data)
        
        # Mostrar en navegador
        response = Response(pdf_data, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'inline; filename=recibo_abono_{abono_id}.pdf'
        
        return response
        
    except Exception as e:
        print(f"ERROR en ver_recibo: {str(e)}")
        flash(f"Error al mostrar recibo: {str(e)}", "danger")
        return redirect('/home')
        
    finally:
        cursor.close()
        conn.close()