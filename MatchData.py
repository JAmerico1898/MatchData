import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import io
import requests
from io import BytesIO
import urllib.request
from soccerplots.radar_chart import Radar
import matplotlib.colors as mcolors
from scipy.stats import pearsonr
# Loading base file
df = pd.read_csv("MediaMovel_4meses_novo.csv")

#clubs = pd.read_csv("clubes.csv")
#alt_clubs = pd.read_csv("alt_clubes.csv")

# Defining clubes
clubes = ["Vasco", "Athletico", "Atlético Mineiro", "Atlético-GO", "Bahia", "Botafogo", 
          "Corinthians", "Criciúma", "Cruzeiro", "Cuiabá", "Flamengo", 
          "Fluminense", "Fortaleza", "Grêmio", "Internacional", 
          "Juventude", "Palmeiras", "Red Bull Bragantino", "São Paulo", "Vitória"]

metricas_defensivas = ["Recuperação de posse", "Duelos ganhos", 
                       "Duelos defensivos", "Finalizações sofridas", 
                       "PPDA"]

metricas_finalização = ["xG", "xG p/ Finalização", "Finalizações", 
                        "Contra-ataques", "Contra-ataques c/ finalização"]

metricas_ofensivas = ["Corridas", "Cruzamentos", "Cruzamentos certos", "Deep completed crosses", 
                      "Deep completed passes", "Duelos ofensivos", "Duelos ofensivos ganhos", 
                      "Entradas na área de pênalti", "Pisadas na área"]

metricas_construção = ["Passes", "Posse %", "Passes frontais", "Passes frontais certos", 
                       "Passes longos", "Passes longos certos", "Passes terço final", 
                       "Passes terço final certos", "Passes progressivos", 
                       "Passes progressivos certos", "Passes inteligentes", 
                       "Passes inteligentes certos", "Velocidade do jogo", 
                       "Passes médios p/ posse", "% Passes longos", "Comprimento médio do passe", 
                       "Perdas"]

st.markdown("<h4 style='text-align: center;  color: black;'>Desempenho Esportivo dos Clubes da Série A<br>2024 </b></h4>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;  color: black;'>app by @JAmerico1898 </b></h6>", unsafe_allow_html=True)
st.markdown("---")

highlight = st.selectbox("Escolha seu Clube", options=clubes, index=None, placeholder="Escolha seu Clube!")

if highlight == "Vasco":

    # Escolha a Métrica Defensiva 
    metrica_defensiva = st.selectbox("Escolha a Métrica Defensiva", options=metricas_defensivas, index=None, placeholder="Métricas Defensivas!")
    fontsize = 24
    
    if metrica_defensiva:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_defensiva:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_defensiva].values
        opponent_values = team_data[metrica_defensiva + '.1'].values
        
        # Define the rounds for the x-axis
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_defensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the min line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Fill the regions with different colors
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 6-10')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 10-16')

        # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
        max_value = max(df_max['max_metric'])
        min_value = min(df_min['min_metric'])
        padding = (max_value - min_value) * 0.1
        ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
        
        annotation_y = max_value + 1.5 * padding

        # Add annotations above the top spine
        ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_defensiva:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_defensiva].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')
                # Fill the regions with different colors
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

                # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
                max_value = max(df_max['max_metric'])
                min_value = min(df_min['min_metric'])
                padding = (max_value - min_value) * 0.1
                ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
                
                annotation_y = max_value + 1.5 * padding

                # Add annotations above the top spine
                ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_defensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot in Streamlit
        st.pyplot(fig)

##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica de Finalização 
    metrica_finalização = st.selectbox("Escolha a Métrica de Finalização", options=metricas_finalização, index=None, placeholder="Métricas de Finalização!")
    fontsize = 24
    
    if metrica_finalização:

        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_finalização:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_finalização].values
        opponent_values = team_data[metrica_finalização + '.1'].values
        
        # Define the rounds for the x-axis
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_finalização, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the min line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Fill the regions with different colors
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

        # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
        max_value = max(df_max['max_metric'])
        min_value = min(df_min['min_metric'])
        padding = (max_value - min_value) * 0.1
        ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
        
        annotation_y = max_value + 1.5 * padding

        # Add annotations above the top spine
        ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_finalização:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_finalização].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

                # Fill the regions with different colors
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

                # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
                max_value = max(df_max['max_metric'])
                min_value = min(df_min['min_metric'])
                padding = (max_value - min_value) * 0.1
                ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
                
                annotation_y = max_value + 1.5 * padding

                # Add annotations above the top spine
                ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))
                
            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_finalização, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)


