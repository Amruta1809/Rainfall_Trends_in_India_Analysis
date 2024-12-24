from flask import Flask, request, render_template
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Handle file upload
        file = request.files.get("file")
        if not file or not file.filename.endswith(".csv"):
            return "No file selected or invalid file type. Please upload a valid CSV file."

        try:
            # Read the CSV file
            rainfall_data = pd.read_csv(file)

            # Generate graphs
            graphs = generate_graphs(rainfall_data)

            # Render the graphs in the HTML template
            return render_template("graphs.html", graphs=graphs)

        except Exception as e:
            # Log error and show a message
            return f"An error occurred: {str(e)}"

    return render_template("index.html")


def generate_graphs(rainfall_data):
    try:
        # Validate if required columns exist
        required_columns = ["YEAR", "ANNUAL", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "Jan-Feb", "Mar-May", "Jun-Sep", "Oct-Dec"]
        for col in required_columns:
            if col not in rainfall_data.columns:
                raise ValueError(f"Missing required column: {col}")

        # 1. Annual Rainfall Trend
        annual_rainfall = rainfall_data[["YEAR", "ANNUAL"]]
        fig_annual = go.Figure()
        fig_annual.add_trace(go.Scatter(
            x=annual_rainfall["YEAR"],
            y=annual_rainfall["ANNUAL"],
            mode="lines",
            name="Annual Rainfall",
            line=dict(color="blue", width=2)
        ))
        fig_annual.update_layout(
            title="Annual Rainfall Trend",
            xaxis_title="Year",
            yaxis_title="Rainfall (mm)",
            template="plotly_white"
        )

        # 2. Monthly Average Rainfall
        monthly_columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        monthly_avg = rainfall_data[monthly_columns].mean()
        fig_monthly = px.bar(
            x=monthly_avg.index,
            y=monthly_avg.values,
            labels={"x": "Month", "y": "Rainfall (mm)"},
            title="Average Monthly Rainfall"
        )

        # 3. Seasonal Rainfall Distribution
        seasonal_columns = ['Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec']
        seasonal_avg = rainfall_data[seasonal_columns].mean()
        fig_seasonal = px.bar(
            x=seasonal_avg.index,
            y=seasonal_avg.values,
            labels={"x": "Season", "y": "Rainfall (mm)"},
            title="Seasonal Rainfall Distribution"
        )

        # Embed graphs into HTML
        graphs = [
            fig_annual.to_html(full_html=False),
            fig_monthly.to_html(full_html=False),
            fig_seasonal.to_html(full_html=False)
        ]
        return graphs

    except Exception as e:
        raise ValueError(f"Error generating graphs: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
