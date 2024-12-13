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

# Create a dictionary for holding player selections
selected_players = []

# 3. Define a function to collect user input
def user_input():
    # Ask for user name
    user_name = st.text_input("Enter your name:")

    if user_name:

        # Create user input form for player selections
        with st.form(key='team_selection'):
            # QB Selection
            qb_choices = df[df['Position'] == 'QB']
            qb = st.multiselect('Select 1 QB:', qb_choices['Player'].tolist(), max_selections=1)
            selected_players = [{'Player': player, 'Position': 'QB',
                                 'Team': qb_choices[qb_choices['Player'] == player]['Team'].values[0]} for player in qb]

            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # RB Selections (limit to 2 players)
            rb_choices = df[df['Position'] == 'RB']
            rbs = st.multiselect('Select 2 RBs:', rb_choices['Player'].tolist(), max_selections=2)
            selected_players += [{'Player': player, 'Position': 'RB',
                                  'Team': rb_choices[rb_choices['Player'] == player]['Team'].values[0]} for player in
                                 rbs]

            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # WR Selections (limit to 2 players)
            wr_choices = df[df['Position'] == 'WR']
            wrs = st.multiselect('Select 2 WRs:', wr_choices['Player'].tolist(), max_selections=2)
            selected_players += [{'Player': player, 'Position': 'WR',
                                  'Team': wr_choices[wr_choices['Player'] == player]['Team'].values[0]} for player in
                                 wrs]

            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # TE Selection
            te_choices = df[df['Position'] == 'TE']
            te = st.multiselect('Select 1 TE:', te_choices['Player'].tolist(), max_selections=1)
            selected_players += [{'Player': player, 'Position': 'TE',
                                  'Team': te_choices[te_choices['Player'] == player]['Team'].values[0]} for player in
                                 te]

            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # Flexible Position Selection (RB/WR/TE)
            flex_choices = df[df['Position'].isin(['RB', 'WR', 'TE'])]
            flex = st.multiselect('Select 1 additional player from RB/WR/TE:', flex_choices['Player'].tolist(),
                                  max_selections=1)
            selected_players += [
                {'Player': player, 'Position': flex_choices[flex_choices['Player'] == player]['Position'].values[0],
                 'Team': flex_choices[flex_choices['Player'] == player]['Team'].values[0]} for player in flex]

            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")

            # Submit button
            submit_button = st.form_submit_button("Submit Selection")

            # Handle the submission logic
            if submit_button:
                # Count how many players have been selected per team
                team_counts = {}
                for selection in selected_players:
                    team = selection['Team']
                    team_counts[team] = team_counts.get(team, 0) + 1

                # Check for any teams with more than 2 players
                error_teams = [team for team, count in team_counts.items() if count > 2]

                if error_teams:
                    st.error(f"Error: You have selected more than 2 players from the following teams: {', '.join(error_teams)}. Please fix your selection.")
                else:
                    st.success("Your selections have been submitted successfully!")
                    st.write(pd.DataFrame(selected_players))  # Optionally display selected players in a table


if __name__ == '__main__':
    user_input()