def get_dr_scale_definition(scale):
    """
    Return the definition for each DR scale level.
    """
    definitions = {
        0: "No apparent Diabetic Retinopathy",
        1: "Mild non-proliferative Diabetic Retinopathy",
        2: "Moderate non-proliferative Diabetic Retinopathy",
        3: "Severe non-proliferative Diabetic Retinopathy",
        4: "Proliferative Diabetic Retinopathy"
    }
    return definitions.get(scale, "Invalid scale")

