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
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter


def generatePDF(_group):
    """Generates the PDF which shows the test data of a specific group. shows the following data:
        * Averages of all tests in a bar graph
        * A per test overview of grades and percentage of questions correct (grouped by difficulty and type)

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
    c.showPage()

    ###############################################################################
    #                          per test scores pages                              #
    ###############################################################################
    for _test in DataContainer.instance.tests:
        generateTestScorePage(c,_test,width,height) #generates a page for each test


    c.save()
    print("Finished generating group data PDF of " + _groupName)

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
    plt.ylim([1,10])
    _imgData = BytesIO()
    _fig.savefig(_imgData, format='svg')
    _fig.set_size_inches(_figwidth/72,_figheight/72)
    _imgData.seek(0)
    _drawing = svg2rlg(_imgData)
    plt.close()
    return _drawing

def generateTestScorePage(_canvas,_test,_width,_height):
    """Generates a page with graphs of a specific test, specified on a group level

    Args:
        _canvas (Canvas): Canvas to draw on
        _test (Test): Test to process
    """
    _canvas.doForm("standardDataPage")
    #title
    _canvas.setLineWidth(10)
    averagesTitleText = _canvas.beginText(_width*0.05,_height*0.9)
    averagesTitleText.setFont("Helvetica",24)
    averagesTitleText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    if(_test.version != None):
        averagesTitleText.textLine(DataContainer.instance.groupDatasheetTitle3 +" " +_test.name + " " + _test.version)
    else:
        averagesTitleText.textLine(DataContainer.instance.groupDatasheetTitle3 +" " +_test.name)
    _canvas.drawText(averagesTitleText)
    #TODO: add data about test (number of students, number of points, n-term etc.)

    #generate diagrams
    _diagramsDrawing = generateTestDiagramsMatPlotLib(_test,_width*0.8,_width*0.8)
    renderPDF.draw(_diagramsDrawing,_canvas,0,_height*0.1)


    #end page
    _canvas.showPage()

def generateTestDiagramsMatPlotLib(_test,_figwidth,_figheight):
    """Generates all diagrams for the group per test datapage in a single matplotlib figure

    Args:
        _test (Test): the test to evaluate
        _figwidth (float): Width of the final figure
        _figheight (float): Height of the final figure

    Returns:
        Drawing: to be used in the PDF
    """
    #generate figure:
    _fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
    _fig.set_size_inches(_figwidth/72,_figheight/72)

    #grades
    _grades = []
    for _tr in _test.testResults:
        _grades.append(_tr.grade)
        
    #generate histogram of grades
    _bins = [0,1,2,3,4,5,6,7,8,9,10]
    ax1.hist(x=_grades,bins=_bins,facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    ax1.set_title(DataContainer.instance.groupDatasheetGraphTitle1)

    #difficulty of questions
    _difficultyDictionaryScores = {}
    _difficultyDictionaryNofQuestions = {}
    for _tr in _test.testResults:
        #loop through all results of test (thus each student)
        _i = 0
        _questionDifficultyLabelArray = []
        _questionDifficultyDataArray = []
        for _score in _tr.scores:
            #loop over all scores (score on a question) for this student and add them to the array
            _questionDifficultyDataArray.append(_score/_test.questions[_i].maxPoints)
            _questionDifficultyLabelArray.append(_test.questions[_i].difficulty)
            _i += 1
        _i = 0
        for _dataPacket in _questionDifficultyLabelArray:     
            try:
                _difficultyDictionaryScores[_dataPacket] += _questionDifficultyDataArray[_i]
                _difficultyDictionaryNofQuestions[_dataPacket] += 1
            except KeyError:
                #if difficulty is not yet in the dictionary, make sure we set it to 0 to initialize
                _difficultyDictionaryScores[_dataPacket] = 0
                _difficultyDictionaryNofQuestions[_dataPacket] = 0
            except:
                print("error in dictionary in generating difficulty diagram")
                raise
            _i += 1
    _difficultyDictionaryPercentage = {}
    #calculate percentages for each type of question
    for key in _difficultyDictionaryScores:
        _difficultyDictionaryPercentage[key] = _difficultyDictionaryScores[key]/_difficultyDictionaryNofQuestions[key]
    #generate bar chart of difficulty
    ax2.bar(x=_difficultyDictionaryPercentage.keys(),height=_difficultyDictionaryPercentage.values(),facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    ax2.set_title(DataContainer.instance.groupDataSheetGraphTitle2)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.set_ylim([0,1])
        
    #type of questions
    _typeDictionaryScores = {}
    _typeDictionaryNofQuestions = {}
    for _tr in _test.testResults:
        #loop through all results of test (thus each student)
        _i = 0
        _questionTypeLabelArray = []
        _questionTypeDataArray = []
        for _score in _tr.scores:
            #loop over all scores (score on a question) for this student and add them to the array
            _questionTypeDataArray.append(_score/_test.questions[_i].maxPoints)
            _questionTypeLabelArray.append(_test.questions[_i].typeOfQuestion)
            _i += 1
        _i = 0
        for _dataPacket in _questionTypeLabelArray:     
            try:
                _typeDictionaryScores[_dataPacket] += _questionTypeDataArray[_i]
                _typeDictionaryNofQuestions[_dataPacket] += 1
            except KeyError:
                #if difficulty is not yet in the dictionary, make sure we set it to 0 to initialize
                _typeDictionaryScores[_dataPacket] = 0
                _typeDictionaryNofQuestions[_dataPacket] = 0
            except:
                print("error in dictionary in generating difficulty diagram")
                raise
            _i += 1
    _typeDictionaryPercentage = {}
    #calculate percentages for each type of question
    for key in _typeDictionaryScores:
        _typeDictionaryPercentage[key] = _typeDictionaryScores[key]/_typeDictionaryNofQuestions[key]
    #generate bar chart of type of questions
    ax3.bar(x=_typeDictionaryPercentage.keys(),height=_typeDictionaryPercentage.values(),facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    ax3.set_title(DataContainer.instance.groupDatasheetGraphTitle3)
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax3.set_ylim([0,1])

    #TODO: figure out 4th plot


    

    #save image to drawing for embedding into PDF
    _imgData = BytesIO()
    _fig.savefig(_imgData, format='svg')
    plt.close()
    _imgData.seek(0)
    _drawing = svg2rlg(_imgData)
    return _drawing

def generateIntroductionPage(_canvas,_width,_height):
    #TODO: make this page easily changeable
    #title
    _canvas.setLineWidth(10)
    introductionTitleText = _canvas.beginText(_width*0.05,_height*0.9)
    introductionTitleText.setFont("Helvetica",24)
    introductionTitleText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    introductionTitleText.textLine("Toelichting bij dit document")
    _canvas.drawText(introductionTitleText)

    #Introduction Paragrah
    return
