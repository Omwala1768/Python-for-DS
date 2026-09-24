import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
F1 = BASE / "Tariff.csv"
F2 = BASE / "Tariff_2.csv"
DIRTY = BASE / "Tariff_dirty.csv"
CLEAN = BASE / "Tariff_cleaned.csv"

SAPPHIRE = "#72B0AB"
ARTIC = "#BCDDDC"
FONT = "Segoe UI"

LIGHT = {
    "bg": "#F3F8F7", "panel": "#FFFFFF", "side": "#073B3B", "side2": "#0D4B4A",
    "text": "#123C3A", "muted": "#607674", "border": "#D5E5E2", "input": "#FFFFFF",
    "hover": "#E5F2F0", "good": "#258A73", "warn": "#E5A33D", "bad": "#E96F5A"
}
DARK = {
    "bg": "#071D21", "panel": "#0D2A2F", "side": "#06191D", "side2": "#0B3437",
    "text": "#E8F5F3", "muted": "#9BB5B2", "border": "#1D4549", "input": "#102F34",
    "hover": "#164448", "good": "#65C8B1", "warn": "#E7B45A", "bad": "#F17C69"
}


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tariff Analytics")
        self.root.geometry("1450x900")
        self.root.minsize(1150, 720)
        self.dark = False
        self.c = LIGHT
        self.page = "Dashboard"
        self.groups = {}

        self.df = self.read(F1)
        if self.df is None:
            messagebox.showerror("Missing Dataset", "Tariff.csv must be in the same folder as this program.")
            root.destroy()
            return
        self.prepare(self.df)

        self.d2 = self.read(F2)
        if self.d2 is not None:
            self.prepare(self.d2)

        self.dirty = self.read(DIRTY)
        if self.dirty is None:
            self.dirty = self.df.head(100).copy()

        self.build()
        self.show_dashboard()

    # ==================== DATA ====================

    def read(self, path):
        if not path.exists():
            return None
        try:
            return pd.read_csv(path)
        except Exception:
            return None

    def prepare(self, d):
        d.columns = d.columns.astype(str).str.strip()
        for col in ["Price Before Tariff", "Price After Tariff"]:
            if col not in d.columns:
                raise ValueError(f"Missing required column: {col}")
            d[col] = pd.to_numeric(d[col], errors="coerce")
        d["Tariff Increase"] = d["Price After Tariff"] - d["Price Before Tariff"]
        d["Tariff Impact %"] = (
            d["Tariff Increase"] / d["Price Before Tariff"].replace(0, np.nan) * 100
        ).fillna(0)
        d["Impact Level"] = d["Tariff Impact %"].apply(
            lambda x: "Low" if x < 20 else "Moderate" if x < 35 else "High"
        )

    def second(self):
        if self.d2 is not None:
            return self.d2
        d = self.df.copy()
        d["Price After Tariff"] = (d["Price Before Tariff"] * 1.3291).round(2)
        self.prepare(d)
        return d

    def money(self, x):
        return f"₹{float(x):,.2f}"

    def pct(self, x):
        return f"{float(x):.2f}%"

    def highest_product_row(self):
        return self.df.loc[self.df["Tariff Impact %"].idxmax()]

    def lowest_product_row(self):
        return self.df.loc[self.df["Tariff Impact %"].idxmin()]

    # ==================== UI SHELL ====================

    def build(self):
        self.root.configure(bg=self.c["bg"])
        self.side = tk.Frame(self.root, bg=self.c["side"], width=235)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        self.main = tk.Frame(self.root, bg=self.c["bg"])
        self.main.pack(side="left", fill="both", expand=True)
        self.build_side()
        self.build_header()
        self.content = tk.Frame(self.main, bg=self.c["bg"])
        self.content.pack(fill="both", expand=True)

    def build_header(self):
        old = getattr(self, "header", None)
        if old:
            old.destroy()
        self.header = tk.Frame(self.main, bg=self.c["panel"], height=70,
                               highlightbackground=self.c["border"], highlightthickness=1)
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        tk.Label(self.header, text="▮▮▮", bg=self.c["panel"], fg=SAPPHIRE,
                 font=(FONT, 20, "bold")).pack(side="left", padx=(22, 7))
        tk.Label(self.header, text="Tariff Analytics", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 19, "bold")).pack(side="left")
        tk.Frame(self.header, bg=self.c["border"], width=1, height=28).pack(side="left", padx=18)
        tk.Label(self.header, text="Analyze   •   Compare   •   Visualize   •   Decide",
                 bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 9)).pack(side="left")

        r = tk.Frame(self.header, bg=self.c["panel"])
        r.pack(side="right", padx=18)
        tk.Label(r, text="●", bg=self.c["panel"], fg=self.c["good"],
                 font=(FONT, 10)).pack(side="left")
        tk.Label(r, text=f" Dataset Loaded  •  {len(self.df):,} records",
                 bg=self.c["panel"], fg=self.c["text"], font=(FONT, 8, "bold")).pack(side="left", padx=10)
        tk.Button(r, text="☀" if self.dark else "☾", command=self.theme,
                  bg=self.c["panel"], fg=self.c["text"], relief="flat", bd=0,
                  activebackground=self.c["hover"], font=(FONT, 17), cursor="hand2").pack(side="left", padx=8)

    def build_side(self):
        for w in self.side.winfo_children():
            w.destroy()
        self.groups = {}

        b = tk.Frame(self.side, bg=self.c["side"])
        b.pack(fill="x", padx=18, pady=(18, 13))
        tk.Label(b, text="▮▮▮", bg=self.c["side"], fg=SAPPHIRE,
                 font=(FONT, 20, "bold")).pack(anchor="w")
        tk.Label(b, text="Tariff Analytics", bg=self.c["side"], fg="white",
                 font=(FONT, 16, "bold")).pack(anchor="w")
        tk.Label(b, text="Data Science Mini Project", bg=self.c["side"],
                 fg="#9BC3BF", font=(FONT, 8)).pack(anchor="w")

        self.nav(self.side, "⌂", "Dashboard", self.show_dashboard)
        self.section(self.side, "EXPLORE & ANALYZE", "explore", [
            ("⌕", "Product Explorer", self.show_product),
            ("◉", "Data Analysis", self.show_analysis)
        ])
        self.section(self.side, "VISUALIZATION", "visual", [
            ("▥", "Visualizations", self.show_visuals)
        ])
        self.section(self.side, "COMPARE", "compare", [
            ("⇄", "Dataset Comparison", self.show_compare)
        ])
        self.section(self.side, "INSIGHTS", "insight", [
            ("★", "Rankings", self.show_rankings),
            ("✦", "Insights Center", self.show_insights)
        ])
        self.section(self.side, "TOOLS", "tools", [
            ("◈", "Tariff Simulator", self.show_simulator),
            ("⌁", "Web Scraping", self.show_scraping)
        ])
        self.nav(self.side, "✎", "Data Cleaning", self.show_cleaning)
        self.nav(self.side, "ⓘ", "About Project", self.show_about)

        tk.Label(self.side, text="Better data.\nSmarter decisions.",
                 bg=self.c["side"], fg="#9ABDB9", justify="left",
                 font=(FONT, 8, "italic")).pack(side="bottom", anchor="w", padx=22, pady=16)

    def nav(self, parent, icon, name, command):
        x = tk.Button(parent, text=f"{icon}   {name}", command=lambda: self.go(command, name),
                      bg=self.c["side"], fg="#E4F1EF", activebackground=SAPPHIRE,
                      activeforeground="white", relief="flat", bd=0, anchor="w",
                      padx=12, font=(FONT, 9, "bold"), cursor="hand2")
        x.pack(fill="x", padx=9, pady=2, ipady=7)
        self.groups.setdefault("_buttons", []).append((name, x))

    def section(self, parent, title, key, items):
        wrapper = tk.Frame(parent, bg=self.c["side"])
        wrapper.pack(fill="x", pady=(7, 1))
        header = tk.Button(wrapper, text=f"▾  {title}", command=lambda: self.toggle(key),
                           bg=self.c["side"], fg="#8EB6B1", activebackground=self.c["side2"],
                           relief="flat", bd=0, anchor="w", padx=8, font=(FONT, 8, "bold"),
                           cursor="hand2")
        header.pack(fill="x")
        body = tk.Frame(wrapper, bg=self.c["side"])
        body.pack(fill="x")
        self.groups[key] = {"wrapper": wrapper, "body": body, "header": header, "open": True}
        for icon, name, command in items:
            x = tk.Button(body, text=f"{icon}   {name}", command=lambda c=command, n=name: self.go(c, n),
                          bg=self.c["side"], fg="#D7E9E6", activebackground=SAPPHIRE,
                          activeforeground="white", relief="flat", bd=0, anchor="w",
                          padx=22, font=(FONT, 8), cursor="hand2")
            x.pack(fill="x", ipady=5)
            self.groups.setdefault("_buttons", []).append((name, x))

    def toggle(self, key):
        info = self.groups[key]
        body = info["body"]
        if info["open"]:
            body.pack_forget()
            info["header"].configure(text=info["header"].cget("text").replace("▾", "▸", 1))
            info["open"] = False
        else:
            body.pack(fill="x")
            info["header"].configure(text=info["header"].cget("text").replace("▸", "▾", 1))
            info["open"] = True

    def go(self, command, name):
        self.page = name
        command()
        for n, b in self.groups.get("_buttons", []):
            b.configure(bg=SAPPHIRE if n == name else self.c["side"],
                         fg="white" if n == name else "#D7E9E6")

    def clear(self, title):
        for w in self.content.winfo_children():
            w.destroy()
        self.page = title

    def pagebox(self):
        f = tk.Frame(self.content, bg=self.c["bg"])
        f.pack(fill="both", expand=True, padx=25, pady=20)
        return f

    def heading(self, p, title, sub):
        tk.Label(p, text=title, bg=self.c["bg"], fg=self.c["text"],
                 font=(FONT, 24, "bold")).pack(anchor="w")
        tk.Label(p, text=sub, bg=self.c["bg"], fg=self.c["muted"],
                 font=(FONT, 9)).pack(anchor="w", pady=(3, 17))

    def panel(self, p):
        return tk.Frame(p, bg=self.c["panel"], highlightbackground=self.c["border"],
                        highlightthickness=1)

    def card(self, p, label, value, accent=SAPPHIRE, sub=""):
        f = self.panel(p)
        tk.Frame(f, bg=accent, width=5).pack(side="left", fill="y")
        b = tk.Frame(f, bg=self.c["panel"])
        b.pack(fill="both", expand=True, padx=13, pady=11)
        tk.Label(b, text=label, bg=self.c["panel"], fg=self.c["muted"],
                 font=(FONT, 8, "bold")).pack(anchor="w")
        tk.Label(b, text=value, bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 18, "bold")).pack(anchor="w", pady=(4, 0))
        if sub:
            tk.Label(b, text=sub, bg=self.c["panel"], fg=self.c["muted"],
                     font=(FONT, 8)).pack(anchor="w")
        return f

    def btn(self, p, text, command, primary=True):
        return tk.Button(p, text=text, command=command,
                         bg=SAPPHIRE if primary else self.c["hover"],
                         fg="white" if primary else self.c["text"],
                         activebackground=self.c["side2"], activeforeground="white",
                         relief="flat", bd=0, font=(FONT, 9, "bold"),
                         padx=14, pady=7, cursor="hand2")

    # ==================== DASHBOARD ====================

    def show_dashboard(self):
        self.clear("Dashboard")
        p = self.pagebox()

        # Reference-style hero: spacious, not overloaded.
        hero = self.panel(p)
        hero.pack(fill="x")
        left = tk.Frame(hero, bg=self.c["panel"])
        left.pack(side="left", fill="both", expand=True, padx=25, pady=21)
        tk.Label(left, text="WELCOME TO", bg=self.c["panel"], fg=SAPPHIRE,
                 font=(FONT, 9, "bold")).pack(anchor="w")
        tk.Label(left, text="Tariff Impact Analysis", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 27, "bold")).pack(anchor="w")
        tk.Label(left, text="Explore, analyze and visualize how tariffs impact\n"
                 "product prices using real-world data.", bg=self.c["panel"], fg=self.c["muted"],
                 font=(FONT, 10), justify="left").pack(anchor="w", pady=5)
        self.btn(left, "Explore Data  →", self.show_product).pack(anchor="w", pady=8)
        tk.Label(hero, text="↗\nDATA • TARIFF • INSIGHTS", bg=self.c["panel"], fg=SAPPHIRE,
                 font=(FONT, 31, "bold"), justify="center").pack(side="right", padx=35)

        # KPI strip: only the six most useful dashboard numbers.
        k = tk.Frame(p, bg=self.c["bg"])
        k.pack(fill="x", pady=13)
        vals = [
            ("Total Records", f"{len(self.df):,}", SAPPHIRE, "Dataset size"),
            ("Product Types", str(self.df["Product Type"].nunique()), "#7CB9E8", "Categories"),
            ("Brands", str(self.df["Brand Name"].nunique()), "#A98BD4", "Unique brands"),
            ("Avg. Price Before", self.money(self.df["Price Before Tariff"].mean()), SAPPHIRE, "Before tariff"),
            ("Avg. Price After", self.money(self.df["Price After Tariff"].mean()), "#F07C69", "After tariff"),
            ("Avg. Impact", self.pct(self.df["Tariff Impact %"].mean()), "#E7AE4D", "Average impact")
        ]
        for item in vals:
            self.card(k, *item).pack(side="left", fill="both", expand=True, padx=(0, 7))

        body = tk.Frame(p, bg=self.c["bg"])
        body.pack(fill="both", expand=True)

        # Main chart.
        cp = self.panel(body)
        cp.pack(side="left", fill="both", expand=True, padx=(0, 7))
        tk.Label(cp, text="Average Price Before vs After Tariff", bg=self.c["panel"],
                 fg=self.c["text"], font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=12)
        fig = self.fig((7.6, 3.5))
        ax = fig.add_subplot(111)
        g = self.df.groupby("Product Type")[["Price Before Tariff", "Price After Tariff"]].mean()
        x = np.arange(len(g))
        ax.bar(x - .18, g["Price Before Tariff"], .36, label="Before Tariff", color=SAPPHIRE)
        ax.bar(x + .18, g["Price After Tariff"], .36, label="After Tariff", color="#F07C69")
        ax.set_xticks(x); ax.set_xticklabels(g.index, rotation=10)
        ax.set_ylabel("Price (₹)"); ax.legend(frameon=False, ncol=2)
        self.axes(ax); self.embed(fig, cp)

        # One supporting chart instead of multiple dashboard panels.
        dp = self.panel(body)
        dp.pack(side="right", fill="both", expand=True, padx=(7, 0))
        tk.Label(dp, text="Tariff Impact by Product Type", bg=self.c["panel"],
                 fg=self.c["text"], font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=12)
        fig2 = self.fig((5.4, 3.5))
        ax2 = fig2.add_subplot(111)
        impact = self.df.groupby("Product Type")["Tariff Impact %"].mean().sort_values()
        sns.barplot(x=impact.values, y=impact.index, ax=ax2, color=SAPPHIRE)
        ax2.set_xlabel("Average Impact (%)"); ax2.set_ylabel("")
        self.axes(ax2); self.embed(fig2, dp)

        # Small, useful insight strip. No duplicate Quick Questions page.
        insight = self.panel(p)
        insight.pack(fill="x", pady=(10, 0))
        ti = self.df.groupby("Product Type")["Tariff Impact %"].mean()
        hp = self.highest_product_row()
        bi = self.df.groupby("Brand Name")["Tariff Impact %"].mean()
        self.insight_item(insight, "Highest category impact", f"{ti.idxmax()} • {self.pct(ti.max())}", SAPPHIRE)
        self.insight_item(insight, "Most affected product", f"{hp['Product Name']} • {self.pct(hp['Tariff Impact %'])}", "#F07C69")
        self.insight_item(insight, "Highest impact brand", f"{bi.idxmax()} • {self.pct(bi.max())}", "#A98BD4")
        self.insight_item(insight, "Average increase", self.money(self.df["Tariff Increase"].mean()), "#E7AE4D")

    def insight_item(self, parent, title, value, accent):
        f = tk.Frame(parent, bg=self.c["panel"])
        f.pack(side="left", fill="x", expand=True, padx=10, pady=9)
        tk.Label(f, text="●", bg=self.c["panel"], fg=accent, font=(FONT, 12)).pack(side="left", padx=(2, 8))
        b = tk.Frame(f, bg=self.c["panel"]); b.pack(side="left", fill="x", expand=True)
        tk.Label(b, text=title, bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 8)).pack(anchor="w")
        tk.Label(b, text=value, bg=self.c["panel"], fg=self.c["text"], font=(FONT, 9, "bold")).pack(anchor="w")

    # ==================== DATASET EXPLORER ====================

    def show_dataset(self):
        self.clear("Dataset Explorer")
        p = self.pagebox()
        self.heading(p, "Dataset Explorer", f"Tariff.csv • {len(self.df):,} records • {len(self.df.columns)} original columns")
        top = tk.Frame(p, bg=self.c["bg"]); top.pack(fill="x", pady=(0, 10))
        sv = tk.StringVar()
        e = tk.Entry(top, textvariable=sv, bg=self.c["input"], fg=self.c["text"],
                     insertbackground=self.c["text"], relief="flat", highlightbackground=self.c["border"],
                     highlightthickness=1, width=42)
        e.pack(side="left", ipady=7)
        tk.Label(top, text="  Search any product, category, brand or value", bg=self.c["bg"],
                 fg=self.c["muted"], font=(FONT, 8)).pack(side="left")

        info = tk.Frame(p, bg=self.c["bg"]); info.pack(fill="x", pady=(0, 10))
        for label, value, accent in [
            ("Rows", len(self.df), SAPPHIRE),
            ("Columns", 6, "#7CB9E8"),
            ("Categories", self.df["Product Type"].nunique(), "#A98BD4"),
            ("Brands", self.df["Brand Name"].nunique(), "#E7AE4D")
        ]:
            self.card(info, label, f"{value:,}", accent).pack(side="left", fill="x", expand=True, padx=(0, 7))

        cols = ["S.No", "Product Name", "Product Type", "Brand Name", "Price Before Tariff",
                "Price After Tariff", "Tariff Increase", "Tariff Impact %"]
        tree = self.table(p, cols)

        def fill(d):
            tree.delete(*tree.get_children())
            for _, r in d.iterrows():
                tree.insert("", "end", values=[r.get("S.No", ""), r.get("Product Name", ""),
                    r.get("Product Type", ""), r.get("Brand Name", ""), self.money(r["Price Before Tariff"]),
                    self.money(r["Price After Tariff"]), self.money(r["Tariff Increase"]), self.pct(r["Tariff Impact %"])])

        fill(self.df)

        def search(*_):
            s = sv.get().lower().strip()
            if not s:
                fill(self.df); return
            mask = self.df.astype(str).apply(lambda x: x.str.lower().str.contains(s, na=False)).any(axis=1)
            fill(self.df[mask])
        sv.trace_add("write", search)

    def table(self, p, cols, height=18):
        f = self.panel(p); f.pack(fill="both", expand=True)
        t = ttk.Treeview(f, columns=cols, show="headings", height=height)
        for col in cols:
            t.heading(col, text=col)
            t.column(col, width=135, minwidth=90, anchor="center")
        y = ttk.Scrollbar(f, orient="vertical", command=t.yview)
        x = ttk.Scrollbar(f, orient="horizontal", command=t.xview)
        t.configure(yscrollcommand=y.set, xscrollcommand=x.set)
        t.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        y.pack(side="right", fill="y", pady=8)
        x.pack(side="bottom", fill="x", padx=8)
        return t

    # ==================== PRODUCT INTELLIGENCE ====================

    def show_product(self):
        self.clear("Product Explorer")
        p = self.pagebox()
        self.heading(p, "Product Explorer", "Search the dataset, filter products and view tariff impact details.")

        # Search and product filters.
        controls = self.panel(p)
        controls.pack(fill="x", pady=(0, 10))
        sv = tk.StringVar()
        e = tk.Entry(controls, textvariable=sv, bg=self.c["input"], fg=self.c["text"],
                     insertbackground=self.c["text"], relief="flat", highlightbackground=self.c["border"],
                     highlightthickness=1, width=35)
        e.pack(side="left", padx=(15, 6), pady=10, ipady=6)
        tk.Label(controls, text="Search product, category, brand or value", bg=self.c["panel"],
                 fg=self.c["muted"], font=(FONT, 8)).pack(side="left", padx=(0, 12))

        tk.Label(controls, text="FILTER PRODUCTS", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 9, "bold")).pack(side="left", padx=(0, 12))
        vars_ = {x: tk.StringVar(value="All") for x in ["Product", "Product Type", "Brand"]}
        values = {
            "Product": ["All"] + sorted(self.df["Product Name"].astype(str).unique()),
            "Product Type": ["All"] + sorted(self.df["Product Type"].astype(str).unique()),
            "Brand": ["All"] + sorted(self.df["Brand Name"].astype(str).unique())
        }
        combos = {}
        for label in ["Product Type", "Brand", "Product"]:
            tk.Label(controls, text=label, bg=self.c["panel"], fg=self.c["muted"],
                     font=(FONT, 8, "bold")).pack(side="left", padx=(5, 5))
            cb = ttk.Combobox(controls, textvariable=vars_[label], values=values[label], state="readonly", width=16)
            cb.pack(side="left", padx=(0, 8), pady=10)
            combos[label] = cb

        result = self.panel(p)
        result.pack(fill="both", expand=True)
        tk.Label(result, text="PRODUCT DATA", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=15, pady=(10, 2))
        cols = ["S.No", "Product Name", "Product Type", "Brand Name", "Before", "After", "Increase", "Impact %"]
        tree = ttk.Treeview(result, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=125, anchor="center")
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        detail = tk.Label(p, text="Select a row to view product details.", bg=self.c["bg"], fg=self.c["muted"],
                          font=(FONT, 9))
        detail.pack(anchor="w", pady=(8, 0))

        def update(*_):
            d = self.df.copy()
            s = sv.get().lower().strip()
            if s:
                mask = d.astype(str).apply(lambda x: x.str.lower().str.contains(s, na=False)).any(axis=1)
                d = d[mask]
            for key, var in vars_.items():
                if var.get() != "All":
                    col = {"Product": "Product Name", "Product Type": "Product Type", "Brand": "Brand Name"}[key]
                    d = d[d[col].astype(str) == var.get()]
            tree.delete(*tree.get_children())
            for idx, r in d.iterrows():
                tree.insert("", "end", iid=str(idx), values=[r["S.No"], r["Product Name"], r["Product Type"],
                    r["Brand Name"], self.money(r["Price Before Tariff"]), self.money(r["Price After Tariff"]),
                    self.money(r["Tariff Increase"]), self.pct(r["Tariff Impact %"])])

        sv.trace_add("write", update)
        for cb in combos.values():
            cb.bind("<<ComboboxSelected>>", update)
        update()

        def selected(_=None):
            sel = tree.selection()
            if not sel:
                return
            r = self.df.loc[int(sel[0])]
            detail.configure(text=f"{r['Product Name']} • {r['Brand Name']} • {r['Product Type']}  |  "
                                  f"Before {self.money(r['Price Before Tariff'])}  →  After {self.money(r['Price After Tariff'])}  |  "
                                  f"Increase {self.money(r['Tariff Increase'])}  |  Impact {self.pct(r['Tariff Impact %'])}")
        tree.bind("<<TreeviewSelect>>", selected)

    # ==================== ANALYSIS ====================

    def show_analysis(self):
        self.clear("Data Analysis")
        p = self.pagebox()
        self.heading(p, "Data Analysis", "Core statistical analysis using Pandas and NumPy.")

        before = self.df["Price Before Tariff"]
        after = self.df["Price After Tariff"]
        inc = self.df["Tariff Increase"]
        imp = self.df["Tariff Impact %"]
        k = tk.Frame(p, bg=self.c["bg"]); k.pack(fill="x", pady=(0, 12))
        for x in [
            ("Mean Increase", self.money(inc.mean()), SAPPHIRE, "mean()"),
            ("Median Increase", self.money(inc.median()), "#7CB9E8", "median()"),
            ("Maximum Increase", self.money(inc.max()), "#F07C69", "max()"),
            ("Minimum Increase", self.money(inc.min()), "#A98BD4", "min()"),
            ("Total Increase", self.money(inc.sum()), "#E7AE4D", "sum()"),
            ("Std. Deviation", self.money(inc.std()), SAPPHIRE, "std()")
        ]:
            self.card(k, *x).pack(side="left", fill="both", expand=True, padx=(0, 7))

        row = tk.Frame(p, bg=self.c["bg"]); row.pack(fill="both", expand=True)
        left = self.panel(row); left.pack(side="left", fill="both", expand=True, padx=(0, 7))
        tk.Label(left, text="Category Impact Analysis", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=12)
        g = self.df.groupby("Product Type").agg(
            Before=("Price Before Tariff", "mean"), After=("Price After Tariff", "mean"),
            Increase=("Tariff Increase", "mean"), Impact=("Tariff Impact %", "mean"), Products=("Product Name", "count")
        ).sort_values("Impact", ascending=False)
        tree = ttk.Treeview(left, columns=list(g.columns), show="headings", height=12)
        for col in g.columns:
            tree.heading(col, text=col); tree.column(col, width=95, anchor="center")
        for idx, r in g.iterrows():
            tree.insert("", "end", values=[idx, self.money(r["Before"]), self.money(r["After"]),
                                             self.money(r["Increase"]), self.pct(r["Impact"]), int(r["Products"])])
        tree.pack(fill="both", expand=True, padx=8, pady=8)

        right = self.panel(row); right.pack(side="right", fill="both", expand=True, padx=(7, 0))
        tk.Label(right, text="Distribution & Counts", bg=self.c["panel"], fg=self.c["text"],
                 font=(FONT, 12, "bold")).pack(anchor="w", padx=16, pady=12)
        most = self.df["Product Type"].value_counts()
        lines = [
            ("Most common product type", f"{most.idxmax()} ({most.max()} records)"),
            ("Least common product type", f"{most.idxmin()} ({most.min()} records)"),
            ("Highest average impact", f"{g.index[0]} ({self.pct(g.iloc[0]['Impact'])})"),
            ("Lowest average impact", f"{g.index[-1]} ({self.pct(g.iloc[-1]['Impact'])})"),
            ("Average price before", self.money(before.mean())),
            ("Average price after", self.money(after.mean())),
            ("Average percentage impact", self.pct(imp.mean()))
        ]
        for title, value in lines:
            f = tk.Frame(right, bg=self.c["hover"]); f.pack(fill="x", padx=12, pady=4)
            tk.Label(f, text=title, bg=self.c["hover"], fg=self.c["muted"], font=(FONT, 8)).pack(anchor="w", padx=10, pady=(6, 1))
            tk.Label(f, text=value, bg=self.c["hover"], fg=self.c["text"], font=(FONT, 10, "bold")).pack(anchor="w", padx=10, pady=(0, 6))

    # ==================== VISUALIZATIONS ====================

    def show_visuals(self):
        self.clear("Visualizations")
        p = self.pagebox()
        self.heading(p, "Visualization Studio", "Choose a chart type, configure the fields, and generate a graph from the dataset.")

        controls = self.panel(p)
        controls.pack(fill="x", pady=(0, 10))

        chart_type = tk.StringVar(value="Bar Chart")
        x_var = tk.StringVar(value="Product Type")
        y_var = tk.StringVar(value="Price After Tariff")
        group_var = tk.StringVar(value="Count")
        bins_var = tk.IntVar(value=10)

        chart_values = [
            "Bar Chart", "Horizontal Bar Chart", "Line Chart", "Histogram",
            "Pie Chart", "Scatter Plot", "Box Plot", "Area Chart"
        ]
        x_values = ["S.No", "Product Name", "Product Type", "Brand Name"]
        y_values = ["Price Before Tariff", "Price After Tariff", "Tariff Increase", "Tariff Impact %"]
        agg_values = ["Count", "Mean", "Sum", "Median", "Maximum", "Minimum"]

        def label(parent, text):
            tk.Label(parent, text=text, bg=self.c["panel"], fg=self.c["muted"],
                     font=(FONT, 8, "bold")).pack(side="left", padx=(10, 5), pady=10)

        label(controls, "Chart Type")
        chart_cb = ttk.Combobox(controls, textvariable=chart_type, values=chart_values,
                                state="readonly", width=21)
        chart_cb.pack(side="left", pady=10)
        label(controls, "Category / X")
        x_cb = ttk.Combobox(controls, textvariable=x_var, values=x_values,
                            state="readonly", width=20)
        x_cb.pack(side="left", pady=10)
        label(controls, "Numeric / Y")
        y_cb = ttk.Combobox(controls, textvariable=y_var, values=y_values,
                            state="readonly", width=21)
        y_cb.pack(side="left", pady=10)
        label(controls, "Aggregation")
        agg_cb = ttk.Combobox(controls, textvariable=group_var, values=agg_values,
                              state="readonly", width=14)
        agg_cb.pack(side="left", pady=10)

        bin_frame = tk.Frame(controls, bg=self.c["panel"])
        bin_frame.pack(side="left", padx=10)
        tk.Label(bin_frame, text="Bins", bg=self.c["panel"], fg=self.c["muted"],
                 font=(FONT, 8, "bold")).pack(side="left")
        tk.Spinbox(bin_frame, from_=5, to=40, textvariable=bins_var, width=5,
                   font=(FONT, 9)).pack(side="left", padx=5)

        actions = tk.Frame(p, bg=self.c["bg"])
        actions.pack(fill="x", pady=(0, 10))
        status = tk.Label(actions, text="Select options and click Generate Graph.",
                          bg=self.c["bg"], fg=self.c["muted"], font=(FONT, 9))
        status.pack(side="left")

        chart_holder = self.panel(p)
        chart_holder.pack(fill="both", expand=True)

        def aggregate(series, method):
            if method == "Count":
                return series.count()
            if method == "Mean":
                return series.mean()
            if method == "Sum":
                return series.sum()
            if method == "Median":
                return series.median()
            if method == "Maximum":
                return series.max()
            return series.min()

        def make_chart():
            for w in chart_holder.winfo_children():
                w.destroy()
            typ = chart_type.get()
            xcol = x_var.get()
            ycol = y_var.get()
            agg = group_var.get()
            fig = self.fig((10.5, 5.4))
            ax = fig.add_subplot(111)
            d = self.df.copy()

            try:
                if typ == "Histogram":
                    values = pd.to_numeric(d[ycol], errors="coerce").dropna()
                    ax.hist(values, bins=int(bins_var.get()), color=SAPPHIRE, edgecolor=self.c["panel"])
                    ax.set_xlabel(ycol); ax.set_ylabel("Frequency")

                elif typ == "Scatter Plot":
                    x_numeric = pd.to_numeric(d[xcol], errors="coerce") if xcol == "S.No" else None
                    if x_numeric is None:
                        raise ValueError("Scatter Plot needs a numeric X field. Choose S.No for X, or use a categorical chart.")
                    y_numeric = pd.to_numeric(d[ycol], errors="coerce")
                    mask = x_numeric.notna() & y_numeric.notna()
                    ax.scatter(x_numeric[mask], y_numeric[mask], s=28, alpha=.65, color=SAPPHIRE)
                    ax.set_xlabel(xcol); ax.set_ylabel(ycol)

                elif typ == "Pie Chart":
                    counts = d[xcol].astype(str).value_counts().head(12)
                    ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
                    ax.set_title(f"Distribution of {xcol}")

                elif typ == "Box Plot":
                    if xcol not in ["Product Type", "Brand Name", "Product Name"]:
                        raise ValueError("Box Plot requires a categorical field for X.")
                    temp = d[[xcol, ycol]].copy()
                    temp[ycol] = pd.to_numeric(temp[ycol], errors="coerce")
                    temp = temp.dropna()
                    groups = [g[ycol].values for _, g in temp.groupby(xcol)]
                    labels = [str(k) for k, _ in temp.groupby(xcol)]
                    ax.boxplot(groups, label=labels, patch_artist=True)
                    ax.set_xlabel(xcol); ax.set_ylabel(ycol)
                    ax.tick_params(axis="x", rotation=20)

                else:
                    if xcol in ["Product Type", "Brand Name", "Product Name"]:
                        grouped = d.groupby(xcol)[ycol].apply(lambda s: aggregate(pd.to_numeric(s, errors="coerce"), agg)).dropna()
                        grouped = grouped.head(20)
                        if typ == "Horizontal Bar Chart":
                            ax.barh(grouped.index.astype(str), grouped.values, color=SAPPHIRE)
                            ax.set_xlabel(f"{agg} of {ycol}")
                        elif typ == "Line Chart":
                            ax.plot(grouped.index.astype(str), grouped.values, marker="o", linewidth=2, color=SAPPHIRE)
                            ax.tick_params(axis="x", rotation=25)
                            ax.set_ylabel(f"{agg} of {ycol}")
                        elif typ == "Area Chart":
                            ax.fill_between(range(len(grouped)), grouped.values, alpha=.25, color=SAPPHIRE)
                            ax.plot(range(len(grouped)), grouped.values, color=SAPPHIRE)
                            ax.set_xticks(range(len(grouped))); ax.set_xticklabels(grouped.index.astype(str), rotation=25)
                            ax.set_ylabel(f"{agg} of {ycol}")
                        else:
                            ax.bar(grouped.index.astype(str), grouped.values, color=SAPPHIRE)
                            ax.tick_params(axis="x", rotation=25)
                            ax.set_ylabel(f"{agg} of {ycol}")
                    else:
                        values = pd.to_numeric(d[ycol], errors="coerce").dropna()
                        ax.plot(values.reset_index(drop=True), color=SAPPHIRE, linewidth=2)
                        ax.set_xlabel("Record Index"); ax.set_ylabel(ycol)

                self.axes(ax)
                self.embed(fig, chart_holder)
                status.configure(text=f"Generated {typ} • X: {xcol} • Y: {ycol} • Aggregation: {agg}", fg=self.c["good"])
            except Exception as exc:
                status.configure(text=str(exc), fg=self.c["bad"])

        self.btn(actions, "Generate Graph", make_chart).pack(side="right")
        chart_cb.bind("<<ComboboxSelected>>", lambda e: None)
        make_chart()

        tk.Label(p, text="Available: bar, horizontal bar, line, histogram, pie, scatter, box and area charts. "
                 "For custom graphs, select the category/brand/product as X and any numeric tariff field as Y.",
                 bg=self.c["bg"], fg=self.c["muted"], font=(FONT, 8)).pack(anchor="w", pady=(7, 0))

    # ==================== COMPARISON CENTER ====================

    def show_compare(self, mode=None):
        self.clear("Dataset Comparison")
        p = self.pagebox()
        self.heading(p, "Dataset Comparison", "One comparison center for datasets, categories, brands, products and product + brand combinations.")

        d2 = self.second()
        top = self.panel(p); top.pack(fill="x", pady=(0, 10))
        tk.Label(top, text="Compare", bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 8, "bold")).pack(side="left", padx=(15, 6), pady=12)
        compare_type = tk.StringVar(value=mode or "Category")
        type_cb = ttk.Combobox(top, textvariable=compare_type, state="readonly", width=20,
                               values=["Overall Dataset", "Category", "Brand", "Product", "Product + Brand"])
        type_cb.pack(side="left", pady=12)
        tk.Label(top, text="Metric", bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 8, "bold")).pack(side="left", padx=(20, 6))
        metric = tk.StringVar(value="Average Tariff Impact %")
        metric_cb = ttk.Combobox(top, textvariable=metric, state="readonly", width=28,
                                 values=["Average Tariff Impact %", "Average Tariff Increase ₹", "Average Price Before Tariff",
                                         "Average Price After Tariff", "Maximum Tariff Impact %", "Minimum Tariff Impact %", "Number of Products"])
        metric_cb.pack(side="left", pady=12)

        choose = tk.Frame(p, bg=self.c["bg"]); choose.pack(fill="x", pady=(0, 10))
        a_var = tk.StringVar(value="Grocery"); b_var = tk.StringVar(value="Electronics")
        a_cb = ttk.Combobox(choose, textvariable=a_var, state="readonly", width=27)
        b_cb = ttk.Combobox(choose, textvariable=b_var, state="readonly", width=27)
        tk.Label(choose, text="Dataset 1", bg=self.c["bg"], fg=self.c["muted"], font=(FONT, 8, "bold")).pack(side="left", padx=(0, 6))
        a_cb.pack(side="left", padx=(0, 25)); tk.Label(choose, text="Dataset 2", bg=self.c["bg"], fg=self.c["muted"], font=(FONT, 8, "bold")).pack(side="left", padx=(0, 6)); b_cb.pack(side="left")

        result = self.panel(p); result.pack(fill="both", expand=True)
        status = tk.Label(result, text="", bg=self.c["panel"], fg=self.c["text"], font=(FONT, 13, "bold"))
        status.pack(anchor="w", padx=20, pady=(18, 8))
        detail = tk.Label(result, text="", bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 9), justify="left")
        detail.pack(anchor="w", padx=20, pady=(0, 12))
        chart_holder = tk.Frame(result, bg=self.c["panel"]); chart_holder.pack(fill="both", expand=True, padx=10, pady=5)

        def options():
            typ = compare_type.get()
            if typ == "Overall Dataset":
                return ["Dataset 1", "Dataset 2"]
            source = self.df
            if typ == "Category": col = "Product Type"
            elif typ == "Brand": col = "Brand Name"
            elif typ == "Product": col = "Product Name"
            else: return sorted(set(source["Product Name"].astype(str)) & set(source["Brand Name"].astype(str)))
            vals = sorted(source[col].astype(str).unique())
            return vals

        def update_options(*_):
            typ = compare_type.get()
            if typ == "Overall Dataset":
                vals = ["Dataset 1", "Dataset 2"]
            elif typ == "Product + Brand":
                vals = ["All combinations"] + sorted((self.df["Brand Name"].astype(str) + " | " + self.df["Product Name"].astype(str)).unique())
            else:
                col = {"Category":"Product Type", "Brand":"Brand Name", "Product":"Product Name"}[typ]
                vals = sorted(self.df[col].astype(str).unique())
            a_cb["values"] = vals; b_cb["values"] = vals
            if vals:
                a_var.set(vals[0]); b_var.set(vals[1] if len(vals) > 1 else vals[0])
            draw()

        def metric_value(d, typ, selected):
            if typ == "Overall Dataset": sub = d
            elif typ == "Product + Brand":
                if selected == "All combinations": sub = d
                else:
                    brand, product = selected.split(" | ", 1)
                    sub = d[(d["Brand Name"].astype(str) == brand) & (d["Product Name"].astype(str) == product)]
            else:
                col = {"Category":"Product Type", "Brand":"Brand Name", "Product":"Product Name"}[typ]
                sub = d[d[col].astype(str) == selected]
            if len(sub) == 0: return np.nan, 0
            m = metric.get()
            if m == "Average Tariff Impact %": return sub["Tariff Impact %"].mean(), len(sub)
            if m == "Average Tariff Increase ₹": return sub["Tariff Increase"].mean(), len(sub)
            if m == "Average Price Before Tariff": return sub["Price Before Tariff"].mean(), len(sub)
            if m == "Average Price After Tariff": return sub["Price After Tariff"].mean(), len(sub)
            if m == "Maximum Tariff Impact %": return sub["Tariff Impact %"].max(), len(sub)
            if m == "Minimum Tariff Impact %": return sub["Tariff Impact %"].min(), len(sub)
            return len(sub), len(sub)

        def draw(*_):
            for w in chart_holder.winfo_children(): w.destroy()
            typ = compare_type.get(); av, ac = metric_value(self.df, typ, a_var.get()); bv, bc = metric_value(d2, typ, b_var.get())
            if np.isnan(av) or np.isnan(bv):
                status.configure(text="No comparable records found."); detail.configure(text="Choose another comparison."); return
            winner = a_var.get() if av >= bv else b_var.get(); diff = abs(av - bv)
            unit = "%" if "Impact" in metric.get() else "₹" if "₹" in metric.get() or "Price" in metric.get() else "records"
            status.configure(text=f"{winner} has the higher {metric.get().lower()}  •  Difference: {diff:.2f}{unit}")
            detail.configure(text=f"Dataset 1: {a_var.get()}  →  {av:.2f}   ({ac} records)\nDataset 2: {b_var.get()}  →  {bv:.2f}   ({bc} records)\n"
                                      f"This same screen also supports cross-category, cross-brand, cross-product and product + brand comparisons.")
            fig = self.fig((8.5, 3.5)); ax = fig.add_subplot(111)
            ax.bar([a_var.get(), b_var.get()], [av, bv], color=[SAPPHIRE, "#F07C69"])
            ax.set_ylabel(metric.get()); self.axes(ax); self.embed(fig, chart_holder)

        type_cb.bind("<<ComboboxSelected>>", update_options)
        metric_cb.bind("<<ComboboxSelected>>", draw)
        a_cb.bind("<<ComboboxSelected>>", draw); b_cb.bind("<<ComboboxSelected>>", draw)
        update_options()

    # ==================== RANKINGS ====================

    def show_rankings(self):
        self.clear("Rankings")
        p = self.pagebox()
        self.heading(p, "Rankings", "Rank products and brands by tariff impact without creating separate repetitive pages.")
        top = self.panel(p); top.pack(fill="x", pady=(0, 10))
        choice = tk.StringVar(value="Top 10 Products by Impact %")
        cb = ttk.Combobox(top, textvariable=choice, state="readonly", width=35,
                          values=["Top 10 Products by Impact %", "Top 10 Products by ₹ Increase", "Brands by Average Impact"])
        cb.pack(side="left", padx=15, pady=12)
        box = self.panel(p); box.pack(fill="both", expand=True)

        def draw(*_):
            for w in box.winfo_children(): w.destroy()
            if choice.get().startswith("Top 10 Products"):
                metric = "Tariff Impact %" if "Impact" in choice.get() else "Tariff Increase"
                d = self.df.nlargest(10, metric).copy().sort_values(metric)
                labels = d["Product Name"].astype(str) + " • " + d["Brand Name"].astype(str)
                fig = self.fig((9, 5)); ax = fig.add_subplot(111)
                ax.barh(labels, d[metric], color=SAPPHIRE)
                ax.set_xlabel("Impact (%)" if metric == "Tariff Impact %" else "Increase (₹)")
                self.axes(ax); self.embed(fig, box)
            else:
                d = self.df.groupby("Brand Name").agg(Impact=("Tariff Impact %", "mean"), Products=("Product Name", "count")).sort_values("Impact", ascending=False).head(15).sort_values("Impact")
                fig = self.fig((9, 5)); ax = fig.add_subplot(111)
                ax.barh(d.index, d["Impact"], color=SAPPHIRE); ax.set_xlabel("Average Tariff Impact (%)")
                self.axes(ax); self.embed(fig, box)
        cb.bind("<<ComboboxSelected>>", draw); draw()

    # ==================== INSIGHTS CENTER ====================

    def show_insights(self):
        self.clear("Insights Center")
        p = self.pagebox()
        self.heading(p, "Insights Center", "Smart observations, key findings and quick answers in one place.")
        b = self.df["Price Before Tariff"]; a = self.df["Price After Tariff"]; inc = self.df["Tariff Increase"]; imp = self.df["Tariff Impact %"]
        ti = self.df.groupby("Product Type")["Tariff Impact %"].mean()
        bi = self.df.groupby("Brand Name")["Tariff Impact %"].mean()
        hb = self.df.loc[b.idxmax()]; lb = self.df.loc[b.idxmin()]; ha = self.df.loc[a.idxmax()]; la = self.df.loc[a.idxmin()]
        hp = self.highest_product_row(); lp = self.lowest_product_row()
        findings = [
            ("Overall impact", f"Average price increased by {self.money(inc.mean())} ({self.pct(imp.mean())}) after tariff.", SAPPHIRE),
            ("Most affected product", f"{hp['Product Name']} by {hp['Brand Name']} has the highest impact at {self.pct(hp['Tariff Impact %'])}.", "#F07C69"),
            ("Least affected product", f"{lp['Product Name']} by {lp['Brand Name']} has the lowest impact at {self.pct(lp['Tariff Impact %'])}.", "#7CB9E8"),
            ("Most affected category", f"{ti.idxmax()} has the highest average tariff impact at {self.pct(ti.max())}.", "#A98BD4"),
            ("Least affected category", f"{ti.idxmin()} has the lowest average tariff impact at {self.pct(ti.min())}.", "#E7AE4D"),
            ("Most affected brand", f"{bi.idxmax()} has the highest average brand impact at {self.pct(bi.max())}.", SAPPHIRE),
            ("Highest price before tariff", f"{hb['Product Name']} — {self.money(hb['Price Before Tariff'])}.", "#F07C69"),
            ("Lowest price before tariff", f"{lb['Product Name']} — {self.money(lb['Price Before Tariff'])}.", "#7CB9E8"),
            ("Highest price after tariff", f"{ha['Product Name']} — {self.money(ha['Price After Tariff'])}.", "#A98BD4"),
            ("Lowest price after tariff", f"{la['Product Name']} — {self.money(la['Price After Tariff'])}.", "#E7AE4D")
        ]
        for title, text, accent in findings:
            f = self.panel(p); f.pack(fill="x", pady=4)
            tk.Label(f, text="●", bg=self.c["panel"], fg=accent, font=(FONT, 14)).pack(side="left", padx=14)
            body = tk.Frame(f, bg=self.c["panel"]); body.pack(side="left", fill="x", expand=True, pady=9)
            tk.Label(body, text=title, bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 8, "bold")).pack(anchor="w")
            tk.Label(body, text=text, bg=self.c["panel"], fg=self.c["text"], font=(FONT, 9), wraplength=1000, justify="left").pack(anchor="w", pady=(2, 0))

    # ==================== TARIFF SIMULATOR ====================

    def show_simulator(self):
        self.clear("Tariff Simulator")
        p = self.pagebox()
        self.heading(p, "Tariff Simulator", "Run a what-if calculation without changing the original dataset.")

        work = tk.Frame(p, bg=self.c["bg"])
        work.pack(fill="both", expand=True)

        controls = self.panel(work)
        controls.pack(fill="x", pady=(0, 12))
        controls.grid_columnconfigure(1, weight=1)
        controls.grid_columnconfigure(3, weight=1)

        tk.Label(controls, text="PRODUCT", bg=self.c["panel"], fg=self.c["muted"],
                 font=(FONT, 8, "bold")).grid(row=0, column=0, sticky="w", padx=(18, 7), pady=(18, 6))
        product = tk.StringVar(value=str(self.df.iloc[0]["Product Name"]))
        product_cb = ttk.Combobox(
            controls, textvariable=product,
            values=sorted(self.df["Product Name"].astype(str).unique()),
            state="readonly", width=30
        )
        product_cb.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(18, 18), pady=(0, 18))

        tk.Label(controls, text="HYPOTHETICAL TARIFF (%)", bg=self.c["panel"], fg=self.c["muted"],
                 font=(FONT, 8, "bold")).grid(row=0, column=2, sticky="w", padx=(10, 7), pady=(18, 6))
        rate = tk.DoubleVar(value=30)
        rate_value = tk.Label(controls, text="30%", bg=self.c["panel"], fg=SAPPHIRE,
                              font=(FONT, 16, "bold"))
        rate_value.grid(row=1, column=2, sticky="w", padx=(10, 5), pady=(0, 18))
        scale = tk.Scale(
            controls, from_=0, to=100, orient="horizontal", variable=rate, length=320,
            resolution=1, bg=self.c["panel"], fg=self.c["text"], troughcolor=self.c["hover"],
            highlightthickness=0, showvalue=False
        )
        scale.grid(row=1, column=3, sticky="ew", padx=(0, 18), pady=(0, 18))

        result = self.panel(work)
        result.pack(fill="both", expand=True)
        result.grid_columnconfigure((0, 1), weight=1)
        result.grid_rowconfigure((0, 1), weight=1)

        metric_info = [
            ("Current Price", "—", SAPPHIRE),
            ("Estimated Price", "—", "#F07C69"),
            ("Estimated Increase", "—", "#E7AE4D"),
            ("Change", "—", "#7CB9E8")
        ]
        value_labels = {}
        for i, (title, initial, accent) in enumerate(metric_info):
            r, c = divmod(i, 2)
            tile = tk.Frame(result, bg=self.c["hover"], highlightbackground=self.c["border"], highlightthickness=1)
            tile.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
            tk.Frame(tile, bg=accent, width=5).pack(side="left", fill="y")
            body = tk.Frame(tile, bg=self.c["hover"]); body.pack(fill="both", expand=True, padx=18, pady=15)
            tk.Label(body, text=title.upper(), bg=self.c["hover"], fg=self.c["muted"],
                     font=(FONT, 8, "bold")).pack(anchor="w")
            value_label = tk.Label(body, text=initial, bg=self.c["hover"], fg=self.c["text"],
                                   font=(FONT, 21, "bold"))
            value_label.pack(anchor="w", pady=(6, 0))
            value_labels[title] = value_label

        explanation = tk.Label(
            p,
            text="Formula: Estimated Price = Current Price × (1 + Tariff Rate / 100). This is a hypothetical simulation only.",
            bg=self.c["bg"], fg=self.c["muted"], font=(FONT, 8)
        )
        explanation.pack(anchor="w", pady=(8, 0))

        def update(*_):
            rows = self.df[self.df["Product Name"].astype(str) == product.get()]
            if rows.empty:
                return
            price = float(rows["Price Before Tariff"].mean())
            estimated = price * (1 + float(rate.get()) / 100)
            value_labels["Current Price"].configure(text=self.money(price))
            value_labels["Estimated Price"].configure(text=self.money(estimated))
            value_labels["Estimated Increase"].configure(text=self.money(estimated - price))
            value_labels["Change"].configure(text=self.pct(rate.get()))
            rate_value.configure(text=f"{rate.get():.0f}%")

        product_cb.bind("<<ComboboxSelected>>", update)
        scale.configure(command=update)
        update()

    # ==================== DATA CLEANING ====================

    def show_cleaning(self):
        self.clear("Data Cleaning")
        p = self.pagebox()
        self.heading(p, "Data Cleaning", "Check and clean missing values, duplicates, numeric types and column names.")
        miss = int(self.dirty.isnull().sum().sum()); dup = int(self.dirty.duplicated().sum())
        r = tk.Frame(p, bg=self.c["bg"]); r.pack(fill="x", pady=(0, 12))
        for x in [("Rows Before", len(self.dirty), SAPPHIRE, "Dirty dataset"), ("Missing Values", miss, "#F07C69", "Needs treatment"),
                  ("Duplicates", dup, "#E7A33D", "Needs removal"), ("Columns", len(self.dirty.columns), SAPPHIRE, "Structure")]:
            self.card(r, x[0], f"{x[1]:,}", x[2], x[3]).pack(side="left", fill="both", expand=True, padx=(0, 8))
        box = self.panel(p); box.pack(fill="both", expand=True)
        tk.Label(box, text="Cleaning Operations", bg=self.c["panel"], fg=self.c["text"], font=(FONT, 13, "bold")).pack(anchor="w", padx=18, pady=15)
        ops = [
            ("01", "Check missing values", "isnull().sum()"), ("02", "Convert numeric columns", "pd.to_numeric()"),
            ("03", "Fill numeric missing values", "Column mean"), ("04", "Fill text missing values", "Unknown"),
            ("05", "Remove duplicates", "drop_duplicates()"), ("06", "Clean column names", "strip()"), ("07", "Verify data types", "dtype check")
        ]
        for a, b, c in ops:
            row = tk.Frame(box, bg=self.c["panel"]); row.pack(fill="x", padx=18, pady=3)
            tk.Label(row, text=a, bg=self.c["hover"], fg=SAPPHIRE, width=5, pady=6, font=(FONT, 8, "bold")).pack(side="left")
            tk.Label(row, text=b, bg=self.c["panel"], fg=self.c["text"], font=(FONT, 9, "bold")).pack(side="left", padx=10)
            tk.Label(row, text=c, bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 9)).pack(side="right", padx=10)
        self.status = tk.Label(box, text="", bg=self.c["panel"], fg=self.c["good"], font=(FONT, 9, "bold"))
        self.status.pack(anchor="w", padx=18, pady=8)
        self.btn(box, "Clean Dataset  →", self.clean_data).pack(anchor="w", padx=18, pady=10)

    def clean_data(self):
        d = self.dirty.copy(); d.columns = d.columns.astype(str).str.strip()
        for col in ["S.No", "Price Before Tariff", "Price After Tariff"]:
            if col in d.columns:
                d[col] = pd.to_numeric(d[col], errors="coerce")
                d[col] = d[col].fillna(d[col].mean())
        for col in ["Product Name", "Product Type", "Brand Name"]:
            if col in d.columns:
                d[col] = d[col].astype("string").fillna("Unknown")
        old = len(d); d = d.drop_duplicates(); removed = old - len(d)
        d.to_csv(CLEAN, index=False)
        self.status.configure(text=f"✓ Cleaning complete • {removed} duplicates removed • saved to Tariff_cleaned.csv")

    # ==================== WEB SCRAPING ====================

    def show_scraping(self):
        self.clear("Web Scraping")
        p = self.pagebox()
        self.heading(p, "Web Scraping", "Scrape the local HTML tariff dataset using Requests and BeautifulSoup.")

        source = self.panel(p)
        source.pack(fill="x", pady=(0, 10))
        tk.Label(source, text="SOURCE", bg=self.c["panel"], fg=SAPPHIRE,
                 font=(FONT, 9, "bold")).pack(anchor="w", padx=18, pady=(13, 4))
        tk.Label(source, text="http://localhost:8000/tariff.html", bg=self.c["panel"],
                 fg=self.c["text"], font=(FONT, 10, "bold")).pack(anchor="w", padx=18)

        action = tk.Frame(source, bg=self.c["panel"]); action.pack(fill="x", padx=18, pady=12)
        status = tk.Label(action, text="Ready to scrape the localhost HTML page.",
                          bg=self.c["panel"], fg=self.c["muted"], font=(FONT, 9))
        status.pack(side="left")
        self.btn(action, "Scrape Dataset  →", lambda: scrape(), True).pack(side="right")

        info = self.panel(p)
        info.pack(fill="x", pady=(0, 10))
        records = tk.Label(info, text="Records scraped: —", bg=self.c["panel"],
                           fg=self.c["text"], font=(FONT, 11, "bold"))
        records.pack(anchor="w", padx=18, pady=12)

        table_frame = self.panel(p)
        table_frame.pack(fill="both", expand=True)
        cols = ["S.No", "Product Name", "Product Type", "Brand Name",
                "Price Before Tariff", "Price After Tariff"]
        tree = self.table(table_frame, cols)

        def scrape():
            try:
                url = "http://localhost:8000/tariff.html"
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                table = soup.find("table", id="tariff-data")
                if table is None:
                    raise ValueError("Tariff table was not found in the HTML page.")

                rows = []
                for row in table.find_all("tr")[1:]:
                    cells = row.find_all("td")
                    if cells:
                        rows.append([cell.get_text(strip=True) for cell in cells])

                scraped = pd.DataFrame(rows, columns=cols)
                tree.delete(*tree.get_children())
                for _, row in scraped.head(100).iterrows():
                    tree.insert("", "end", values=list(row))

                records.configure(text=f"Records scraped: {len(scraped):,}")
                status.configure(text="✓ Scraping successful • HTML parsed with BeautifulSoup",
                                 fg=self.c["good"])
            except Exception as exc:
                status.configure(text=f"✗ Scraping failed: {exc}", fg=self.c["bad"])

        # Keep the button command connected after the local function is created.
        for widget in action.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text").startswith("Scrape Dataset"):
                widget.configure(command=scrape)

    # ==================== ABOUT ====================

    def show_about(self):
        self.clear("About Project")
        p = self.pagebox()
        self.heading(p, "About Project", "Tariff Impact Analysis • Python Data Science Mini Project")
        sections = [
            ("OBJECTIVE", "Analyze product prices before and after tariff and identify patterns across products, categories and brands."),
            ("DATASET", f"Tariff.csv contains {len(self.df):,} records and 6 original columns: serial number, product name, product type, brand name, price before tariff and price after tariff."),
            ("CALCULATED METRICS", "Tariff Increase = Price After − Price Before. Tariff Impact % = (Tariff Increase ÷ Price Before) × 100."),
            ("TOOLS", "NumPy, Pandas, Matplotlib, Seaborn and BeautifulSoup."),
            ("APPLICATION STRUCTURE", "Dashboard, Product Explorer, Data Analysis, Visualizations, Dataset Comparison, Rankings, Insights Center, Tariff Simulator, Data Cleaning and About Project. Dataset exploration is integrated into Product Explorer."),
            ("COMPARISON", "If Tariff_2.csv is placed beside this program, the comparison center uses it as Dataset 2. If it is not present, a clearly hypothetical comparison scenario is generated for demonstration."),
            ("PROJECT MEMBERS", "S091 — Shreyash Kadam\nS199 — Om Wala"),
        ]
        for h, t in sections:
            f = self.panel(p); f.pack(fill="x", pady=5)
            tk.Label(f, text=h, bg=self.c["panel"], fg=SAPPHIRE, font=(FONT, 10, "bold")).pack(anchor="w", padx=18, pady=(13, 4))
            tk.Label(f, text=t, bg=self.c["panel"], fg=self.c["text"], font=(FONT, 9), wraplength=1100, justify="left").pack(anchor="w", padx=18, pady=(0, 13))

    # ==================== CHART HELPERS / THEME ====================

    def fig(self, size=(8, 4)):
        return plt.Figure(figsize=size, dpi=90, facecolor=self.c["panel"])

    def axes(self, ax):
        ax.set_facecolor(self.c["panel"])
        ax.tick_params(colors=self.c["muted"], labelsize=8)
        ax.xaxis.label.set_color(self.c["muted"]); ax.yaxis.label.set_color(self.c["muted"])
        for s in ax.spines.values(): s.set_color(self.c["border"])
        ax.grid(axis="y", alpha=.15, color=self.c["muted"])

    def embed(self, fig, parent):
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=8)
        parent._figure_canvas = canvas

    def theme(self):
        self.dark = not self.dark
        self.c = DARK if self.dark else LIGHT
        for w in self.root.winfo_children():
            w.destroy()
        self.build()
        pages = {
            "Dashboard": self.show_dashboard, "Dataset Explorer": self.show_dataset,
            "Product Explorer": self.show_product, "Data Analysis": self.show_analysis,
            "Visualizations": self.show_visuals, "Dataset Comparison": self.show_compare,
            "Rankings": self.show_rankings, "Insights Center": self.show_insights,
            "Tariff Simulator": self.show_simulator, "Web Scraping": self.show_scraping,
            "Data Cleaning": self.show_cleaning,
            "About Project": self.show_about
        }
        pages.get(self.page, self.show_dashboard)()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("clam")
    except Exception:
        pass
    App(root)
    root.mainloop()
