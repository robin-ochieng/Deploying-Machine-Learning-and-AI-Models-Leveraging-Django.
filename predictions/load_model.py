from joblib import load

def get_model():
    model = load('C:/Users/Robin Ochieng/OneDrive - Kenbright/Gig/DJANGO/EM Site/Emerging Markerts/models/xgb_model.joblib')
    return model
