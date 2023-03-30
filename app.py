import os
import time

import pandas as pd
import streamlit as st
from PIL import Image


@st.cache_data
def load_data():
    return pd.read_csv('reactions.tsv', delimiter='\t')


@st.cache_data
def load_image(image_name):
    image_path = os.path.join('images', '{0}.png'.format(image_name))
    return Image.open(image_path)


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
    show_prediction_form(main_column, reactions)
    show_contacts(main_column)
    add_scripts()


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

    options = reactions['name'].unique().tolist()
    product = container.selectbox(options=options, label='Product')
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
            <button class="btn btn-lg btn-outline-success" style="width: 40%">
                Demo
            </button>
            <div style="width: 3%"></div>
            <button class="btn btn-lg btn-outline-secondary" style="width: 40%">
                Sing Up
            </button>
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
    columns = container.columns([3, 2, 2])
    text_column, image_columns = columns[0], columns[1:]
    image_columns[0].image(load_image('itmo'), width=300)
    image_columns[1].image(load_image('scamt'), width=300)
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
