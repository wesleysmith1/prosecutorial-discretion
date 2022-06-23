from otree.api import *




doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1

    quiz_answers = [4, True, True, 3, 2,]
    question_earnings = cu(.5) # todo: this should be deleted


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_requests = models.CurrencyField()


class Player(BasePlayer):
    q1 = models.IntegerField(
            label="Which of the following statements is correct?",
            widget=widgets.RadioSelect,
            choices=[
                [1, "The L box contains $10.00 and the R box has a random amount of money (between $0.00 and $5.00)."],
                [2, "The L box contains $10.00 and the R box has a random amount of money (between $5.00 and $10.00)."],
                [3, "The L box contains $5.00 and the R box has a random amount of money (between $5.00 and $10.00)."],
                [4, "The L box contains $5.00 and the R box has a random amount of money (between $0.00 and $10.00)."],
            ]
        )
    q2 = models.BooleanField(
            label=f"True or False: A Chooser who chooses the L box has a 50% chance of the period continuing to the offer phase, while a chooser who chooses the R box has a 25% chance of the period continuing to the offer phase.",
            choices=[[True, "True"], [False, "False"]]# answer: True
        )
    q3 = models.BooleanField(
            label=f"True or False: A Chooser who chooses the L box has a 50% chance of losing an additional $4.00 in the resolution phase, while a chooser who chooses the R box has a 25% chance of losing an additional $4.00 in the resolution phase.",
            choices=[[True, "True"], [False, "False"]]# answer: True
        )
    q4 = models.IntegerField(
            label="Which of the following statements is correct?",
            widget=widgets.RadioSelect,
            choices=[
                [1, "If a Chooser accepts an offer, the Offeror gains no money and the Chooser loses this money."],
                [2, "If a Chooser accepts an offer, the Offeror gains this money and the Chooser loses no money."],
                [3, "If a Chooser accepts an offer, the Offeror gains this money and the Chooser loses this money."], # correct
                [4, "If a Chooser accepts an offer, the Offeror gains no money and the Chooser loses no money."],
            ]
        )
    q5 = models.IntegerField(
            label="Which of the following statements is correct?",
            widget=widgets.RadioSelect,
            choices=[
                [1, "Both the Chooser and the Offeror will be told the amount of money in the R box."],
                [2, "Only the Chooser will be told the amount of money in the R box."], # correct
                [3, "Only the Offeror will be told the amount of money in the R box."],
                [4, "Neither the Chooser nor the Offeror will be told the amount of money in the R box."],
            ]
        )


# FUNCTIONS
def set_payoffs(group: Group):

    # todo: check if the answers are correct and pay players accordingly

    players = group.get_players()

    for p in players:
        if p.q1 == Constants.quiz_answers[0]:
            p.payoff += Constants.question_earnings

        if p.q2 == Constants.quiz_answers[1]:
            p.payoff += Constants.question_earnings

        if p.q3 == Constants.quiz_answers[2]:
            p.payoff += Constants.question_earnings

        if p.q4 == Constants.quiz_answers[3]:
            p.payoff += Constants.question_earnings

        if p.q5 == Constants.quiz_answers[4]:
            p.payoff += Constants.question_earnings
        
        p.participant.comprehension_payment = p.payoff
    

# PAGES
class Instructions1(Page):
    pass

class Instructions2(Page):
    pass

class Instructions3(Page):
    pass

class Instructions4(Page):
    pass

class Instructions5(Page):
    pass

class Instructions6(Page):
    pass


class Quiz1(Page):
    form_model = 'player'
    form_fields = ['q1']


class Quiz1Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        correct = player.q1 == Constants.quiz_answers[0]
        solution = "The L box contains $5.00 and the R box has a random amount of money (between $0.00 and $10.00)."
        return dict(correct=correct, solution=solution)


class Quiz2(Page):
    form_model = 'player'
    form_fields = ['q2']


class Quiz2Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        correct = player.q2 == Constants.quiz_answers[1]
        solution = "True"
        return dict(correct=correct, solution=solution)


class Quiz3(Page):
    form_model = 'player'
    form_fields = ['q3']


class Quiz3Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        correct = player.q3 == Constants.quiz_answers[2]
        solution = "True"
        return dict(correct=correct, solution=solution)


class Quiz4(Page):
    form_model = 'player'
    form_fields = ['q4']


class Quiz4Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        correct = player.q4 == Constants.quiz_answers[3]
        solution = "If a Chooser accepts an offer, the Offeror gains this money and the Chooser loses this money."
        return dict(correct=correct, solution=solution)


class Quiz5(Page):
    form_model = 'player'
    form_fields = ['q5']


class Quiz5Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        correct = player.q5 == Constants.quiz_answers[4]
        solution = "Only the Chooser will be told the amount of money in the R box."
        return dict(correct=correct, solution=solution)


class QuizWait(WaitPage):
    after_all_players_arrive = set_payoffs

page_sequence = [
    Instructions1, 
    Instructions2, 
    Instructions3, 
    Instructions4, 
    Instructions5, 
    Instructions6, 
    Quiz1,
    Quiz1Feedback, 
    Quiz2,
    Quiz2Feedback, 
    Quiz3,
    Quiz3Feedback, 
    Quiz4,
    Quiz4Feedback, 
    Quiz5,
    Quiz5Feedback, 
    QuizWait, 
    ]
