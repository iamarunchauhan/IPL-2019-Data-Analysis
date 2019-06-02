from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd
df = pd.read_csv(r"C:\\Users\\Arun\\Desktop\\IPL2019\\media\\matches.csv")
df["team1"] = df["team1"].str.replace("Daredevils","Capitals", case= False)
df["team2"] = df["team2"].str.replace("Daredevils","Capitals", case= False)
df["winner"] = df["winner"].str.replace("Daredevils","Capitals", case= False)
df1 = pd.concat([df.iloc[:, 1:3], df.iloc[:, 4:8], df.iloc[:, 10:11], df.iloc[:, 14:15]], axis=1)
#print(df1.index)

def home(requests):
	if requests.method == 'POST':
		team1_name = requests.POST['tname1'].strip()
		team2_name = requests.POST['tname2'].strip()

		if(team1_name == team2_name):
			return HttpResponse("OOPS ! THE NAME OF TEAM NAMES SHOULD BE DIFFERENT !! ")

		t1bat, t1field, t2bat, t2field = predict(team1_name, team2_name)
		context = {
			'team1_name': team1_name,
			't1bat': t1bat,
			't1field': t1field,
			'team2_name': team2_name,
			't2bat': t2bat,
			't2field': t2field,
		}
		return render(requests, "pages/result.html", context)
	return render(requests, "pages/index.html")

def predict(team_name1, team_name2):
	temp1 = df1[df1['team1'].str.contains(team_name1, regex=False)]
	temp11 = df1[df1['team2'].str.contains(team_name2, regex=False)]
	temp1 = pd.concat([temp1, temp11], axis=0)
	#temp1 = df1[(df1['team1'].str.contains(team_name1, regex=False)) & (df1['team2'].str.contains(team_name2, regex=False))]
	#temp1 = df1.loc[(df1['team1'] == team_name1) & (df1['team2'] == team_name2)]
	#print(temp1.index)
	temp2 = df1[df1['team1'].str.contains(team_name2, regex=False)]
	temp22 = df1[df1['team2'].str.contains(team_name1, regex=False)]
	#temp2 = df1.loc[(df1['team1'] == team_name2) & (df1['team2'] == team_name1)]
	temp2 = pd.concat([temp2, temp22], axis=0)
	resultant = pd.concat([temp1, temp2], axis=0)

	rs = resultant.loc[((resultant['toss_winner'] == team_name2) & (resultant['toss_decision'] == 'bat')) | ((resultant['toss_winner'] == team_name1) & (resultant['toss_decision'] == 'field'))]


	totalchance = len(rs.index)

	rs1 = rs.loc[rs['winner'] == team_name2]

	v1 = len(rs1.index)
	v2 = totalchance - v1
	# ZeroByDivision Error
	team1bat = (v1 / totalchance) * 100
	team1bat = round(team1bat,2)
	team1field = (v2 / totalchance) * 100
	team1field = round(team1field,2)

	rs2 = resultant.loc[((resultant['toss_winner'] == team_name2) & (resultant['toss_decision'] == 'field')) | ((resultant['toss_winner'] == team_name1) & (resultant['toss_decision'] == 'bat'))]

	totalchance1 = len(rs2.index)

	rs3 = rs2.loc[rs2['winner'] == team_name1]

	v3 = len(rs3.index)
	v4 = totalchance1 - v3
	team2bat = (v3 / totalchance1) * 100
	team2bat = round(team2bat, 2)

	team2field = (v4 / totalchance1) * 100
	team2field = round(team2field, 2)

	return team1bat, team1field, team2bat, team2field


def table():
	from bs4 import BeautifulSoup
	import numpy as np
	# import matplotlib.pyplot as plt

	import requests
	page = requests.get("https://www.cricbuzz.com/cricket-series/2810/indian-premier-league-2019/points-table")

	soup = BeautifulSoup(page.text,"html5lib")
	tbl = soup.find("table", class_="table cb-srs-pnts")
	col_names = [x.get_text() for x in tbl.find_all('td', class_="cb-srs-pnts-th")]
	col_names[5] = 'pts'
	team_names = [x.get_text() for x in tbl.find_all('td',class_= "cb-srs-pnts-name")]

	print(team_names)

	pnt_tbl = [x.get_text() for x in tbl.find_all('td', class_="cb-srs-pnts-td")]
	np_pnt_tbl = (np.array(pnt_tbl)).reshape(len(team_names), 7)
	np_pnt_tbl = np.delete(np_pnt_tbl, 6, 1)

	np_pnt_tbl

	np_pnt_tbl = np_pnt_tbl.astype(int)
	print(np_pnt_tbl)

	return render(requests, "pages/index.html")


