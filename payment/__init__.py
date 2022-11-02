from otree.api import *
import random


class Constants(BaseConstants):
    name_in_url = 'payment'
    players_per_group = None
    num_rounds = 1

    # this gets added to the payment from the selected round
    initial_endowment = cu(5)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payment_period = models.IntegerField()
    selected_payment = models.CurrencyField()
    showup_fee = models.CurrencyField()
    comprehension_payment = models.CurrencyField()
    total_payoff = models.CurrencyField()
    full_name = models.StringField(label="Please enter your full name")


# FUNCTIONS
def creating_session(subsession):
    pass


# PAGES
class Payment(Page):
    form_model = 'player'
    form_fields = ['full_name']

    @staticmethod
    def vars_for_template(player: Player):

        try:
            player.showup_fee = player.participant.showup_fee

            player.comprehension_payment = player.participant.comprehension_payment

            player.payment_period = player.participant.payment_period
            player.selected_payment = player.participant.selected_payment  + Constants.initial_endowment
        except:
            player.showup_fee = 0

            player.comprehension_payment = 0

            player.payment_period = 0
            player.selected_payment = 0 + Constants.initial_endowment

        player.total_payoff = player.showup_fee + player.comprehension_payment + player.selected_payment

        return dict()
        

class FinalInstructions(Page):
    pass

page_sequence = [Payment, FinalInstructions]
