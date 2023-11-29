"""
3. Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів.
"""


class InstancesCounter:
    instances_count = 0

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        cls.instances_count += 1
        return instance

    @classmethod
    def get_instances_count(cls):
        return cls.instances_count

inst_1 = InstancesCounter()
print(inst_1.get_instances_count())

inst_2 = InstancesCounter()
print(inst_2.get_instances_count())

inst_3 = InstancesCounter()
print(inst_3.get_instances_count())