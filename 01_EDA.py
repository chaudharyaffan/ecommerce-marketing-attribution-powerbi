import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

print("\n🚀 STARTING E-COMMERCE ANALYTICS PROJECT\n")

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv('data/ga4_ecommerce_data.csv')

print("✅ Data Loaded Successfully!")
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")

# =====================================================
# CLEAN DATA
# =====================================================

df['revenue'] = df['revenue'].fillna(0)

# =====================================================
# KPI METRICS
# =====================================================

print("\n" + "="*60)
print("KEY BUSINESS METRICS")
print("="*60)

total_revenue = df['revenue'].sum()

total_purchases = df[
    df['event_name'] == 'purchase'
].shape[0]

unique_users = df['user_id'].nunique()

conversion_rate = (
    total_purchases / unique_users * 100
)

print(f"Total Revenue           : ${total_revenue:,.2f}")
print(f"Total Purchases         : {total_purchases:,}")
print(f"Unique Users            : {unique_users:,}")
print(f"Overall Conversion Rate : {conversion_rate:.2f}%")

# =====================================================
# FUNNEL ANALYSIS
# =====================================================

print("\n" + "="*60)
print("FUNNEL ANALYSIS")
print("="*60)

funnel_events = [
    'page_view',
    'view_item',
    'add_to_cart',
    'begin_checkout',
    'purchase'
]

funnel_data = []

for event in funnel_events:

    users = df[
        df['event_name'] == event
    ]['user_id'].nunique()

    funnel_data.append([event, users])

funnel_df = pd.DataFrame(
    funnel_data,
    columns=['event_stage', 'users']
)

funnel_df['conversion_%'] = (
    funnel_df['users'] /
    funnel_df['users'].iloc[0] * 100
).round(2)

print(funnel_df)

# =====================================================
# FUNNEL CHART
# =====================================================

plt.figure(figsize=(10,6))

bars = plt.bar(
    funnel_df['event_stage'],
    funnel_df['users']
)

plt.title('E-commerce Conversion Funnel')
plt.xlabel('Funnel Stage')
plt.ylabel('Users')

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f'{int(height)}',
        ha='center'
    )

plt.tight_layout()

plt.savefig('images/funnel_chart.png')

plt.show()

# =====================================================
# REVENUE BY CHANNEL
# =====================================================

print("\n" + "="*60)
print("REVENUE BY CHANNEL")
print("="*60)

revenue_channel = df.groupby(
    'source'
)['revenue'].sum().reset_index()

top_revenue_channels = revenue_channel.sort_values(
    'revenue',
    ascending=False
).head(10)

print(top_revenue_channels)

# =====================================================
# REVENUE CHART
# =====================================================

plt.figure(figsize=(12,6))

bars = plt.bar(
    top_revenue_channels['source'],
    top_revenue_channels['revenue']
)

plt.title('Top Revenue Generating Channels')
plt.xlabel('Traffic Source')
plt.ylabel('Revenue')

for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x() + bar.get_width()/2,
        height,
        f'{int(height)}',
        ha='center'
    )

plt.xticks(rotation=25)

plt.tight_layout()

plt.savefig('images/revenue_channels.png')

plt.show()

# =====================================================
# RFM ANALYSIS
# =====================================================

print("\n" + "="*60)
print("RFM CUSTOMER SEGMENTATION")
print("="*60)

df['event_timestamp'] = pd.to_datetime(
    df['event_timestamp'],
    unit='us',
    errors='coerce'
)

purchase_df = df[
    df['event_name'] == 'purchase'
].copy()

rfm = purchase_df.groupby(
    'user_id'
).agg({

    'event_timestamp': lambda x:
        (
            purchase_df['event_timestamp'].max()
            - x.max()
        ).days,

    'user_id': 'count',

    'revenue': 'sum'

})

rfm.columns = [
    'Recency',
    'Frequency',
    'Monetary'
]

print(rfm.head())

# =====================================================
# RFM CHART
# =====================================================

plt.figure(figsize=(10,6))

plt.hist(
    rfm['Monetary'],
    bins=20
)

plt.title('Customer Spending Distribution')
plt.xlabel('Revenue')
plt.ylabel('Customers')

plt.tight_layout()

plt.savefig('images/rfm_chart.png')

plt.show()

# =====================================================
# FINAL MESSAGE
# =====================================================

print("\n" + "="*60)
print("PROJECT ANALYSIS COMPLETED SUCCESSFULLY ✅")
print("="*60)
# =====================================================
# ONLY RFM CHART
# =====================================================

import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

plt.hist(
    rfm['Monetary'],
    bins=20
)

plt.title('Customer Spending Distribution')
plt.xlabel('Revenue')
plt.ylabel('Customers')

plt.tight_layout()

plt.savefig('images/rfm_chart.png')

plt.show()

plt.close()

print("✅ RFM Chart Saved Successfully!")