"""
File for Streamlit standalone interactive page
"""

from matplotlib.figure import Figure

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


total_sample_df = pd.read_csv('./data/blog_data.csv')
total_sample_df = total_sample_df[total_sample_df['sample_id'] != 'wc2018']

plotting_label_dict = {
    "short_pass_pct": "% passes short",
    "ground_pass_pct": "% passes on ground",
    "is_restart_pass": "# restarts",
    "restart_p_m": "Restarts p/\nin-play min.",
    "live_pct": "% passes live play",
    "pct_in_play": "In-play %"
}

# Plotting
def its_a_chart(sample_slug: str) -> Figure:
    fig, axs = plt.subplots(2, 2, sharex=True)
    for ax, stat_label in zip(
            [axs[0, 0], axs[0, 1], axs[1, 0], axs[1, 1]],
            [
                "short_pass_pct",
                "ground_pass_pct",
                "live_pct",
                "restart_p_m",
            ],
    ):
        ax.grid(visible=True, which='major', axis='x', linestyle='--', c='grey')
        ax.set_xlabel("Ball-in-play minutes")
        ax.set_ylabel(plotting_label_dict[stat_label])

        sns.scatterplot(
            data=total_sample_df, x="in_play_time_min", y=stat_label, ax=ax, alpha=0.3, zorder=3
        )
        if sample_slug:
            sns.scatterplot(
                data=total_sample_df[total_sample_df["sample_id"] == sample_slug],
                x="in_play_time_min",
                y=stat_label,
                ax=ax,
                alpha=0.5,
                c="orange",
                zorder=4
            )

    fig.tight_layout()
    fig.subplots_adjust(left=0, bottom=0.1, right=1, top=0.9)

    return fig

st.title("Let's have a sporting kick into touch for ball-in-play measures")

with st.expander("Note on World Cup 2018 data"):
    st.markdown(
        """
        If you're coming to this page from the _Get Goalside_ newsletter then you'll know this already, but I've taken the 
        decision to remove the World Cup 2018 data sample from this work. After checking a particular outlier (the 3rd-place 
        play-off match which, according to the output of my code, had close to 80 minutes of in-play time, I realised that 
        some stoppages were not accurately being captured in the data. In my methodology, this meant that this time - when 
        the TV broadcast was showing replays and it was unclear whether the ball was in or out of play - was being included 
        as in-play time. 
        
        As this was one of the first samples of data that StatsBomb released, and was a clear outlier to the other samples 
        in its high amount of ball-in-play time, my assumed belief is that StatsBomb improved their data collection after 
        releasing this data. 
        """
    )

st.markdown(
    """
    In Sunday school, as a child, we were taught that God loves all His creation in all its diversity, from the lowliest frog to the 
    highliest mountain goat, whether they be big or small, beautiful or not. But FIFA is not God.
    
    There's a diversity of ball-in-play times in football, and football authorities do not seem to love it. As we talked 
    about in the [first newsletter on ball-in-play time](https://www.getgoalsideanalytics.com/stop-the-clock/), matches 
    appear to drift towards an average of 54-56 minutes, within each average is a pretty wide range of ball-in-play 
    values. Many of the sample competitions that we looked at last time had matches with around 45 minutes of in-play 
    time (sometimes called 'effective time'), stretching all the way up to 65. Take a look below: every dot is a single 
    match. 
    """
)

with st.expander("Data sample names key"):
    st.markdown(
        """
        - EPL 2015/16 = English Premier League 2015/16
        - Invincibles = Arsenal 2003/04 Premier League matches
        - ISL 2021/22 = Indian Super League 2021/22
        - WSL 2020/21 = English Women's Super League 2020/21
        - WC 2019 = FIFA Women's World Cup 2019
        - WC 2022 = FIFA Men's World Cup 2022
        - 'Messi' 2011/12 = Barcelona LaLiga games in which Lionel Messi featured, part of StatsBomb's dataset on Messi's LaLiga career
        - LaLiga 2015/16 = Spanish LaLiga 2015/16
        - 'StatsBomb Icons' = StatsBomb Icons dataset, a sample of 10 matches each featuring Johan Cruyff, Diego Maradona, Pelé; filtered to matches which had more than 90 minutes of 'video' time to account for old video issues/U20 matches
        
        _NB: All knock-out tournaments filter out matches which went to extra-time_ 
        """
    )

