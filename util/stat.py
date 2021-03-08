import requests
from collections import defaultdict
from tqdm import trange
import matplotlib.pyplot as plt
import random
import pandas as pd
import json
import time
import os

plt.rcParams['font.sans-serif']=['Microsoft Yahei', 'SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['legend.fontsize'] = 12
builtin_colors = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']

api_src = 'http://iamwyh.cn:3300/'
songlist_src = api_src + 'songlist'
song_src = api_src + 'song'

def get_song_list(list_id: int):
    list_info = requests.get(songlist_src, params = {'id': list_id})
    if list_info.status_code != 200:
        return list_info.status_code
    
    list_info = list_info.json()
    if list_info['result'] != 100:
        return list_info['result']
    if len(list_info['data']) == 0:
        return 308

    cutie = list_info['data']['nickname']
    list_name = list_info['data']['dissname']
    time_stamp = int(time.time())
    with open(f'./data/raw/{cutie}-{list_name}-{time_stamp}.json', 'w') as f:
        json.dump(list_info, f)
    
    return list_info

def analyze_song_list(list_info, folder_name = ''):
    cutie = list_info['data']['nickname']
    n_song = list_info['data']['total_song_num']
    song_list = list_info['data']['songlist']
    list_name = list_info['data']['dissname']

    genre_ct = defaultdict(int)
    time_ct = defaultdict(int)
    lan_ct = defaultdict(int)
    singer_ct = defaultdict(int)

    name_lst = [''] * n_song
    genre_lst = [''] * n_song
    time_lst = [0] * n_song
    lan_lst = [''] * n_song
    singer_lst = [''] * n_song

    for i in trange(n_song):
        song = song_list[i]
        sid = song['songmid']
        song_info = requests.get(song_src, params = {'songmid':sid}).json()['data']
        
        name_lst[i] = song_info['track_info']['name']
        
        pub_time = song_info['track_info']['time_public']
        
        singers = song_info['track_info']['singer']
        singers = [x['name'] for x in singers]
        singer_lst[i] = '/'.join(singers)
        for singer in singers:
            singer_ct[singer] += 1
        
        info = song_info['info']
        
        if 'genre' in info:
            genres = info['genre']['content']
            genres = [x['value'] for x in genres]
            genre_lst[i] = '/'.join(genres)
            for genre in genres:
                genre_ct[genre] += 1
        
        lans = info['lan']['content']
        lans = [x['value'].strip() for x in lans]
        lan_lst[i] = '/'.join(lans)
        for lan in lans:
            lan_ct[lan] += 1
        
        if len(pub_time) > 0:    
            pub_year = pub_time[2] + '0s'
            time_ct[pub_year] += 1
            time_lst[i] = int(pub_time[:4])
    
    song_df = pd.DataFrame({'name': name_lst, 'year': time_lst, 'singer': singer_lst, 'language': lan_lst, 'genre': genre_lst})

    time_stamp = int(time.time())
    file_name = os.path.join('data', folder_name, f'{cutie}-{list_name}-{time_stamp}.csv')
    song_df.to_csv(file_name, index = False, encoding = "utf-8")

    return singer_ct, lan_ct, time_ct, genre_ct

def draw_graph(ct: defaultdict, title: str, quant: str, cutie: str, folder_name: str) -> str:
    global builtin_colors
    random.shuffle(builtin_colors)
    tmp = [(x, ct[x]) for x in ct]
    tmp.sort(key = lambda x:x[1], reverse = True)
    
    pie_threshold = 10
    bar_threshold = 25
    
    names = [x[0] for x in tmp]
    nums = [x[1] for x in tmp]
    
    total = sum(nums)
    
    plt.figure(figsize = (20,20), facecolor = 'white')
    
    def auto_pct(values):
        def mypct(pct):
            total = sum(values)
            val = round(pct / 100 * total)
            return str(val)
        return mypct
    
    plt.subplot(2,1,1)
    
    if len(names) > pie_threshold:
        plt_names = names[:pie_threshold]
        plt_nums = nums[:pie_threshold]
        n_items = pie_threshold
    else:
        plt_names = names
        plt_nums = nums
        n_items = len(names)
    
    plt.title(f'{cutie}的歌单的前{n_items}{quant}{title}', fontsize = 20)
    
    patches, l_text, p_text = plt.pie(plt_nums, labels = plt_names, autopct = auto_pct(plt_nums), 
                                      colors = builtin_colors[:n_items], explode = [0.02] * n_items, pctdistance = 0.8)
    plt.legend(loc = (1,0))
    
    for text in l_text:
        text.set_size(20)
    for text in p_text:
        text.set_size(20)
    
    plt.subplot(2,1,2)
    
    if len(names) > bar_threshold:
        plt_names = names[:bar_threshold]
        plt_nums = nums[:bar_threshold]
        n_items = bar_threshold
    else:
        plt_names = names
        plt_nums = nums
        n_items = len(names)
    
    x = list(range(n_items, 0, -1))
    
    plt.xticks(fontsize = 15)
    plt.yticks(fontsize = 15)
    
    plt.title(f'{cutie}的歌单的前{n_items}{quant}{title}', fontsize = 20)
    plt.barh(x, plt_nums, tick_label = plt_names, color = builtin_colors, alpha = 0.8)
    
    for a,b in zip(plt_nums, x):
        plt.text(a + 0.05, b - 0.1, str(a), fontsize = 15)
    
    time_stamp = int(time.time())
    filename = os.path.join(folder_name, f'{cutie}-{title}-{time_stamp}.jpg')
    filepath = os.path.join('data', filename)

    plt.savefig(filepath)

    return filename

def process_all(list_id: int):
    list_info = get_song_list(list_id)
    if isinstance(list_info, int):
        return list_info

    cutie = list_info['data']['nickname']
    time_stamp = int(time.time())
    folder_name = f'{cutie}-{time_stamp}'
    folder_path = os.path.join('data', f'{cutie}-{time_stamp}')
    os.mkdir(folder_path, 0o777)

    singer_ct, lan_ct, time_ct, genre_ct = analyze_song_list(list_info, folder_name)

    singer_fname = draw_graph(singer_ct, '歌手', '位', cutie, folder_name)
    lan_fname = draw_graph(lan_ct, '语言', '种', cutie, folder_name)
    time_fname = draw_graph(time_ct, '年代', '段', cutie, folder_name)
    genre_fname = draw_graph(genre_ct, '题材', '种', cutie, folder_name)

    return [singer_fname, lan_fname, time_fname, genre_fname]

def main():
    s = process_all(124444444)
    print(s)

if __name__ == '__main__':
    main()