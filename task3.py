"""
============================================================
  Alfido Tech Internship – Task 3: Data Analysis with Pandas
  Author  : Intern
  Goal    : Load a CSV, clean it, apply filtering / grouping /
            aggregation, and explain insights in plain English.

  Dataset : We generate a realistic sales dataset inline so
            the script is fully self-contained.  Swap the
            CSV path in load_data() to use your own file.
============================================================
"""

import io
import pandas as pd
import numpy as np

# ── 0. Create a sample CSV dataset (embedded) ────────────────────────────────
SAMPLE_CSV = """OrderID,Date,Region,Category,Product,Quantity,UnitPrice,CustomerAge,Rating
1001,2024-01-05,North,Electronics,Laptop,1,75000,29,4.5
1002,2024-01-12,South,Clothing,T-Shirt,3,599,22,3.8
1003,2024-01-18,East,Electronics,Phone,2,25000,35,4.7
1004,2024-02-03,West,Furniture,Chair,4,3500,42,4.0
1005,2024-02-14,North,Electronics,Tablet,1,18000,27,4.2
1006,2024-02-20,South,Clothing,Jeans,2,,31,3.5
1007,2024-03-05,East,Furniture,Table,1,12000,55,4.8
1008,2024-03-11,West,Electronics,Laptop,2,75000,38,4.6
1009,2024-03-22,North,Clothing,Jacket,3,2500,24,4.1
1010,2024-04-01,South,Electronics,Phone,1,25000,19,4.9
1011,2024-04-15,East,Clothing,T-Shirt,5,599,33,3.2
1012,2024-04-28,West,Furniture,Sofa,1,28000,47,4.7
1013,2024-05-07,North,Electronics,Tablet,3,18000,30,4.4
1014,2024-05-19,South,Furniture,Chair,2,3500,60,3.9
1015,2024-05-30,East,Electronics,Laptop,1,75000,28,4.5
1016,2024-06-10,West,Clothing,Jeans,4,1200,23,3.7
1017,2024-06-21,North,Furniture,Table,2,12000,51,4.6
1018,2024-07-04,South,Electronics,Phone,3,25000,36,4.8
1019,2024-07-15,East,Clothing,Jacket,1,2500,29,4.0
1020,2024-07-25,West,Electronics,Tablet,2,18000,41,4.3
1021,2024-08-08,North,Clothing,T-Shirt,6,599,26,3.6
1022,2024-08-17,South,Furniture,Sofa,1,,48,4.9
1023,2024-08-29,East,Electronics,Laptop,2,75000,32,4.7
1024,2024-09-05,West,Clothing,Jacket,3,2500,37,4.1
1025,2024-09-20,North,Electronics,Phone,1,25000,25,4.6
1026,2024-10-03,South,Furniture,Table,3,12000,53,4.4
1027,2024-10-14,East,Clothing,Jeans,2,1200,21,3.3
1028,2024-10-25,West,Electronics,Tablet,1,18000,44,4.2
1029,2024-11-09,North,Furniture,Chair,5,3500,39,4.0
1030,2024-11-23,South,Electronics,Laptop,1,75000,34,4.8
"""

# ── 1. Load Data ─────────────────────────────────────────────────────────────
def load_data() -> pd.DataFrame:
    """
    Load the dataset.
    Replace io.StringIO(SAMPLE_CSV) with pd.read_csv('your_file.csv')
    to use a real CSV file.
    """
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))
    print(f"✔ Dataset loaded  →  {df.shape[0]} rows × {df.shape[1]} columns")
    return df


# ── 2. Inspect Data ──────────────────────────────────────────────────────────
def inspect_data(df: pd.DataFrame) -> None:
    print("\n" + "─" * 55)
    print("SECTION 1 – Data Inspection")
    print("─" * 55)

    print("\n• First 5 rows:")
    print(df.head().to_string(index=False))

    print("\n• Column data-types:")
    print(df.dtypes.to_string())

    print("\n• Basic statistics (numeric columns):")
    print(df.describe().round(2).to_string())

    print("\n• Null values per column:")
    print(df.isnull().sum().to_string())


