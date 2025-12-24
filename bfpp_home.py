import streamlit as st
import functions as func

st.markdown("""## <b><u>2025 Burholme Fantasy Playoff Pool</u></b>""", unsafe_allow_html=True)
st.markdown("""**One entry per person - \$20 Venmo @Larry-LoveIV or CashApp \$LarryLoveIV. Build one team to ride throughout the playoffs and get the highest cumulative score through the Super Bowl.**

**Top 3 cumulative scores will earn prizes. Last season we had 29 entries for a total pot of $580. Let's try to get a bigger pot this year - if we do, the prizes will look like this:**

**1st - Remaining pot \(\$460 if we reach 30 entries\)  \n2nd - \$100  \n3rd - \$40**

**Submissions must be in before kickoff of the first wildcard playoff game: Saturday Jan. 11th @ 4:30PM EST.**""")
st.markdown("""#### <b><u>Team Building Rules</u></b>  
Fill the positions below using players from the all the playoff teams - you can use no more than 2 players from the 
same team. i.e: you can take Goff and St. Brown, but you can't have Goff, St. Brown, and Gibbs/Lions DST/Jake Bates.

Your first flex position will get you 1.5x points. Last year we had a 2x points flex position, 
but I think 1.5x makes it less important to get that position correct and hopefully diversifies the player ownership there.""", unsafe_allow_html=True)

#
st.markdown("""#### <b><u>Positions</u></b>  
2 QBs  
4 RBs  
4 WRs  
2 TEs  
1 Flex (RB,WR, or TE) - 1.5x Points!  
1 Flex (RB,WR, or TE)  
1 Def/Special Teams  
1 Kicker
""", unsafe_allow_html=True)

# st.markdown("""<b><u>Scoring:</u></b>
# **Passing**
# * Touchdown = 6
# * Yards = 1 / 30 Yards
# * 2 Pt Conv. = 2
# * Interception = -2
# * Fumble = -2
#
# **Receiving**
# * Touchdown = 6
# * Yards = 1 / 10 Yards
# * 2 Pt Conv. = 2
# * Reception = 1
# * Reach 100 Yards = 3
# * Fumble = -2
#
# **Rushing**
# * Touchdown = 6
# * Yards = 1 / 10 Yards
# * 2 Pt Conv. = 2
# * Reach 100 Yards = 3
# * Fumble = -2
#
# **Kickers - No yardage bonus**
# * FG = 3
# * XP = 1
#
# **Defense/ST**
# * 0 Points allowed = 12
# * 2-10 Points allowed = 8
# * 11-20 Points allowed = 5
# * 21-30 Points allowed = 0
# * 31+ Points allowed  = -5
# * Takeaways = 2
# * Touchdowns = 6
# """, unsafe_allow_html=True)
st.markdown("""#### <b><u>Scoring - No decimals</u></b>""", unsafe_allow_html=True)

col1, col2, col3= st.columns([1,1,1])
col5, col6, col7= st.columns([1,1,1])

with col1:
    st.markdown("""**Passing**
* Touchdown = 6
* Yards = 1 / 30 Yards
* 2 Pt Conv. = 2
* Interception = -2
* Fumble = -2""", unsafe_allow_html=True)
with col2:
    st.markdown("""**Receiving**
* Touchdown = 6
* Yards = 1 / 10 Yards
* 2 Pt Conv. = 2
* Reception = 1
* Reach 100 Yards = 3
* Fumble = -2""", unsafe_allow_html=True)
with col3:
    st.markdown("""**Rushing**
* Touchdown = 6
* Yards = 1 / 10 Yards
* 2 Pt Conv. = 2
* Reach 100 Yards = 3
* Fumble = -2""", unsafe_allow_html=True)
with col5:
    st.markdown("""**Kickers - No yardage bonus**
* FG = 3
* XP = 1""", unsafe_allow_html=True)
with col6:
    st.markdown("""**Defense/ST**
* 0 Points allowed = 12
* 2-10 Points allowed = 8
* 11-20 Points allowed = 5
* 21-30 Points allowed = 0
* 31+ Points allowed  = -5
* Takeaways = 2
* Touchdowns = 6""", unsafe_allow_html=True)

st.markdown("""**If you encounter any issues - missing players, players on the wrong team, you want to redo submission, payment issues - just text me: 267-334-6282**""")

if __name__ == '__main__':
    func.main()
