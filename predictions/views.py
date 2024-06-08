from django.shortcuts import render
from django.http import HttpResponse
from .models import SalesData
import pandas as pd
from joblib import load


def home(request):
    # Assume we have some data to pass to the template
    context = {'message': 'Welcome to our site!'}
    return render(request, 'predictions/index.html', context)


def dashboard(request):
    return render(request, 'predictions/dashboard.html')


def generate_forecast(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Load your model
        model = load('C:/Users/Robin Ochieng/OneDrive - Kenbright/Gig/DJANGO/EM Site/models/xgb_model.joblib')

        # Fetch sales data from the database
        sales_data = SalesData.objects.all().order_by('date')
        
        # Convert QuerySet to DataFrame
        df = pd.DataFrame(list(sales_data.values('date', 'sales')))
        
        # Ensure 'date' is of type datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Create future dates based on user input
        future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
        future_data = pd.DataFrame({
            'year': future_dates.year,
            'month': future_dates.month,
            'day': future_dates.day,
            'weekday': future_dates.weekday,
            'week': future_dates.isocalendar().week,
            'quarter': future_dates.quarter
        })

        # Create lag features
        for i in range(1, 32):
            future_data[f'sales_lag_{i}'] = df['sales'].shift(i).values[-len(future_data):]  # Ensure index aligns with future_data length

        # Predict
        future_predictions = model.predict(future_data)
        forecast = pd.DataFrame({'Dates': future_dates, 'Predictions': future_predictions})

        # Convert DataFrame to Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Newbusinessforecast.xlsx"'
        with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
            forecast.to_excel(writer, index=False)
        
        return response
    else:
        # If not POST, return to form page or handle differently
        return HttpResponse("Please submit the form with a start and end date.")


def show_forecast_form(request):
    return render(request, 'predictions/forecast_generation_form.html')
