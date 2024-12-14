import streamlit as st
import pandas as pd
import gspread as gs

gc = gs.service_account_from_dict(st.secrets.cred)
sh1 = gc.open('2024 Playoff Fantasy Football Player Pool')
ws1 = sh1.worksheet('2024 Player Pool')

df = pd.DataFrame.from_dict(ws1.get_all_records())

        #
        # if st.button("Submit"):
        #     # # Save user selections to Google Sheets
        #     # client = authenticate_google_sheets()
        #     # sheet = client.open('Fantasy Football Draft Selections').sheet1
        #
        #     # Prepare data to be saved
        #     data = {
        #         'Name': user_name,
        #         'QB': qb_selection,
        #         'RB1': rb_selections[0] if len(rb_selections) > 0 else '',
        #         'RB2': rb_selections[1] if len(rb_selections) > 1 else '',
        #         'WR1': wr_selections[0] if len(wr_selections) > 0 else '',
        #         'WR2': wr_selections[1] if len(wr_selections) > 1 else '',
        #         'TE': te_selection,
        #         'Flex': section_5_selection,
        #     }
        #
        #     # # Append to Google Sheet
        #     # sheet.append_row([data[key] for key in data])
        #
        #     st.success(f"Thank you, {user_name}! Your selections have been submitted.")

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

    # st.title("Fantasy Team Picker")
    st.markdown("""#### <b><u>Player Selection</u></b>""", unsafe_allow_html=True)

    # User name input
    user_name = st.text_input("Please enter your name:")

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

        # QB Selection (1 player)
        st.header("Quarterback Selection")
        qb_options = df[df['Position'] == 'QB']['Player_Team'].tolist()
        selected_qb = st.multiselect("Select 1 QB:", qb_options, max_selections=1)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # RB Selection (2 players)
        st.header("Running Back Selection")
        rb_options = df[df['Position'] == 'RB']['Player_Team'].tolist()
        selected_rbs = st.multiselect("Select 2 RBs:", rb_options, max_selections=2)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # WR Selection (2 players)
        st.header("Wide Receiver Selection")
        wr_options = df[df['Position'] == 'WR']['Player_Team'].tolist()
        selected_wrs = st.multiselect("Select 2 WRs:", wr_options, max_selections=2)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # te Selection (1 player)
        st.header("Tight End Selection")
        te_options = df[df['Position'] == 'TE']['Player_Team'].tolist()
        selected_te = st.multiselect("Select 1 TE:", te_options, max_selections=1)

        st.markdown("")
        st.markdown("")
        st.markdown("")

        # Flex Selection (1 player from RB/WR/TE)
        st.header("Flex (RB, WR, or TE) Selection - 1.5x Points!!")
        # Remove already selected players from options
        selected_players_so_far = selected_qb + selected_rbs + selected_wrs + selected_te
        flex_options = df[(~df['Player_Team'].isin(selected_players_so_far)) & (df['Position'].isin(['RB','WR','TE']))]['Player_Team'].tolist()
        selected_flex = st.multiselect("Select 1 Flex 1.5x:", flex_options, max_selections=1)

        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        # Validate team selections
        all_selections = selected_qb + selected_rbs + selected_wrs + selected_te + selected_flex

        # Button to finalize team
        if st.button("Validate Team"):
            if len(selected_qb) != 1:
                st.error("Please select exactly 1 Quarterback")
            elif len(selected_rbs) != 2:
                st.error("Please select exactly 2 Running Backs")
            elif len(selected_flex) != 1:
                st.error("Please select exactly 1 Flex Player")
            else:
                # Check for team violations
                team_violations = validate_team_selection(all_selections)

                if team_violations:
                    # Detailed error message about team violations
                    error_message = "Error: You have too many players from the following team(s):\n"
                    for team, players in team_violations.items():
                        error_message += f"- {team}: {', '.join(players)}\n"
                    st.error(error_message)
                else:
                    st.success(f"Team successfully created for {user_name}!")
                    # Display final team
                    st.write("Your Team:")
                    for player in all_selections:
                        player_info = df[df['Player_Team'] == player].iloc[0]
                        st.write(f"{player} - {player_info['Position']}")
