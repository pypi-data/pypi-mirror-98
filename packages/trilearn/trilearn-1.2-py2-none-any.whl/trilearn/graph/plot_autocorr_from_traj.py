import pandas as pd
import numpy as np
import networkx as nx                                                  
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
import seaborn as sns
from trilearn.graph import trajectory

sns.set_style("whitegrid")

def edges_str_to_list(str):
    edges_str = str[1:-1].split(",")
    edges = [(int(edge.split("-")[0]), int(edge.split("-")[1])) for edge in edges_str if len(edge.split("-"))==2]
    return edges

df = pd.read_csv("traj.csv", sep=";")
g = nx.Graph()
size = []

for index, row in df.iterrows():
    added = edges_str_to_list(row["added"])
    removed = edges_str_to_list(row["removed"])
    g.add_edges_from(added)
    g.remove_edges_from(removed)
    size.append(g.size())

df["size"] = size
T= df["index"].iloc[-1] # approximate length

newindex = pd.Series(range(T))
df2 = df[["index","size"]][2:].set_index("index") # removes the two first rows.

df2 = df2.reindex(newindex).reset_index().reindex(columns=df2.columns).fillna(method="ffill")

pd.plotting.autocorrelation_plot(df2["size"])
plt.savefig("autocorr.png")
plt.clf()
df2["size"].plot()
plt.savefig("sizetraj.png")
