import streamlit as st
import pandas as pd
import gspread as gs
import datetime

gc = gs.service_account_from_dict(st.secrets.cred)
## gspread - Player Pool
sh1 = gc.open('2025 Playoff Fantasy Football Player Pool')
ws1 = sh1.worksheet('2025 Player Pool')
## entry sheet
# sh2 = gc.open('2024 BFPP Submissions')
# ws2 = sh2.worksheet('Sheet 1')


def connect_to_google_sheets():
    try:
        # gc = gs.service_account_from_dict(creds)
        sh2 = gc.open('2025 BFPP Submissions')
        ws2 = sh2.worksheet('Entries')

        return ws2
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

def save_team_to_sheets(user_name, email, selected_players):
    """
    Save the selected team to Google Sheets
    """
    try:
        sheet = connect_to_google_sheets()
        if sheet is None:
            return False

        # Prepare the row to be inserted
        # You can customize the columns as needed
        row_data = [
            user_name,
            email,
            selected_players[0],  # QB1
            selected_players[1],  # QB2
            selected_players[2],  # RB1
            selected_players[3],  # RB2
            selected_players[4],  # RB3
            selected_players[5],  # RB4
            selected_players[6],  # WR1
            selected_players[7],  # WR2
            selected_players[8],  # WR3
            selected_players[9],  # WR4
            selected_players[10],  # TE1
            selected_players[11],  # TE2
            selected_players[12],  # Flex -- Removed 1.5x for 2025
            selected_players[13],  # Flex
            selected_players[14],  # K
            selected_players[15],  # DST
            ', '.join(selected_players),  # All players
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ]

        # Append the row to the sheet
        sheet.append_row(row_data)
        return True
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
        return False

df = pd.DataFrame.from_dict(ws1.get_all_records())

def validate_team_selection(selected_players):
    """
    Validate team selection and return details about team violations
    """
    team_counts = {}
    team_players = {}
    for player in selected_players:
        team = df[df['Player_Team'] == player]['Team'].values[0]
        team_counts[team] = team_counts.get(team, 0) + 1

        if team not in team_players:
            team_players[team] = []
        team_players[team].append(player)

    # Check for teams with more than 2 players
    violations = {
        team: players
        for team, players in team_players.items()
        if len(players) > 2
    }

    return violations


