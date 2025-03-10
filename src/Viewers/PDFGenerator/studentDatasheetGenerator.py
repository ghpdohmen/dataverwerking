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


def generatePDF(_student):
    """Generates the PDF which shows the test data of a specific student. shows the following data:
        * Averages of all tests in a bar graph
        * A per test overview of 

    Args:
        _student (Student): student to generate the PDF of
    """
    _studentName = _student.name
    #generate document
    c = canvas.Canvas(_studentName + "-studentDatasheet.pdf", pagesize=A4)
    width,height = A4
    
    ###############################################################################
    #                               cover page                                    #
    ###############################################################################
    #Top text:
    c.setLineWidth(14)
    
    groupNameText = c.beginText(width*0.4,height*0.8)
    groupNameText.setFont("Helvetica",72)
    groupNameText.setFillColor(colors.HexColor(DataContainer.instance.colorHex1))
    groupNameText.textLine(_studentName)
    groupNameText.setTextOrigin(width/2-groupNameText.getCursor()[0]/2,height*0.8)
    c.drawText(groupNameText)
    infoText = c.beginText(width*0.3,height*0.7)
    infoText.setFont("Helvetica",24)
    infoText.setFillColor(colors.HexColor(DataContainer.instance.colorHex3))
    infoText.textLine(DataContainer.studentDatasheetTitle + " " + DataContainer.subject)
    infoText.setTextOrigin(width/2-infoText.getCursor()[0]/2,height*0.7)
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
    #TODO: vanaf hier alles nalopen
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
    for _tr in _student.testResults:
        _testNames.append(_tr.test.name)
        _testAverages.append(_tr.grade)
    #_averagesDrawing = generateBarChart(_testAverages,_testNames)
    #_averagesDrawing.drawOn(c,int(width*0.1),int(height*0.2))
    _averagesDrawing = generateBarChartMatPlotLib(_testAverages,_testNames, width*0.8, width*0.8)
    renderPDF.draw(_averagesDrawing,c,0,height*0.2)
    c.showPage()

    ###############################################################################
    #                          per test scores pages                              #
    ###############################################################################
    for _test in DataContainer.instance.tests:
        generateTestScorePage(c,_test,_student,width,height) #generates a page for each test


    c.save()
    print("Finished generating student data PDF of " + _studentName)


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
    return _drawing



def generateTestScorePage(_canvas,_test,_student,_width,_height):
    """Generates a page with graphs of a specific test, specified on a group level

    Args:
        _canvas (Canvas): Canvas to draw on
        _test (test): Test to process
    """
    #generate diagrams
    _diagramsDrawing = generateTestDiagramsMatPlotLib(_test,_student,_width*0.8,_width*0.8)
    if(_diagramsDrawing == None):
        return
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

    
    renderPDF.draw(_diagramsDrawing,_canvas,0,_height*0.1)


    #end page
    _canvas.showPage()

def generateTestDiagramsMatPlotLib(_test,_student,_figwidth,_figheight):
    #generate figure:
    _fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
    _fig.set_size_inches(_figwidth/72,_figheight/72)

    #gather data
    _percentagePoints = []
    _questionNames = []
    _questionDifficulty = []
    _questionTypes = []
    _difficultyDictionaryScores = {}
    _difficultyDictionaryNofQuestions = {}
    _typeDictionaryScores = {}
    _typeDictionaryNofQuestions = {}
    _difficultyDictionary = {}
    _typeDictionary = {}

    _tr = _student.findTestResult(_test)
    if(_tr == None):
        return #test was not taken by student
    _i = 0

    #calculate percentage of total points for each question
    for _score in _tr.scores:
        _percentagePoints.append(_score/_test.questions[_i].maxPoints) #add the percentage of points recieved to the percentage array. Looks up the max points in the question at index _i.
        _questionNames.append(_test.questions[_i].name)
        _questionDifficulty.append(_test.questions[_i].difficulty)
        _questionTypes.append(_test.questions[_i].typeOfQuestion)
        _i += 1
    _i = 0

    #calculate percentage of points gotten per question difficulty
    for _dataPacket in _questionDifficulty:     
        try:
            _difficultyDictionaryScores[_dataPacket] += _percentagePoints[_i]
            _difficultyDictionaryNofQuestions[_dataPacket] += 1
        except KeyError:
            #if difficulty is not yet in the dictionary, make sure we set it to 0 to initialize
            _difficultyDictionaryScores[_dataPacket] = _percentagePoints[_i]
            _difficultyDictionaryNofQuestions[_dataPacket] = 1
        except:
            print("error in dictionary in generating difficulty diagram")
            raise
        _i += 1
    for key in _difficultyDictionaryScores:
        _difficultyDictionary[key] = _difficultyDictionaryScores[key]/_difficultyDictionaryNofQuestions[key]


    _i = 0
    #calculate percentage of points gotten for each type of question
    for _dataPacket in _questionTypes:     
        try:
            _typeDictionaryScores[_dataPacket] += _percentagePoints[_i]
            _typeDictionaryNofQuestions[_dataPacket] += 1
        except KeyError:
            #if difficulty is not yet in the dictionary, make sure we set it to 0 to initialize
            _typeDictionaryScores[_dataPacket] = _percentagePoints[_i]
            _typeDictionaryNofQuestions[_dataPacket] = 1
        except:
            print("error in dictionary in generating type diagram")
            raise
        _i += 1
    for key in _typeDictionaryScores:
        _typeDictionary[key] = _typeDictionaryScores[key]/_typeDictionaryNofQuestions[key]

        
    #generate bar graph of percentage of points per question
    ax1.bar(x=_questionNames,height=_percentagePoints,facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=1, )
    ax1.set_title(DataContainer.instance.groupDatasheetGraphTitle1)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    #difficulty of questions
    
    #generate bar chart of difficulty
    ax2.bar(x=_difficultyDictionary.keys(),height=_difficultyDictionary.values(),facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    ax2.set_title(DataContainer.instance.groupDataSheetGraphTitle2)
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.set_ylim([0,1])

    #generate bar chart of type of questions
    ax3.bar(x=_typeDictionary.keys(),height=_typeDictionary.values(),facecolor=DataContainer.instance.colorHex1, edgecolor=DataContainer.instance.colorHex3,linewidth=2, )
    ax3.set_title(DataContainer.instance.groupDatasheetGraphTitle3)
    ax3.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax3.set_ylim([0,1])

    #TODO: figure out 4th plot
    ax4 = None

    

    #save image to drawing for embedding into PDF
    _imgData = BytesIO()
    _fig.savefig(_imgData, format='svg')
    _imgData.seek(0)
    _drawing = svg2rlg(_imgData)
    return _drawing
