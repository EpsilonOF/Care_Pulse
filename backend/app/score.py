

def sum_domain_scores(response_dict):

    sum_physical_limitations = sum([int(response_dict[i][0]) for i in [1, 2, 3]])
    sum_symptom_frequency = sum([int(response_dict[i][0]) for i in [5, 6]])
    sum_symptom_burden = sum([int(response_dict[i][0]) for i in [4, 7]])
    sum_quality_of_life = sum([int(response_dict[i][0]) for i in [8, 9]])
    sum_social_limitations = sum([int(response_dict[i][0]) for i in [10, 11, 12]])

    return [sum_physical_limitations, sum_symptom_frequency, sum_symptom_burden, sum_quality_of_life, sum_social_limitations]


def calculate_transformed_score(sum_of_items, min_possible_sum, max_possible_sum):
    """
    Calculate the transformed score on a 0-100 scale.

    Parameters:
    sum_of_items (int): The sum of the item scores for the domain.
    min_possible_sum (int): The minimum possible sum for the domain.
    max_possible_sum (int): The maximum possible sum for the domain.

    Returns:
    float: The transformed score on a 0-100 scale.
    """
    if sum_of_items < min_possible_sum or sum_of_items > max_possible_sum:
        raise ValueError("Sum of items is out of the possible range.")

    transformed_score = ((sum_of_items - min_possible_sum) /
                         (max_possible_sum - min_possible_sum)) * 100
    return transformed_score


def calculate_total_score(patient_dict):
    """
    Calculate the total score across all domains.

    Parameters:
    physical_limitations_sum (int): Sum of scores for Physical Limitations items.
    symptom_frequency_sum (int): Sum of scores for Symptom Frequency items.
    symptom_burden_sum (int): Sum of scores for Symptom Burden items.
    quality_of_life_sum (int): Sum of scores for Quality of Life items.
    social_limitations_sum (int): Sum of scores for Social Limitations items.

    Returns:
    dict: patient name and overall summary score
    """
    physical_limitations_sum, symptom_frequency_sum, symptom_burden_sum, quality_of_life_sum, social_limitations_sum = sum_domain_scores(patient_dict["responses"])
    min_max_values = {
        'physical_limitations': (3, 18),
        'symptom_frequency': (2, 14),
        'symptom_burden': (2, 10),
        'quality_of_life': (2, 10),
        'social_limitations': (3, 18)
    }
    patient_name = patient_dict["patient_name"]
    # Calculate transformed scores for each domain
    transformed_scores = {
        'physical_limitations': calculate_transformed_score(physical_limitations_sum, *min_max_values['physical_limitations']),
        'symptom_frequency': calculate_transformed_score(symptom_frequency_sum, *min_max_values['symptom_frequency']),
        'symptom_burden': calculate_transformed_score(symptom_burden_sum, *min_max_values['symptom_burden']),
        'quality_of_life': calculate_transformed_score(quality_of_life_sum, *min_max_values['quality_of_life']),
        'social_limitations': calculate_transformed_score(social_limitations_sum, *min_max_values['social_limitations'])
    }

    # Calculate the overall summary score
    overall_summary_score = sum(transformed_scores.values()) / len(transformed_scores)
    return {"patient_name": patient_name, "overall_summary_score": overall_summary_score}
