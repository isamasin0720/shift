#最終版
create table carehomes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
homename VARCHAR,
hometype VARCHAR,
day_worktime INTEGER,
day_shiftnumber INTEGER,
night_worktime INTEGER,
night_shiftnumber INTEGER,
part_worktime INTEGER,
part_shiftnumber INTEGER,
nurse_worktime INTEGER,
nurse_shiftnumber INTEGER,
must_carenumber INTEGER
);

#データ入れ(1行のみ)
insert into carehomes values (1,"小西苑","特別養護老人ホーム",8,10,16,4,4,5,8,6,25);

#データ入れ(複数行)
insert into carehomes values (1,"小西苑","特別養護老人ホーム",8,10,16,4,4,5,8,6,25);
insert into carehomes values (2,"ミノルホーム日野","介護付き有料老人ホーム",8,14,16,6,4,6,8,7,10);
insert into carehomes values (3,"SKTの里","介護老人保健施設",8,6,16,8,4,8,8,7,15);
insert into carehomes values (4,"ヒトメク","サービス付き高齢者住宅",8,14,16,5,4,2,8,0,18);

#テスト版
create table homes (
    id INTEGER　PRIMARY KEY AUTOINCREMENT,
    homename TEXT,
    hometype TEXT,
    worktime1 INTEGER,
);
insert into homes (homename,hometype,worktime1) values ('小西苑','特別養護老人ホーム','8');
insert into homes (homename,hometype,worktime1) values ('実太の里','介護付き有料老人ホーム','16') ;