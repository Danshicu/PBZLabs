import datetime
import uuid


import streamlit as st

from time import sleep
from ..db import db
from ..db import db_interactions


class PagesController:

    @staticmethod
    def set_current_worker_state(state):
        st.session_state.currentWorkerOption = state

    @staticmethod
    def set_current_subscription_state(state):
        st.session_state.currentSubscriptionOption = state

    @staticmethod
    def set_current_worker_received_state(state):
        st.session_state.currentWorkerReceivedEditionsOptions = state

    @staticmethod
    def set_current_issued_by_year_edition_state(state):
        st.session_state.currentIssuedByYearEditionOptions = state

    @staticmethod
    def init_states():
        if 'currentWorkerReceivedEditionsOption' not in st.session_state:
            st.session_state.currentWorkerReceivedEditionsOptions = 'write'
        if 'currentWorkerOption' not in st.session_state:
            st.session_state.currentWorkerOption = 'look'
        if 'currentSubscriptionOption' not in st.session_state:
            st.session_state.currentSubscriptionOption = 'look'
        if 'currentIssuedByYearEditionOptions' not in st.session_state:
            st.session_state.currentIssuedByYearEditionOptions = 'write'

    @staticmethod
    def reset_states():
        PagesController.init_states()
        st.session_state.currentIssuedByYearEditionOptions = 'write'
        st.session_state.currentWorkerOption = 'look'
        st.session_state.currentSubscriptionOption = 'look'
        st.session_state.currentWorkerReceivedEditionsOptions = 'write'

    @staticmethod
    def add_worker_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Добавление нового сотрудника', layout='wide')
        st.write('## Информация о новом сотруднике')
        nameInput = st.text_input('ФИО сотрудника', placeholder='Введите ФИО сотрудника сюда...', max_chars=30)
        posts = db_interactions.get_post_id_to_name_dictionary()
        postID = st.selectbox('Должность', options=list(posts.values()))
        isActive = st.checkbox('Работник в данный момент активен?')
        workerid=str(uuid.uuid4())
        addButton = st.button('Добавить работника в базу')
        values = [nameInput, postID, isActive]
        if addButton:
            if all(values):
                db_interactions.insert_into(db.DBConnection.WORKERS_TABLE,
                                        [workerid, nameInput, db_interactions.find_key_by_value(posts, postID), isActive])
                st.write('Работник добавлен')

    @staticmethod
    def edit_worker_container(placeholder):
        with placeholder.container():
            st.header = 'Изменение информации о сотруднике'
            st.write('## Новая информация о сотруднике')
            nameInput = st.text_input('ФИО сотрудника', placeholder='Введите ФИО сотрудника сюда...', max_chars=30)
            posts = db_interactions.get_post_id_to_name_dictionary()
            postID = st.selectbox('Должность', options=list(posts.values()))
            isActive = st.checkbox('Работник в данный момент активен?')
            if st.button('Отменить', on_click=lambda : PagesController.set_current_worker_state('look')):
                pass
            change_button =  st.button('Изменить данные работника')
            if change_button:
                db_interactions.edit_worker(
                    [st.session_state.edit_worker_id, nameInput, db_interactions.find_key_by_value(posts, postID),
                     isActive],
                    st.session_state.edit_worker_id)
                PagesController.reset_states()
                placeholder.empty()
                sleep(0.03)
                PagesController.lookup_workers_container(placeholder)

    @staticmethod
    def lookup_all_subscriptions_page():
        PagesController.init_states()
        st.set_page_config(page_title='Просмотр всех оформленных подписок', layout='wide')
        placeholder = st.empty()
        if st.session_state.currentSubscriptionOption == 'look':
            PagesController.lookup_subscriptions_container(placeholder)
        if st.session_state.currentSubscriptionOption == 'edit':
            PagesController.edit_subscription_container(placeholder)

    @staticmethod
    def lookup_subscriptions_container(placeholder):
        st.header = 'Просмотр всех подписок'
        subscriptions = db_interactions.get_all_values(db.DBConnection.SUBSCRIPTIONS_TABLE)
        idToNameDictionary = db_interactions.get_edition_index_to_name_dictionary()
        frequencyNames = db_interactions.create_dictionary_from_tuples(
            db_interactions.get_all_values(db.DBConnection.FREQUENCY_OF_RELEASE_TABLE))
        deliveryTypeName = db_interactions.create_dictionary_from_tuples(
            db_interactions.get_all_values(db.DBConnection.DELIVERY_TYPES_TABLE))
        with placeholder.container():
            st.write('## Все оформленные подписки')
            columns = st.columns(12)
            names = ['Идентификатор подписки', 'Название издания', 'Количество экземпляров за одну доставку', 'Дата начала подписки',
                     'Дата окончания подписки', 'Стоимость подписки', 'Периодичность доставки', 'Способ доставки',
                     'Предполагаемая дата доставки', 'Подписка активна', 'Изменить', 'Удалить']
            for i in range(0, len(names)):
                with columns[i]:
                    st.write(names[i])
            for edition in subscriptions:
                with st.container():
                    columns=st.columns(12)
                    with columns[0]:
                        st.write(edition[0])
                    with columns[1]:
                        st.write(idToNameDictionary[edition[1]])
                    with columns[2]:
                        st.write(edition[2])
                    with columns[3]:
                        st.write(edition[3])
                    with columns[4]:
                        st.write(edition[4])
                    with columns[5]:
                        st.write(edition[5])
                    with columns[6]:
                        name = str(frequencyNames[edition[6]]).split(', ')
                        st.write(name[0])
                    with columns[7]:
                        st.write(deliveryTypeName[edition[7]])
                    with columns[8]:
                        st.write(edition[8])
                    with columns[9]:
                        st.write(edition[9])
                    with columns[10]:
                        edit_button = st.button('⚙️', key = edition[0])
                        if edit_button:
                            st.session_state.edit_subscription_id = edition[0]
                            PagesController.set_current_subscription_state('edit')
                            st.rerun()
                    with columns[11]:
                        delete_button = st.button('🗑️', key = f'{edition[0]}_to_delete')
                        if delete_button:
                            db_interactions.delete_subscription(edition[0])

    @staticmethod
    def edit_subscription_container(placeholder):
        with placeholder.container():
            st.header = 'Изменение информации о подписке'
            st.write('## Новая информация о подписке')
            names = ['Название издания', 'Количество экземпляров за одну доставку', 'Дата начала подписки',
                     'Дата окончания подписки', 'Стоимость подписки', 'Периодичность доставки', 'Способ доставки',
                     'Предполагаемая дата доставки']
            idToNameDictionary = db_interactions.get_edition_index_to_name_dictionary()
            frequencyNames = db_interactions.create_dictionary_from_tuples(
                db_interactions.get_all_values(db.DBConnection.FREQUENCY_OF_RELEASE_TABLE))
            visibleFrequencyNames = dict()
            for freq in frequencyNames.values():
                visibleFrequencyNames[freq] = str(freq).split(', ')[0]
            deliveryTypeName = db_interactions.create_dictionary_from_tuples(
                db_interactions.get_all_values(db.DBConnection.DELIVERY_TYPES_TABLE))
            namesSelectionInput = st.selectbox(names[0], index=None, options=list(idToNameDictionary.values()))
            countInput = st.number_input(names[1], min_value=1, step=1)
            startDateInput = st.date_input(names[2])
            endDateInput = st.date_input(names[3])
            subscriptionCost: st.text
            cost: float
            if namesSelectionInput and countInput:
                cost = round(countInput * db_interactions.get_edition_cost_from_index(
                    db_interactions.find_key_by_value(idToNameDictionary, namesSelectionInput)), 3)
                subscriptionCost = st.text(f"Стоимость подписки : {cost}")
            else:
                subscriptionCost = st.text(names[4])
            frequencyInput = st.selectbox(names[5], options=list(visibleFrequencyNames.values()))
            deliveryTypeInput = st.selectbox(names[6], options=list(deliveryTypeName.values()))
            deliveryTimeInput = st.date_input(names[7])
            isActive = st.checkbox('Подписка активна')
            values = [namesSelectionInput, countInput, startDateInput, endDateInput, subscriptionCost, frequencyInput,
                      deliveryTypeInput, deliveryTimeInput, isActive]
            if st.button('Отменить', on_click=lambda: PagesController.set_current_subscription_state('look')):
                pass
            if st.button('Изменить данные подписки'):
                if all(values):
                    db_interactions.edit_subscription(
                        [db_interactions.find_key_by_value(idToNameDictionary, namesSelectionInput), countInput,
                         startDateInput, endDateInput, cost,
                         db_interactions.find_key_by_value(frequencyNames, db_interactions.find_key_by_value(visibleFrequencyNames, frequencyInput)),
                         db_interactions.find_key_by_value(deliveryTypeName, deliveryTypeInput), deliveryTimeInput, isActive],
                        st.session_state.edit_subscription_id)
                    PagesController.reset_states()
                    placeholder.empty()
                    sleep(0.03)
                    PagesController.lookup_subscriptions_container(placeholder)


    @staticmethod
    def lookup_all_posts_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех должностей в библиотеке', layout='wide')
        st.write('## Все должности в библиотеке')
        positions = db_interactions.get_all_values(db.DBConnection.POSTS_TABLE)
        columns = st.columns(2)
        with columns[0]:
            st.write('*Код должности*')
        with columns[1]:
            st.write('*Название должности*')
        for position in positions:
            with columns[0]:
                st.write(position[0])
            with columns[1]:
                st.write(position[1])

    @staticmethod
    def add_post_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Добавить новую должность', layout='wide')
        st.write('## Добавить должность')
        input1 = st.text_input('Кодовый номер должности', placeholder='Введите кодовый номер должности сюда...')
        input2 = st.text_input('Полное название должности', placeholder='Введите полное название должности сюда...', max_chars=20)
        addButton = st.button('Добавить новую должность')
        if addButton:
            db_interactions.insert_into(db.DBConnection.POSTS_TABLE, [input1, input2])
            st.write('Должность добавлена')

    @staticmethod
    def lookup_workers_container(placeholder):
        st.header = 'Просмотр всех сотрудников библиотеки'
        workers = db_interactions.get_all_values(db.DBConnection.WORKERS_TABLE)
        postIdToNameDictionary = db_interactions.get_post_id_to_name_dictionary()
        with placeholder.container():
            st.write('## Все сотрудники библиотеки')
            columns = st.columns(6)
            with columns[0]:
                st.write('*Код сотрудника*')
            with columns[1]:
                st.write('*ФИО сотрудника*')
            with columns[2]:
                st.write('*Должность сотрудника*')
            with columns[3]:
                st.write('*Сотрудник работает в данный момент*')
            with columns[4]:
                st.write('*Изменить*')
            with columns[5]:
                st.write('*Удалить*')
            for worker in workers:
                with st.container():
                    columns = st.columns(6)
                    with columns[0]:
                        st.write(worker[0])
                    with columns[1]:
                        st.write(worker[1])
                    with columns[2]:
                        st.write(postIdToNameDictionary[worker[2]])
                    with columns[3]:
                        st.write(worker[3])
                    with columns[4]:
                        edit_button = st.button('⚙️', key = worker[0])
                        if edit_button:
                            st.session_state.edit_worker_id = worker[0]
                            PagesController.set_current_worker_state('edit')
                            st.rerun()
                    with columns[5]:
                        delete_button = st.button('🗑️', key = f'{worker[0]}_to_delete')
                        if delete_button:
                            db_interactions.delete_worker(worker[0])
                            placeholder.empty()
                            st.rerun()


    @staticmethod
    def lookup_all_workers_page():
        PagesController.init_states()
        st.set_page_config(layout='wide')
        placeholder = st.empty()
        if st.session_state.currentWorkerOption == 'look':
            PagesController.lookup_workers_container(placeholder)
        if st.session_state.currentWorkerOption == 'edit':
            PagesController.edit_worker_container(placeholder)


    @staticmethod
    def lookup_all_edition_types_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех видов изданий', layout='wide')
        st.write('## Все виды изданий')
        editionTypes = db_interactions.get_all_values(db.DBConnection.EDITION_TYPES_TABLE)
        columns = st.columns(2)
        with columns[0]:
            st.write('*Код вида издания*')
        with columns[1]:
            st.write('*Название вида издания*')
        for edType in editionTypes:
            with columns[0]:
                st.write(edType[0])
            with columns[1]:
                st.write(edType[1])

    @staticmethod
    def lookup_all_editions_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех изданий', layout='wide')
        st.write('## Все издания')
        editions = db_interactions.get_all_values(db.DBConnection.EDITION_TABLE)
        columns = st.columns(4)
        with columns[0]:
            st.write('*Подписной индекс издания*')
        with columns[1]:
            st.write('*Название издания*')
        with columns[2]:
            st.write('*Тип издания*')
        with columns[3]:
            st.write('*Стоимость одного экземпляра*')
        idToTypeNameDictionary = db_interactions.create_dictionary_from_tuples(db_interactions.get_all_values(db.DBConnection.EDITION_TYPES_TABLE))
        for edition in editions:
            with columns[0]:
                st.write(edition[0])
            with columns[1]:
                st.write(edition[1])
            with columns[2]:
                st.write(idToTypeNameDictionary[edition[2]])
            with columns[3]:
                st.write(edition[3])

    @staticmethod
    def lookup_all_received_editions_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех полученных изданий', layout='wide')
        st.write('## Все полученные издания')
        editions = db_interactions.get_all_values(db.DBConnection.RECEIVED_EDITIONS_TABLE)
        columns = st.columns(6)
        with columns[0]:
            st.write('*Дата получения*')
        with columns[1]:
            st.write('*Дата выписки*')
        with columns[2]:
            st.write('*Код подписки')
        with columns[3]:
            st.write('*Количество экземпляров*')
        with columns[4]:
            st.write('*ФИО сотрудника*')
        with columns[5]:
            st.write('*Должность сотрудника*')
        workers_name_post = db_interactions.get_worker_uuid_name_post_tuples()
        for edition in editions:
            columns = st.columns(6)
            with columns[0]:
                st.write(edition[0])
            with columns[1]:
                st.write(edition[1])
            with columns[2]:
                st.write(edition[2])
            with columns[3]:
                st.write(edition[3])
            with columns[4]:
                st.write(workers_name_post[edition[4]][0])
            with columns[5]:
                st.write(workers_name_post[edition[4]][1])

    @staticmethod
    def insert_received_editions_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Подтвердить получение издания', layout='wide')
        st.write('## Подтвердить получение')
        idToName = db_interactions.get_valid_workers_uuid_to_name_dict()
        workerBox = st.selectbox('Выберите работника который подтверждает получение', options=idToName.values())
        issueDate = st.date_input('Выберите дату выписки изданий')
        receiveDate = datetime.date.today()
        editions = db_interactions.get_all_values(db.DBConnection.ISSUED_EDITIONS_TABLE)
        subscripionIndex = st.selectbox('Выберите подписку', options = [subscription[0] for subscription in editions if subscription[1]>0])
        count:int
        if subscripionIndex and issueDate:
            countInput = st.number_input('Введите количество полученных экземпляров', min_value=1, max_value=db_interactions.get_non_received_count(subscripionIndex, issueDate), step=1)
            count = int(countInput)
        addButton = st.button('Подтвердить получение изданий')
        if addButton:
            db_interactions.insert_into(db.DBConnection.RECEIVED_EDITIONS_TABLE, [receiveDate, issueDate, subscripionIndex, count, db_interactions.find_key_by_value(idToName, workerBox)])
            st.write('Издание получено')


    @staticmethod
    def lookup_all_delivery_types_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех видов доставки', layout='wide')
        st.write('## Все виды доставки')
        deliveryTypes = db_interactions.get_all_values(db.DBConnection.DELIVERY_TYPES_TABLE)
        columns = st.columns(2)
        with columns[0]:
            st.write('*Код вида доставки*')
        with columns[1]:
            st.write('*Название вида доставки*')
        for delType in deliveryTypes:
            with columns[0]:
                st.write(delType[0])
            with columns[1]:
                st.write(delType[1])

    @staticmethod
    def lookup_all_issued_editions_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех выписанных изданий', layout='wide')
        st.write('## Все выписанные издания')
        editions = db_interactions.get_all_values(db.DBConnection.ISSUED_EDITIONS_TABLE)
        columns = st.columns(3)
        with columns[0]:
            st.write('*Подписной индекс издания*')
        with columns[1]:
            st.write('*Количество не полученных экземпляров*')
        with columns[2]:
            st.write('*Дата выписки*')
        for edition in editions:
            with columns[0]:
                st.write(edition[0])
            with columns[1]:
                st.write(edition[1])
            with columns[2]:
                st.write(edition[2])

    @staticmethod
    def insert_subscription_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех подписок', layout='wide')
        st.header = 'Информация о всех подписках'
        names = ['Название издания', 'Количество экземпляров за одну доставку', 'Дата начала подписки',
                 'Дата окончания подписки', 'Стоимость подписки', 'Периодичность доставки', 'Способ доставки',
                 'Предполагаемая дата доставки']
        idToNameDictionary = db_interactions.get_edition_index_to_name_dictionary()
        frequencyNames = db_interactions.create_dictionary_from_tuples(
            db_interactions.get_all_values(db.DBConnection.FREQUENCY_OF_RELEASE_TABLE))
        deliveryTypeName = db_interactions.create_dictionary_from_tuples(
            db_interactions.get_all_values(db.DBConnection.DELIVERY_TYPES_TABLE))
        namesSelectionInput = st.selectbox(names[0], index=None, options=list(idToNameDictionary.values()))
        countInput = st.number_input(names[1], min_value=1, step=1)
        startDateInput = st.date_input(names[2])
        endDateInput = st.date_input(names[3])
        subscriptionCost: st.text
        cost:float
        if namesSelectionInput and countInput:
            cost = round(countInput * db_interactions.get_edition_cost_from_index(
                db_interactions.find_key_by_value(idToNameDictionary, namesSelectionInput)), 3)
            subscriptionCost = st.text(f"Стоимость подписки : {cost}")
        else:
            subscriptionCost = st.text(names[4])
        shortFreqNames = dict(zip(frequencyNames.keys(), [str(name).split(', ')[0] for name in frequencyNames.values()]))
        frequencyInput = st.selectbox(names[5], options=shortFreqNames.values())
        deliveryTypeInput = st.selectbox(names[6], options=deliveryTypeName.values())
        deliveryTimeInput = st.date_input(names[7])
        subscriptionId = str(uuid.uuid4())
        values = [namesSelectionInput, countInput, startDateInput, endDateInput, subscriptionCost, frequencyInput,
                  deliveryTypeInput, deliveryTimeInput]
        addButton = st.button('Добавить подписку')
        if addButton:
            if all(values):
                db_interactions.insert_into(db.DBConnection.SUBSCRIPTIONS_TABLE,[subscriptionId, db_interactions.find_key_by_value(idToNameDictionary, namesSelectionInput), countInput, startDateInput, endDateInput, cost, db_interactions.find_key_by_value(shortFreqNames, frequencyInput), db_interactions.find_key_by_value(deliveryTypeName, deliveryTypeInput), deliveryTimeInput, True])
                st.write('Подписка создана')

    @staticmethod
    def lookup_all_frequences_of_release_page():
        PagesController.reset_states()
        st.set_page_config(page_title='Просмотр всех вариантов периодичности доставки', layout='wide')
        st.write('## Все варианты периодичности доставки')
        frequencies = db_interactions.get_all_values(db.DBConnection.FREQUENCY_OF_RELEASE_TABLE)
        columns = st.columns(2)
        with columns[0]:
            st.write('*Код варианта периодичности*')
        with columns[1]:
            st.write('*Название варианта периодичности*')
        for frequency in frequencies:
            with columns[0]:
                st.write(frequency[0])
            with columns[1]:
                name = str(frequency[1]).split(', ')
                st.write(name[0])

    @staticmethod
    def write_issued_editions_by_year_container(placeholder):
        getButton: st.button
        with placeholder.container():
            currentYear = datetime.date.today().year
            years = list(range(currentYear, currentYear - 10, -1))
            dateBox = st.selectbox(label='Выберите год для просмотра', options = years)
            getButton = st.button(label='Найти издания')
            if getButton:
                if dateBox:
                    PagesController.set_current_issued_by_year_edition_state('look')
                    st.session_state.find_editions_by_year = dateBox
                    placeholder.empty()
                    sleep(0.03)
                    PagesController.lookup_issued_editions_by_year_container(placeholder)

    @staticmethod
    def lookup_issued_editions_by_year_container(placeholder):
        with placeholder.container():
            received = db_interactions.get_editions_by_year(st.session_state.find_editions_by_year)
            columns = st.columns(5)
            with columns[0]:
                st.write("Название издания")
            with columns[1]:
                st.write("Тип издания")
            with columns[2]:
                st.write("Стоимость на период подписки")
            with columns[3]:
                st.write("Начало подписки")
            with columns[4]:
                st.write("Конец подписки")
            for edition in received:
                columns = st.columns(5)
                with columns[0]:
                    st.write(edition[0])
                with columns[1]:
                    st.write(edition[1])
                with columns[2]:
                    st.write(edition[2])
                with columns[3]:
                    st.write(edition[3])
                with columns[4]:
                    st.write(edition[4])

    @staticmethod
    def lookup_issued_by_year_editions_page():
        PagesController.init_states()
        st.set_page_config(layout='wide')
        placeholder = st.empty()
        if st.session_state.currentIssuedByYearEditionOptions == 'write':
            PagesController.write_issued_editions_by_year_container(placeholder)
        if st.session_state.currentIssuedByYearEditionOptions == 'look':
            PagesController.lookup_issued_editions_by_year_container(placeholder)

    @staticmethod
    def write_workers_received_editions_by_month_container(placeholder):
        addButton:st.button
        with placeholder.container():
            dateBox = st.date_input(label = 'Выберите месяц для просмотра')
            idToNameEditions = db_interactions.get_edition_index_to_name_dictionary()
            editionBox = st.selectbox(label = 'Выберите издание', options=idToNameEditions.values())
            addButton = st.button(label = 'Найти сотрудников')
            values = [dateBox, editionBox]
            if addButton:
                if all(values):
                    PagesController.set_current_worker_received_state('look')
                    st.session_state.find_received_editions_month = dateBox
                    st.session_state.find_received_editions_edition = db_interactions.find_key_by_value(idToNameEditions, editionBox)
                    placeholder.empty()
                    sleep(0.03)
                    PagesController.lookup_workers_received_editions_by_month_container(placeholder)



    @staticmethod
    def lookup_workers_received_editions_by_month_container(placeholder):
        with placeholder.container():
            received = db_interactions.get_worker_received_edition(st.session_state.find_received_editions_edition, st.session_state.find_received_editions_month)
            columns = st.columns(3)
            idToNames = db_interactions.get_worker_uuid_to_name_dict()
            with columns[0]:
                st.write("Дата получения")
            with columns[1]:
                st.write("Количество экземпляров")
            with columns[2]:
                st.write("ФИО работника")
            for edition in received:
                columns = st.columns(3)
                with columns[0]:
                    st.write(edition[0])
                with columns[1]:
                    st.write(edition[3])
                with columns[2]:
                    st.write(idToNames[edition[4]])


    @staticmethod
    def lookup_workers_received_editions_by_month_page():
        PagesController.init_states()
        st.set_page_config(layout = 'wide')
        placeholder = st.empty()
        if st.session_state.currentWorkerReceivedEditionsOptions == 'write':
            PagesController.write_workers_received_editions_by_month_container(placeholder)
        if st.session_state.currentWorkerReceivedEditionsOptions == 'look':
            PagesController.lookup_workers_received_editions_by_month_container(placeholder)



    @staticmethod
    def lookup_non_received_editions_before_2_months_page():
        pass

