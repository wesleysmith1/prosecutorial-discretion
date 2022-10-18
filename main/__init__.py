from otree.api import *

import numpy as np
import random

import config

doc = """"""


class Constants(BaseConstants):
    name_in_url = 'main'
    players_per_group = 2
    num_rounds = 40
    # instructions_template = 'main/instructions.html'
    # Initial amount allocated to the dictator

    header_template = 'main/Header.html'

    i = 'I'
    l = 'L'

    showup_fee = cu(7)

    # treatment variables
    # todo: change the variable descriptions. these are a litle mixed
    v =  cu(config.config[0]) # fixed total that is earned with L box (legal)
    s = cu(config.config[1]) # what defendant pays prosecutor if found guilty at trial
    c = cu(config.config[2]) # trial cost for both defendant and Offeror 

    # charged probability
    g_i = config.config[3] # prob of getting charged if the individual does not commit the crime
    g_g = config.config[4] # prob of getting charged if individual commits crime 

    # conviction probability
    q_i = config.config[5] # innocent defendant probability of conviction
    q_g = config.config[6] # guilty defendant probability of being conviction

    w_upperbar = cu(config.config[7]) # max opportunity cost for defendant inclusive
    b_lowerbar = cu(config.config[8]) # the lowest offer that a offeror can offer under this inclusive restriction.

    b_upperbar = cu(5) # todo this needs to be taken from the 


class Subsession(BaseSubsession):
    # treatment variables
    v =  models.FloatField(initial=cu(config.config[0])) # fixed total that is earned with L box (legal)
    s = models.CurrencyField(initial=cu(config.config[1])) # what defendant pays prosecutor if found guilty at trial
    c = models.CurrencyField(initial=cu(config.config[2])) # trial cost for both defendant and Offeror 

    # arrested probability
    g_i = models.FloatField(initial=config.config[3]) # prob of getting arrested if the individual does not commit the crime
    g_g = models.FloatField(initial=config.config[4]) # prob of getting arrsted if individual commits crime 

    # conviction probability
    q_i = models.FloatField(initial=config.config[5]) # innocent defendant probability of conviction
    q_g = models.FloatField(initial=config.config[6]) # guilty defendant probability of being conviction

    w_upperbar = models.CurrencyField(initial=cu(config.config[7])) # max opportunity cost for defendant inclusive
    b_lowerbar = models.CurrencyField(initial=cu(config.config[8]))
    b_upperbar = models.CurrencyField(initial=Constants.b_upperbar)
    # ===============================================


class Group(BaseGroup):
    l_box_selected = models.BooleanField() # selects 'L' box
    r_box_amount = models.CurrencyField() # opportunity cost
    charged = models.BooleanField() # if charged offer phase begins
    offer = models.CurrencyField(label=f'Please choose an offer greater than or equal to {Constants.b_lowerbar} and less than or equal to {Constants.b_upperbar}.')
    offer_accepted = models.BooleanField(initial=None, label="Do you accept?")
    prosecuted = models.BooleanField()

# error functions
def offer_error_message(player, value):
    if value < Constants.b_lowerbar or value > Constants.b_upperbar:
        return f'The offer must be greater than or equal to {Constants.b_lowerbar} and less than or equal to {Constants.b_upperbar}.'
    else:
        return None


class Player(BasePlayer):
    resolution_cost = models.CurrencyField(initial=0) # resolution fee and resolution cost

##################################################################################################

# FUNCTIONS
def is_defendant(player: Player):
    return player.id_in_group == 1

def box_amount(player: Player):
    if player.group.l_box_selected:
        return Constants.v
    else:
        return player.group.r_box_amount

def final_phase(group: Group):
    phase = "choosing"

    if group.field_maybe_none('offer_accepted'):
        phase = "resolution"
    elif group.charged == True:
        phase = "offer"

    return phase

def chooser_earnings(group: Group):
    return group.get_player_by_id(1).payoff

def offeror_earnings(group: Group):
    return group.get_player_by_id(2).payoff

def offer_payment(group: Group):
    """Subtrack offer from defendant, transfer to Offeror"""

    # todo: make sure this is how to identify defendant and Offeror
    chooser = group.get_player_by_id(1)
    offeror = group.get_player_by_id(2)

    chooser.payoff -= group.offer

    offeror.payoff += group.offer

