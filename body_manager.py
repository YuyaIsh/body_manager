from datetime import datetime, timedelta
import PySimpleGUI as sg
import psycopg2
import locale

import env_supabase.supabase_env as supabase

locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')

location=(100,0)
popup_location = (location[0]+100,location[1]+200)

black = "#000000"
red = "#ff0000"

date_format = "%Y/%m/%d(%a)"

def main():
    sg.theme("Dark2")

    # 体重
    data_weight = get_weight()
    colnames_weight = ["日付","体重","移動平均"]
    display_date_weight = (datetime.strptime(data_weight[0][0],date_format)+timedelta(days=1)).strftime(date_format)

    weight_layout = [[sg.Column([
        [sg.T("体重入力"),sg.HorizontalSeparator()],
        [sg.Column([
            [sg.B("◀",key="pre_day_weight",font=fontsize(13),pad=(0,10)),
             sg.Input(display_date_weight,size=14,key="date_weight",justification="center",pad=(0,10)),
             sg.B("▶",key="next_day_weight",font=fontsize(13),pad=((0,10),0)),
             sg.B("TODAY",key="today_weight",font=fontsize(13),pad=(0,0))],
            [sg.T("体重:",pad=(0,5)),
             sg.Input("",size=5,justification="right",key="weight",pad=0,focus=True),sg.T("kg",pad=0),
             sg.B("登録",key="input_weight",pad=((15,0),0))],
            [sg.B("前日と同じ体重を登録",key="input_weight_preday")],
            [sg.Text("",key="result_weight")]
        ],element_justification="center",justification="center")],
        [sg.T("デイリーデータ"),sg.B("更新",font=fontsize(13),key="update_table_weight"),sg.HorizontalSeparator()],
        [sg.Table(data_weight,colnames_weight,auto_size_columns=False,justification="center",col_widths=[14,7,7],key="table_weight")]
    ])]]

    # BIG3
    data_big3 = get_big3()
    colnames_big3 = ["種目","記録(kg)","更新日"]
    big3_total = data_big3[0][1]+data_big3[1][1]+data_big3[2][1]

    big3_layout =[[sg.Column([
        [sg.T("キャリアハイ入力"),sg.HorizontalSeparator()],
        [sg.Column([
            [sg.B("◀",key="pre_day_big3",font=fontsize(13),pad=(0,10)),
             sg.Input(datetime.now().strftime(date_format),size=14,key="date_big3",justification="center",pad=(0,10)),
             sg.B("▶",key="next_day_big3",font=fontsize(13),pad=((0,10),0)),
             sg.B("TODAY",key="today_big3",font=fontsize(13),pad=(0,0))],
            [sg.T("ベンチプレス",pad=(0,5),size=8),
             sg.Input("",size=5,justification="right",key="benchpress",pad=0,focus=True),sg.T("kg",pad=0),
             sg.B("登録",key="inputbig3_benchpress",pad=((15,0),0),font=fontsize())],
            [sg.T("スクワット",pad=(0,5),size=8),
             sg.Input("",size=5,justification="right",key="squat",pad=0,focus=True),sg.T("kg",pad=0),
             sg.B("登録",key="inputbig3_squat",pad=((15,0),0),font=fontsize())],
            [sg.T("デッドリフト",pad=(0,5),size=8),
             sg.Input("",size=5,justification="right",key="deadlift",pad=0,focus=True),sg.T("kg",pad=0),
             sg.B("登録",key="inputbig3_deadlift",pad=((15,0),0),font=fontsize())],
        ],justification="center")],
        [sg.Text("")],
        [sg.T("キャリアハイ記録"),sg.B("更新",font=fontsize(13),key="update_table_big3"),
         sg.HorizontalSeparator()],
        [sg.Table(data_big3,colnames_big3,auto_size_columns=False,justification="center",col_widths=[8,8,10],key="table_big3",num_rows=3)],
        [sg.Text("BIG3 Total:"),sg.Text(f"{big3_total}",key="big3_total"),sg.Text("kg",pad=0)]
    ])]]

    # 上腕
    data_armsize = get_armsize()
    colnames_armsize = ["日付","左腕","右腕"]

    armsizesize_layout =[[sg.Column([
        [sg.T("上腕サイズ入力"),sg.HorizontalSeparator()],
        [sg.Column([
            [sg.B("◀",key="pre_day_armsize",font=fontsize(13),pad=(0,10)),
             sg.Input(datetime.now().strftime(date_format),size=14,key="date_armsize",justification="center",pad=(0,10)),
             sg.B("▶",key="next_day_armsize",font=fontsize(13),pad=((0,10),0)),
             sg.B("TODAY",key="today_armsize",font=fontsize(13),pad=(0,0))],
            [sg.Column([
                [sg.T("左腕",pad=(0,5),size=8)],
                [sg.Input("",size=5,justification="right",key="left_armsize",pad=0,focus=True),sg.T("cm",pad=0)],
            ]),
             sg.Column([
                [sg.T("右腕",pad=(0,5),size=8)],
                [sg.Input("",size=5,justification="right",key="right_armsize",pad=0,focus=True),sg.T("cm",pad=0)],
            ]),
             sg.Column([
                [sg.B("登録",key="input_armsize",font=fontsize())],
            ],vertical_alignment="bottom")],
        ],justification="center")],
        [sg.Text("")],
        [sg.T("データ"),sg.B("更新",font=fontsize(13),key="update_table_armsize"),sg.HorizontalSeparator()],
        [sg.Table(data_armsize,colnames_armsize,auto_size_columns=False,justification="center",col_widths=[10,4,4],key="table_armsize",num_rows=1)],
    ],justification="center")]]

    tab = [sg.TabGroup([
            [sg.Tab("体重",weight_layout)],
            [sg.Tab("BIG3",big3_layout)],
            [sg.Tab("上腕",armsizesize_layout)],
          ],key="tab")]


    layout = [
        [sg.Text("Body manager",font=fontsize(22,bold=True),pad=(2,(2,10)))],
        [tab]
        ]


    window = sg.Window("Body Manager",
                       layout,
                       location=location,
                       finalize=True,
                       font=fontsize(18))

    window["weight"].bind("<Return>","-return")
    window["benchpress"].bind("<Return>","-return")
    window["squat"].bind("<Return>","-return")
    window["deadlift"].bind("<Return>","-return")
    window["right_armsize"].bind("<Return>","-return")


    while True:
        event, values = window.read(timeout=100)

        if event == None:
            break

        # 当日以外の日付は赤文字に
        if values["date_weight"] == datetime.now().strftime(date_format):
            window["date_weight"].update(text_color=black)
        else:
            window["date_weight"].update(text_color=red)

