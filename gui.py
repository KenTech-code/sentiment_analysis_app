import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from preprocessing import preprocess_text
from sentiment import analyze_sentiment
from visualization import (
    draw_bar_chart_on_canvas,
    draw_word_cloud_on_canvas,
    draw_pie_chart_on_canvas
)

class SentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Offline Sentiment Analysis Tool")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")

        self.df_raw = pd.DataFrame()
        self.processed_data = pd.DataFrame()
        self.save_wordcloud_flag = tk.BooleanVar()

        # Title
        title = tk.Label(
            root,
            text="Offline Sentiment Analysis Tool",
            font=("Helvetica", 18, "bold"),
            bg="#f0f2f5",
            fg="#333"
        )
        title.pack(pady=10)

        # Button Frame
        btn_frame = tk.Frame(root, bg="#f0f2f5")
        btn_frame.pack(pady=5)

        self.upload_btn = tk.Button(btn_frame, text="📁 Upload File", command=self.upload_file, bg="#4caf50", fg="white", width=15)
        self.upload_btn.grid(row=0, column=0, padx=5)

        self.analyze_btn = tk.Button(btn_frame, text="🧠 Analyze Sentiment", command=self.analyze_sentiment_data, bg="#673ab7", fg="white", width=20, state="disabled")
        self.analyze_btn.grid(row=0, column=1, padx=5)

        self.visual_btn = tk.Button(btn_frame, text="📊 Show Visualizations", command=self.show_visuals, bg="#2196f3", fg="white", width=20, state="disabled")
        self.visual_btn.grid(row=0, column=2, padx=5)

        self.export_btn = tk.Button(btn_frame, text="💾 Export Results", command=self.export_results, bg="#ff9800", fg="white", width=15, state="disabled")
        self.export_btn.grid(row=0, column=3, padx=5)

        self.exit_btn = tk.Button(btn_frame, text="❌ Exit", command=root.quit, bg="#f44336", fg="white", width=10)
        self.exit_btn.grid(row=0, column=4, padx=5)

        self.save_wc_checkbox = tk.Checkbutton(
            root, text="Also save word clouds on export 📁", variable=self.save_wordcloud_flag, bg="#f0f2f5"
        )
        self.save_wc_checkbox.pack()

        # Treeview
        self.columns = ("Text", "Sentiment", "Polarity")
        self.tree = ttk.Treeview(root, columns=self.columns, show='headings')
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=300)
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        # Canvas for visualizations
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            if file_path.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path, encoding='utf-8')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='ISO-8859-1')
                if df.shape[1] > 1:
                    selected_col = self.ask_column_selection(list(df.columns))
                    if selected_col is None:
                        return
                    df = df[[selected_col]].rename(columns={selected_col: "Text"})
                else:
                    df.columns = ["Text"]
            else:
                df = pd.read_csv(file_path, delimiter='\t', header=None, names=["Text"])

            self.df_raw = df
            self.analyze_btn.config(state="normal")
            self.visual_btn.config(state="disabled")
            self.export_btn.config(state="disabled")
            messagebox.showinfo("Success", "File uploaded successfully!\nClick 'Analyze Sentiment' to continue.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file:\n{e}")

    def analyze_sentiment_data(self):
        if self.df_raw.empty:
            messagebox.showwarning("Warning", "Please upload a file first.")
            return
        df = self.df_raw.copy()
        df["Cleaned_Text"] = df["Text"].apply(preprocess_text)
        df[["Sentiment", "Polarity"]] = df["Cleaned_Text"].apply(lambda x: pd.Series(analyze_sentiment(x)))
        self.processed_data = df
        self.update_treeview(df)
        self.visual_btn.config(state="normal")
        self.export_btn.config(state="normal")
        messagebox.showinfo("Analysis Complete", "Sentiment analysis completed.\nResults displayed in the table below.")

    def ask_column_selection(self, column_list):
        selection_window = tk.Toplevel(self.root)
        selection_window.title("Select Column for Analysis")
        selection_window.geometry("350x150")

        label = tk.Label(selection_window, text="Select the column containing text to analyze:")
        label.pack(pady=10)

        selected = tk.StringVar()
        combo = ttk.Combobox(selection_window, values=column_list, textvariable=selected)
        combo.pack(pady=5)
        combo.current(0)

        def confirm():
            selection_window.destroy()

        tk.Button(selection_window, text="Confirm", command=confirm).pack(pady=10)
        selection_window.grab_set()
        selection_window.wait_window()

        return selected.get() if selected.get() else None

    def update_treeview(self, df):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=(row["Text"], row["Sentiment"], round(row["Polarity"], 3)))

    def show_visuals(self):
        if self.processed_data.empty:
            messagebox.showwarning("Warning", "No data to visualize.")
            return

        vis_window = tk.Toplevel(self.root)
        vis_window.title("Select Visualizations")
        vis_window.geometry("350x300")

        tk.Label(vis_window, text="Choose which visualizations to display:").pack(pady=10)

        bar_var = tk.BooleanVar()
        pie_var = tk.BooleanVar()
        sentiment_wc_var = tk.BooleanVar()

        tk.Checkbutton(vis_window, text="📊 Bar Chart (Sentiment Distribution)", variable=bar_var).pack(anchor="w", padx=20)
        tk.Checkbutton(vis_window, text="🥧 Pie Chart (Sentiment Percentages)", variable=pie_var).pack(anchor="w", padx=20)
        tk.Checkbutton(vis_window, text="☁️ Word Clouds by Sentiment", variable=sentiment_wc_var).pack(anchor="w", padx=20)

        def run_selected_visuals():
            vis_window.destroy()
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            if bar_var.get():
                draw_bar_chart_on_canvas(self.processed_data, self.canvas_frame)
            if pie_var.get():
                draw_pie_chart_on_canvas(self.processed_data, self.canvas_frame)
            if sentiment_wc_var.get():
                draw_word_cloud_on_canvas(self.processed_data, self.canvas_frame, show_all=False, show_by_sentiment=True)

        tk.Button(vis_window, text="View Selected", command=run_selected_visuals).pack(pady=15)
        vis_window.grab_set()

    def export_results(self):
        if self.processed_data.empty:
            messagebox.showwarning("Warning", "No data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.processed_data.to_csv(file_path, index=False)
            if self.save_wordcloud_flag.get():
                draw_word_cloud_on_canvas(self.processed_data, self.canvas_frame, show_all=False, show_by_sentiment=True, save_images=True)
            messagebox.showinfo("Exported", "Results exported successfully.")
