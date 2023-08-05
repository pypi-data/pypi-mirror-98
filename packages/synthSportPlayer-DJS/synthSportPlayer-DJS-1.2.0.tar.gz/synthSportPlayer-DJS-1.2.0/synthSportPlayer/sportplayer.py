from numpy.random import normal, randint, rand
from numpy import log2
from math import ceil
import pandas as pd
from random import shuffle
import pickle
import os

class player:
    """
    A class to model any sports player/team.
    
    Parameters
    ----------
    skill : int or float
            The underlying 'true' skill of a player
    variance : int or float
               How much the player varies in their performance. The lower this is the more consistent they are in their performance
    name : str
           The players name/id that will be used as a reference later on
    pointLimit : int, default 10
                 The max number of points a player is allowed to keep in the :py:attr:`pointRec`.
    
    Attributes
    ----------
    pointRec : list of int
               A record of the points the this player has earnt from a tournament in the order that they earnt them.
    totalPoints : int
                  The total of all the points in :py:attr:`pointRec`.
    """
    def __init__(self,skill,variance,name,pointLimit=10):
        """
        The init method of the class.
        """
        if not((type(skill)==int)|(type(skill)==float)):
            raise TypeError('Skill must be an int or a float')
        if not((type(variance)==int)|(type(variance)==float)):
            raise TypeError('variance must be an int or a float')
        if type(name)!=str:
            raise TypeError('name must be a str')
        if type(pointLimit)!=int:
            raise TypeError('pointLimit must be an int')
        
        self.skill = skill
        self.variance = variance
        self.name = name
        self.pointRec=[]
        self.totalPoints=0
        self.pointLimit=pointLimit
        
    def perform(self):
        """
        A method getting the player to perform.
        
        A numerical value is returned representing the players performance 'on the day'. 
        This is generate from a normal dist. with mean equal to the players skill and var equal to the player variance, 
        which is then rounded to the nearest integer.
        
        Returns
        -------
        performance : int
                      The value representing the player performance on the day, which is greater than or equal to 0.
        """
        return max(round(normal(self.skill,self.variance)),0)
    
    def selfsummary(self):
        """
        A method to print out the characteristics of the player.
        """
        outstr = "Name: {}\nSkill: {}\nVar: {}\nPoint Record: {}\nTotal points: {}\nPoint limit: {}"
        print(outstr.format(self.name,self.skill,self.variance,self.pointRec,self.totalPoints,self.pointLimit))
        
    def gainPoints(self,points):
        """
        A method to update the current points of the player.
        
        The points provided are added to the players :py:attr:`pointRec`. If the number of entries in the :py:attr:`pointRec` is greater than pointLimit, 
        then the oldest entry is removed. After this the :py:attr:`totalPoints` arrtibute is updated with the new total of :py:attr:`pointRec`.
        
        Parameters
        ----------
        points : int
                 Points to be added to the players :py:attr:`pointRec`.
        """
        if type(points)!=int:
            raise TypeError('points must be an int')
            
        self.pointRec.append(points)
        if len(self.pointRec)>self.pointLimit:
            self.pointRec.pop(0)
        self.totalPoints = sum(self.pointRec)
    
class match:
    """
    A class to handle the match between two :py:class:`player`'s or any :py:class:`bye`.
    
    Parameters
    ----------
    player1 : player or bye
              The first :py:class:`player` or :py:class:`bye` that is participating in the match.
    player2 : player or bye
              The second :py:class:`player` or :py:class:`bye` that is participating in the match.
    """
    def __init__(self,player1,player2):
        """
        The init function of the class.
        """
        if not((type(player1)==player)|(type(player1)==bye)):
            raise TypeError('player1 must be a player or a bye')
        if not((type(player2)==player)|(type(player2)==bye)):
            raise TypeError('player2 must be a player or a bye')
            
        self.player1 = player1
        self.player2 = player2
    
    def playMatch(self):
        """
        A method to excute the match between the two player's given to the match.
        
        Both the perform methods of the players are activated and the :py:class:`player` with the higher performance score is the winner. 
        If the two values are equal, then a winner is randomly chosen. If the match is a player vs a bye then the player automatically wins
        
        Returns
        -------
        winner : player or bye
                 The :py:class:`player` who won the match. A :py:class:`bye` is only returned if the match is between 2 byes.
        loser : player or bye
                The :py:class:`player` who lost the match
        matchReport : list
                      A list containing the information from the match it has just played out. 
                      Containing for both players: their name, their total points, their performance value for that match. 
                      Then finally the name of the player who won.
        """
        p1 = self.player1.perform()
        p2 = self.player2.perform()
        if p1==p2:
            t=(rand()-0.5)
        else:
            t=0
        if (p1+t)>p2:
            return self.player1,self.player2,[self.player1.name,self.player1.totalPoints,p1,self.player2.name,self.player2.totalPoints,p2,self.player1.name]
        else:
            return self.player2,self.player1,[self.player1.name,self.player1.totalPoints,p1,self.player2.name,self.player2.totalPoints,p2,self.player2.name]
        
