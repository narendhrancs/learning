
# 60 hours of work can result in 20% drop in productivity
import scipy.optimize

def test(hours_worked, hourly_pay=12, constant=1):
    productivity = constant (1-((hours_worked-40) * 0.01))
    productivity_per_employee = productivity*hours_worked
    cost = hours_worked * hourly_pay
    return productivity_per_employee, cost


