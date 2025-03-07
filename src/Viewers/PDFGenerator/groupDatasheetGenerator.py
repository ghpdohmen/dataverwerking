from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from datetime import datetime

from dataContainer import DataContainer
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
import matplotlib.pyplot as plt
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF


def generatePDF(_group):
    """Generates the PDF which shows the test data of a specific group. shows the following data:
        * Averages of all tests in a bar graph

    Args:
        _group (group): group to generate the PDF of
    """
    _groupName = _group.name
    #generate document
    c = canvas.Canvas(_groupName + "-groupDatasheet.pdf", pagesize=A4)
    width,height = A4
    
    ###############################################################################
    #                               cover page                                    #
    ###############################################################################
    #Top text:
    c.setLineWidth(14)
    groupNameText = c.beginText(width*0.4,height*0.8)
    groupNameText.setFont("Helvetica",72)
    groupNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    groupNameText.textLine(_groupName)
    c.drawText(groupNameText)
    infoText = c.beginText(width*0.3,height*0.7)
    infoText.setFont("Helvetica",24)
    infoText.setFillColor(colors.HexColor(DataContainer.instance.colorHex3))
    infoText.textLine(DataContainer.groupDatasheetTitle + " " + DataContainer.subject)
    c.drawText(infoText)

    
    #lower colored bar
    c.setLineWidth(0.1*height)
    c.setStrokeColor(colors.HexColor(DataContainer.instance.colorHex1))
    c.line(0,height*0.025,width,height*0.025)
    #bottom text
    c.setLineWidth(14)
    teacherNameText = c.beginText(width*0.1,height*0.03)
    teacherNameText.setFont("Helvetica",14)
    teacherNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    teacherNameText.textLine(DataContainer.instance.teacher)
    c.drawText(teacherNameText)
    schoolNameText = c.beginText(width*0.425,height*0.03)
    schoolNameText.setFont("Helvetica",14)
    schoolNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    schoolNameText.textLine(DataContainer.instance.schoolName)
    c.drawText(schoolNameText)
    dateText = c.beginText(width*0.8,height*0.03)
    dateText.setFont("Helvetica",14)
    dateText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    dateText.textLine(datetime.today().strftime("%d %B %Y"))
    c.drawText(dateText)



    c.showPage()
    ###############################################################################
    #                         form for all data pages                             #
    ###############################################################################
    dataPage = c.beginForm("standardDataPage")
    #bar below title
    c.setStrokeColor(colors.HexColor(DataContainer.instance.colorHex3))
    c.line(0,height*0.885,width,height*0.885)


    #lower colored bar
    c.setLineWidth(0.1*height)
    c.setStrokeColor(colors.HexColor(DataContainer.instance.colorHex1))
    c.line(0,height*0.025,width,height*0.025)
    #bottom text
    c.setLineWidth(14)
    teacherNameText = c.beginText(width*0.1,height*0.03)
    teacherNameText.setFont("Helvetica",14)
    teacherNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    teacherNameText.textLine(DataContainer.instance.teacher)
    c.drawText(teacherNameText)
    schoolNameText = c.beginText(width*0.425,height*0.03)
    schoolNameText.setFont("Helvetica",14)
    schoolNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    schoolNameText.textLine(DataContainer.instance.schoolName)
    c.drawText(schoolNameText)
    dateText = c.beginText(width*0.8,height*0.03)
    dateText.setFont("Helvetica",14)
    dateText.setFillColor(colors.HexColor(DataContainer.instance.colorHex2))
    dateText.textLine(datetime.today().strftime("%d %B %Y"))
    c.drawText(dateText)
    c.endForm()

    ###############################################################################
    #                               averages page                                 #
    ###############################################################################
    c.doForm("standardDataPage")
    #title
    c.setLineWidth(10)
    averagesTitleText = c.beginText(width*0.05,height*0.9)
    averagesTitleText.setFont("Helvetica",24)
    averagesTitleText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    averagesTitleText.textLine(DataContainer.instance.groupDatasheetTitle2)
    c.drawText(averagesTitleText)
    
    #get data and create graph
    _testNames = []
    _testAverages = []
    for _test in DataContainer.instance.tests:
        _testNames.append(_test.name)
        _testAverages.append(_group.testAverage(_test))
    #_averagesDrawing = generateBarChart(_testAverages,_testNames)
    #_averagesDrawing.drawOn(c,int(width*0.1),int(height*0.2))
    _averagesDrawing = generateBarChartMatPlotLib(_testAverages,_testNames, width*0.8, width*0.8)
    renderPDF.draw(_averagesDrawing,c,0,height*0.2)

    ###############################################################################
    #                          per test scores pages                              #
    ###############################################################################
    for _test in DataContainer.instance.tests:
        generateTestScorePage(c,_test) #generates a page for each test


    c.save()

#generatePDF("test")
def generateBarChartMatPlotLib (_data, _labels,_figwidth,_figheight):
    """Generates a bar chart with the specified data

    Args:
        _data (float[]): height of each bar
        _labels (string[]): name of each bar
        _figwidth (float): width of figure
        _figheight (float): height of figure

    Returns:
        Drawing: _description_
    """
    _fig = plt.figure()
    plt.bar(x=_labels,height=_data,facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    #plt.ax
    _imgData = BytesIO()
    _fig.savefig(_imgData, format='svg')
    _fig.set_size_inches(_figwidth/72,_figheight/72)
    _imgData.seek(0)
    _drawing = svg2rlg(_imgData)
    return _drawing

def generateTestScorePage(_canvas,_test):
    """Generates a page with graphs of a specific test, specified on a group level

    Args:
        _canvas (Canvas): Canvas to draw on
        _test (test): Test to process
    """
    c.doForm("standardDataPage")
    #title
    c.setLineWidth(10)
    averagesTitleText = c.beginText(width*0.05,height*0.9)
    averagesTitleText.setFont("Helvetica",24)
    averagesTitleText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    averagesTitleText.textLine(DataContainer.instance.groupDatasheetTitle3 +" " +_test.name)
    c.drawText(averagesTitleText)

    #generate bar graph with grades in boxes per grade.
    