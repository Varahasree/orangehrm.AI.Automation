from faker import Faker


fake = Faker()


def generate_employee_data():

    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
    }