def trial_fee(group: Group):
    """Offeror and defendant pay trial fee"""
    defendant = group.get_player_by_id(1)
    offeror = group.get_player_by_id(2)

    defendant.payoff -= Constants.c
    defendant.resolution_cost -= Constants.c

    offeror.payoff -= Constants.c
    offeror.resolution_cost -= Constants.c

def trial_payment(group: Group): 
    """called when chooser is prosecuted"""
    defendant = group.get_player_by_id(1)
    offeror = group.get_player_by_id(2)

    defendant.payoff -= Constants.s
    defendant.resolution_cost -= Constants.s

    offeror.payoff += Constants.s
    offeror.resolution_cost += Constants.s


def creating_session(subsession):
    # generate I box money 
    for player in subsession.get_players():

        # initialize player initial endowment
        # player.payoff = Constants.initial_endowment

        player.participant.payment_period = random.randint(1,Constants.num_rounds)

        player.participant.showup_fee = Constants.showup_fee

        if is_defendant(player):
            # generate amount in 'L' box
            player.group.r_box_amount = random.randint(0, Constants.w_upperbar * 100) / 100

            # initial resolution cost is 0
            player.resolution_cost = 0
            

##################################################################################################            

# PAGES
class RoundSync(WaitPage):
    pass

class ChoosingPhase(Page):
    ''' There is an individual who has the opportunity to commit a crime or engage in a pro-ductive activity. '''

    form_model = 'group'
    form_fields = ['l_box_selected']

    @staticmethod
    def is_displayed(player: Player):
        return is_defendant(player)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(r_box_amount=player.group.r_box_amount, phase="Choosing Phase")

    @staticmethod
    def before_next_page(player, timeout_happened):
        if is_defendant(player):

            # L box is illegal w/fixed amount
            if player.group.l_box_selected:
                # 'L' box selected
                player.payoff += Constants.v
                prob_charged = Constants.g_g

            else:
                # opportunity cost of choosing L box has restricted random amount
                player.payoff += player.group.r_box_amount
                prob_charged = Constants.g_i
            
            #calculate if defendent gets charged
            player.group.charged = np.random.binomial(1, prob_charged)


class ChoiceWait(WaitPage):
    pass


class OfferorPhase(Page):
    form_model = 'group'
    form_fields = ['offer']

    @staticmethod
    def is_displayed(player: Player):
        return not is_defendant(player) and player.group.charged

    @staticmethod
    def vars_for_template(player: Player):
        return dict(phase="Offer Phase")


class OfferWait(WaitPage):
    pass


class OfferPhase2(Page):
    form_model = 'group'
    form_fields = ['offer_accepted']

    @staticmethod
    def is_displayed(player: Player):
        return is_defendant(player) and player.group.charged

    @staticmethod
    def vars_for_template(player: Player):
        return dict(phase="Offer Phase")

    @staticmethod
    def before_next_page(player, timeout_happened):
        if is_defendant(player):

            if player.group.offer_accepted:
                offer_payment(player.group)
            else:
                # trial occurs when offer is not accepted

                # both players pay 1 dollar
                trial_fee(player.group)

                # determine probability of prosecution
                prob_prosecuted = Constants.q_i
                if player.group.l_box_selected:
                    prob_prosecuted = Constants.q_g
                
                #calculate 
                player.group.prosecuted = np.random.binomial(1, prob_prosecuted)

                if player.group.prosecuted:
                    trial_payment(player.group)


class ResultsWait(WaitPage):
    pass


class Results(Page):
    
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            box_selected='L' if player.group.l_box_selected else 'R',
            box_amount=box_amount(player),
            is_chooser=is_defendant(player),
            chooser_earnings=chooser_earnings(player.group),
            offeror_earnings=offeror_earnings(player.group),
            final_stage=final_phase(player.group),
            phase="<b>Results</b>",
            trial_fee=Constants.c,
            trial_charge=Constants.s,
            offeror_prosecuted_total_trial=Constants.s - Constants.c,
            chooser_prosecuted_total_trial=-Constants.s - Constants.c
            )

    @staticmethod
    def before_next_page(player, timeout_happened):

        if player.participant.payment_period == player.round_number:
            player.participant.selected_payment = player.payoff


page_sequence = [RoundSync, ChoosingPhase, ChoiceWait, OfferorPhase, OfferWait, OfferPhase2, ResultsWait, Results]
