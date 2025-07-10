from flask import Flask, render_template, request, redirect, url_for, jsonify
import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

#=====================load datasets======================
precautions = pd.read_csv("recommender systems/antibiotic recommendation system/datasets/disease_precaution_plan_with_uniqueness.csv")
workout = pd.read_csv("recommender systems/antibiotic recommendation system/datasets/disease_workout_plan_unique.csv")
antib = pd.read_csv('recommender systems/antibiotic recommendation system/datasets/updated_antibiotics (1).csv')
diet = pd.read_csv("recommender systems/antibiotic recommendation system/datasets/disease_diet_plan_unique.csv")


#=====================load model=================
svc = pickle.load(open('recommender systems/antibiotic recommendation system/svc.pkl','rb'))

#=======================custom and helping function======================
def helper(dis):
    # Check if disease exists in precautions dataset
    pre_data = precautions[precautions['Disease'] == dis]
    if pre_data.empty:
        pre = [["Rest and adequate sleep", "Maintain good hygiene", "Stay hydrated", "Monitor symptoms", "Consult healthcare provider"]]
    else:
        pre = pre_data[['Precaution 1', 'Precaution 2', 'Precaution 3', 'Precaution 4', 'Precaution 5']].values.tolist()

    # Check if disease exists in antibiotics dataset
    anti_data = antib[antib['Disease'] == dis]
    if anti_data.empty:
        anti = [["Consult doctor for specific antibiotics", "Avoid self-medication", "Complete prescribed course", "Follow dosage instructions", "Monitor for side effects"]]
    else:
        anti = anti_data[['Primary Antibiotic', 'Alternate Antibiotic 1', 'Alternate Antibiotic 2', 'Reason for Recommendation', 'Primary Antibiotic Description']].values.tolist()

    # Check if disease exists in diet dataset
    die_data = diet[diet['Disease'] == dis]
    if die_data.empty:
        die = [["Light and easily digestible food", "Plenty of fluids", "Avoid spicy foods", "Include fruits and vegetables", "Small frequent meals"]]
    else:
        die = die_data[['Morning', 'Lunch', 'Snacks', 'Dinner', 'Night']].values.tolist()

    # Check if disease exists in workout dataset
    work_data = workout[workout['Disease'] == dis]
    if work_data.empty:
        work = [["Light walking if possible", "Gentle stretching", "Avoid strenuous exercise", "Rest when needed", "Gradual return to activity"]]
    else:
        work = work_data[['Workout 1', 'Workout 2', 'Workout 3', 'Workout 4', 'Workout 5']].values.tolist()

    return pre, anti, die, work


symptoms_dict = {"abdominal_pain": 0, "abdominal_swelling": 1, "bad_breath": 2, "bleeding_gums": 3,
                 "blood_in_sputum": 4, "bloody_stool": 5, "blue_skin": 6, "blurred_vision": 7, "body_ache": 8,
                 "burning_urination": 9, "chest_pain": 10, "chills": 11, "cold_extremities": 12, "confusion": 13,
                 "cough": 14, "crusting_skin": 15, "dark_urine": 16, "dehydration": 17, "delirium": 18, "diarrhea": 19,
                 "difficulty_breathing": 20, "difficulty_swallowing": 21, "difficulty_urinating": 22, "discharge": 23,
                 "dizziness": 24, "dry_cough": 25, "ear_pain": 26, "facial_swelling": 27, "fast_breathing": 28,
                 "fatigue": 29, "fatigue_after_exercise": 30, "fever": 31, "frequent_urination": 32, "headache": 33,
                 "hearing_loss": 34, "high_blood_pressure": 35, "hoarseness": 36, "increased_heart_rate": 37,
                 "involuntary_movements": 38, "irregular_heartbeat": 39, "itching": 40, "joint_pain": 41,
                 "light_sensitivity": 42, "loss_of_appetite": 43, "loss_of_smell": 44, "loss_of_taste": 45,
                 "low_blood_pressure": 46, "memory_loss": 47, "muscle_weakness": 48, "nausea": 49, "night_sweats": 50,
                 "numbness": 51, "open_wounds": 52, "painful_skin": 53, "painful_swallowing": 54, "paleness": 55,
                 "persistent_cough": 56, "productive_cough": 57, "pus_discharge": 58, "rash_with_blisters": 59,
                 "red_eyes": 60, "red_spots": 61, "runny_nose": 62, "seizures": 63, "shortness_of_breath": 64,
                 "sinus_pain": 65, "skin_rash": 66, "sneezing": 67, "sore_ears": 68, "sore_throat": 69,
                 "stiff_neck": 70, "sunken_eyes": 71, "sweating": 72, "swelling": 73, "swollen_joints": 74,
                 "swollen_lymph_nodes": 75, "throat_tightness": 76, "tingling": 77, "tooth_pain": 78, "ulcers": 79,
                 "unusual_bruising": 80, "vomiting": 81, "weight_loss": 82, "wheezing": 83, "yellow_skin": 84}
