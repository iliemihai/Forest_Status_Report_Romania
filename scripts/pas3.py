import geopandas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

COUNTIES = ["Arad",
"Argeș",
"Bacău",
"Bihor",
"Bistrița-Năsăud",
"Botoșani",
"Brașov",
"Brăila",
"Buzău",
"Caraș-Severin",
"Constanța",
"Covasna",
"Dolj",
"Galați",
"Harghita",
"Ialomița",
"Maramureș",
"Mehedinți",
"Mureș",
"Olt",
"Prahova",
"Satu Mare",
"Sibiu",
"Suceava",
"Teleorman",
"Timiș",
"Tulcea",
"Vaslui",
"Vâlcea",
"Vrancea",
"București",
"Giurgiu",
"Dâmbovița",
"Gorj",
"Hunedoara",
"Alba",
"Cluj",
"Sălaj",
"Călărași",
"Ilfov",
"Iași",
"Neamț"]

sns.set(style="ticks",
        rc={
            "figure.figsize": [12, 7],
            "text.color": "white",
            "axes.labelcolor": "white",
            "axes.edgecolor": "white",
            "xtick.color": "white",
            "ytick.color": "white",
            "axes.facecolor": "#5C0E10",
            "figure.facecolor": "#5C0E10"}
        )

def get_word_counts(df):

    words = df[df["is_alphabet"] == True]["text_lower"].count()
    print("Words:", words)

    unique_words = df[df["is_alphabet"] == True]["lemma_lower"].nunique()
    print("Unique words:", unique_words)

def plot_most_used_words(df):

    # Only take into account alphabet tokens that are longer than 1 character and are not stop words.
    words = df[
        (df["is_alphabet"] == True) &
        (df["is_stopword"] == False) &
        (df["lemma_lower"].str.len() > 1)
    ]["lemma_lower"].value_counts()[:20]

    sns.barplot(x=words.values, y=words.index, palette="Blues_d", linewidth=0)
    plt.xlabel("Occurrences Count")
    plt.title("Most Frequent Words")
    plt.savefig("words_counts.png", facecolor="#5C0E10")

def get_entity_counts(df):

    entities = df["label"].value_counts()
    print(entities)

    locations = df[df["label"] == "ORG"]["text"].value_counts()
    print(locations)

def get_state_counts(df):
    """Gets the number of counts per state.
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be analyzed.
    """

    total_count = 0
    state_counts = list()

    # We will get the count for each state.
    for state in STATES:

        state_count = len(df[df["text_lower"] == state.lower()])

        state_counts.append([state, state_count])
        total_count += state_count

    state_counts.sort(key=lambda x: x[1])

    print(state_counts)
    print(total_count)


def plot_map(df):


    # First we read the shape file from its unzipped folder.
    romania_df = geopandas.read_file("./ro_judete_poligon")

    for state in COUNTIES:

        # We remove accent marks and rename Ciudad de Mexico to its former name.
        #clean_name = clean_word(state)

        #if clean_name == "Ciudad de Mexico":
        #    clean_name = "Distrito Federal"
        #elif clean_name == "Estado de Mexico":
        #    clean_name = "Mexico"

        # We insert the count value into the row with the matching ADMIN_NAME (state name).
        romania_df.loc[romania_df["name"] == state, "count"] = len(df[df["text_lower"].str.contains(state.lower())])

    plt.rcParams["figure.figsize"] = [12, 8]

    romania_df.plot(column="count", cmap="plasma", legend=True)
    plt.title("Mentions by State")
    plt.savefig("map.png", facecolor="#5C0E10")


def clean_word(word):

    for index, char in enumerate(ACCENT_MARKS):
        word = word.replace(char, FRIENDLY_MARKS[index])

    return word

def plot_sentiment_analysis(df):

    # Only take into account scores between -10 and 10.
    df = df[(df["score"] <= 10) & (df["score"] >= -10)]

    # We will make bars with a score below zero yellow and
    # bars with a score above zero blue.
    colors = np.array([(0.811, 0.913, 0.145)]*len(df["score"]))
    colors[df["score"] >= 0] = (0.529, 0.870, 0.972)

    yticks_labels = [str(i) for i in range(-12, 12, 2)]
    plt.yticks(np.arange(-12, 12, 2), yticks_labels)

    plt.bar(df.index, df["score"], color=colors, linewidth=0)
    plt.xlabel("Sentence Number")
    plt.ylabel("Score")
    plt.title("Sentiment Analysis")
    plt.savefig("sentiment_analysis.png", facecolor="#5C0E10")

def plot_donut(df):

    # We will only need 3 categories and 3 values.
    labels = ["Positivo", "Negativo", "Neutro"]

    positive = len(df[df["score"] > 0])
    negative = len(df[df["score"] < 0])
    neutral = len(df[df["score"] == 0])

    values = [positive, negative, neutral]
    colors = ["green", "orange", "yellow"]
    explode = (0, 0, 0)  # Explode a slice if required

    plt.rcParams["font.size"] = 18
    plt.rcParams["legend.fontsize"] = 20

    plt.pie(values, explode=explode, labels=None,
            colors=colors, autopct='%1.1f%%', shadow=False)

    # We draw a circle in the Pie chart to make it a donut chart.
    centre_circle = plt.Circle(
        (0, 0), 0.75, color="#5C0E10", fc="#5C0E10", linewidth=0)

    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis("equal")
    plt.legend(labels)
    plt.savefig("donut.png",  facecolor="#5C0E10")

if __name__ == "__main__":

    tokens_df = pd.read_csv("./tokens.csv")
    entities_df = pd.read_csv("./entities.csv")
    sentences_df = pd.read_csv("./sentences.csv")

    get_word_counts(tokens_df)
    get_entity_counts(entities_df)
    plot_most_used_words(tokens_df)
    plot_map(entities_df)
    #plot_sentiment_analysis(sentences_df)
    #plot_donut(sentences_df)