################################# 日付の処理 ########################################
        if "_day" in event:
            if "pre_" in event: delta = -1
            if "next_" in event: delta = 1
            if "_weight" in event: key = "date_weight"
            if "_big3" in event: key = "date_big3"
            if "_armsize" in event: key = "date_armsize"

            date = datetime.strptime(values[key],date_format)
            date = date + timedelta(days=delta)
            date = date.strftime(date_format)
            window[key].update(value=date)

        if "today_" in event:
            if "_weight" in event: key = "date_wight"
            if "_big3" in event: key = "date_big3"
            date = datetime.now().strftime(date_format)
            window[key].update(value=date)

#############################w 体重を入力する処理 ######################################
        if event == "weight-return":
            window["input_weight"].ButtonCallBack()

        if "input_weight" in event:
            # 日付
            date = datetime.strptime(values["date_weight"],date_format)

            # 体重
            if "preday" not in event:
                try:
                    weight = "{:.2f}".format(float(values["weight"]))
                except:
                    sg.PopupOK("入力値が不正です。",location=popup_location)
                    continue
            else:
                weight_log = window["table_weight"].get()
                preday =  (date+timedelta(-1)).strftime(date_format)
                for i in weight_log:
                    if i[0] == preday:
                        weight = i[1]

            try:
                insert_weight(date,weight)
            except psycopg2.errors.UniqueViolation:
                comfirm = confirm_update_popup(values["date_weight"])
                if comfirm == "OK":
                    update_weight(date,weight)

            except psycopg2.OperationalError:
                sg.PopupOK("サーバーに接続できません。",location=popup_location)
                continue

            # 入力完了後、日付表示を翌日に
            date = datetime.strptime(values["date_weight"],date_format)
            date = date + timedelta(days=1)
            date = date.strftime(date_format)
            window["date_weight"].update(date)

            data_weight = get_weight()
            window["table_weight"].update(data_weight)

#############################w BIG3記録を入力する処理 ######################################
        if event == "benchpress-return":
            window["inputbig3_benchpress"].ButtonCallBack()
        if event == "squat-return":
            window["inputbig3_squat"].ButtonCallBack()
        if event == "deadlift-return":
            window["inputbig3_deadlift"].ButtonCallBack()

        if "inputbig3_" in event:
            if "benchpress" in event:event_name = "ベンチプレス"
            if "squat" in event:event_name = "スクワット"
            if "deadlift" in event:event_name = "デッドリフト"

            if values[event[event.find("_")+1:]]:
                try:
                    insert_big3(values["date_big3"],event_name,values[event[event.find("_")+1:]])
                except psycopg2.errors.UniqueViolation:
                    comfirm = confirm_update_popup(values["date_big3"])
                    if comfirm == "OK":
                        update_big3(values["date_big3"],event_name,values[event[event.find("_")+1:]])
                except psycopg2.OperationalError:
                    sg.PopupOK("サーバーに接続できません。",location=popup_location)
                    continue

            data_big3 = get_big3()
            window["table_big3"].update(data_big3)
            big3_total = data_big3[0][1]+data_big3[1][1]+data_big3[2][1]
            window["big3_total"].update(data_big3)

