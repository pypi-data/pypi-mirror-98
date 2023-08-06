import asyncio
import aiohttp
import pandas
from concurrent.futures import ThreadPoolExecutor
from fpl import FPL
from fpl.constants import API_URLS
from fpl.utils import fetch, logged_in

class FPLTransfers():
    '''
    '''
    
    def __init__(self, email=None, password=None):
        '''
        Placeholder - the email and password will be sent to an authentication function in the future
        once it is enabled.
        '''
        self._email = email
        self._password = password
        
        self._aio_pool = ThreadPoolExecutor(1)
        self._aio_loop = asyncio.new_event_loop()
        self._aio_pool.submit(asyncio.set_event_loop, self._aio_loop).result()
                    
    async def _call_api_async(self, func, login=False):
        """ Calls the given FPL API function asynchronously.
        Args:
            func: The API function to execute.
            requires_login: Whether the call requires authentication.
        Returns:
            The Future of the passed function.
        """

        if login and self._email is None:
            raise ValueError('Email is not provided, the functionality which has been called requires an email')
        elif login and self._password is None:
            raise ValueError('Password is not provided, the functionality which has been called requires a password')
        
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session) #if self.__fpl is None else self.__fpl

            if login:
                await fpl.login(self._email, self._password)

            return await func(fpl)
            
    def _call_api(self, func, login=False):
        """ Calls the given FPL API function synchronously.
        Args:
            func: The API function to execute.
        Returns:
            The result of the passed function.
        """
        return self._aio_pool.submit(self._aio_loop.run_until_complete, self._call_api_async(func, login)).result()
    
    def _get_team_dict(self, team_data):
        '''
        '''
        team_dict = {}
        for i, val in enumerate(team_data.iterrows()):
            team_dict[team_data.loc[i+1, 'code']] = team_data.loc[i+1, 'name']
        return team_dict 
    
    def _ensure_costs_work(self, money_left, it):
        '''
        Returns
        -------
        result:  boolean
            Returns True if the difference between actual money spent and total average money spent is
            less than the tolerance defined by the exponential decay equation which reaches approximately
            0 at x=15.
        '''
        def func(x):
            return -1.35 * (0.8 ** ((1/15) + x)) + 1.05
        tol = func(it)
        mean_money_left = 100 - ((100 / 15) * it)
        if it == 13:
            mean_money_left = 10
        if it == 14:
            mean_money_left = 4.5
        elif it == 15:
            mean_money_left = 0.1
        #print(money_left, mean_money_left, (mean_money_left/money_left), (1 - tol) + 1)
        result = 0 < mean_money_left / money_left < (1 - tol) + 1
        return result
    
    def normalise(self, df=None):
        '''
        '''
        max_vals = df.max()
        df[['points', 'dreamteam', 'bps', 'form', 'ppg', 'av_difficulty']] = \
        df[['points', 'dreamteam', 'bps', 'form', 'ppg', 'av_difficulty']] / \
        max_vals[['points', 'dreamteam', 'bps', 'form', 'ppg', 'av_difficulty']]
        
        for i, val in enumerate(df.iterrows()):
            overall = (df.loc[val[0], 'points'] * 0.2) + (df.loc[val[0], 'form'] * 0.3) + \
            (df.loc[val[0], 'ppg'] * 0.15) + (df.loc[val[0], 'dreamteam'] * 0.1) + \
            (df.loc[val[0], 'bps'] * 0.1) + (df.loc[val[0], 'av_difficulty'] * 0.15)
              
            df.loc[val[0], 'overall'] = overall
        return df
    
    def _get_players(self, no_weeks):
        '''
        '''
        json_data = self._call_api(lambda fpl: fpl.get_players(include_summary=True, return_json=True))
        teams_data = self._call_api(lambda fpl: fpl.get_teams(return_json=True))
        # Creates pandas dataframe from player attributes and cuts to only include required columns
        data = pandas.DataFrame.from_records(json_data, index=['id'])
        data = data[['first_name', 'second_name', 'element_type', 'team_code', 
                                   'total_points', 'form', 'points_per_game', 'dreamteam_count',
                                   'now_cost', 'chance_of_playing_next_round', 'bps', 
                                   'selected_by_percent']]
        
        self.original_attributes = list(data.columns)
        new_cols = ['first_name', 'second_name', 'pos', 'team', 'points', 'form', 'ppg', 'dreamteam',
                    'cost', 'chance', 'bps', '%']
        data.columns = new_cols
        
        # Get all the future fixtures for players and sorts by player and "event"
        fixtures_df = pandas.DataFrame()
        for player in json_data:
            player_df = pandas.DataFrame.from_records(player['fixtures'])
            player_df['player_id'] = player['id']
            fixtures_df = pandas.concat([fixtures_df, player_df], sort=False)
        fixtures_df = fixtures_df.set_index(['player_id', 'event'])

        # Creates teams pandas dataframe and finds the conversion for team IDs and their names
        teams = pandas.DataFrame.from_records(teams_data, index=['id'])
        team_dict = self._get_team_dict(teams)
        
        # Changes team code to team name and puts in average difficulty for the next selected number of weeks
        cur_week = fixtures_df.loc[1].index[0]
        for i, val in enumerate(data.iterrows()):
            data.loc[val[0], 'team'] = team_dict[data.loc[val[0], 'team']]
            # Is there a better way to do this nested try except bracket?
            try:
                fixtures = fixtures_df.loc[val[0]][cur_week:cur_week+no_weeks]['difficulty']
            except KeyError:
                try:
                    fixtures = fixtures_df.loc[val[0]][cur_week:cur_week+no_weeks-1]['difficulty']
                except KeyError:
                    try:
                        fixtures = fixtures_df.loc[val[0]][cur_week+1:cur_week+no_weeks]['difficulty']
                    except KeyError:
                        av_difficulty = 0
            av_difficulty = 5 - (sum(fixtures) / (len(fixtures)))
            data.loc[val[0], 'av_difficulty'] = av_difficulty

        # This implementation is ugly and hard coded. Find a way to improve it if you can
        data[['pos']] = data[['pos']].astype(str)
        data[['points', 'dreamteam']] = data[['points', 'dreamteam']].astype(int)
        data[['form', 'ppg', 'cost', 'bps', '%']] = data[['form', 'ppg', 'cost', 
                                                                        'bps', '%']].astype(float)
        data['chance'] = data['chance'].fillna(100)
        data[['cost']] = data[['cost']] / 10
        self.data = data
        
    def _get_user_team(self):
        '''
        '''
        async def get_user_team_async(self, fpl=FPL, user_id=None):
            response = await fetch(
                    self.session, API_URLS["user_team"].format(user_id))
            return response
        
        json_data = self._call_api(lambda fpl: fpl.get_user(return_json=True), login=True)
        self._user_id = json_data['id']
        self._bank = json_data['last_deadline_bank'] / 10

        team = self._call_api(lambda fpl: get_user_team_async(fpl, user_id=self._user_id), login=True)
        current_team = pandas.DataFrame.from_records(team['picks'], index=['element'])
        return current_team
    
    def _transfer_finder(self, cur_team, all_players):
        '''
        '''
        idx = cur_team.index
        pos = ['1', '2', '3', '4']
        full_set = []
        for i in pos:
            pos_team = cur_team.loc[cur_team['pos'] == i]
            player = pos_team.iloc[-1]
            for j, val in all_players.loc[all_players['pos'] == i].iterrows():
                if j not in idx and val.cost < (player.cost + self._bank) and player.overall < val.overall and val.chance > 51:
                        temp = {'existing player': player.first_name + ' ' + player.second_name,
                                'new player': val.first_name + ' ' + val.second_name,
                                'diff': val.overall - player.overall,
                                'ex_pl_id': player.name,
                                'n_pl_id': j}
                        full_set.append(temp)
                        break
        return full_set
        
    
    def single_transfer(self, no_weeks=5):
        '''
        Finds the best transfer to do based on the following methodology:
            - Finds the lowest ranked player by position (based on "overall" metric)
            - Finds the player with the highest "overall" rank in that position that is within cost
            - Finds the difference in "overall" rank between existing player and new player
            - Recommends the transfer with the highest difference
        '''
        user_team = self._get_user_team()
        self._get_players(no_weeks=no_weeks)
        data = self.normalise(df=self.data)
        
        cur_team = data.loc[user_team.index].sort_values('overall', ascending=False)
        data = data.sort_values('overall', ascending=False)
        self.current_team = cur_team
        full_set = self._transfer_finder(cur_team, data)

        try:            
            diff_val = max([i['diff'] for i in full_set])
            idx= [i['diff'] for i in full_set].index(diff_val)
            print(f"Replace {full_set[idx]['existing player']} with {full_set[idx]['new player']}")
        except ValueError:
            print('No transfers to do this week')

    def double_transfer(self, no_weeks=5):
        '''
        - Check first to see if any players are "chance" < 51 and find highest differential for those players.
        - Otherwise do same as single transfer for first player.
        - Remove first player transfer from current team and replacement from data
        - Perform the same operation again
        '''
        user_team = self._get_user_team()
        self._get_players(no_weeks=no_weeks)
        data = self.normalise(df=self.data)
        
        cur_team = data.loc[user_team.index].sort_values('overall', ascending=False)
        data = data.sort_values('overall', ascending=False)
        self.current_team = cur_team
        
        # Run the _transfer_finder code twice, removing found player each time.
        for i in range(2):
            full_set = self._transfer_finder(cur_team, data)
            try:
                diff_val = max([i['diff'] for i in full_set])
                idx = [i['diff'] for i in full_set].index(diff_val)
                print(f"Replace {full_set[idx]['existing player']} with {full_set[idx]['new player']}")
                data = data.drop(index=full_set[idx]['n_pl_id'])
                cur_team = cur_team.drop(index=full_set[idx]['ex_pl_id'])
            except ValueError:
                print('No transfers to do this week')
                   
    def wildcard(self, no_weeks=5):
        '''
        Finds the best team to create using a wildcard based on the following methodology:
            - Filters player list by those with >51% chance of playing next round and sorts by "overall" column
            - Iterates through the list fifteen times to fill squad
            - Checks the player is in a position which still needs to be filled and hasn't already been picked
            - Checks whether the selected player is within a tolerance price
                - If the player is within the tolerance price, moves on to find the next place in the squad
                - If not, moves to the next player in the list to see if they fulfill all the criteria
        '''
        self._get_players(no_weeks)
        data = self.data
        data = self.normalise(df=data)
        element_type = {'1': 2, '2': 5, '3': 5, '4': 3}
        player_list = []
        
        # This implementation is also messy - I have filtered both lists for players likely to play
        # and sorted but "overall" rank. Need to figure out a way to do this without creating a separate list
        eval_data = data.loc[data['chance'] > 51]
        eval_data = eval_data.sort_values(by='overall', ascending=False).reset_index(drop=True)
        data = data.loc[data['chance'] > 51]
        data = data.sort_values(by='overall', ascending=False).reset_index(drop=True)

        for i in range(16):
            for j, val in enumerate(data.iterrows()):
                if element_type[val[1]['pos']] >= 1 and not val[0] in player_list:
                    player_list.append(val[0])
                    players_temp = data.iloc[player_list]
                    try:
                        money_left = 100 - sum(players_temp['cost'])
                    except (AttributeError, NameError) as e:
                        money_left = 100
                    result = self._ensure_costs_work(money_left, i)    
                    if result == True:
                        element_type[val[1]['pos']] -= 1
                        eval_data = eval_data.drop(val[0])
                        break
                    else:
                        player_list = player_list[:-1] 
        return data.iloc[player_list]
    