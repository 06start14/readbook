import json
import os
import pygal_maps_world.maps
import pygal

code_country = {
    'cn': '中国',
    'gb': '英国',
    'co': '哥伦比亚',
    'us': '美国',
    'jp': '日本',
    'fr': '法国',
    'dk': '丹麦',
    'it': '意大利',
    'il': '以色列',
    'ru': '俄罗斯',
    'de': '德国',
    'se': '瑞典',
    'in': '印度',
    'ar': '阿根廷',
    'at': '奥地利',
    'pt': '葡萄牙',
    'no': '挪威',
    'by': '白俄罗斯',
    'ca': '加拿大',
    'gr': '希腊',
    'za': '南非',
    'au': '澳大利亚',
    'br': '巴西',
}
base_filename = 'venv/results'
files = os.listdir(base_filename)
# 存储所有文件内容的列表
papers = []
# 存储papers列表统计数据的字典
number = {}
# 存储papers列表书得分统计的字典
score = {}
# 存储number字典所有国家百分比的字典
percent_number = {}
number1 = {}


# 按字典的键排序
def sort_by_key(d):
    return dict(sorted(d.items(), key=lambda k: k[0]))


# 打开file_s文件夹中所闻文件并把数据读取到列表中
def get_data_from_file(file_s, data):
    for file in file_s:
        filename = base_filename + '/' + file
        with open(filename, encoding='utf-8') as f:
            pop_data = json.load(f)
            data.append(pop_data)


# 从列表中读取name的数据保存到字典中
def get_data_from_list(lis, d, name):
    for li in lis:
        if li[name] in d.keys():
            d[li[name]] += 1
        else:
            d[li[name]] = 1


get_data_from_file(files, papers)
get_data_from_list(papers, number, 'country_code')
get_data_from_list(papers, score, 'score')
for num in number.items():
    percent_number[num[0]] = num[1] / 250
# 构建作者国籍的可视化
bigger_100 = {}
bigger_50_smaller_100 = {}
bigger_20_smaller_50 = {}
bigger_10_smaller_20 = {}
bigger_5_smaller_10 = {}
smaller_5 = {}
for num in number.items():
    if num[1] >= 100:
        bigger_100[num[0]] = num[1]
    elif num[1] >= 50:
        bigger_50_smaller_100[num[0]] = num[1]
    elif num[1] >= 20:
        bigger_20_smaller_50[num[0]] = num[1]
    elif num[1] >= 10:
        bigger_10_smaller_20[num[0]] = num[1]
    elif num[1] >= 5:
        bigger_5_smaller_10[num[0]] = num[1]
    else:
        smaller_5[num[0]] = num[1]
wm = pygal_maps_world.maps.World()
wm.title = 'book——data'
wm.add('>=100', bigger_100)
wm.add('>=50', bigger_50_smaller_100)
wm.add('>=20', bigger_20_smaller_50)
wm.add('>=10', bigger_10_smaller_20)
wm.add('>=5', bigger_5_smaller_10)
wm.add('<5', smaller_5)
wm.render_to_file('book_data.svg')
# 构建书籍评分数据的可视化
hist = pygal.Bar()
hist.title = "Result of score"
hist.x_labels = sort_by_key(score).keys()
hist._x_title = "score"
hist._y_title = "result"
hist.add('个数', sort_by_key(score).values())
hist.render_to_file('score_data.svg')
# 构建作者国籍百分比的饼状图
for num in number.items():
    number1[code_country[num[0]]] = num[1]
pie_chart = pygal.Pie()
pie_chart.title = "the country of writer(in %)"
for num in number1.items():
    pie_chart.add(str(num[0]), num[1])
pie_chart.render_to_file('percent.svg')