class tournament:
    """
    A class to model a tournament
    
    The tournament is the classic 1v1 elimination tournament where the winner of a match proceeds through to the next round.
    
    Parameters
    ----------
    playerList : list of :py:class:`player`
                 A list containg the players who are competing in this tournament. If this is not a power of 2 then byes will be added 
                 to make up the numbers then then the list of players shuffled.
    pointPerRound : int, default 5
                    The number of points that a player earns at each stage that they get to.
                    
    Attributes
    ----------
    matchRec :  list of list
                A list where the match results are stored when they are completed.
    round : int
            An integer used to track what current round the tournament is in.
    tournRes : DataFrame
               A pandas dataframe that is created and assigned once the tournament is complete containing all the match results, made from the :py:attr:`matchRec` attribute.
    
    """
    def __init__(self, playerList,pointPerRound=5):
        """
        The init function of this class.
        """
        if not(all(type(n)==player for n in playerList)):
            raise TypeError("playerList is not a list of only players")
        if type(pointPerRound)!=int:
            raise TypeError('pointPerRound must be an int')
            
        self.currentRound = playerList
        if not(log2(len(self.currentRound)).is_integer()):
            self.currentRound+=[bye() for i in range(0,(2**ceil(log2(len(self.currentRound)))-len(self.currentRound)))]
            shuffle(self.currentRound)
        
        self.points=pointPerRound
        self.matchRec=[]
        self.round=1
        self.tournRes=None
    
    def playTourn(self):
        """
        A method to play the entire tournament.
        
        Activating this method will play out the tournament until there is one :py:class:`player` remaining as the winner. 
        At which point the final tournament results are created and stored in :py:attr:`tournRes`.
        """
        while len(self.currentRound)>1:
            nextRound = self.playRound()
            self.currentRound = nextRound
            self.round+=1
        self.currentRound[0].gainPoints(self.round*self.points)
        self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match","player1_id","player1_rnkPoints","player1_perform","player2_id","player2_rnkPoints","player2_perform","winner_id"])
        
        
    def playRound(self):
        """
        A method to play all the matches in the current round.
        
        This plays out the round with the players that have made it through to the current stage. Each match result is added to the :py:attr:`matchRec`, 
        and the loser gains points equal to the round where they got to.
        
        Returns
        -------
        nextRound : list of players
                    A list of players who won their matches and proceed through to the next round
        """
        nextRound=[]
        for i in range(0,len(self.currentRound)//2):
            currentMatch=match(self.currentRound[2*i],self.currentRound[(2*i)+1])
            winner,loser,res = currentMatch.playMatch()
            loser.gainPoints(self.round*self.points)
            nextRound.append(winner)
            self.matchRec.append([self.round,i+1]+res)
        return nextRound
    
    def reset(self):
        """
        A method to reset the tournament to be able to be played again.
        """
        self.matchRec=[]
        self.round=1
        self.tournRes=None
        
def generatePlayers(number,maxSkill=100,var=10):
    """
    A function to generate a numbers of players.
    
    This will generate the given number of players whose skill is uniformly random between 1 and maxSkill, and whose variance is equal to var.
    
    Parameters
    ----------
    number : int
             The number of players that are to be created.
    maxSkill : int or float, default 100
               The max skill that a player can have.
    var : int or float, default 10
          The variance to give to each player.
             
    Returns
    -------
    playerList : list of players
                 A list containing the players created.
    playerInfo : DataFrame
                 A table with information about the players created.
    """
    if type(number)!=int:
        raise TypeError('number must be an int')
    if not((type(maxSkill)==int)|(type(maxSkill)==float)):
        raise TypeError('maxSkill must be an int or a float')
    if not((type(var)==int)|(type(var)==float)):
        raise TypeError('var must be an int or a float')
    
    playerList = []
    playerinfo = []
    for i in range(0,number):
        skill = randint(1,maxSkill)
        playerList.append(player(skill,var, str(i)))
        playerinfo.append([str(i),skill,var,0])
    playerinfo = pd.DataFrame(playerinfo,columns=["name","skill","variance","week_-1"])
    playerinfo.sort_values("skill",ascending=False,inplace=True)
    return playerList, playerinfo


def fetchPlayerSummary(playerList):
    """
    A function to generate a player summary table.
    
    Given a list of players this will generate a pandas table with the players summary.
    
    Parameters
    ----------
    playerList : list of player
                 A list of players whose summary wants to be fetched
                 
    Returns
    -------
    playerinfo : DataFrame
                 A data frame containg the summary information of all the players provided.
    """
    playerinfo = []
    for player in playerList:
        playerinfo.append([player.name,player.skill,player.variance,player.totalPoints])
    playerinfo = pd.DataFrame(playerinfo,columns=["name","skill","variance","week_-1"])
    playerinfo.sort_values("skill",ascending=False,inplace=True)
    return playerinfo

class season:
    """
    A class to handle a season of tournaments being played.
    
    A season is a squence of tournaments that are played by a group of players one after another and collect points as they go based 
    on performance in each tournament.
    
    Notes
    -----
    At this points the seasons automatically use :py:class:`tournament` and does not work with :py:class:`robin`
    
    Parameters
    ----------
    numPlayers : int, default 16
                 The number of players that will be generated to play in this season. This will be overridden if players are provided
    tournToPlay : int, default 20
                  The number of tournaments that this season will have,
    players : list of players, default None
              Optional. If there are pre-existing players that the user wishes to enter into this season. The number of players in the list will override numPlayers. 
    playerSum : DataFrame, default None
                Optional. If the player are being provided externally then their summary data table can be provided for their total point record to be appended to.
    
    Attributes
    ----------
    week : int
           An integer to keep track of what week (tournament) is being played out.
    tournRecs : list of DataFrames
                A list that stores the results from each tournament.
    seasonRes : Dataframe, default None
                A pandas dataframe with all of the tournament results concatenated into one dataframe, which is done upon season completion.
    """
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        """
        The init method of this class.
        """
        if type(numPlayers)!=int:
            raise TypeError('numPlayers must be an int')
        if type(tournToPlay)!= int:
            raise TypeError('tournToPlay must be an int')
        if players!=None:
            if not(all(type(n)==player for n in players)):
                raise TypeError("playerList is not a list of only players")
        if playerSum!=None:
            if not(type(playerSum)==pd.core.frame.DataFrame):
                raise TypeError("playerSum must be a pandas dataframe")
        
        self.tournsToPlay = tournToPlay
        self.week=0
        self.tournRecs=[]
        self.seasonRes=None
        if players == None:
            self.numPlayers = numPlayers
            self.players, self.playerSum = generatePlayers(self.numPlayers)
        else:
            self.numPlayers = len(players)
            self.players = players
            
            if playerSum==None:
                self.playerSum = fetchPlayerSummary(players)
            else:
                self.playerSum = playerSum
    
    def playSeason(self):
        """
        A method to play out the season of tournaments.
        
        This method will play all of the tournaments in order, storing tournament results, recording players total points and shuffling the order of players
        inbetween each tournament.
        """
        if self.week == self.tournsToPlay:
            print("This season has already been played. Please reset, use: .rest()")
        while self.week<self.tournsToPlay:
            shuffle(self.players)
            tourn = tournament(self.players)
            tourn.playTourn()
            self.gatherPoints()
            tourn.tournRes["Tourn"] = self.week
            self.tournRecs.append(tourn.tournRes)
            self.week+=1
            self.players = [x for x in self.players if type(x)==player]
        self.seasonRes = pd.concat(self.tournRecs)
    
    def reset(self):
        """
        A method to reset the season. 
        
        It won't reset the players but resets the week count and the tournament results record. 
        """
        self.week=0
        self.tournRecs=[]
        
    def gatherPoints(self):
        """
        A method to gather the total points of players aftern a tournament has been completed. These are store it in the playerSum.
        """
        pointlist=[]
        for player in self.players:
            pointlist.append([player.name,player.totalPoints])
        pointlist=pd.DataFrame(pointlist,columns = ['name','week_'+str(self.week)] )
        self.playerSum = self.playerSum.merge(pointlist, on= 'name')
    
    def export(self,fldr='seasonData'):
        """
        A function to export the players, the tournament results tables, and the season points table as CSVs.
        
        Parameters
        ----------
        fldr : str, default 'seasonData'
               The name to call the folder the results shall be stored in.
        """
        if type(fldr)!=str:
            raise TypeError("fldr must be a str")
        if fldr in [x for x in os.listdir() if os.path.isdir(x)]:
            pass
        else:
            os.mkdir(fldr)
        file_to_store = open(fldr+"/players.pickle", "wb")
        pickle.dump(self.players, file_to_store)
        file_to_store.close()
        
        for i in range(0,len(self.tournRecs)):
            self.tournRecs[i].to_csv(fldr+"/tournament_"+str(i)+".csv",index=False)
        
        self.playerSum.to_csv(fldr+"/seasonPoints.csv",index=False)
        
    
class liveTourn(tournament):
    """
    A class to facilitate live dashboarding of a season/tournament being played
    
    For further info see the parent class tournament.
    """
    def __init__(self, playerList,pointPerRound=5):
        super().__init__(playerList,pointPerRound)
    
    def playTourn(self):
        """
        A method to play the tournament. 
        
        Unlike it's parent class, when this method is called it will only play the next round of the tournament.
        
        Returns
        -------
        complete : bool
                   A boolean to indicate if the tournament is now complete.
        """
        if len(self.currentRound)>1:
            nextRound = self.playRound()
            self.currentRound = nextRound
            self.round+=1
            if len(self.currentRound)==1:
                self.currentRound[0].gainPoints(self.round*self.points)
                self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match",
                                                                    "player1_id","player1_rnkPoints","player1_perform",
                                                                    "player2_id","player2_rnkPoints","player2_perform","winner_id"])
                return True
            else:
                return False
        else:
            return True
        
