import streamlit as st
import http.client as http
import json
import pandas as pd
import os
# from dotenv import load_dotenv

# Load variables from .env file
# load_dotenv()
key = "64c004a78ca539de6c7cde0858ec2010"


def get_standings(season):
    connection = http.HTTPSConnection("v1.basketball.api-sports.io")

    headers = {
    'x-rapidapi-host': "v1.basketball.api-sports.io",
    'x-rapidapi-key': key
    }

    connection.request("GET", f"/standings?league=12&season={season}", headers=headers)
    res = connection.getresponse()
    data = res.read()

    try:
        json_data  = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
        exit(1)

    response = json_data.get("response", [])
    standings_data = response[0]

    return standings_data

def sort_standings_data(seasons):
    nba_data = get_standings(seasons)
    team_list = []
    nba_standings = []
    for team in nba_data:
        if team['team']['name'] not in team_list:
            team_data = {
                "Rank": team.get("position", ""),
                "Team": team.get("team", {}).get("name"),
                "Wins": team.get("games", {}).get("win", {}).get("total", 0),
                "Losses": team.get("games", {}).get("lose", {}).get("total", 0),
                "Conference": team.get("group", {}).get("name", "")
            }
            team_list.append(team['team']['name'])
            nba_standings.append(team_data)
    return nba_standings



with st.container():
    st.header("NBA Standings")

    option = st.selectbox(
        "What NBA season do you want to see standings for?",
        ("2021-2022", "2022-2023")
    )
    
    tab1, tab2 = st.tabs(["Western Conference", "Eastern Conference"])

    with tab1:
        nba_west = []
        for nba_team in sort_standings_data(option):
            if nba_team['Conference'] == "Western Conference":
                nba_west.append(nba_team)
        df = pd.DataFrame(nba_west)
        st.dataframe(df, hide_index=True)

    with tab2:
        nba_east = []
        for nba_team in sort_standings_data(option):
            if nba_team['Conference'] == "Eastern Conference":
                nba_east.append(nba_team)
        df = pd.DataFrame(nba_east)
        st.dataframe(df, hide_index=True)
        