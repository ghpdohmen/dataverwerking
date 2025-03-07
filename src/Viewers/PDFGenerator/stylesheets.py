from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(name='Title_CENTER',
                          parent=styles['Normal'],
                          fontName='Helvetica',
                          wordWrap='LTR',
                          alignment=TA_CENTER,
                          fontSize=64,
                          leading=13,
                          textColor=colors.black,
                          borderPadding=0,
                          leftIndent=0,
                          rightIndent=0,
                          spaceAfter=0,
                          spaceBefore=0,
                          splitLongWords=True,
                          spaceShrinkage=0.05,
                          ))