class liveSeason(season):
    """
    A class to facilitate live dashboarding of a season/tournament being played
    
    For further info see the parent class season.
    
    Attributes
    ----------
    currentTourn : liveTourn
                   The current tournament that is in progress
    currentTournComplete : bool
                           A boolean indicating if the current tournament is completed or not.
    """
    def __init__(self,numPlayers=16,tournToPlay=20, players=None, playerSum=None):
        super().__init__(numPlayers=16,tournToPlay=20, players=None, playerSum=None)
        shuffle(self.players)
        self.currentTourn = liveTourn(self.players)
        self.currentTournComplete = False
        
    def playSeason(self):
        """
        A method to play the season.
        
        Unlike it's parent class, when this method is called it will only play the next round of the tournament. But if the tournament is complete 
        it will update the records and move onto make the next tournament and play the first round.
        
        Returns
        -------
        complete : bool
                   A boolean indicating if the season is completed or not.
        """
        if self.week == self.tournsToPlay:
            self.seasonRes = pd.concat(self.tournRecs)
            return True
        else:
            if self.currentTournComplete:
                shuffle(self.players)
                self.currentTourn = liveTourn(self.players)

            self.currentTournComplete = self.currentTourn.playTourn()
            if self.currentTournComplete:
                self.gatherPoints()
                self.currentTourn.tournRes["Tourn"] = self.week
                self.tournRecs.append(self.currentTourn.tournRes)
                self.week+=1
                self.players = [x for x in self.players if type(x)==player]
            return False
            