disease_list = {3: "bacterial_pneumonia", 26: "tuberculosis", 28: "urinary_tract_infection", 14: "lyme_disease",
                1: "bacterial_conjunctivitis", 11: "gonorrhea", 24: "syphilis", 23: "strep_throat", 7: "chlamydia",
                15: "meningitis", 16: "otitis_media", 4: "bacterial_skin_infection", 22: "sinusitis", 8: "cholera",
                27: "typhoid_fever", 29: "whooping_cough", 12: "legionnaires_disease", 19: "scarlet_fever",
                20: "septicemia", 2: "bacterial_endocarditis", 0: "anthrax", 9: "diphtheria", 18: "rheumatic_fever",
                21: "shigellosis", 17: "plague", 13: "leprosy", 6: "campylobacteriosis", 5: "brucellosis",
                25: "trachoma", 10: "epiglottitis"}





#============model prediction function
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))

    for item in patient_symptoms:
        input_vector[symptoms_dict[item]] = 1
    return disease_list[svc.predict([input_vector])[0]]


#creating routes
@app.route('/')
def index():
    # Render the welcome page
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/general')
def general():
    return render_template('general.html')

@app.route('/specific')
def specific():
    return render_template('specific.html')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        if not symptoms:
            return render_template('specific.html', message="Please select at least one symptom")
        
        # Split the comma-separated symptoms
        user_symptoms = [s.strip() for s in symptoms.split(',') if s.strip()]
        
        if not user_symptoms:
            return render_template('specific.html', message="Please select at least one symptom")
        
        try:
            predicted_disease = get_predicted_value(user_symptoms)
            pre, anti, die, work = helper(predicted_disease)
            return render_template(
                'specific.html',
                predicted_disease=predicted_disease,
                dis_pre=pre,
                dis_anti=anti,
                dis_die=die,
                dis_work=work
            )
        except (KeyError, IndexError):
            # Instead of showing "Disease not found", provide symptom-based suggestions
            # Create a generic response based on common symptoms
            common_precautions = [
                ["Rest and adequate sleep", "Maintain good hygiene", "Stay hydrated", "Monitor symptoms", "Consult healthcare provider"]
            ]
            common_antibiotics = [
                ["Consult doctor for specific antibiotics", "Avoid self-medication", "Complete prescribed course", "Follow dosage instructions", "Monitor for side effects"]
            ]
            common_diet = [
                ["Light and easily digestible food", "Plenty of fluids", "Avoid spicy foods", "Include fruits and vegetables", "Small frequent meals"]
            ]
            common_workouts = [
                ["Light walking if possible", "Gentle stretching", "Avoid strenuous exercise", "Rest when needed", "Gradual return to activity"]
            ]
            
            return render_template(
                'specific.html',
                predicted_disease="Based on your symptoms",
                dis_pre=common_precautions,
                dis_anti=common_antibiotics,
                dis_die=common_diet,
                dis_work=common_workouts
            )
    return render_template('specific.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/developers')
def developers():
    return render_template('developers.html')

@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html')

if __name__ == '__main__':
    app.run(debug=True)
