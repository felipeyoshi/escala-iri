import json

def calculate_scores(data):
    # Invert response for question 7
    if "7" in data:
        if data["7"] == 1:
            data["7"] = 5
        elif data["7"] == 2:
            data["7"] = 4
        elif data["7"] == 4:
            data["7"] = 2
        elif data["7"] == 5:
            data["7"] = 1

    # Domains questions
    domains = {
        "Tomada de Perspectiva": ["3", "8", "15", "18", "20", "25"],
        "Consideração Empática": ["2", "4", "9", "11", "14", "21", "26"],
        "Fantasia": ["1", "5", "7", "12", "16", "22", "24"],
        "Angústia Pessoal": ["6", "10", "13", "17", "19", "23"]
    }

    # Ranges for each domain based on gender
    ranges = {
        "Masculino": {
            "Tomada de Perspectiva": (22.37, 29.93),
            "Consideração Empática": (20.84, 31.44),
            "Fantasia": (15.87, 27.75),
            "Angústia Pessoal": (15.7, 25.68),
            "IRI": (80.72, 108.86)
        },
        "Feminino": {
            "Tomada de Perspectiva": (23.88, 31.26),
            "Consideração Empática": (25.45, 32.73),
            "Fantasia": (20.43, 30.67),
            "Angústia Pessoal": (18.97, 28.35),
            "IRI": (93.74, 118)
        }
    }

    # Calculate scores for each domain
    scores = {}
    for domain, questions in domains.items():
        scores[domain] = sum(data[q] for q in questions)

    # Calculate IRI
    scores["IRI"] = sum(scores.values())

    # Classify each domain score
    gender = data["sex"]
    classifications = {}
    for domain, score in scores.items():
        low, high = ranges[gender][domain]
        if low <= score <= high:
            classifications[domain] = "Congruente"
        elif score < low:
            classifications[domain] = "Reduzido"
        else:
            classifications[domain] = "Elevado"
    
    # Generate report
    domain_descriptions = {
        "Tomada de Perspectiva": {
            "name": "Tomada de Perspectiva (TP)",
            "description": """
O domínio da tomada de perspectiva se refere ao domínio cognitivo da Empatia, que envolve a habilidade da cognição social implicada na consideração dos elementos do estado mental de terceiros (emoções, necessidades, desejos e intenções). 
Baixos escores atingidos podem ser sugestivos de falhas primárias no desenvolvimento dos componentes da Teoria da Mente (ToM) ou secundárias à presença de variáveis tais como a inflexibilidade cognitiva, elevados níveis de estresse ou desregulação emocional;
Escores médios ou elevados atingidos podem estar associados com maiores índices de inteligência emocional."""
        },
        "Consideração Empática": {
            "name": "Consideração Empática (CE)",
            "description": """
O domínio da consideração empática investiga elementos afetivos e cognitivos da empatia. Dentre os componentes cognitivos avaliados pelos itens estão a Teoria da Mente e o Conhecimento Social. Elevados escores neste item podem ser sugestivos de que o avaliando tende a considerar o conhecimento social aprendido e a sua motivação social no seu funcionamento social."""
        },
        "Fantasia": {
            "name": "Fantasia (FS)",
            "description": """
O domínio primariamente denominado “Fantasia” envolve as habilidades de imaginação e do compartilhamento de experiências afetivas. A capacidade de imaginação está geralmente associada com melhores habilidades de inferência, que favorecem uma melhor competência social."""
        },
        "Angústia Pessoal": {
            "name": "Angústia Pessoal (AP)",
            "description": """
O domínio primariamente denominado como “Angústia Pessoal” se refere à capacidade de ser contagiado emocionalmente pela emoção de terceiros. Escores reduzidos podem sugerir a presença de “apatia” ou “indiferença” sociais. Escores elevados sugerem maior sensibilidade ao contágio emocional interpessoal ou maiores níveis de desregulação emocional."""
        }
    }

    report = "Este instrumento se propõe a avaliar os domínios que estruturam a habilidade de empatia. De acordo com a literatura atual, os domínios da empatia podem ser classificados entre cognitivos e afetivos. Cada um dos domínios avaliados através deste instrumento deve considerado precursor essencial da expressão de comportamentos pró-sociais empáticos.\nDomínios\nDescrição\n"

    for domain, info in domain_descriptions.items():
        classification = classifications[domain]
        report += f"{info['name']}\nO escore atingido no domínio primariamente nomeado como a “{info['name']}” se revelou {classification.upper()}, quando comparado com a média de outros indivíduos brasileiros (Sampaio et al., 2011).\n{info['description']}\n"

    report += """
Escore total (IRI)
O escore total se refere ao índice de reatividade interpessoal do avaliado. Maiores índices globais são sugestivos de maior reatividade aos estímulos interpessoais e, em níveis não extremos, tendem a se associar com a competência social preservada."""

    result = {
        "Tipo": "Escala IRI",
        "Escores": scores,
        "Classificações": classifications,
        "Report": report
    }

    # Return result in JSON format
    return json.dumps({"Resultado": result}, indent=4)