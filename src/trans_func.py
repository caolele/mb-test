from datetime import datetime, date
preAB = {'product_crowdfunding', 'initial_coin_offering', 'seed', 'angel', 'grant', 
         'pre_seed', 'convertible_note', 'equity_crowdfunding', 'non_equity_assistance'}
postAB = {'post_ipo_debt', 'secondary_market', 'series_f', 'series_g', 'series_h', 
          'post_ipo_secondary', 'series_j', 'series_i', 'series_c', 'series_d', 
          'series_e', 'private_equity', 'post_ipo_equity'}
AB = {'series_a', 'series_b'}
non_specific = {'debt_financing', 'corporate_round'}

# preprocess investment_type into simpler case-specific feature to the following
# PreAB (1 0 0): investment before A/B series
# PostAB (0 1 0): investment after A/B series
# AB (0 0 1): A/B series investment
# non-specific (1 1 1): can happen at any stage
# series_unknown (0 1 1)
# undisclosed (0 0 0)
def process_investment_type(x):
    # x = x.strip().lower()
    if x in preAB:
        return [1, 0, 0]
    if x in postAB:
        return [0, 1, 0]
    if x in AB:
        return [0, 0, 1]
    if x in non_specific:
        return [1, 1, 1]
    if x == 'series_unknown':
        return [0, 1, 1]
    if x == 'undisclosed':
        return [0, 0, 0]
    raise ValueError('Investment type {} not recognized!'.format(x))


def process_founded(x):
    dtobj = datetime.strptime(x, '%Y-%m-%d')
    lapse = (datetime(2018,10,7,0,0,0) - dtobj).days / 7 # days granularity's probably too much for discovery
    return lapse

# [0, 0] unknown, [1, 0] has AB series, [0, 1] not yet
def get_has_series_ab(x):
    result = [0, 1]
    if type(x) is not list:
        return result
    else:
        for entry in x:
            if entry == [0, 1, 0] or entry == [0, 0, 1]:
                return [1, 0]
            if entry == [0, 0, 0] or entry == [0, 1, 1]:
                result = [0, 0]
    return result