#
#
# # 3. Define a function to collect user input
# def user_input():
#     # Ask for user name
#     user_name = st.text_input("Enter your name:")
#
#     if user_name:
#
#         st.markdown("""
#              <style>
#                  .stMultiSelect [data-baseweb="select"] span{
#                      max-width: none !important;
#                      white-space: normal !important;
#                      overflow: visible !important;
#                      text-overflow: clip !important;
#                  }
#              </style>
#              """, unsafe_allow_html=True)
#
#         # Create user input form for player selections
#         with st.form(key='team_selection'):
#             # Track selected players to exclude from subsequent selections
#             already_selected_players = []
#
#             # QB Selection
#             qb_choices = df[df['Position'] == 'QB']
#             qb = st.multiselect('Select 1 QB:', qb_choices['Player'].tolist(), max_selections=1)
#             selected_players = [{'Player': player, 'Position': 'QB',
#                                  'Team': qb_choices[qb_choices['Player'] == player]['Team'].values[0]} for player in qb]
#             already_selected_players.extend(qb)
#
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#
#             # RB Selections (limit to 2 players)
#             rb_choices = df[(df['Position'] == 'RB') & (~df['Player'].isin(already_selected_players))]
#             rbs = st.multiselect('Select 2 RBs:', rb_choices['Player'].tolist(), max_selections=2)
#             selected_players += [{'Player': player, 'Position': 'RB',
#                                   'Team': rb_choices[rb_choices['Player'] == player]['Team'].values[0]} for player in
#                                  rbs]
#             already_selected_players.extend(rbs)
#
            # st.markdown("")
            # st.markdown("")
            # st.markdown("")
#             st.markdown("")
#             st.markdown("")
#
#             # WR Selections (limit to 2 players)
#             wr_choices = df[(df['Position'] == 'WR') & (~df['Player'].isin(already_selected_players))]
#             wrs = st.multiselect('Select 2 WRs:', wr_choices['Player'].tolist(), max_selections=2)
#             selected_players += [{'Player': player, 'Position': 'WR',
#                                   'Team': wr_choices[wr_choices['Player'] == player]['Team'].values[0]} for player in
#                                  wrs]
#             already_selected_players.extend(wrs)
#
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#
#             # TE Selection
#             te_choices = df[(df['Position'] == 'TE') & (~df['Player'].isin(already_selected_players))]
#             te = st.multiselect('Select 1 TE:', te_choices['Player'].tolist(), max_selections=1)
#             selected_players += [{'Player': player, 'Position': 'TE',
#                                   'Team': te_choices[te_choices['Player'] == player]['Team'].values[0]} for player in
#                                  te]
#             already_selected_players.extend(te)
#
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#
#             # Flexible Position Selection (RB/WR/TE)
#             flex_choices = df[
#                 (df['Position'].isin(['RB', 'WR', 'TE'])) & (~df['Player'].isin(already_selected_players))].copy()
#             flex = st.multiselect('Select 1 additional player from RB/WR/TE:', flex_choices['Player'].tolist(),
#                                   max_selections=1)
#
#             selected_players += [
#                 {'Player': player, 'Position': flex_choices[flex_choices['Player'] == player]['Position'].values[0],
#                  'Team': flex_choices[flex_choices['Player'] == player]['Team'].values[0]} for player in flex]
#
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#             st.markdown("")
#
#             # Submit button
#             submit_button = st.form_submit_button("Submit Selection")
#
#             # Handle the submission logic
#             if submit_button:
#                 # Count how many players have been selected per team
#                 team_counts = {}
#                 for selection in selected_players:
#                     team = selection['Team']
#                     team_counts[team] = team_counts.get(team, 0) + 1
#
#                 # Check for any teams with more than 2 players
#                 error_teams = [team for team, count in team_counts.items() if count > 2]
#
#                 if error_teams:
#                     st.error(f"Error: You have selected more than 2 players from the following teams: {', '.join(error_teams)}. Please fix your selection.")
#                 else:
#                     st.success("Your selections have been submitted successfully!")
#                     st.write(pd.DataFrame(selected_players))  # Optionally display selected players in a table


if __name__ == '__main__':
    user_input()