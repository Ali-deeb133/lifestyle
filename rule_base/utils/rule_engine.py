import math

def classify_bmi(bmi):
    if bmi < 16: return "Severe Thinness", "Severe underweight – high risk of malnutrition"
    if 16 <= bmi < 17: return "Moderate Thinness", "Clear underweight condition"
    if 17 <= bmi < 18.5: return "Mild Thinness", "Slightly underweight"
    if 18.5 <= bmi < 25: return "Normal", "Healthy weight range"
    if 25 <= bmi < 30: return "Overweight", "Increased fat accumulation"
    if 30 <= bmi < 35: return "Obese Class I", "Moderate obesity"
    if 35 <= bmi < 40: return "Obese Class II", "Severe obesity"
    return "Obese Class III", "Very high health risk"

def classify_bfp(bfp, gender):
    if gender == "female":
        if bfp < 12: return "Essential Low", "Critically low fat (hormonal risk)"
        if 12 <= bfp < 20: return "Athletic", "Very lean and fit"
        if 20 <= bfp < 30: return "Healthy", "Normal fat distribution"
        if 30 <= bfp < 35: return "Overfat", "Increased fat storage"
        if 35 <= bfp < 45: return "Obese", "High fat accumulation"
        return "Very High", "Severe fat excess"
    else:
        if bfp < 6: return "Essential Low", ""
        if 6 <= bfp < 14: return "Athletic", ""
        if 14 <= bfp < 24: return "Healthy", ""
        if 24 <= bfp < 30: return "Overfat", ""
        if 30 <= bfp < 35: return "Obese", ""
        return "Very High", ""

def classify_lean_mass(lean_percent):
    if lean_percent < 50: return "Very Low", "Very low muscle mass"
    if 50 <= lean_percent < 65: return "Below Average", "Below average"
    if 65 <= lean_percent < 80: return "Healthy", "Healthy"
    return "Very Muscular", "Very muscular"

def classify_fat_mass(fat_percent):
    if fat_percent < 15: return "Very Low", "Very low fat reserves"
    if 15 <= fat_percent < 25: return "Normal", "Normal"
    if 25 <= fat_percent < 35: return "Elevated", "Elevated"
    return "High", "High fat accumulation"

def classify_bmr(bmr, gender):
    if gender == "female":
        if bmr < 1100: return "Low", "Low metabolic rate"
        if 1100 <= bmr < 1500: return "Average", "Average metabolic rate"
        return "High", "High metabolism"
    else:
        if bmr < 1300: return "Very Low", "Likely low muscle mass or undernutrition"
        if 1300 <= bmr < 1600: return "Low", "Below average metabolism"
        if 1600 <= bmr < 1900: return "Average", "Normal metabolic rate"
        if 1900 <= bmr < 2300: return "High", "Good muscle mass and metabolic activity"
        return "Very High", "Very muscular or highly active metabolism"

def classify_tdee(tdee):
    if tdee < 1500: return "Low", "Low energy requirement"
    if 1500 <= tdee < 2200: return "Moderate", "Moderate"
    if 2200 <= tdee < 3000: return "Active", "Active lifestyle"
    return "Highly Active", "Highly active"