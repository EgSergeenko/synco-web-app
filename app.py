import base64
import os
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image

PRODUCT_MAPPING = {
    'CAS number': {
        '119-61-9': 'Diphenyl ketone',
        '134-81-6': 'Diphenylethanedione',
        '486-25-9': '9H-Fluoren-9-one',
        '576-26-1': '2,6-Dimethylphenol',
        '92-93-3': '4-Nitrobiphenyl',
    },
    'SMILES': {
        'O=C(C1CCCCC1)C2CCCCC2': 'Diphenyl ketone',
        'O=C(C1CCCCC1)C(=O)C2CCCCC2': 'Diphenylethanedione',
        'O=C1C2CCCCC2C3CCCCC13': '9H-Fluoren-9-one',
        'CC1CCCC(C)C1O': '2,6-Dimethylphenol',
        '[O-][N+](=O)C1CCC(CC1)C2CCCCC2': '4-Nitrobiphenyl',
    },
}


@st.cache_data
def load_data():
    return pd.read_csv('reactions.tsv', delimiter='\t')


@st.cache_data
def load_image(image_name):
    image_path = os.path.join('images', '{0}.png'.format(image_name))
    return Image.open(image_path)


@st.cache_data
def load_image_bytes(img_path):
    image_bytes = Path(img_path).read_bytes()
    return base64.b64encode(image_bytes).decode()


def app():
    st.set_page_config(
        layout='wide',
        page_title='SynCo',
        page_icon=Image.open('images/favicon.ico'),
    )
    st.markdown(
        '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )
    reactions = load_data()
    main_column = st.columns([1, 5, 1])[1]
    show_description(main_column)
    show_benefits(main_column)
    show_prediction_form(main_column, reactions)
    show_contact_form(main_column)
    show_team(main_column)
    show_contacts(main_column)
    add_scripts()


def show_contact_form(container):
    container.header('Learn more')
    left_column, right_column = container.columns(2)

    with container.form(key='contact_form'):
        left_column.text_input(
            'Name',
            placeholder='Your name',
        )
        left_column.text_input(
            'Industry',
            placeholder='Chemistry',
        )
        right_column.text_input(
            'Organization',
            placeholder='ITMO University',
        )
        right_column.text_input(
            'Research field',
            placeholder='Organic synthesis',
        )
        # container.text_input(
        #     'Country code and phone number',
        #     placeholder='+799999999'
        # )
        container.text_input(
            'E-mail',
            placeholder='email@address.com',
        )
        container.text_area(
            'Your message',
            label_visibility='collapsed',
            placeholder='Your message',
        )
        container.button('Send', use_container_width=True)

    container.markdown('---')


def show_benefits(container):
    container.header('Key benefits')

    left_column, right_column = container.columns(2)

    left_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-evenly">
                <div class="col">
                    <img class="d-block m-auto" style="width: 105px" src="data:image/png;base64,{0}" />
                </div>
                <div class="col">
                    <h4>Various types of conditions</h4>
                    <p>Temperature, pressure, solvent, catalyst and reagent are available for every reaction</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/various_types_of_conditions.png'),
        ),
        unsafe_allow_html=True,
    )

    right_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-evenly">
                <div class="col">
                    <img class="m-auto d-block" style="width: 105px" src="data:image/png;base64,{0}" />
                </div>
                <div class="col">
                    <h4>Yield ranking</h4>
                    <p>Best product yields are located above</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/yield_ranking.png'),
        ),
        unsafe_allow_html=True,
    )

    left_column, right_column = container.columns(2)

    left_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-evenly">
                <div class="col">
                    <img class="m-auto d-block" style="width: 105px" src="data:image/png;base64,{0}" />
                </div>
                <div class="col">
                    <h4>Convenient request</h4>
                    <p>Input your molecule in SMILES, CAS registry number and IUPAC name formats</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/convenient_request.png'),
        ),
        unsafe_allow_html=True,
    )

    right_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-evenly">
                <div class="col">
                    <img class="m-auto d-block" style="width: 105px" src="data:image/png;base64,{0}" />
                </div>
                <div class="col">
                    <h4>Fast predictions</h4>
                    <p>Conditions selection is carried out within a few seconds</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/fast_predictions.png'),
        ),
        unsafe_allow_html=True,
    )

    container.markdown('---')


