import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':
    df = pd.read_csv(r"C:\Users\Dan\PycharmProjects\Random-Walk-Betweenness\scripts\presentation_fig2_data.csv")
    df["method_name"] = df["method_name"].apply(lambda x: "my implementation" if x == "brandes" else "existing implementation")
    df = df[df["nodes"] % 100 == 0]

    ax = sns.pointplot(
        x="nodes",
        y="time",
        hue="method_name",
        data=df,
        dodge=False,
        ci=95,
        capsize=0.5,
        linestyles=":",
        errwidth=1,
        markers="."
    )

    plt.show()