# There should be an interactive chart here to show that, maybe density plot or something
in_play_fig, in_play_ax = plt.subplots()
in_play_ax.grid(visible=True, which='major', axis='x', linestyle='--', c='grey')
in_play_ax.set_xlabel("Ball-in-play minutes")
in_play_ax.set_ylabel("Sample")
in_play_ax.set_yticklabels(["EPL 2015/16", "Invincibles", "ISL 2021/22", "WSL 2020/21", "WC 2019", "WC 2022", "'Messi' 2011/12", "LaLiga 2015/16", "'StatsBomb Icons'"])
sns.swarmplot(data=total_sample_df, x="in_play_time_min", y="sample_id", ax=in_play_ax, alpha=0.7, size=4, hue="sample_id", legend=False)
in_play_fig.tight_layout()
in_play_fig.subplots_adjust(left=0, bottom=0.05, right=1, top=0.95)

st.pyplot(in_play_fig)

st.markdown(
    """
    What causes these differences though? Why do some matches have a lot more ball-in-play time than others? Why is it 
    apparently perfectly normal for the in-competition range to be ten minutes or more? 
    
    That's the thing I've been looking at, and I, simply put, have a stupidly lowly frog-level thing to say about 
    it. 
    
    If the ball doesn't go out of play, the in-play time is higher. 
    
    That's what it seems to boil down to. Lemme take you through it.
    """
)
st.subheader("In, out, in, out, shake it all about")
st.markdown(
    """
    After the first newsletter, the first thing I wanted to look at was the ball-in-play time for 
    different teams alongside some 'stylistic' statistics. It was kinda boringly predictable though: 
    as a trend, high-possession teams with lots of short passes were involved in matches which, on average, had a higher
    amount of ball-in-play time. 
    
    This was fun and all, but felt like distracting from the point. So let's go right back to basics. 
    
    The charts below have four statistics which are compared with the ball-in-play time of all matches I ran my code on. 
    They are:
    - Short passes: _the percentage of passes which were 15 metres or shorter_
    - Ground passes: _the percentage of passes which were along the ground_
    - Live passes: _the percentage of passes which were 'live' (so, _not_ goal kicks, free kicks, etc)_
    - Restarts per minute of ball-in-play time
    
    You can see the total data, each point representing a match. If you want, you can choose a sample to highlight using 
    the dropdown menu.
    """
)

sample_slug_label_dict = {
    "EPL 2015/16": "epl1516",
    "LaLiga 2015/16": "laliga1516",
    "Arsenal Invincibles EPL season (2003/04)": "invincibles",
    "Barcelona LaLiga 2011/12 (feat. Messi, 37 games)": "messi1112",
    # "Men's World Cup 2018": "wc2018",
    "Women's World Cup 2019": "wc2019",
    "Men's World Cup 2022": "wc2022",
    "StatsBomb Icons sample (Cruyff, Maradona, Pelé)": "statsbombicons",
    "Indian Super League 2021/22": "isl2122",
    "English Women's Super League 2020/21": "wsl2021"
}

selected_sample = st.selectbox(
    label="Choose a sample to highlight: ",
    options=["None - just all data"] + list(sample_slug_label_dict.keys()),
)

selected_slug = sample_slug_label_dict.get(selected_sample)

st.pyplot(its_a_chart(selected_slug))

with st.expander("Read more on the choice of stats..."):
    st.write(
        """
        An interesting thing about choosing these stats is that they probably shouldn't be total numbers: a longer match
        is always likely to have more passes than a shorter match. 
        
        For the number of restarts, I looked at the total number (talked about further down this piece), and the average 
        per _total_ minutes played as well as the in-play minutes. I ultimately decided that restarts per in-play minute
        was the more relevant version, because that's the thing people are interested in and long stoppages between 
        restarts would increase the total time while not increasing the number of restarts.
        
        The two latter statistics - '% of passes live' and 'restarts per in-play minute' are kind of just two ways of 
        showing the same thing. I decided to show them both due to being less sure about the choice of how to show 
        restarts.  
        """
    )

