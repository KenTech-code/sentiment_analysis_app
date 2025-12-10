import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wordcloud import WordCloud
import tkinter as tk

def draw_bar_chart_on_canvas(df, tk_canvas):
    for widget in tk_canvas.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    sentiment_counts = df["Sentiment"].value_counts()
    sentiment_counts.plot(kind="bar", color=["green", "blue", "red"], ax=ax)
    ax.set_title("Sentiment Distribution")
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Count")
    fig.tight_layout()

    plot_to_canvas(fig, tk_canvas)

def draw_word_cloud_on_canvas(df, tk_canvas, show_all=True, show_by_sentiment=True, save_images=False):
    # Clear previous content
    for widget in tk_canvas.winfo_children():
        widget.destroy()

    # --- Scrollable Canvas Setup ---
    scroll_canvas = tk.Canvas(tk_canvas, bg="#f3f3f3")
    scroll_frame = tk.Frame(scroll_canvas, bg="#f3f3f3")

    v_scrollbar = tk.Scrollbar(tk_canvas, orient="vertical", command=scroll_canvas.yview)
    h_scrollbar = tk.Scrollbar(tk_canvas, orient="horizontal", command=scroll_canvas.xview)

    scroll_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")
    scroll_canvas.pack(side="left", fill="both", expand=True)

    window_id = scroll_canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    def on_configure(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all'))
        scroll_canvas.itemconfig(window_id, width=scroll_canvas.winfo_width())

    scroll_frame.bind("<Configure>", on_configure)

    figures = []

    # --- Word Cloud for All Comments ---
    if show_all:
        all_text = " ".join(df["Cleaned_Text"])
        if all_text.strip():
            wc = WordCloud(width=800, height=400, background_color="white").generate(all_text)
            if save_images:
                wc.to_file("wordcloud_all_comments.png")
            fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            ax.set_title("Word Cloud of All Comments")
            fig.tight_layout(rect=[0, 0.03, 1, 0.95])
            figures.append(fig)

    # --- Word Clouds by Sentiment ---
    if show_by_sentiment:
        sentiment_colormaps = {
            "Positive": "Greens",
            "Neutral": "Blues",
            "Negative": "Reds"
        }

        for sentiment, cmap in sentiment_colormaps.items():
            subset = df[df["Sentiment"] == sentiment]
            text = " ".join(subset["Cleaned_Text"])
            if not subset.empty and text.strip():
                wc = WordCloud(width=800, height=400, background_color="white", colormap=cmap).generate(text)
                if save_images:
                    wc.to_file(f"wordcloud_{sentiment.lower()}.png")
                fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                ax.set_title(f"Word Cloud - {sentiment} Comments")
                fig.tight_layout(rect=[0, 0.03, 1, 0.95])
                figures.append(fig)

    # --- Embed All Figures ---
    for fig in figures:
        canvas_plot = FigureCanvasTkAgg(fig, master=scroll_frame)
        canvas_plot.draw()
        canvas_plot.get_tk_widget().pack(pady=15, fill='both', expand=True)

def draw_pie_chart_on_canvas(df, tk_canvas):
    for widget in tk_canvas.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(5.5, 4), dpi=100)
    sentiment_counts = df["Sentiment"].value_counts()
    colors = ["green", "blue", "red"]
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", colors=colors, startangle=140)
    ax.set_title("Sentiment Distribution (Pie Chart)")
    fig.tight_layout()

    plot_to_canvas(fig, tk_canvas)

def draw_color_legend(tk_canvas):
    for widget in tk_canvas.winfo_children():
        widget.destroy()

    legend_window = tk.Frame(tk_canvas, bg="#ffffff")
    legend_window.pack(pady=10)

    tk.Label(legend_window, text="Color Legend", font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=5)

    for label, color in [("Positive", "green"), ("Neutral", "blue"), ("Negative", "red")]:
        row = tk.Frame(legend_window, bg="#ffffff")
        row.pack(pady=2)
        color_box = tk.Label(row, bg=color, width=3, height=1)
        color_box.pack(side="left", padx=10)
        tk.Label(row, text=label, bg="#ffffff", font=("Arial", 10)).pack(side="left")

def plot_to_canvas(fig, tk_canvas):
    for widget in tk_canvas.winfo_children():
        widget.destroy()

    canvas_plot = FigureCanvasTkAgg(fig, master=tk_canvas)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack(pady=10, fill="both", expand=True)
