
import matplotlib as mpl
import matplotlib.pyplot as plt

#Primary Colours
intellify_blue = '#2f3649'
intellify_orange = '#f4972d'

#Secondary Colours
intellify_pantone713 = '#febd85'
intellify_pantone712 = '#fdc899'
intellify_pantone7544 = '#748592'
intellify_pantone7543 = '#96a3ad'
intellify_white = '#ffffff'

#Colours that go well with primary
complementary_green = '#2395B5'
complementary_skyblue = '#40B4A6'
complementary_brown = '#603737'

tableau21 = [(1.0, 0.4980392156862745, 0.054901960784313725),
 (0.1843137254901961, 0.21176470588235294, 0.28627450980392155),
 (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
 (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
 (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
 (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
 (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
 (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
 (0.6823529411764706, 0.7803921568627451, 0.9098039215686274),
 (0.7725490196078432, 0.6901960784313725, 0.8352941176470589),
 (1.0, 0.7333333333333333, 0.47058823529411764),
 (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
 (0.596078431372549, 0.8745098039215686, 0.5411764705882353),
 (1.0, 0.596078431372549, 0.5882352941176471),
 (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
 (0.7686274509803922, 0.611764705882353, 0.5803921568627451),
 (0.9686274509803922, 0.7137254901960784, 0.8235294117647058),
 (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
 (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
 (0.8588235294117647, 0.8588235294117647, 0.5529411764705883),
 (0.6196078431372549, 0.8549019607843137, 0.8980392156862745)]

all_colors = [intellify_orange, intellify_blue, complementary_green, complementary_brown, complementary_skyblue]

def setmpl():

    #Setting Colours for graphs
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=tableau21)

    #Setting Line Attributes
    plt.rc('lines', linewidth = 1.5, linestyle = '-', marker = 'o', markersize = 2.5)

    #Setting Font
    plt.rc('font', family = 'serif')
    plt.rcParams['font.serif'] = 'Arial'
    plt.rc('text', color = intellify_blue)

    #Setting Figure Properties
    plt.rc('figure', dpi = 150, figsize = (5,3), facecolor = 'white', edgecolor = 'white')
    plt.rcParams['figure.subplot.right'] = 0.9
    plt.rcParams['figure.subplot.left'] = 0.1
    

    #Setting Axes & Ticks
    plt.rc('axes', edgecolor = 'grey', titlesize = 11, labelsize = 9, \
    labelcolor = intellify_blue, titlecolor = intellify_blue)
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['xtick.color'] = intellify_blue
    plt.rcParams['ytick.color'] = intellify_blue

    #Setting Legend
    plt.rc('legend', frameon = False, labelspacing = 0.3, fontsize = 8)
    

def getHeatMapColors():
    heatmap_colors = ['#2f3649', '#353a51', '#353a51', '#45405f', '#4e4365', '#58456b', '#63476f', \
                  '#6f4973', '#7b4a76', '#874c78', '#934d79', '#a04e78', \
                 '#ab5077', '#b75275', '#c15472', '#cb576e', '#d55b69', '#dd6063', \
                  '#e4655d', '#ea6c56', '#ee734f', '#f27b47', '#f4843f', '#f58d36', '#f4972d']
    return heatmap_colors

def timeseries(x = None, y = None, legend = True, title = None, xAxis = None, yAxis = None, labels = None):
    if(x == None or y == None):
        print("Error: Either one or both of x & y empty. They both must not be empty")
        return
    y_size = len(y)
    if(type(y[0]) != list and type(y[0]) != np.ndarray):
        print("Error: Contents of y must be either lists of numpy arrays")
        return
    for i in range(0, y_size):
        plt.plot(x, y[i], label = (labels[i] if labels != None else None))
    
    plt.title(title)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    if(legend):
        plt.legend() 
    return 
