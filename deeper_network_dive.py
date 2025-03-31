import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import datetime
import community as community_louvain  # For Louvain community detection
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64
from io import BytesIO
import plotly.graph_objects as go  # For interactive visualization
import re  # For pattern matching in account names

# Set up directories with date
current_date = datetime.datetime.now().strftime('%Y-%m-%d')
base_dir = '/Users/charleenadams/scraping_insta'
output_dir = os.path.join(base_dir, f'network_analysis_{current_date}')
os.makedirs(output_dir, exist_ok=True)

# Read the data
input_file = os.path.join(base_dir, 'instagram_following.txt')
data = {}
all_following = set()
with open(input_file, 'r') as file:
    for line in file:
        if ':' in line:
            account, following = line.split(':', 1)
            account = account.strip()
            following = following.strip().strip('[]').replace("'", "").split(', ')
            data[account] = following
            all_following.update(following)

# Create a directed graph
G = nx.DiGraph()
for account in data:
    G.add_node(account)
for account, following in data.items():
    for followed in following:
        G.add_node(followed)
        G.add_edge(account, followed)

# Basic stats
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
print(f"Number of nodes (accounts): {num_nodes}")
print(f"Number of edges (follow relationships): {num_edges}")

# Industry-standard metrics
# 1. Degree Centrality (In-degree: most followed, Out-degree: most following)
in_degree_centrality = nx.in_degree_centrality(G)
out_degree_centrality = nx.out_degree_centrality(G)
top_in_degree = sorted(in_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
top_out_degree = sorted(out_degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

# 2. Betweenness Centrality (key connectors)
betweenness_centrality = nx.betweenness_centrality(G)
top_connectors = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

# 3. Closeness Centrality (proximity to others)
closeness_centrality = nx.closeness_centrality(G)
top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

# 4. PageRank (influence)
pagerank = nx.pagerank(G)
top_pagerank = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:10]

# 5. Community Detection (Louvain method)
partition = community_louvain.best_partition(G.to_undirected())
communities = {}
for node, comm_id in partition.items():
    if comm_id not in communities:
        communities[comm_id] = []
    communities[comm_id].append(node)
print(f"\nNumber of communities detected: {len(communities)}")
community_sizes = [(comm_id, len(comm)) for comm_id, comm in communities.items()]
community_sizes.sort(key=lambda x: x[1], reverse=True)

# Save metrics to tables
in_degree_df = pd.DataFrame(top_in_degree, columns=['Account', 'In-Degree Centrality'])
in_degree_df.to_csv(os.path.join(output_dir, 'in_degree_centrality.csv'), index=False)

out_degree_df = pd.DataFrame(top_out_degree, columns=['Account', 'Out-Degree Centrality'])
out_degree_df.to_csv(os.path.join(output_dir, 'out_degree_centrality.csv'), index=False)

betweenness_df = pd.DataFrame(top_connectors, columns=['Account', 'Betweenness Centrality'])
betweenness_df.to_csv(os.path.join(output_dir, 'betweenness_centrality.csv'), index=False)

closeness_df = pd.DataFrame(top_closeness, columns=['Account', 'Closeness Centrality'])
closeness_df.to_csv(os.path.join(output_dir, 'closeness_centrality.csv'), index=False)

pagerank_df = pd.DataFrame(top_pagerank, columns=['Account', 'PageRank'])
pagerank_df.to_csv(os.path.join(output_dir, 'pagerank.csv'), index=False)

community_df = pd.DataFrame(community_sizes, columns=['Community ID', 'Size'])
community_df.to_csv(os.path.join(output_dir, 'community_sizes.csv'), index=False)

# Export network edges
edges_df = pd.DataFrame(G.edges(), columns=['Source', 'Target'])
edges_df.to_csv(os.path.join(output_dir, 'network_edges.csv'), index=False)

# Function to save figure and generate HTML
def save_fig_and_html(fig, filename, title):
    fig.savefig(os.path.join(output_dir, filename), dpi=600, bbox_inches='tight')
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=600, bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    html_content = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
    <h1>{title}</h1>
    <img src="data:image/png;base64,{img_str}" alt="{title}">
    </body>
    </html>
    """
    with open(os.path.join(output_dir, filename.replace('.png', '.html')), 'w') as f:
        f.write(html_content)
    plt.close(fig)

# Function to save table to HTML
def save_table_to_html(df, filename, title):
    html_content = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
    <h1>{title}</h1>
    {df.to_html(index=False)}
    </body>
    </html>
    """
    with open(os.path.join(output_dir, filename), 'w') as f:
        f.write(html_content)

# Deep Dive into Communities
# Categorize accounts based on naming patterns
def categorize_account(account):
    account = account.lower()
    # University-based
    university_keywords = ['harvard', 'mit', 'bu', 'yale', 'brown', 'columbia']
    if any(keyword in account for keyword in university_keywords):
        return 'University'
    # Regional
    regional_keywords = ['boston', 'bayarea', 'pittsburgh', 'nyc', 'chicago']
    if any(keyword in account for keyword in regional_keywords):
        return 'Regional'
    # Thematic
    thematic_keywords = ['healthcare', 'legal', 'youth', 'sjp', 'bds', 'jvp', 'palestine']
    if any(keyword in account for keyword in thematic_keywords):
        return 'Thematic'
    return 'Other'

# Analyze the largest communities (around 400 accounts)
largest_communities = [comm_id for comm_id, size in community_sizes if 350 <= size <= 450]
community_composition = []
for comm_id in largest_communities:
    accounts = communities[comm_id]
    categories = [categorize_account(account) for account in accounts]
    category_counts = Counter(categories)
    total_accounts = len(accounts)
    composition = {
        'Community ID': comm_id,
        'Size': total_accounts,
        'University': category_counts['University'],
        'Regional': category_counts['Regional'],
        'Thematic': category_counts['Thematic'],
        'Other': category_counts['Other']
    }
    community_composition.append(composition)

# Save community composition to a table
community_composition_df = pd.DataFrame(community_composition)
community_composition_df.to_csv(os.path.join(output_dir, 'largest_community_composition.csv'), index=False)

# Visualize community composition
fig_composition, ax_composition = plt.subplots(figsize=(10, 6))
community_composition_df.set_index('Community ID')[['University', 'Regional', 'Thematic', 'Other']].plot(kind='bar', stacked=True, ax=ax_composition)
plt.title("Composition of Largest Communities (350-450 Accounts)")
plt.xlabel("Community ID")
plt.ylabel("Number of Accounts")
plt.legend(title="Category")
save_fig_and_html(fig_composition, 'largest_community_composition.png', 'Composition of Largest Communities')

# Visualizations
# 1. Interactive Network Visualization with Plotly
pos = nx.spring_layout(G, k=0.1)  # Use spring layout for better spread
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
node_text = []
node_colors = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)
    node_colors.append(partition[node])

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    text=node_text,
    marker=dict(
        showscale=True,
        colorscale='Viridis',
        color=node_colors,
        size=10,
        colorbar=dict(
            thickness=15,
            title='Community',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

fig_interactive = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='Interactive Instagram Following Network',
                                titlefont_size=16,
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=20, l=5, r=5, t=40),
                                annotations=[dict(
                                    text="Zoom and hover to explore nodes",
                                    showarrow=False,
                                    xref="paper", yref="paper",
                                    x=0.005, y=-0.002)],
                                xaxis=dict(showgrid=False, zeroline=False),
                                yaxis=dict(showgrid=False, zeroline=False))
                            )

