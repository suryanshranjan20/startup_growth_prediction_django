from django.shortcuts import render
import seaborn as sns
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import io
import base64
import os

def home(request):
    prediction = None
    chart_div = None
    comparison_chart = None
    scatter_chart = None
    similar_info = None
    error = None

    if request.method == 'POST':
        try:
            investment_amount = float(request.POST['investment_amount'])
            number_of_investors = int(request.POST['number_of_investors'])
            year_founded = int(request.POST['year_founded'])
            industry = request.POST['industry']
            country = request.POST['country']

            # Load model and feature names
            with open('prediction_model.pkl', 'rb') as f:
                model, feature_names = pickle.load(f)

            # Prepare input data
            row = {
                'Investment Amount (USD)': investment_amount,
                'Number of Investors': number_of_investors,
                'Year Founded': year_founded
            }

            for feature in feature_names:
                if feature.startswith('Industry_'):
                    row[feature] = 1 if feature == f'Industry_{industry}' else 0
                elif feature.startswith('Country_'):
                    row[feature] = 1 if feature == f'Country_{country}' else 0

            input_df = pd.DataFrame([row]).reindex(columns=feature_names, fill_value=0)

            predicted_growth = model.predict(input_df)[0]
            prediction = f"{predicted_growth:.2f}%"

            # --- Main Chart ---
            plt.figure(figsize=(7, 5))
            sns.set(style="whitegrid")
            bar = plt.bar(['Predicted Growth Rate'], [predicted_growth], color='#007bff', edgecolor='black')
            plt.ylim(0, 100)
            plt.ylabel('Growth Rate (%)')
            plt.title('Predicted Startup Growth Rate')
            for rect in bar:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2., height + 2, f'{height:.2f}%', ha='center')
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            chart_div = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # Loading CSV for visuals
            df = pd.read_csv('startup_growth_investment_data.csv')

            # --- Industry Comparison Chart ---
            industry_df = df[df['Industry'] == industry]
            if not industry_df.empty:
                industry_avg = industry_df['Growth Rate (%)'].mean()
                plt.figure(figsize=(7, 5))
                bars = plt.bar(['Predicted', f'{industry} Avg'], [predicted_growth, industry_avg], color=['#007bff', '#28a745'])
                plt.ylim(0, 100)
                plt.ylabel('Growth Rate (%)')
                plt.title('Predicted vs Industry Average Growth')
            for rect in bars:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2., height + 2, f'{height:.2f}%', ha='center')
            buffer = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            comparison_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()

            # --- Scatterplot ---
            if not industry_df.empty:
                plt.figure(figsize=(7, 5))
                sns.scatterplot(data=industry_df, x='Investment Amount (USD)', y='Growth Rate (%)', hue='Country')
                plt.title(f'Investment vs Growth in {industry}')
                plt.xlabel('Investment Amount (USD)')
                plt.ylabel('Growth Rate (%)')
                plt.legend(loc='best', fontsize='small')
                buffer = io.BytesIO()
                plt.tight_layout()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                scatter_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()
                
            # --- Similar Startups ---
            similar_startups = df[
                (df['Industry'] == industry) &
                (df['Country'] == country) &
                (df['Year Founded'].between(year_founded - 2, year_founded + 2))
            ].sort_values(by='Growth Rate (%)', ascending=False).head(5)

            similar_info = similar_startups[[
                'Investment Amount (USD)', 'Number of Investors', 'Year Founded', 'Growth Rate (%)'
            ]].to_dict(orient='records')

        except Exception as e:
            error = f"Error: {str(e)}"

    return render(request, 'prediction_app/home.html', {
        'prediction': prediction,
        'chart_div': chart_div,
        'comparison_chart': comparison_chart,
        'scatter_chart': scatter_chart,
        'similar_info': similar_info,
        'error': error
    })