class robin:
    """
    A class to model a round robin tournament.
    
    A round robin is a variation on a tournament setting where all the players play against each other. 
    The winner is normally the one with the most matches. If there's any a draw it then goes to their win difference. 
    
    Parameters
    ----------
    playerList : list of player
                 The players who are to play in this this round robin. If there is an odd number of players, a :py:class:`bye` will be added in.
    pointPerWin : int, default 5
                  The number of points that players will recieve at the end of the tournament for each win.
    
    Attributes
    ----------
    numPlayers : int
                 The number of players that are competing in this round robin.
    matchRec :  list of list
                A list where the match results are stored when they are completed.
    round : int
            An integer used to track what current round the tournament is in.
    tournRec : DataFrame
               A pandas dataframe that is created and assigned once the tournament is complete containing all the match results, made from the :py:attr:`matchRec` attribute.
    winLossRec : DataFrame
                 A pandas dataframe containing the number of wins, losses and the winning point difference for each player
    """
    def __init__(self,playerList,pointPerWin=5):
        """
        The init function of the class.
        """
        if not(all(type(n)==player for n in playerList)):
            raise TypeError("playerList is not a list of only players")
        if type(pointPerWin)!=int:
            raise TypeError('pointPerWin must be an int')
        
        self.playerList = playerList
        self.pointPerWin = pointPerWin
        self.numPlayers = len(self.playerList)
        if (self.numPlayers%2)!=0:
            self.playerList.append(bye())
            self.numPlayers+=1
        self.matchRec=[]
        self.tournRes=None
        self.round=1
        
        names=[]
        for py in self.playerList:
            names.append([py.name,0,0,0])
        self.winLossRec = pd.DataFrame(names,columns=["Player","Wins","Losses","Diff"])
        self.winLossRec.set_index("Player",inplace=True)
        
    def permute(self):
        """
        Permute the order of the players for the next round of the round robin.
        
        For a round robin you have to permute the players in a certain way to make everyone play everyone else.
        """
        self.playerList = [self.playerList[0]]+self.playerList[2:]+[self.playerList[1]]
        
    def playRound(self):
        """
        A method to play all the matches in the current round.
        
        This plays out the round with the players against their allocated opponent for the current round. 
        Each match result is added to the :py:attr:`matchRec`, and the :py:attr:`winLossRec` is updated with the results, 
        unless it is against a :py:class:`bye`
        """
        matchNum = 1 
        for i in range(0,self.numPlayers//2):
            p1=self.playerList[i]
            p2=self.playerList[(self.numPlayers)-i-1]
            currentMatch=match(p1,p2)
            winner,loser,res = currentMatch.playMatch()
            if type(loser)!=bye:
                self.winLossRec.loc[winner.name,"Wins"]+=1
                self.winLossRec.loc[winner.name,"Diff"]+=abs(res[2]-res[5])
                self.winLossRec.loc[loser.name,"Losses"]+=1
            
            self.matchRec.append([self.round,matchNum]+res)
            matchNum+=1
        self.round+=1
    
    def playTourn(self):
        """
        A method to play the entire tournament.
        
        Activating this method will play out the tournament until every :py:class:`player` has played everyother :py:class:`player`. 
        At which point the final tournament results are created and stored in :py:attr:`tournRec`. Points are then given to the players in 
        accordance with how many matches they won.
        """
        while self.round<self.numPlayers:
            self.playRound()
            self.permute()
        self.tournRes = pd.DataFrame(self.matchRec,columns=["Round", "Match","player1_id","player1_rnkPoints","player1_perform","player2_id","player2_rnkPoints","player2_perform","winner_id"])
        self.winLossRec.sort_values(by=["Wins","Diff"],ascending=[False,False],inplace=True)
        self.distributePoints()
        
    def distributePoints(self):
        """
        A method to distribute the points.
        
        For each match a player has won, the value that is stored in the corresponding entry of :py:attr:`winLossRec`, they will gain points equal 
        to :py:attr:`pointPerWin`.
        """
        for py in self.playerList:
            py.gainPoints(int(self.winLossRec.loc[py.name,"Wins"])*self.pointPerWin)
    
    def reset(self):
        """
        A method to reset the tournament.
        """
        self.matchRec=[]
        self.tournRes=None
        self.round=1
        
        names=[]
        for py in self.playerList:
            names.append([py.name,0,0,0])
        self.winLossRec = pd.DataFrame(names,columns=["Player","Wins","Losses","Diff"])
        self.winLossRec.set_index("Player",inplace=True)
            
class bye(player):
    """
    A class to model a bye.
    
    In some tournaments there are not enough player, so the empty spots are filled up with a bye. Whenever a player is against a bye they automatically win.
    """
    def __init__(self):
        super().__init__(-1,0,"Bye",0)
    
    def perform(self):
        return self.skill