def show_team(container):
    container.header('Our team')

    left_column, right_column = container.columns(2)

    left_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-around">
                <div class="col">
                    <img class="w-75 m-auto d-block" src="data:image/png;base64,{0}" />
                </div>
                <div class="col align-self-center">
                    <h4>Anastasiia Lavrinenko</h4>
                    <p>Project curator<br/>Domain expert</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/anastasiia_lavrinenko.png'),
        ),
        unsafe_allow_html=True,
    )

    right_column.markdown(
        """
        <div class="container">
            <div class="row justify-content-around">
                <div class="col">
                    <img class="w-75 m-auto d-block" src="data:image/png;base64,{0}" />
                </div>
                <div class="col align-self-center">
                    <h4>Anastasia Orlova</h4>
                    <p>Domain expert<br/>Data scientist</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/anastasiia_orlova.png'),
        ),
        unsafe_allow_html=True,
    )

    left_column, right_column = container.columns(2)

    left_column.markdown(
        """
        <div class="container mt-5">
            <div class="row justify-content-around">
                <div class="col">
                    <img class="w-75 m-auto d-block" src="data:image/png;base64,{0}" />
                </div>
                <div class="col align-self-center">
                    <h4>Ksenia Nikitina</h4>
                    <p>Domain expert<br/>Data scientist</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/ksenia_nikitina.png'),
        ),
        unsafe_allow_html=True,
    )

    right_column.markdown(
        """
        <div class="container mt-5">
            <div class="row justify-content-around">
                <div class="col">
                    <img class="w-75 m-auto d-block" src="data:image/png;base64,{0}" />
                </div>
                <div class="col align-self-center">
                    <h4>Egor Sergeenko</h4>
                    <p>Developer<br/>Data scientist</p>
                </div>
            </div>
        </div>
        """.format(
            load_image_bytes('images/egor_sergeenko.png'),
        ),
        unsafe_allow_html=True,
    )

    container.markdown('---')


def add_scripts():
    st.markdown(
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.bundle.min.js" crossorigin="anonymous"></script>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js" crossorigin="anonymous"></script>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha2/dist/js/bootstrap.min.js" crossorigin="anonymous"></script>',
        unsafe_allow_html=True,
    )


def show_prediction_form(container, reactions):
    container.header('Demo')

    search_by_container, product_container = container.columns(2)
    with container.form(key='predict_form'):
        search_by = search_by_container.selectbox(
            options=['IUPAC name', 'CAS number', 'SMILES'], label='Search by',
        )
        options = reactions['name'].unique().tolist()
        if search_by != 'IUPAC name':
            options = PRODUCT_MAPPING[search_by].keys()
        product = product_container.selectbox(
            options=options, label='Product',
        )
        if search_by != 'IUPAC name':
            product = PRODUCT_MAPPING[search_by][product]
        clicked = container.button('Predict', use_container_width=True)

    container.markdown('---')

    if clicked:
        progres_text = 'Predicting results...'
        progress_bar = container.progress(0, text=progres_text)

        placeholder = container.markdown(
            """
            <div style="height: 200px;"></div>
            """,
            unsafe_allow_html=True,
        )

        separator = container.markdown('---')

        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1, text=progres_text)

        progress_bar.empty()
        placeholder.empty()
        separator.empty()

        show_prediction_results(
            container, reactions[reactions['name'] == product],
        )
    else:
        container.markdown(
            """
            <div style="height: 200px;"></div>
            """,
            unsafe_allow_html=True,
        )
        container.markdown('---')