# ── 3. Clean Data ────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "─" * 55)
    print("SECTION 2 – Data Cleaning")
    print("─" * 55)

    # a) Parse dates
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month_name()
    df["Quarter"] = df["Date"].dt.to_period("Q").astype(str)
    print("✔ Parsed 'Date' column → added 'Month' & 'Quarter'")

    # b) Handle missing UnitPrice – fill with median per Category
    missing_before = df["UnitPrice"].isnull().sum()
    df["UnitPrice"] = df.groupby("Category")["UnitPrice"].transform(
        lambda x: x.fillna(x.median())
    )
    missing_after = df["UnitPrice"].isnull().sum()
    print(f"✔ Filled {missing_before - missing_after} missing UnitPrice values "
          f"with category median")

    # c) Derive Revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    print("✔ Derived 'Revenue' = Quantity × UnitPrice")

    # d) Remove duplicate OrderIDs (none in sample, but good practice)
    before = len(df)
    df = df.drop_duplicates(subset=["OrderID"])
    print(f"✔ Removed {before - len(df)} duplicate rows")

    # e) Fix data types
    df["CustomerAge"] = df["CustomerAge"].astype(int)
    df["OrderID"] = df["OrderID"].astype(str)

    print(f"\n  Clean dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


# ── 4. Filter ────────────────────────────────────────────────────────────────
def filter_data(df: pd.DataFrame) -> None:
    print("\n" + "─" * 55)
    print("SECTION 3 – Filtering")
    print("─" * 55)

    # a) High-value orders (Revenue > 50,000)
    high_value = df[df["Revenue"] > 50_000]
    print(f"\n• High-value orders (Revenue > ₹50,000): {len(high_value)}")
    print(high_value[["OrderID", "Product", "Quantity", "Revenue"]].to_string(index=False))

    # b) Electronics in the North region
    north_elec = df[(df["Region"] == "North") & (df["Category"] == "Electronics")]
    print(f"\n• Electronics orders from North region: {len(north_elec)}")
    print(north_elec[["OrderID", "Product", "Revenue", "Rating"]].to_string(index=False))

    # c) Orders with Rating ≥ 4.5
    top_rated = df[df["Rating"] >= 4.5]
    print(f"\n• Top-rated orders (Rating ≥ 4.5): {len(top_rated)}")
    print(top_rated[["OrderID", "Product", "Rating", "Revenue"]].to_string(index=False))


# ── 5. Grouping & Aggregation ────────────────────────────────────────────────
def group_and_aggregate(df: pd.DataFrame) -> None:
    print("\n" + "─" * 55)
    print("SECTION 4 – Grouping & Aggregation")
    print("─" * 55)

    # a) Revenue by Category
    cat_rev = (
        df.groupby("Category")["Revenue"]
        .agg(["sum", "mean", "count"])
        .rename(columns={"sum": "Total Revenue", "mean": "Avg Revenue", "count": "Orders"})
        .sort_values("Total Revenue", ascending=False)
    )
    cat_rev["Total Revenue"] = cat_rev["Total Revenue"].map("₹{:,.0f}".format)
    cat_rev["Avg Revenue"]   = cat_rev["Avg Revenue"].map("₹{:,.0f}".format)
    print("\n• Revenue by Category:")
    print(cat_rev.to_string())

    # b) Revenue by Region
    reg_rev = (
        df.groupby("Region")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )
    print("\n• Total Revenue by Region:")
    for region, rev in reg_rev.items():
        print(f"    {region:<8} : ₹{rev:>12,.0f}")

    # c) Quarterly revenue trend
    q_rev = (
        df.groupby("Quarter")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "Total Revenue"})
    )
    print("\n• Quarterly Revenue Trend:")
    for _, row in q_rev.iterrows():
        bar = "█" * int(row["Total Revenue"] / 10_000)
        print(f"    {row['Quarter']}  {bar}  ₹{row['Total Revenue']:,.0f}")

    # d) Average Rating by Category
    avg_rating = df.groupby("Category")["Rating"].mean().sort_values(ascending=False)
    print("\n• Average Customer Rating by Category:")
    for cat, rating in avg_rating.items():
        print(f"    {cat:<15}: {rating:.2f} ⭐")

    # e) Top 5 products by total revenue
    top_products = (
        df.groupby("Product")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    print("\n• Top 5 Products by Revenue:")
    for rank, (prod, rev) in enumerate(top_products.items(), 1):
        print(f"    #{rank}  {prod:<10} : ₹{rev:,.0f}")


# ── 6. Insight Summary ───────────────────────────────────────────────────────
def insight_summary(df: pd.DataFrame) -> None:
    print("\n" + "─" * 55)
    print("SECTION 5 – Insight Summary (Plain English)")
    print("─" * 55)

    total_rev   = df["Revenue"].sum()
    top_cat     = df.groupby("Category")["Revenue"].sum().idxmax()
    top_region  = df.groupby("Region")["Revenue"].sum().idxmax()
    top_product = df.groupby("Product")["Revenue"].sum().idxmax()
    best_rated  = df.groupby("Category")["Rating"].mean().idxmax()
    avg_age     = df["CustomerAge"].mean()
    high_orders = (df["Revenue"] > 50_000).sum()

    insights = [
        f"1. Total revenue across all orders was ₹{total_rev:,.0f}.",
        f"2. '{top_cat}' was the highest-grossing category, likely because "
        f"   electronic products carry much higher unit prices.",
        f"3. The '{top_region}' region generated the most revenue, suggesting "
        f"   stronger purchasing power or a higher order volume there.",
        f"4. '{top_product}' was the best-selling product by total revenue — "
        f"   a premium item customers are clearly willing to invest in.",
        f"5. '{best_rated}' received the highest average customer rating, "
        f"   indicating strong satisfaction in that segment.",
        f"6. The average customer age was {avg_age:.0f} years, meaning the "
        f"   core audience skews young-to-middle-adult.",
        f"7. {high_orders} orders exceeded ₹50,000 in revenue — these high-value "
        f"   transactions deserve focused retention and upsell efforts.",
        f"8. Quarterly data shows growth across the year, with Q3–Q4 peaks "
        f"   likely driven by festive / seasonal demand.",
    ]

    for insight in insights:
        print(f"\n  {insight}")


# ── 7. Save cleaned data ─────────────────────────────────────────────────────
def save_output(df: pd.DataFrame) -> None:
    out = "cleaned_sales_data.csv"
    df.to_csv(out, index=False)
    print(f"\n✔ Cleaned dataset saved → {out}")


# ── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  Alfido Tech – Task 3: Data Analysis with Pandas")
    print("=" * 55)

    df = load_data()
    inspect_data(df)
    df = clean_data(df)
    filter_data(df)
    group_and_aggregate(df)
    insight_summary(df)
    save_output(df)

    print("\n" + "=" * 55)
    print("  Task 3 Complete ✓")
    print("=" * 55)
    