##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica de Construção 
    metrica_construção = st.selectbox("Escolha a Métrica de Construção", options=metricas_construção, index=None, placeholder="Métricas de Construção!")
    fontsize = 24
    
    if metrica_construção:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_construção, metrica_construção + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_construção, metrica_construção + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_construção, metrica_construção + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_construção:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Debugging print statement
        #st.write(f"Team data for {highlight}:")
        #st.dataframe(team_data)

        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_construção].values
        opponent_values = team_data[metrica_construção + '.1'].values
        
        # Define the rounds for the x-axis
        #rounds = [4, 5, 6, 7, 8, 9, 10]
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_construção, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the mean line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Fill the regions with different colors
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

        # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
        max_value = max(df_max['max_metric'])
        min_value = min(df_min['min_metric'])
        padding = (max_value - min_value) * 0.1
        ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
        
        annotation_y = max_value + 1.5 * padding

        # Add annotations above the top spine
        ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_construção:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_construção].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

                # Fill the regions with different colors
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

                # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
                max_value = max(df_max['max_metric'])
                min_value = min(df_min['min_metric'])
                padding = (max_value - min_value) * 0.1
                ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
                
                annotation_y = max_value + 1.5 * padding

                # Add annotations above the top spine
                ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_construção, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)

##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica Ofensiva 
    metrica_ofensiva = st.selectbox("Escolha a Métrica de Ofensiva", options=metricas_ofensivas, index=None, placeholder="Métricas Ofensivas!")
    fontsize = 24
    
    if metrica_ofensiva:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_ofensiva:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Debugging print statement
        #st.write(f"Team data for {highlight}:")
        #st.dataframe(team_data)

        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_ofensiva].values
        opponent_values = team_data[metrica_ofensiva + '.1'].values
        
        # Define the rounds for the x-axis
        #rounds = [4, 5, 6, 7, 8, 9, 10]
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_ofensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the mean line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Fill the regions with different colors
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
        ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

        # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
        max_value = max(df_max['max_metric'])
        min_value = min(df_min['min_metric'])
        padding = (max_value - min_value) * 0.1
        ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
        
        annotation_y = max_value + 1.5 * padding

        # Add annotations above the top spine
        ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
        ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                    ha='center', va='bottom', fontsize=10, color='black',
                    bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_ofensiva:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_ofensiva].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

                # Fill the regions with different colors
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 4) & (rounds <= 6), color='lightblue', alpha=0.3, label='Round 4-6')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 6) & (rounds <= 10), color='lightgreen', alpha=0.3, label='Round 7-10')
                ax.fill_between(rounds, 0, team_values, where=(rounds >= 10) & (rounds <= 16), color='lightcoral', alpha=0.3, label='Round 11-16')

                # Calculate the position for annotations (10% higher than the maximum value of the y-axis)
                max_value = max(df_max['max_metric'])
                min_value = min(df_min['min_metric'])
                padding = (max_value - min_value) * 0.1
                ax.set_ylim(bottom=min_value - padding, top=max_value + 2 * padding)
                
                annotation_y = max_value + 1.5 * padding

                # Add annotations above the top spine
                ax.annotate('Paiva 1', xy=(5, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Boina', xy=(8, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightgreen', edgecolor='black', boxstyle='round,pad=0.5'))
                ax.annotate('Paiva 2', xy=(13, annotation_y), xycoords='data',
                            ha='center', va='bottom', fontsize=10, color='black',
                            bbox=dict(facecolor='lightcoral', edgecolor='black', boxstyle='round,pad=0.5'))
                
            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_ofensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

else:

    # Escolha a Métrica Defensiva 
    metrica_defensiva = st.selectbox("Escolha a Métrica Defensiva", options=metricas_defensivas, index=None, placeholder="Métricas Defensivas!")
    fontsize = 24
    
    if metrica_defensiva:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_defensiva, metrica_defensiva + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_defensiva:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_defensiva].values
        opponent_values = team_data[metrica_defensiva + '.1'].values
        
        # Define the rounds for the x-axis
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_defensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the min line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_defensiva:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_defensiva].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_defensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Show the plot in Streamlit
        st.pyplot(fig)

##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica de Finalização 
    metrica_finalização = st.selectbox("Escolha a Métrica de Finalização", options=metricas_finalização, index=None, placeholder="Métricas de Finalização!")
    fontsize = 24
    
    if metrica_finalização:

        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_finalização, metrica_finalização + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_finalização:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_finalização].values
        opponent_values = team_data[metrica_finalização + '.1'].values
        
        # Define the rounds for the x-axis
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_finalização, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the min line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_finalização:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_finalização].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_finalização, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)