def show_description(container):
    text_column, image_column = container.columns([5, 2])
    text_column.markdown(
        """
        <h1 style=font-size:80px>
            SynCo
        </h1>
        """,
        unsafe_allow_html=True,
    )
    text_column.markdown(
        """
        <h2 style=font-size:40px>
            AI for synthesis conditions and yield prediction
        </h2>
        """,
        unsafe_allow_html=True,
    )

    text_column.markdown(
        """
        <p style=font-size:20px>
            Welcome to a platform for exploration of organic synthesis space.
            We provide a comprehensive tool for prediction of organic reactions conditions,
            that ranks them by their product yield.
            Just enter your target molecule.
        </p>
        """,
        unsafe_allow_html=True,
    )
    text_column.markdown(
        """
        <div class="w-100 d-flex justify-content-start">
            <a id="demo_button" href="#demo" role="button" class="btn btn-lg btn-outline-success text-decoration-none" style="width: 40%;">
                Demo
            </a>
            <div style="width: 3%"></div>
            <button class="btn btn-lg btn-outline-secondary" style="width: 40%">
                Sing Up
            </button>
            <style>
                #demo_button:hover {
                    color: white;
                }
                #demo_button {
                    color: #198754;
                }
            </style>
        </div>
        """,
        unsafe_allow_html=True,
    )
    image_column.image(load_image('logo'), width=300)

    container.markdown('---')


def show_prediction_results(container, reactions):
    reactions = reactions.sort_values(by='yield_value', ascending=False)
    for reaction in reactions.to_dict(orient='records'):
        container.subheader(
            '**Yield**: {0}%'.format(reaction['yield_value']),
        )
        show_conditions(container, reaction)
        show_prediction(container, reaction)
        container.markdown('---')


def show_prediction(container, reaction):
    columns = container.columns(6)

    columns[0].image(
        load_image(reaction['reactants']),
        caption=reaction['reactants_smiles'].upper(),
    )

    if isinstance(reaction['reactants_II'], float):
        columns[1].image(load_image('arrow'))
        columns[2].image(
            load_image(reaction['products']),
            caption=reaction['products_smiles'].upper(),
        )
    else:
        columns[1].image(load_image('plus'))
        columns[2].image(
            load_image(reaction['reactants_II']),
            caption=reaction['reactants_II_smiles'].upper(),
        )
        columns[3].image(load_image('arrow'))
        columns[4].image(
            load_image(reaction['products']),
            caption=reaction['products_smiles'].upper(),
        )


def show_conditions(container, reaction):
    conditions = [
        '* **Temperature**: {0} °C'.format(int(reaction['temperature_1'])),
        '* **Pressure**: {0} MPa'.format(reaction['pressure_1']),
        get_condition_markdown('catalysts', reaction),
        get_condition_markdown('solvents', reaction),
        get_condition_markdown('reagents', reaction),
    ]
    container.markdown('\n'.join(conditions))


def get_condition_markdown(substance_type, reaction):
    substances = [
        reaction['{0}_1'.format(substance_type)],
        reaction['{0}_1_II'.format(substance_type)],
    ]
    substances = [
        substance for substance in substances if not isinstance(substance, float)
    ]
    if not substances:
        substances = ['-']
    return '* **{0}**: {1}'.format(
        substance_type.capitalize(),
        ', '.join(substances),
    )


def show_contacts(container):
    container.header('Contact us')
    columns = container.columns([5, 2, 2])
    text_column, image_columns = columns[0], columns[1:]
    image_columns[0].image(load_image('itmo'), width=200)
    image_columns[1].image(load_image('scamt'), width=200)
    text_column.text(
        """
        Anastasiia Orlova       orlova@scamt-itmo.ru
        Anastasiia Lavrinenko   lavrinenko@scamt-itmo.ru
        Ksenia Nikitina         nikitina.xena@gmail.com
        Egor Sergeenko          es.egor.sergeenko@gmail.com
                
        Lomonosova St. 9, St. Petersburg, 191002, Russia
        """,
    )


if __name__ == '__main__':
    app()