st.write(
    """
    There doesn't look like much of a correlation between a match having lots of short passes (top left) and its 
    ball-in-play time, across these samples of data anyway. (That might just be about the particular cut-off point of 
    'short'). There's more of a link when focusing on passes along the ground (top right), although still with quite a 
    wide range. 
    
    That brings us to the two charts on the bottom row, '% of passes live' and 'restarts per in-play minute'. In a way, 
    they both represent the same type of data: how many passes are in live play compared to being a dead-ball restart. 
    I read them both as saying 'more restarts/stoppages means less in-play time'. After all, this makes sense: if the 
    ball doesn't go out of play then the 'in-play' timer just keeps ticking up and up and up, even if nothing much is 
    really happening. 
    
    Let's look at this in its purest state then, with the total number of restarts for each match compared to the 
    in-play time. The link is a little fuzzier than some of the previous charts, but it's still clear: 
    """
)

# Show that chart
restarts_fig, restarts_ax = plt.subplots()
restarts_ax.grid(visible=True, which='major', axis='x', linestyle='--', c='grey')
restarts_ax.set_xlabel("Ball-in-play minutes")
restarts_ax.set_ylabel("Total restarts")
sns.scatterplot(
    data=total_sample_df, x="in_play_time_min", y="is_restart_pass", ax=restarts_ax, alpha=0.3, zorder=3
)
restarts_fig.tight_layout()
restarts_fig.subplots_adjust(left=0, bottom=0.1, right=1, top=0.9)
st.pyplot(restarts_fig)

st.write(
    """
    This restart correlation might even explain the link between ground pass proportion and in-play time, although my 
    intuition is that any _meaning_ in the link is actually about high passes: 
    - restarts like free-kicks and goal kicks and throw-ins tend to be high passes 
    - high passes are less controlled and therefore probably more likely to bounce out of play (possibly also having 
    longer stoppages as teams collectively move up or down the pitch to follow the long path of the ball).  
    
    The link between number of restarts and in-play time is always going to be a _little_ fuzzy. The stoppages 
    between the restarts can vary in length, meaning two matches can differ in in-play time even with the same number of
    stops, and the length of added time to make up for excessiveness of breaks will also vary. But, yeah - this is a 
    pretty plausible and stupidly simple link.  
    """
)

st.subheader("What this means...")

st.write(
    """
    We've done the data, now we're going to do the semantics.
    
    There's a way of describing football that says that if the ball is in play it's 'live' and if it's not, or if the 
    play hasn't been restarted yet, it's 'dead'. I re-watched half an hour of the 2018 men's World Cup 3rd-place match 
    between Belgium and England to check that data and, believe me, in-play football can be dead.
    
    If you think I've been banging away at this, Twenty First Group have also called the added time push ['a 
    sledgehammer looking for a nail'](https://www.twentyfirstgroup.com/issue-16-injury-time-solution-is-a-sledgehammer-looking-for-a-nail/).
    And Omar Chaudhuri there reaches a similar conclusion that I do: 
    
    _"The single biggest driver of effective playing time is the on-field technical quality of play – not time wasting, 
    as is commonly believed. This is why the Premier League has 15% more ball in play time than League Two, and the 
    Champions League 5% more than the Premier League. Better players and teams keep the ball in play."_
    
    I'm inclined to believe that there's a tactical choice element as well, but the tactical choices to play ground 
    pass-based, keep-ball football only become unlocked when technical, spatial, and pitch-quality levels are good. 
    (That said, high-quality pressing may still disrupt this).  
    
    I don't think it's too far over the line to say that a continued push to increase ball-in-play time beyond levels 
    we have historically seen in football risks casting certain styles of play as illegitimate. If you _want_ a 
    guaranteed 60 minutes of the ball in play (something that appears to be more uncommon than common historically in 
    football, even at the highest level) then what you do not want is the ball to go out of play.
    
    A smarter approach - although an investigation that may be difficult with data taken from TV broadcasts - would be 
    to look at the average time that certain stoppages usually take. There'll be a range for throw-ins, a range for long 
    goal kicks, short goal kicks, corners, goals. There may be important effects for high-physical intensity matches. 
    If the length of time of goal-kick stoppages is increasing compared to matches of similar intensity and exertion 
    from five years ago, then we can talk. But ball-in-play time is a clumsy, flawed - and possibly tactically 
    geo-engineering - measure to use.         
    """
)
