import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
# st.set_page_config(page_title="GitHub Projects Insights", layout="wide")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv("github_dataset.csv")

df = load_data()

# Title
st.title("GitHub Projects Insights Dashboard")

# Sidebar
st.sidebar.header("Filters")
selected_language = st.sidebar.multiselect("Select Language", options=df['language'].unique(), default=df['language'].unique()[:5])

# Filter data
filtered_df = df[df['language'].isin(selected_language)]

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Repositories by Stars")
    top_repos = filtered_df.nlargest(10, 'stars_count')
    fig_stars = px.bar(top_repos, x='repositories', y='stars_count', color='language',
                       labels={'stars_count': 'Stars Count', 'repositories': 'Repositories'}, height=400)
    st.plotly_chart(fig_stars, use_container_width=True)

with col2:
    st.subheader("Language Distribution")
    lang_dist = filtered_df['language'].value_counts()
    fig_lang = px.pie(values=lang_dist.values, names=lang_dist.index, height=400)
    st.plotly_chart(fig_lang, use_container_width=True)

st.subheader("Correlation between Stars and Forks")
fig_scatter = px.scatter(filtered_df, x='stars_count', y='forks_count', color='language',
                         hover_data=['repositories'], labels={'stars_count': 'Stars Count', 'forks_count': 'Forks Count'},
                         title='Stars vs Forks by Language')
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Average Contributors per Language")
avg_contributors = filtered_df.groupby('language')['contributors'].mean().sort_values(ascending=False)
fig_contrib = px.bar(avg_contributors, x=avg_contributors.index, y='contributors',
                     labels={'contributors': 'Average Contributors', 'index': 'Language'},
                     title='Average Contributors per Language')
st.plotly_chart(fig_contrib, use_container_width=True)

# Interesting Insight: Pull Request to Issue Ratio
st.subheader("Interesting Insight: Pull Request to Issue Ratio")
filtered_df['pr_issue_ratio'] = filtered_df['pull_requests'] / filtered_df['issues_count']
avg_ratio = filtered_df.groupby('language')['pr_issue_ratio'].mean().sort_values(ascending=False)

fig_ratio = go.Figure()
fig_ratio.add_trace(go.Bar(x=avg_ratio.index, y=avg_ratio.values, name='PR to Issue Ratio'))
fig_ratio.update_layout(title='Average Pull Request to Issue Ratio by Language',
                        xaxis_title='Language', yaxis_title='PR to Issue Ratio')
st.plotly_chart(fig_ratio, use_container_width=True)

st.markdown("""
### Key Insight: Pull Request to Issue Ratio

The Pull Request to Issue Ratio is an interesting metric that can provide insights into the collaborative nature and efficiency of different programming language communities on GitHub. Here's what we can interpret from this ratio:

1. A higher ratio suggests that for every issue opened, there are more pull requests submitted. This could indicate:
   - More active community participation in problem-solving
   - Potentially faster bug fixes and feature implementations
   - A higher proportion of contributors who are comfortable submitting code changes

2. A lower ratio might suggest:
   - More discussion or planning happens in issues before code changes are made
   - The community might be more focused on reporting issues than submitting fixes
   - There could be a higher barrier to entry for submitting pull requests in these languages

This insight can be valuable for understanding the dynamics of different programming language communities on GitHub and could help in making decisions about which languages or projects to focus on for collaboration or contribution.
""")