import streamlit as st
import requests
import os
from django.core.wsgi import get_wsgi_application
from st_aggrid import AgGrid
from pymongo import MongoClient
import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'strategy_engine.settings')

application = get_wsgi_application()
from django.contrib.auth import authenticate

def check_password():

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        user = authenticate(
            username=st.session_state['username'],
            password=st.session_state['password']
        )

        if (user is not None):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]

        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password and a login button.


        st.text_input("Username", key="username")

        st.text_input("Password", type="password", key="password")

        st.button("Login", on_click=password_entered)
        return False

    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        return True

if check_password():
    jwt_tocken = requests.post("http://127.0.0.1:8000/gettocken/")

    print('tocken',jwt_tocken.json())

    client = MongoClient("mongodb://localhost:27017/")
    db = client["strategy_engine2"]
    strategy_collection = db["instance_strategy"]
    parameter_collection = db["instance_parameter"]
    instance_collection = db["instance_instance"]



    def get_strategy():
        response = requests.get("http://127.0.0.1:8000/get_strategy/")
        strategies = response.json()
        st.write("All strategies:")
        df = pd.DataFrame(strategies)
        AgGrid(df)

        # Create a list of dictionaries representing each strategy



    def strategy_form(jwt_token):
        st.title("Strategy Form")
        headers = {"Authorization": "Bearer " + jwt_token}
        parameter_response = requests.get("http://127.0.0.1:8000/get_parameter/", headers=headers)
        parameters = parameter_response.json()

        parameter_options = [{'id': parameter['id'], 'variable': parameter['variable']} for parameter in parameters]

        parameter = st.multiselect("Select Parameter", [parameter['variable'] for parameter in parameter_options])
        name = st.text_input('name')
        code = st.text_input('code')
        type = st.text_input('type')
        script = st.text_input('script')

        selected_parameter_ids = [p['id'] for p in parameter_options if p['variable'] in parameter]

        if st.button("Submit"):
            data = {'parameter':selected_parameter_ids,'name':name, 'code':code, 'type':type, 'script':script}
            headers = {"Authorization":"Bearer " + jwt_token}
            st.write(requests.post("http://127.0.0.1:8000/strategy/",data, headers = headers).json())

            st.success("Successfully submited")


    def get_strategy1(code):
        api_url = f"http://127.0.0.1:8000/strategy/{code}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None


    def update_strategy():
        response = requests.get(f"http://127.0.0.1:8000/get_strategy/")
        strategies = response.json()
        print(strategies)
        codes = []
        for strategy in strategies:
            code = strategy['code']
            codes.append(code)

        code = st.selectbox("Select Strategy", codes)
        if not code:
            st.warning("Invalid strategy code. Please enter a valid code.")
            st.stop()

        record = get_strategy1(code)
        if record:
            st.header("Update Parameters")
            exclude_fields = ["_id", "strategy_id", "add_time", "update_time"]
            new_data = {}
            for key in record.keys():
                if key not in exclude_fields:
                    new_value = None
                    if key == "parameter":
                        parameter_response = requests.get("http://127.0.0.1:8000/get_parameter/")
                        parameters = parameter_response.json()

                        parameter_options = [{'id': parameter['id'], 'variable': parameter['variable']} for parameter in
                                             parameters]

                        parameter = st.multiselect("Select Parameter",
                                                   [parameter['variable'] for parameter in parameter_options])

                        selected_parameter_ids = [p['id'] for p in parameter_options if p['variable'] in parameter]
                        new_value = selected_parameter_ids
                    else:
                        new_value = st.text_input(key, value=record[key])
                    new_data[key] = new_value

            name = new_data["name"]
            code = new_data["code"]
            type1 = new_data["type"]
            script = new_data["script"]
            parameter = new_data["parameter"]
            d = {"name": name, "code": code, "type1": type1, "script": script, "parameter": parameter}

            if st.button("Update"):
                # headers = {"Authorization": "Bearer " + jwt_token}
                response = requests.put(f"http://127.0.0.1:8000/strategy/{code}", d)

                if response.status_code == 201:
                    st.success("Successfully updated the strategy.")
                else:
                    st.error("Failed to update the strategy.")
        else:
            st.warning("Record not found.")


    def delete_strategy():

        response = requests.get(f"http://127.0.0.1:8000/get_strategy/")
        strategies = response.json()
        print(strategies)
        codes = []
        for strategy in strategies:
            code = strategy['code']
            codes.append(code)

        code = st.selectbox("Select Strategy", codes)

        if not code:
            st.warning("Invalid strategy Code. Please enter a valid Code.")
            st.stop()

        # Find the document in the instance_instance collection with the given ID
        record = get_strategy1(code)
        if record:
            if st.button("Delete"):
                response = requests.delete(f"http://127.0.0.1:8000/strategy/{code}")

                if response.status_code == 201:
                    st.success("Successfully Deleted the strategy.")
                else:
                    st.error("Failed to Delete the strategy.")
        else:
            st.error("No strategy found")




    def get_parameter():
        response = requests.get("http://127.0.0.1:8000/get_parameter/")
        parameters = response.json()

        # Display parameters in a table
        st.write("All Parameters:")
        df = pd.DataFrame(parameters)
        AgGrid(df)

        # Get record ID from user input



    def parameter_form(jwt_token):
        st.title("Parameter Form")

        name = st.text_input('name')
        description = st.text_input('description')
        variable = st.text_input('variable')

        if st.button("Submit"):
            data = {'name': name, 'description':description, 'variable':variable}
            headers = {"Authorization":"Bearer " + jwt_token}
            st.write(requests.post("http://127.0.0.1:8000/parameter",data, headers = headers).json())

            st.success("Successfully submited")

    def parameter_update(variable):
        api_url = f"http://127.0.0.1:8000/parameter/{variable}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def update_parameter():
        response = requests.get(f"http://127.0.0.1:8000/get_parameter/")
        strategies = response.json()
        codes = []
        for strategy in strategies:
            code = strategy['variable']
            codes.append(code)

        variable = st.selectbox("Select Strategy", codes)
        if not code:
            st.warning("Invalid Parameter Name. Please enter a valid Name.")
            st.stop()
            print('hiii3')

        # Find the document in the instance_instance collection with the given ID
        record = parameter_update(variable)
        if record:
            st.header("Update Parameters")
            exclude_fields = ["_id", "id", "parameter_id", "add_time", "update_time"]
            new_data = {}
            for key in record.keys():
                if key not in exclude_fields:
                    new_value = st.text_input(key, value=record[key])
                    new_data[key] = new_value

            # Update record when form is submitted
            name = new_data["name"]
            description = new_data["description"]
            variable = new_data["variable"]
            d = {"name": name, "description": description, "variable": variable}
            print(new_data)
            print(type(new_data))
            if st.button("Update"):
                response = requests.put(f"http://127.0.0.1:8000/parameter/{variable}", d)
                print(response)
                print(response.status_code)

                if response.status_code == 201:
                    st.success("Successfully updated the strategy.")
                else:
                    st.error("Failed to update the strategy.")
        else:
            st.warning("Record not found.")

    def delete_parameter():

        response = requests.get(f"http://127.0.0.1:8000/get_parameter/")
        strategies = response.json()
        codes = []
        for strategy in strategies:
            code = strategy['variable']
            codes.append(code)

        variable = st.selectbox("Select Strategy", codes)

        if not code:
            st.warning("Invalid record Name. Please enter a valid Name.")
            st.stop()

        # Find the document in the instance_instance collection with the given ID
        record = parameter_update(variable)
        if record:
            if st.button("Delete"):
                response = requests.delete(f"http://127.0.0.1:8000/parameter/{variable}")
                print(response.status_code)

                if response.status_code == 204:
                    st.success("Successfully Deleted the strategy.")
                else:
                    st.error("Failed to Delete the strategy.")
        else:
            st.error("No parameter found")


    def get_instance():
        response = requests.get("http://127.0.0.1:8000/get_instance/")
        instances = response.json()

        # Display the strategies in a table
        st.write("All Instances:")
        df = pd.DataFrame(instances)
        AgGrid(df, height=250)


    def instance_form(jwt_token):
        st.title("Instance Form")

        headers = {"Authorization": "Bearer " + jwt_token}
        strategies_response = requests.get("http://127.0.0.1:8000/get_strategy/", headers=headers)
        strategies = strategies_response.json()

        strategy_options = [strategy['code'] for strategy in strategies]
        DAYS_CHOICES = {
            'Monday': 0,
            'Tuesday': 1,
            'Wednesday': 2,
            'Thursday': 3,
            'Friday': 4
        }

        strategy_fk = st.selectbox("Select strategy", strategy_options)
        symbol = st.text_input('symbol')
        initialize_day = st.multiselect('Select days:', list(DAYS_CHOICES.keys()))
        initialize_time = st.time_input('initialize_time')
        terminate_time = st.time_input('terminate_time')
        initialize_day = [DAYS_CHOICES[day] for day in initialize_day]

        if st.button("Submit"):
            data = {
                'strategy_fk': strategy_fk,
                'symbol': symbol,
                'initialize_day': initialize_day,
                'initialize_time': initialize_time,
                'terminate_time': terminate_time
            }

            headers = {"Authorization": "Bearer " + jwt_token}
            st.write(requests.post("http://127.0.0.1:8000/instances/",data, headers = headers))
            st.success("submited")

    def instance_update(name):
        api_url = f"http://127.0.0.1:8000/instance/{name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def update_instance():
        response = requests.get(f"http://127.0.0.1:8000/get_instance/")
        strategies = response.json()
        #print(strategies)
        codes = []
        for strategy in strategies:
            code = strategy['name']
            codes.append(code)
            print(code)

        name = st.selectbox("Select Instance", codes)
        if  code:
            st.warning("Invalid Instance. Please enter a valid Instance.")
            st.stop()

        # Find the document in the instance_instance collection with the given ID
        record = instance_update(name)
        if record:
            # st.write("Record found:")
            # st.write(record)

            # Create form to update record
            st.header("Update Instance")
            exclude_fields = ["_id","id","parameter_id", "add_time", "update_time","name"]
            new_data = {}
            for key in record.keys():
                if key not in exclude_fields:
                    new_value = st.text_input(key, value=record[key])
                    new_data[key] = new_value

            # Update record when form is submitted
            strategy_fk_id = new_data["strategy_fk"]
            symbol = new_data["symbol"]
            initialize_day = new_data["initialize_day"]
            initialize_time = new_data["initialize_time"]
            terminate_time = new_data["terminate_time"]

            d = {"strategy_fk_id": strategy_fk_id, "symbol": symbol, "initialize_day": initialize_day,"initialize_time":initialize_time,"terminate_time":terminate_time}

            if st.button("Update"):
                response = requests.put(f"http://127.0.0.1:8000/instance/{name}", d)
                print(response)
                print(response.status_code)

                if response.status_code == 201:
                    st.success("Successfully updated the strategy.")
                else:
                    st.error("Failed to update the strategy.")
        else:
            st.warning("Record not found.")

    def delete_instance():
        response = requests.get(f"http://127.0.0.1:8000/get_instance/")
        strategies = response.json()
        # print(strategies)
        codes = []
        for strategy in strategies:
            code = strategy['name']
            codes.append(code)
            print(code)

        name = st.selectbox("Select Instance", codes)

        if not name:
            st.warning("Invalid record Name. Please enter a valid Name.")
            st.stop()

        # Find the document in the instance_instance collection with the given ID
        record = instance_update(name)
        if record:
            if st.button("Delete"):
                response = requests.delete(f"http://127.0.0.1:8000/instance/{name}")

                if response.status_code == 204:
                    st.success("Successfully Deleted the Instance.")
                else:
                    st.error("Failed to Delete the Instance.")
        else:
            st.error("No Instance found")

    def instance_parameter_update(name):
        api_url = f"http://127.0.0.1:8000/instance/{name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def Instance_Parameters():
        response = requests.get(f"http://127.0.0.1:8000/get_instance_parameter/")
        strategies = response.json()
        #print(strategies)
        codes = []
        for strategy in strategies:
            code = strategy['name']
            codes.append(code)

        code = st.selectbox("Select Strategy", codes)
        day_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}

        if not code:
            st.warning("Invalid Instance. Please enter a valid Instance.")
            st.stop()

        # Find the document in the instance_instance collection with the given ID
        record = instance_parameter_update(code)


        # If the record is found, retrieve all records with the same strategy_fk_id
        if record:
            strategy_fk = record["strategy_fk"]
            records = instance_collection.find({"strategy_fk_id": strategy_fk})

            # Display the records in a form for editing
            data = {}

            for record in records:
                exclude_fields = ["_id", "id", "symbol", "initialize_time", "terminate_time", "add_time", "update_time",
                                  "strategy_fk_id", "name"]
                keys = [key for key in record.keys() if key not in exclude_fields]

                with st.form(f"{strategy_fk}_{record['_id']}"):
                    for key in keys:
                        if key == "initialize_day":
                            days = record[key].split(",")
                            if len(days) == 1:
                                day_name = day_names[int(days[0])]
                                st.text(day_name)
                        else:
                            data[key] = st.text_input(key, record[key])

                    submit_button = st.form_submit_button("Save")

                if submit_button:
                    response = requests.put(f"http://127.0.0.1:8000/put_instance_parameter/{code}",data)

                    if response.status_code == 200:
                        st.success("Successfully updated the Instance Parameter.")
                    else:
                        st.error("Failed to update the Instance Parameter.")

        else:
            st.warning("Record not found.")


    def Strategy_type_form(jwt_token):
        st.title('Strategy Type')

        strategy_type = st.text_input('Strategy Type')

        if st.button("Submit"):
            data = {'strategy_type':strategy_type}
            headers = {"Authorization": "Bearer " + jwt_token}
            st.write(requests.post("http://127.0.0.1:8000/Strategy_type", data, headers=headers).json())

            st.success("Successfully submited")

    def Time_frame_form(jwt_token):
        st.title('Time Frame')

        Time_frame = st.text_input('Time Frame')

        if st.button("Submit"):
            data = {'time_frame':Time_frame}
            headers = {"Authorization": "Bearer " + jwt_token}
            st.write(requests.post("http://127.0.0.1:8000/Time_frame", data, headers=headers).json())

            st.success("Successfully submited")




    def main():
        st.set_page_config(page_title="Forms Example", page_icon=":form:", layout="wide")

        jwt_token = st.text_input("JWT Token", value="")

        st.sidebar.title("Forms")
        form_choice = st.sidebar.radio("Select Form", ["Strategy", "Parameter", "Instance","Strategy Type","Time Frame","Instance Parameter"])

        if form_choice == "Strategy":
            get_strategy()

            show_form = st.session_state.get("show_form", False)
            if not show_form:
                add_button = st.button("Add Strategy")
                if add_button:
                    show_form = True
                    st.session_state.show_form = True
            else:
                s = st.radio("options",["Add strategy","Update strategy","Delete strategy"])
                if s == "Add strategy":
                    strategy_form(jwt_token)
                elif s == "Update strategy":
                    update_strategy()
                elif s == "Delete strategy":
                    delete_strategy()

        elif form_choice == "Parameter":
            get_parameter()
            show_form = st.session_state.get("show_form",False)
            if not show_form:
                add_button = st.button("Add Parameter")
                if add_button:
                    show_form = True
                    st.session_state.show_form = True
            else:
                p = st.radio("option", ["Add parameter", "Update parameter","Delete parameter"])
                if p == "Add parameter":
                    parameter_form(jwt_token)
                elif p == "Update parameter":
                    update_parameter()
                elif p == "Delete parameter":
                    delete_parameter()
        elif form_choice == "Instance":
            get_instance()
            show_form = st.session_state.get("show_form",False)
            if not show_form:
                add_button = st.button("Add Instance")
                if add_button:
                    show_form = True
                    st.session_state.show_form = True
            else:
                I = st.radio("options",["Add Instance","Update Instance","Delete Instance"])
                if I == "Add Instance":
                    instance_form(jwt_token)
                elif I == "Update Instance":
                    update_instance()
                elif I == "Delete Instance":
                    delete_instance()
        elif form_choice == "Strategy Type":
            Strategy_type_form(jwt_token)
        elif form_choice == "Time Frame":
            Time_frame_form(jwt_token)
        elif form_choice == "Instance Parameter":
            Instance_Parameters()

    if __name__ == "__main__":
        main()
