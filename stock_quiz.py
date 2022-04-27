class StockQuiz:
    
    def __init__(self, questions):
        self.quiz_done = 0
        self.score = 0
        self.questions = questions
    
    def check_left(self):
        return self.quiz_done < len(self.questions)

    def next_question(self):
        """Get the next question by incrementing the question number"""
        
        self.current_question = self.questions[self.quiz_done]
        self.quiz_done += 1
        q_text = self.current_question.question_text
        return f"Q.{self.quiz_done}: {q_text}"
    
    def cumulate_score(self, score):
        self.score += score

    def get_score(self):
        return self.score