#############################w 腕サイズ記録を入力する処理 ######################################
        if event == "right_armsize-return":
            window["input_armsize"].ButtonCallBack()

        if "input_armsize" in event:
            try:
                insert_armsize(values["date_armsize"],values["left_armsize"],values["right_armsize"])
            except psycopg2.errors.UniqueViolation:
                comfirm = confirm_update_popup(values["date_armsize"])
                if comfirm == "OK":
                    update_armsize(values["date_armsize"],values["left_armsize"],values["right_armsize"])
            except psycopg2.OperationalError:
                sg.PopupOK("サーバーに接続できません。",location=popup_location)
                continue

            data_armsize = get_armsize()
            window["table_armsize"].update(data_armsize)

#############################w テーブル更新 ######################################
        if "update_table_" in event:
            if "_weight" in event:
                data_weight = get_weight()
                window["table_weight"].update(data_weight)
            if "_big3" in event:
                data_big3 = get_big3()
                window["table_big3"].update(data_big3)
            if "_armsize" in event:
                data_armsize = get_armsize()
                window["table_armsize"].update(data_armsize)


def fontsize(fontsize=15,bold=False):
    if not bold:
        return ("Meiryo UI",fontsize)
    else:
        return ("Meiryo UI",fontsize,"bold")

def confirm_update_popup(confirmation_date):
    return sg.PopupOKCancel(f'{confirmation_date}のデータは既に存在しています。\n更新しますか？',location=popup_location,font=fontsize())


##################################### 体重テーブル d########################################dd
def conn_db():
    ip = supabase.IP
    port = supabase.PORT
    dbname = supabase.DB
    user = supabase.USER
    pw = supabase.PW

    return f"host={ip} port={port} dbname={dbname} user={user} password={pw}"

def get_weight():
    sql = f"""
        SELECT date,yuya_weight,yuya_moving_avg
        FROM weekly_weight_moving_avg
        ORDER BY date DESC
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()

    for i in range(len(data)):
        data[i] = list(data[i])
        data[i][0] = data[i][0].strftime(date_format)

    return data

def insert_weight(date,weight):
    sql = f"""
        INSERT INTO weight_log (date,yuya_weight)
        VALUES (\'{date}\',{weight})
        """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def update_weight(date,weight):
    sql = f"""
        update weight_log
        SET yuya_weight = {weight}
        WHERE date = \'{date}\'
        """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

##################################### BIG3テーブル d########################################dd
def get_big3():
    sql = f"""
        SELECT
            event_name,
            record,
            to_char(date_updated,'YYYY/MM/DD')
        FROM big3_max
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchall()

    # ソート
    order_list = ["ベンチプレス","スクワット","デッドリフト"]
    big3_record = [data[j] for i in range(3) for j in range(3) if order_list[i]==data[j][0]]

    return big3_record

def insert_big3(date,event_name,record):
    sql = f"""
        INSERT INTO big3_record (date_updated,event_name,record)
        VALUES (\'{date}\',\'{event_name}\',{record})
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def update_big3(date,event_name,record):
    sql = f"""
        update big3_record
        SET record = {record}
        WHERE date_updated = \'{date}\'
        AND event_name = \'{event_name}\'
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

##################################### 上腕サイズテーブル d########################################dd
def get_armsize():
    sql = f"""
        SELECT
            to_char(date_updated,'YYYY/MM/DD'),
            left_arm,
            right_arm
        FROM arm_size
        ORDER BY right_arm DESC
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            data = cur.fetchone()

    return [data]

def insert_armsize(date,left,right):
    sql = f"""
        INSERT INTO arm_size (date_updated,left_arm,right_arm)
        VALUES (\'{date}\',\'{left}\',{right})
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

def update_armsize(date,left,right):
    sql = f"""
        UPDATE arm_size
        SET left_arm = {left},
            right_arm = {right}
        WHERE date_updated = \'{date}\'
    """
    with psycopg2.connect(conn_db()) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

try:
    main()
except psycopg2.OperationalError as e:
    window = sg.Window("Body Manager",[[sg.Text(f"サーバーに接続できません。\n{e}")]], location=location,finalize=True)
    while True:
        event,values = window.read()
        if event is None:
            break
