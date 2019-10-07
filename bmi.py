def calculate_bmi(weight, height):
    bmi = weight / ((height/100) * (height/100))
    bmi = round(bmi, 2)
    return bmi