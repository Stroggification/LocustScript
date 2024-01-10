from locust import HttpUser, task, between

from locust import HttpUser, task, between

class ExpenseUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):

        auth_url = "http://revisedlb2-1862277086.us-east-1.elb.amazonaws.com/login"
        auth_payload = {
            "email": "test@demo.com",
            "password": "test"
        }

        # Sending a request to the authentication endpoint
        with self.client.post(auth_url, json=auth_payload, catch_response=True) as response:
            if response.status_code == 200:
                # Extracting the bearer token and setting it for all subsequent requests
                self.token = "Bearer " + response.json()['token']
                self.client.headers.update({"Authorization": self.token})
            else:
                # Handling failed authentication
                response.failure("Failed to authenticate")


    @task    # FRONTEND REQUEST
    def get_FrontEnd(self):
        self.client.get(":8080", headers={"Authorization": self.token})

    @task    # GET EXPENSES
    def get_expenses(self):
        self.client.get("/expenses", headers={"Authorization": self.token})

    @task  # GET EXPENSES BY YEAR
    def get_expense_categories_by_year(self):
        self.client.get("/expenses/getbyyear/2022", headers={"Authorization": self.token})

    @task #GET EXPENSE CATEGORIES BY ID
    def get_expense_categories_by_id(self):
        self.client.get("/expensecategories/1",  headers={"Authorization": self.token})

    @task #GET EXPENSE TYPES
    def get_expense_types(self):
        self.client.get("/expensetypes", headers={"Authorization": self.token})

    @task #GET EXPENSE TYPES BY ID
    def get_expense_types_by_id(self):
        self.client.get("/expensetypes/2", headers={"Authorization": self.token})

    @task #GET CURRENT YEAR CATEGORIES BREAKDOWN
    def get_current_year_categories_breakdown(self):
        self.client.get("/statistics/getcurrentyearcategoriesbreakdown", headers={"Authorization": self.token})

    @task  # GET CURRENT YEAR EXPENSES BY CATEGORIES BREAKDOWN
    def get_current_year_expenses_by_categories_breakdown(self):
        self.client.get("/statistics/getcurrentyearexpensesbycategorybreakdown", headers={"Authorization": self.token})

    @task  # GET CATEGORIES BREAKDOWN FOR YEAR
    def get_categories_breakdown_for_year(self):
        self.client.get("/statistics/getcategoriesbreakdownforyear/2021/3", headers={"Authorization": self.token})

    @task  # GET TYPES BREAKDOWN FOR YEAR
    def get_types_breakdown_for_year(self):
        self.client.get("/statistics/getcategoriesbreakdownforyear/2022/6", headers={"Authorization": self.token})

    @task  # CREATE EXPENSES
    def create_expense(self):
        payload = {
            "id": 200,
            "date": "03.03.2023",
            "category": "string",
            "categoryId": 1,
            "categoryBudget": 1,
            "categoryColour": "string",
            "type": "string",
            "typeId": 1,
            "value": 1,
            "comments": "string",
            "month": 3
        }
        headers = {"Authorization": self.token}
        self.client.post("/expenses", json=payload, headers=headers)
