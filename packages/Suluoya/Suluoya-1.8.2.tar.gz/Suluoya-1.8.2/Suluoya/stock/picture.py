from pyecharts import options as opts
from pyecharts.charts import EffectScatter
from pyecharts.globals import SymbolType
import pyecharts.options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Scatter
from pyecharts.render import make_snapshot
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.rcParams['backend'] = 'HTML'
import matplotlib.pyplot as plt
def weights_pie(weights):
    #weights={'伊利股份': 0.665225115503282, '新华保险': 0.20896815868555363, '中国建筑': 0.12580672581116445}
    lab = list(weights.keys()) 
    num = list(weights.values())
    (
        Pie(init_opts=opts.InitOpts(width='1440px', height='729px')) #自定义画布大小
        .add(series_name='', data_pair=[(i, j)for i, j in zip(lab, num)],radius=['40%', '75%']) #遍历数据
        .set_global_opts(title_opts=opts.TitleOpts(title="weights",subtitle="")) #添加主、副标题
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%")) #添加数据标签   

    ).render('Markowit\\weights.html')

def effect_scatter(datax,datay):
    v1 =datax
    v2 =datay
    c = (
        EffectScatter()
        .add_xaxis(v1)
        .add_yaxis('',v2)
            .set_global_opts(title_opts=opts.TitleOpts(title="EffectScatter"))
        )
    c.render('scatter.html')

#df=pd.read_csv(r"C:\Users\19319\Desktop\Suluoya_package\Markowit\'贵州茅台', '五粮液', '隆基股份'.csv")
#plt.scatter(df['risk'], df['rate'], s=np.pi*4, c='#00CED1', alpha=0.4)
#plt.savefig('Markowit\\scatter.svg')

#import pygal

#饼图
def pie(dic=None,path=''):
    pie=pygal.Pie()
    #Pie.force_uri_protocol = 'http'
    if dic==None:
        pie.add("优秀",19)
        pie.add("良好",36)
        pie.add("合格",36)
        pie.add("不合格",4)
        pie.add("较差",2)
    elif type(dic)==dict:
        for i,j in dic.items():
            pie.add(i,j)
    
    pie.render_to_file(f'{path}\\pie.svg')
#pie(dic={'伊利股份': 0.665225115503282, '新华保险': 0.20896815868555363, '中国建筑': 0.12580672581116445},path='try')

##Pie(inner_radius=xx)创建圆环图
#circle=pygal.Pie(inner_radius=0.6)
#circle.title="小学生成绩分布图"
#circle.add("优秀",19)
#circle.add("良好",36)
#circle.add("合格",36)
#circle.add("不合格",4)
#circle.add("较差",2)
#circle.render_to_file('circle.svg')
#
#
##Bar()绘制条形图
#hist = pygal.Bar()
#x= ['1', '2', '3', '4', '5', '6']
#y=[10,30,15,35,67,43]
#hist.x_labels =x
#hist.x_title = "Result"
#hist.y_title = "Number"
#hist.add('条形图', y)
#hist.render_to_file('bar.svg')
#
##HorizontalBar()创建水平条形图
#bar=pygal.HorizontalBar()
#bar.title="小学生成绩分布图"
#bar.add("优秀",19)
#bar.add("良好",36)
#bar.add("合格",36)
#bar.add("不合格",4)
#bar.add("较差",2)
#bar.render_to_file('bar1.svg')
#
#
##HorizontalStackedBar()绘制水平堆叠条形图
#bar2=pygal.HorizontalStackedBar()
#bar2.title='员工销售情况图'
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#bar2.x_labels=["小二","张三","李四","小桐","王五","小小","赵六"]
#bar2.x_title='销售量'
#bar2.y_title='人员'
#bar2.add('旺季',x)
#bar2.add('淡季',y)
#bar2.render_to_file('bar2.svg')
#
##XY()绘制函数图像
##数学公式这些要用到math模块
#from math import cos 
#xy_chart = pygal.XY()
#xy_chart.title = '函数图'
##需提供一个横纵坐标元组作为元素的列表,即提供几个（x,y）坐标点的列表
#xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
#xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
#xy_chart.add('x = 1', [(1, -5), (1, 5)])
#xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
#xy_chart.add('y = 1', [(-5, 1), (5, 1)])
#xy_chart.add('y = -1', [(-5, -1), (5, -1)])
#xy_chart.render_to_file('bar_chart.svg')
#
#
##Line()绘制折线图
#line=pygal.Line()
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#line.x_labels=map(str,range(2008,2014))
#line.add('旺季',x)
#line.add('淡季',y)
#line.render_to_file('line.svg')
#
##HorizontalLine()绘制水平折线图
#line1=pygal.HorizontalLine()
#line1.title='销售线图'
#line1.x_labels=map(str,range(2008,2014))
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#line1.add('旺季',x)
#line1.add('淡季',y)
#line1.render_to_file('line1.svg')
#
##StackedLine(fill=True)绘制叠加侧线图
#line2=pygal.StackedLine(fill=True)
#line2.title='叠加侧线图'
#line2.x_labels=map(str,range(2008,2014))
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#line2.add('旺季',x)
#line2.add('淡季',y)
#line2.render_to_file('line2.svg')
#
##Radar()绘制雷达图
#radar=pygal.Radar()
#x=[2,3,6,5,9,16,18]
#y=[1,2,3,5,6,2,7]
#radar.title='淡旺季雷达分布图'
#radar.add('旺季',x)
#radar.add('淡季',y)
#radar.render_to_file('radar.svg')
#
##Histogram()绘制直方图
##使用函数Histogram()绘制直方图是一个特殊的条形图，它包含3个数值：纵坐标高度，横坐标开始和横坐标结束。
#gram=pygal.Histogram()
#gram.title='直方图'
#gram.add('宽直条',[(4,0,10),(4,5,12),(2,0,16)])
#gram.add('窄直条',[(9,1,2),(12,4,4.6)])
#gram.render_to_file('gram.svg')