def main():

    # User name input
    user_name = st.text_input("Please enter your name:")

    # User name input
    email = st.text_input("Enter your email if you want the link to the leaderboard and any other updates:")

    if user_name:

        st.markdown("""
             <style>
                 .stMultiSelect [data-baseweb="select"] span{
                     max-width: none !important;
                     white-space: normal !important;
                     overflow: visible !important;
                     text-overflow: clip !important;
                 }
             </style>
             """, unsafe_allow_html=True)
        # Initialize session state for selections
        if 'selected_players' not in st.session_state:
            st.session_state.selected_players = []

        st.markdown("""#### <b><u>Player Selection</u></b>""", unsafe_allow_html=True)
        st.write("**Ignore the the message that says 'You can only select up to x options. Remove an option first.' \n"
                 "That message will pop up when you've picked the proper amount of players in that section.")

        # QB Selection (2 players)
        st.header("Quarterback Selection")
        qb_options = df[df['Position'] == 'QB']['Player_Team'].tolist()
        selected_qb = st.multiselect("Select 2 QBs:", qb_options, max_selections=2)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # RB Selection (4 players)
        st.header("Running Back Selection")
        rb_options = df[df['Position'] == 'RB']['Player_Team'].tolist()
        selected_rbs = st.multiselect("Select 4 RBs:", rb_options, max_selections=4)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # WR Selection (4 players)
        st.header("Wide Receiver Selection")
        wr_options = df[df['Position'] == 'WR']['Player_Team'].tolist()
        selected_wrs = st.multiselect("Select 4 WRs:", wr_options, max_selections=4)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # te Selection (1 player)
        st.header("Tight End Selection")
        te_options = df[df['Position'] == 'TE']['Player_Team'].tolist()
        selected_tes = st.multiselect("Select 2 TEs:", te_options, max_selections=2)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # REMOVED IN 2025 - CHANGED TO 2 REGULAR FLEX
        # # Flex Selection (1 player from RB/WR/TE) 1.5x
        # st.header("Flex (RB, WR, or TE) Selection - 1.5x Points!!")
        # # Remove already selected players from options
        # selected_players_so_far = selected_qb + selected_rbs + selected_wrs + selected_tes
        # flex_options1 = df[(~df['Player_Team'].isin(selected_players_so_far)) & (df['Position'].isin(['RB','WR','TE']))]['Player_Team'].tolist()
        # selected_flex1 = st.multiselect("Select 1 Flex 1.5x:", flex_options1, max_selections=1)

        # Flex Selection (1 player from RB/WR/TE)
        st.header("Flex (RB, WR, or TE) Selection")
        # Remove already selected players from options
        selected_players_so_far = selected_qb + selected_rbs + selected_wrs + selected_tes #+ selected_flex1
        flex_options2 = df[(~df['Player_Team'].isin(selected_players_so_far)) & (df['Position'].isin(['RB','WR','TE']))]['Player_Team'].tolist()
        selected_flex2 = st.multiselect("Select 2 Flex:", flex_options2, max_selections=2)

        # Kicker (1 player from K)
        st.header("Kicker Selection")
        k_options = df[df['Position'] == 'K']['Player_Team'].tolist()
        selected_k = st.multiselect("Select 1 K:", k_options, max_selections=1)

        # DST (1 player from K)
        st.header("Defense/Special Teams Selection")
        dst_options = df[df['Position'] == 'DST']['Player_Team'].tolist()
        selected_dst = st.multiselect("Select 1 DST:", dst_options, max_selections=1)

        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        # Validate team selections
        all_selections = selected_qb + selected_rbs + selected_wrs + selected_tes + selected_flex2 + selected_k + selected_dst #+ selected_flex1

        # Button to finalize team
        if st.button("Validate Team"):
            if len(selected_qb) != 2:
                st.error("Please select exactly 2 Quarterback")
            elif len(selected_rbs) != 4:
                st.error("Please select exactly 4 Running Backs")
            elif len(selected_wrs) != 4:
                st.error("Please select exactly 4 Wide Receivers")
            elif len(selected_tes) != 2:
                st.error("Please select exactly 2 Tight Ends")
            # elif len(selected_flex1) != 1:
            #     st.error("Please select exactly 1 Flex 1.5x Player")
            elif len(selected_flex2) != 2:
                st.error("Please select exactly 2 Flex Players")
            elif len(selected_k) != 1:
                st.error("Please select exactly 1 Kicker")
            elif len(selected_dst) != 1:
                st.error("Please select exactly 1 Defense/Special Teams")
            else:
                # Check for team violations
                team_violations = validate_team_selection(all_selections)

                if team_violations:
                    # Detailed error message about team violations
                    error_message = "Error: You have too many players from the following team(s):\n"
                    for team, players in team_violations.items():
                        error_message += f"- {team}: {', '.join(players)}\n"
                    st.error(error_message)
                # else:
                #     st.success(f"Team successfully created for {user_name}!")
                #     # Display final team
                #     st.write("Your Team:")
                #     for player in all_selections:
                #         player_info = df[df['Player_Team'] == player].iloc[0]
                #         st.write(f"{player} - {player_info['Position']}")

                else:
                    # Attempt to save to Google Sheets
                    if save_team_to_sheets(user_name, email, all_selections):
                        st.success(f"Team successfully created and saved for {user_name}!")
                        # Display final team
                        st.write("Take a screenshot of your team:")
                        for player in all_selections:
                            player_info = df[df['Player_Team'] == player].iloc[0]
                            st.write(f"{player}")
                    else:
                        st.error("Failed to save team to Google Sheets")

    return

if __name__ == '__main__':
    user_input()
