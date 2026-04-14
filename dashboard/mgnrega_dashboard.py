import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ✅ Load Data
data_path = r"C:\Users\sharan\OneDrive\Desktop\MGNREGA-Karnataka-Analytics\data\district_kpis_FY2023_24.csv"
df = pd.read_csv(data_path)
df.columns = [c.strip() for c in df.columns]

# ✅ Create App
app = Dash(__name__, title="MGNREGA Karnataka Dashboard")

# ✅ Layout
app.layout = html.Div([
    html.H1("MGNREGA Karnataka Dashboard", style={'textAlign': 'center', 'color': '#0066cc'}),

    # Filter Dropdown
    html.Div([
        html.Label("Select District:"),
        dcc.Dropdown(
            id='district_dropdown',
            options=[{'label': d, 'value': d} for d in sorted(df['district_name'].unique())],
            value=None,
            placeholder="Select a district or leave blank for overall view"
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),

    # KPI Cards
    html.Div(id='kpi_cards', style={'display': 'flex', 'justifyContent': 'space-around', 'margin': '20px'}),

    # Charts Row
    html.Div([
        dcc.Graph(id='individuals_bar', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='expenditure_pie', style={'width': '48%', 'display': 'inline-block'})
    ])
])

# ✅ Callbacks
@app.callback(
    [Output('kpi_cards', 'children'),
     Output('individuals_bar', 'figure'),
     Output('expenditure_pie', 'figure')],
    [Input('district_dropdown', 'value')]
)
def update_dashboard(selected_district):
    if selected_district:
        dff = df[df['district_name'] == selected_district]
    else:
        dff = df.copy()

    # KPIs
    total_individuals = int(dff['Total_Individuals_Worked'].sum())
    total_expenditure = round(dff['Total_Exp'].sum(), 2)
    avg_wage = round(dff['Average_Wage_rate_per_day_per_person'].mean(), 2)

    kpi_cards = [
        html.Div([
            html.H3("Total Individuals Worked"),
            html.H2(f"{total_individuals:,}")
        ], style={'border': '1px solid #ccc', 'borderRadius': '10px', 'padding': '15px', 'textAlign': 'center'}),

        html.Div([
            html.H3("Total Expenditure (₹)"),
            html.H2(f"{total_expenditure:,}")
        ], style={'border': '1px solid #ccc', 'borderRadius': '10px', 'padding': '15px', 'textAlign': 'center'}),

        html.Div([
            html.H3("Average Wage Rate (₹/day)"),
            html.H2(f"{avg_wage}")
        ], style={'border': '1px solid #ccc', 'borderRadius': '10px', 'padding': '15px', 'textAlign': 'center'})
    ]

    # Charts
    bar_fig = px.bar(
        df.sort_values('Total_Individuals_Worked', ascending=False).head(10),
        x='district_name', y='Total_Individuals_Worked',
        title='Top 10 Districts by Individuals Worked', color='Total_Individuals_Worked'
    )

    pie_fig = px.pie(
        df, names='district_name', values='Total_Exp',
        title='District-wise Expenditure Share'
    )

    return kpi_cards, bar_fig, pie_fig


if __name__ == "__main__":
    app.run(debug=True)

