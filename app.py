import streamlit as st
from score import calculate_scores

name = ''
age = None 
sex = ''
results = {}

tab1, tab2, tab3 = st.tabs(["DADOS", "AVALIAÇÃO", "RESULTADO"])

with tab1:
    with st.form('user_input'):
        name = st.text_input('Nome')
        age = st.number_input('Idade', min_value=0, max_value=120, value=0) 
        sex = st.selectbox('Sexo', ['Masculino', 'Feminino'])
        
        submitted = st.form_submit_button("Enviar")

    if submitted:
        st.success("Dados salvos!")

if name and age and sex:
    tab2.enabled = True
    tab3.enabled = True

if "submit" not in st.session_state:
    st.session_state.submit = False

with tab2:
    if name and age:
        questions = {"1": "1. Costumo fantasiar com coisas que poderiam me acontecer",
                     "2": "2. Preocupo-me com as pessoas que não têm uma boa qualidade de vida",
                     "3": "3. Tento compreender meus amigos imaginando como eles veem as coisas",
                     "4": "4. Sinto compaixão quando alguém é tratado injustamente",
                     "5": "5. Depois de ver uma peça de teatro ou um filme sinto-me envolvido com os personagens",
                     "6": "6. Fico apreensivo em situações emergenciais",
                     "7": "7. Sou neutro quando vejo filmes",
                     "8": "8. Antes de tomar alguma decisão procuro avaliar todas as perspectivas",
                     "9": "9. Quando vejo que se aproveitam de alguém, sinto necessidade de protegê-lo",
                     "10": "10. Fico tenso em situações que envolvem fortes emoções",
                     "11": "11. Descrevo-me como uma pessoa de “coração mole” (muito sensível)",
                     "12": "12. Quando vejo uma história interessante, imagino como me sentiria se ela estivesse acontecendo comigo",
                     "13": "13. Habitualmente eu fico nervoso quando vejo pessoas feridas",
                     "14": "14. Incomodo-me com as coisas ruins que acontecem aos outros",
                     "15": "15. Escuto os argumentos dos outros, mesmo quando estou convicto da minha opinião",
                     "16": "16. Sinto emoções de um personagem de filme como se fossem minhas próprias emoções",
                     "17": "17. Sinto-me indefeso em situações de fortes emoções",
                     "18": "18. Imagino como as pessoas se sentem quando eu as critico",
                     "19": "19. Tendo a perder o controle durante emergências",
                     "20": "20. Tento compreender o argumento dos outros",
                     "21": "21. Fico comovido com os problemas dos outros",
                     "22": "22. Tenho facilidade de assumir a posição de um personagem de filme",
                     "23": "23. Perco o controle quando vejo alguém que esteja precisando de muita ajuda",
                     "24": "24. Habitualmente me envolvo emocionalmente com filmes e/ou livros",
                     "25": "25. Coloco-me no lugar do outro se eu me preocupo com ele",
                     "26": "26. Costumo me emocionar com as coisas que vejo acontecer com os outros"
        }

        st.write("1 = Não me descreve bem; 5 = Me descreve muito bem")
        
        for key, question in questions.items():
            # Split the space into two columns: 
            # The first one for the question and the second one for the slider.
            col1, col2 = st.columns([3, 1])
            with col1:
                col1.write("\n\n\n\n\n")
                # Making the question bold using Markdown
                col1.markdown(f"**{question}**")
            with col2:
                # Use the slider within the second column
                answer = col2.slider("Resposta", 1, 5, 3, key=f'slider_{key}', label_visibility="hidden")    
            results[key] = answer
        
        results['sex'] = sex
        results['age'] = age

        final_score = calculate_scores(results)

        # Add a submit button
        if st.button('Enviar respostas'):
            st.session_state.submit = True
            st.session_state.results = results
            st.success("Respostas enviadas!")

with tab3:
    if st.session_state.submit:
        final_score = calculate_scores(st.session_state.results)
        st.json(final_score)
    else:
        st.warning('Sem resultado ainda. Clique em "Enviar respostas" na tab "AVALIAÇÃO" para ver o resultado.')

