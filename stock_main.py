#%%
from stock_ui import *
from stock_quiz import *
from stock_quiz_body import StockQuizBody
# from kernel import *
#%%
# get all questions
all_q = ["Age",
         "Experience on investment?",
         "Which description best suits your investment knowledge?",
         "Annual amount to invest (million yen)",
         "When do you expect the upcoming largest expenditures (retirement, children's education ...) that will use your investment to happen?",
         "The amount of emergency reserve? (times monthly income)",
         "The acceptable range of net value change? (+-%)",
         "Assume you lost 10% of your 4 million yen investment within one year, what will you do?",
         "What's the most commonly used instrument except for the fund.",
         "Main source of investment funds."]

all_a = [["70+", "60~69", "50~59", "20~29", "30~49"],
        ["None", "less than 2 years", "2~5 years", "5~10 years", "10 years+"],
        ["Not familiar, my friends recommend, I buy.", "Less familiar, will invest even I'm not clear about it.",
         "Having basic knowledge on serveral instruments, will think twice before invest.",
         "Familiar with lots of different instruments, never invest until I get the whole picture.",
         "I'm an expert or professional investment advisor, I have my own strats."],
        ["2-", "2 ~ 4", "4 ~ 12", "12 ~ 40", "40+"],
        ["In 1 year", "1 ~ 2 years", "2 ~ 5 years", "5 ~ 10 years", "10+ years"],
        ["None", "3-", "3~6", "6~12", "12+"],
        ["5", "15", "25", "35", "45"],
        ["Sacrifice sale, take the rest back", "Sale a part of it and reinvest to other low risk targets",
        "Doing nothing, just wait and see", "Consider add to a losing position", "Continously add to a losing position"],
        ["Cash deposit", "Foreign currency deposit", "Real estate", "Stock", "Warrants/other"],
        ["Pension", "Salary", "Rent/Business income", "Investment income", "Heritage"]]

question_pairs = []
for q, o in zip(all_q, all_a):
    question_pairs.append(StockQuizBody(q, o))
#%%
question_pairs = question_pairs[:1]

s_quiz = StockQuiz(question_pairs)
s_ui = stockUI(stock_quiz = s_quiz)
# %%