fig_interactive.write_html(os.path.join(output_dir, 'interactive_network.html'))

# 2. Subgraph of Top In-Degree Nodes
top_nodes = [node for node, _ in top_in_degree]
subgraph = G.subgraph(top_nodes)
fig2, ax2 = plt.subplots(figsize=(10, 8))
pos_sub = nx.spring_layout(subgraph)
nx.draw(subgraph, pos_sub, node_size=300, node_color='salmon', edge_color='gray', with_labels=True, font_size=8)
plt.title("Subgraph of Top 10 Most Followed Accounts")
save_fig_and_html(fig2, 'top_in_degree_subgraph.png', 'Subgraph of Top 10 Most Followed Accounts')

# 3. Bar Plot for In-Degree Centrality
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x='In-Degree Centrality', y='Account', data=in_degree_df, palette='Blues_r')
plt.title("Top 10 Most Followed Accounts (In-Degree Centrality)")
save_fig_and_html(fig3, 'in_degree_barplot.png', 'Top 10 Most Followed Accounts (In-Degree Centrality)')

# 4. Bar Plot for Out-Degree Centrality
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x='Out-Degree Centrality', y='Account', data=out_degree_df, palette='Greens_r')
plt.title("Top 10 Accounts Following the Most (Out-Degree Centrality)")
save_fig_and_html(fig4, 'out_degree_barplot.png', 'Top 10 Accounts Following the Most (Out-Degree Centrality)')

# 5. Community Size Distribution
fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.histplot([size for _, size in community_sizes], bins=20, kde=True)
plt.title("Distribution of Community Sizes")
plt.xlabel("Community Size")
plt.ylabel("Frequency")
save_fig_and_html(fig5, 'community_size_distribution.png', 'Distribution of Community Sizes')

# Save tables to HTML
save_table_to_html(in_degree_df, 'in_degree_table.html', 'Top 10 Most Followed Accounts (In-Degree Centrality)')
save_table_to_html(out_degree_df, 'out_degree_table.html', 'Top 10 Accounts Following the Most (Out-Degree Centrality)')
save_table_to_html(betweenness_df, 'betweenness_table.html', 'Top 10 Key Connectors (Betweenness Centrality)')
save_table_to_html(closeness_df, 'closeness_table.html', 'Top 10 Accounts by Closeness Centrality')
save_table_to_html(pagerank_df, 'pagerank_table.html', 'Top 10 Accounts by PageRank')
save_table_to_html(community_df, 'community_sizes_table.html', 'Community Sizes')
save_table_to_html(community_composition_df, 'largest_community_composition_table.html', 'Composition of Largest Communities')

print(f"\nAll figures and tables saved to {output_dir}")
print(f"Interactive network visualization saved as 'interactive_network.html' in {output_dir}")