##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica de Construção 
    metrica_construção = st.selectbox("Escolha a Métrica de Construção", options=metricas_construção, index=None, placeholder="Métricas de Construção!")
    fontsize = 24
    
    if metrica_construção:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_construção, metrica_construção + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_construção, metrica_construção + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_construção, metrica_construção + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_construção:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Debugging print statement
        #st.write(f"Team data for {highlight}:")
        #st.dataframe(team_data)

        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_construção].values
        opponent_values = team_data[metrica_construção + '.1'].values
        
        # Define the rounds for the x-axis
        #rounds = [4, 5, 6, 7, 8, 9, 10]
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_construção, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the mean line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_construção:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_construção].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_construção, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)

##################################################################################################################
##################################################################################################################
##################################################################################################################

    # Escolha a Métrica Ofensiva 
    metrica_ofensiva = st.selectbox("Escolha a Métrica de Ofensiva", options=metricas_ofensivas, index=None, placeholder="Métricas Ofensivas!")
    fontsize = 24
    
    if metrica_ofensiva:
        # Calculate the mean for both metrica_defensiva and metrica_defensiva + '.1'
        df['mean_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].mean(axis=1)
        df_mean = df.groupby('Order')['mean_metric'].mean().reset_index()
        # Calculate the maximum for both metrica_defensiva and metrica_defensiva + '.1'
        df['max_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].max(axis=1)
        df_max = df.groupby('Order')['max_metric'].max().reset_index()
        # Calculate the minimum for both metrica_defensiva and metrica_defensiva + '.1'
        df['min_metric'] = df[[metrica_ofensiva, metrica_ofensiva + '.1']].min(axis=1)
        df_min = df.groupby('Order')['min_metric'].min().reset_index()

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_ofensiva:}</div>"
        st.markdown("<h4 style='text-align: center;  color: black;'>Análise Comparativa Clube vs Oponentes (2024)<br>Média móvel de 4 jogos</b></h4>", unsafe_allow_html=True)
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")
        
        # Filter the data for the selected team and opponent
        team_data = df[df['Equipe'] == highlight]
        
        # Debugging print statement
        #st.write(f"Team data for {highlight}:")
        #st.dataframe(team_data)

        # Extract the selected variable data for team and opponent
        team_values = team_data[metrica_ofensiva].values
        opponent_values = team_data[metrica_ofensiva + '.1'].values
        
        # Define the rounds for the x-axis
        #rounds = [4, 5, 6, 7, 8, 9, 10]
        rounds = team_data['Order'].values

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(rounds, team_values, label=f'{highlight}', color='red')
        ax.plot(rounds, opponent_values, label=f'Oponentes', color='blue')
        ax.plot(df_mean['Order'], df_mean['mean_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_max['Order'], df_max['max_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.plot(df_min['Order'], df_min['min_metric'], linestyle='--', color='green', linewidth=0.8, label=None)
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_ofensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.set_xticks(rounds)
        ax.set_xticklabels(rounds, fontsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
        
        # Annotate the mean line
        ax.annotate('Média', xy=(df_mean['Order'].iloc[-1], df_mean['mean_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the max line
        ax.annotate('Máximo', xy=(df_max['Order'].iloc[-1], df_max['max_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')
        # Annotate the mean line
        ax.annotate('Mínimo', xy=(df_min['Order'].iloc[-1], df_min['min_metric'].iloc[-1]),
                    xytext=(5, 0), textcoords='offset points', color='green', fontsize=7,
                    ha='left', va='center')

        # Show the plot in Streamlit
        st.pyplot(fig)
        
#Plotting line chart for all clubs highlighting the selected one        

        markdown_1 = f"<div style='text-align:center;  color: black; color: red; font-weight: bold; font-size:{fontsize}px'>{metrica_ofensiva:}</div>"
        st.markdown(markdown_1, unsafe_allow_html=True)
        st.markdown("---")

        # Plot the data for all teams
        fig, ax = plt.subplots()
        for team in df['Equipe'].unique():
            team_data = df[df['Equipe'] == team]
            rounds = team_data['Order'].values
            team_values = team_data[metrica_ofensiva].values
            if team == highlight:
                ax.plot(rounds, team_values, label=f'{team}', color='red', linewidth=2.5)
                # Annotate the team name at the end of the line
                ax.annotate(f'{team}', xy=(rounds[-1], team_values[-1]), xytext=(5, 0),
                            textcoords='offset points', color='red', fontsize=9,
                            ha='left', va='center')

            else:
                ax.plot(rounds, team_values, label=f'{team}', color='grey', linewidth=1, alpha=0.5)
        
        ax.set_xlabel('Média Móvel de 4 Rodadas', fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.set_ylabel(metrica_ofensiva, fontdict={'fontsize': 10, 'fontweight': 'bold'})
        ax.tick_params(axis='y', labelsize=9)
        ax.tick_params(axis='x', labelsize=9)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Show the plot in Streamlit
        st.pyplot(fig)


