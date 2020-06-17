import pandas as pd
import string
import tbapy
import os

tba = tbapy.TBA(os.getenv('TBA_KEY'))

valid_teams = {}
invalid_teams = []


def get_team_num(in_str):
    try:
        for c in in_str:
            if c not in string.digits:
                in_str = in_str.replace(c, ' ')
        return int(in_str.strip().split()[0])
    except IndexError:
        return -1


# Check if provided number is a valid FRC team
# Stores valid and invalid teams as identified to reduce requests
# If location data can't be fetched treat team as invalid (eg 420)
# returns status and location string for teams
def is_frc_team(in_num):
    if in_num in valid_teams:
        return [True, valid_teams[in_num]]
    elif in_num in invalid_teams:
        return [False, '']
    else:
        try:
            tm = tba.team(in_num)
            if tm['city'] is not None and tm['state_prov'] is not None and 2020 in tba.team_years(in_num):
                loc = tm['city'] + ', ' + tm['state_prov']
                valid_teams[in_num] = loc
                return [True, loc]
            else:
                invalid_teams.append(in_num)
                return [False, '']
        except tbapy.TBAErrorList:
            invalid_teams.append(in_num)
            return [False, '']
        except TypeError:
            print(in_num)


user_data = pd.read_csv('chsUsers.txt', sep='\n',  header=None, names=['raw'])
user_data['nums'] = user_data['raw'].apply(get_team_num)
user_data['tmp'] = user_data['nums'].apply(is_frc_team)
user_data[['valid_team', 'loc']] = pd.DataFrame(user_data['tmp'].tolist(), index=user_data.index)
user_data[user_data['valid_team']][['nums', 'loc']].to_csv('chs_team_info.csv', index=False, header=['Team', 'Location'])
