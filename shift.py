#coding: UTF-8
from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)

#sqliteからデータを取り出す関数
def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list=[]
    for i in c.execute('select * from carehomes'):
        prof_list.append(
            {'id':i[0],
            #'homename':i[1],
            'hometype':i[2],
            'day_worktime':i[3],
            'day_shiftnumber':i[4],
            'night_worktime':i[5],
            'night_shiftnumber':i[6],
            'part_worktime':i[7],
            'part_shiftnumber':i[8],
            'nurse_worktime':i[9],
            'nurse_shiftnumber':i[10],
            'must_carenumber':i[11]}
        )
    conn.commit()
    conn.close()
    return prof_list

#sqliteのテーブルを更新する関数
def update_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute(
        f'''
        update carehomes 
        set 
            hometype='{prof['hometype']}',
            day_worktime={prof['day_worktime']},
            day_shiftnumber={prof['day_shiftnumber']},
            night_worktime={prof['night_worktime']},
            night_shiftnumber={prof['night_shiftnumber']},
            part_worktime={prof['part_worktime']},
            part_shiftnumber={prof['part_shiftnumber']},
            nurse_worktime={prof['nurse_worktime']},
            nurse_shiftnumber={prof['nurse_shiftnumber']},
            must_carenumber={prof['must_carenumber']}
        WHERE id={prof['id']}
        '''
    )
    conn.commit()
    conn.close()

#sqliteのテーブルを追加する関数
def insert_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute(
        f'''
        insert into carehomes(
            hometype,
            day_worktime,
            day_shiftnumber,
            night_worktime,
            night_shiftnumber,
            part_worktime,
            part_shiftnumber,
            nurse_worktime,
            nurse_shiftnumber,
            must_carenumber
        )
        values (
            '{prof['hometype']}',
            {prof['day_worktime']},
            {prof['day_shiftnumber']},
            {prof['night_worktime']},
            {prof['night_shiftnumber']},
            {prof['part_worktime']},
            {prof['part_shiftnumber']},
            {prof['nurse_worktime']},
            {prof['nurse_shiftnumber']},
            {prof['must_carenumber']}
        );
        '''
    )
    conn.commit()
    conn.close()

#idを検索する関数
def search_prof(prof_list, id):
    result = {}
    for x in prof_list:
        if x['id'] == id:
            result = x
            break
        
    return result

#人員配置人数を計算する
def shift_analysis(
    day_worktime, 
    day_shiftnumber, 
    night_worktime, 
    night_shiftnumber, 
    part_worktime, 
    part_shiftnumber, 
    nurse_worktime, 
    nurse_shiftnumber, 
    must_carenumber
):
    daytotal = \
        (day_worktime * day_shiftnumber) \
        + (night_worktime * night_shiftnumber) \
        + (part_worktime * part_shiftnumber)\
        + (nurse_worktime * nurse_shiftnumber)
    weektotal = int(daytotal)* 7
    weekaverage = int(weektotal) / 40
    arrange = must_carenumber / float(weekaverage)
    return round(float(arrange), 2)

#prof_listに人員配置人数を加える関数
def add_arrange(prof_list):
    result_arranges = []
    for x in prof_list:
        result_arrange = x
        result_arrange['arrange'] = shift_analysis(
            x['day_worktime'], 
            x['day_shiftnumber'], 
            x['night_worktime'], 
            x['night_shiftnumber'], 
            x['part_worktime'], 
            x['part_shiftnumber'], 
            x['nurse_worktime'], 
            x['nurse_shiftnumber'], 
            x['must_carenumber']
        )
        result_arranges.append(
            result_arrange
        )
    return result_arranges


@app.route('/')
def top():
    return redirect(url_for('profile'))

#一覧表示画面
@app.route('/shift_profile')
def profile():
    prof_list = get_profile()
    prof_list = add_arrange(prof_list)
    return render_template('shift_profile.html', title='シフト情報', user=prof_list)

#追加画面
@app.route('/shift_add')
def add():
    prof_dict = {}
    return render_template('shift_add.html', title='シフト追加', user=prof_dict)

#編集画面
@app.route('/shift_edit/<int:id>')
def edit(id):
    prof_list = get_profile()
    prof_dict = search_prof(prof_list, id)
    return render_template('shift_edit.html', title='シフト分析', user=prof_dict)

#上書き
@app.route('/shift_update/<int:id>', methods=['POST'])
def update(id):
    prof_list = get_profile()
    prof_dict = search_prof(prof_list, id)
    #prof_dictの値を変更
    #prof_dict['homename'] = request.form['homename']
    prof_dict['hometype'] = request.form['hometype']
    prof_dict['day_worktime'] = request.form['day_worktime']
    prof_dict['day_shiftnumber'] = request.form['day_shiftnumber']
    prof_dict['night_worktime'] = request.form['night_worktime']
    prof_dict['night_shiftnumber'] = request.form['night_shiftnumber']
    prof_dict['part_worktime'] = request.form['part_worktime']
    prof_dict['part_shiftnumber'] = request.form['part_shiftnumber']
    prof_dict['nurse_worktime'] = request.form['nurse_worktime']
    prof_dict['nurse_shiftnumber'] = request.form['nurse_shiftnumber']
    prof_dict['must_carenumber'] = request.form['must_carenumber']
        
    update_profile(prof_dict)
    
    return redirect(url_for('profile'))

#追加
@app.route('/shift_insert', methods=['POST'])
def insert():
    prof_dict = {}
    #prof_dictの値を追加
    #prof_dict['homename'] = request.form['homename']
    prof_dict['hometype'] = request.form['hometype']
    prof_dict['day_worktime'] = request.form['day_worktime']
    prof_dict['day_shiftnumber'] = request.form['day_shiftnumber']
    prof_dict['night_worktime'] = request.form['night_worktime']
    prof_dict['night_shiftnumber'] = request.form['night_shiftnumber']
    prof_dict['part_worktime'] = request.form['part_worktime']
    prof_dict['part_shiftnumber'] = request.form['part_shiftnumber']
    prof_dict['nurse_worktime'] = request.form['nurse_worktime']
    prof_dict['nurse_shiftnumber'] = request.form['nurse_shiftnumber']
    prof_dict['must_carenumber'] = request.form['must_carenumber']
        
    insert_profile(prof_dict)
    
    return redirect(url_for('add'))

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))