__author__ = 'leilei'

import codecs
from math import sqrt
class acrecommender:
    def __init__(self,data,n=10):
         """initialized acrecommender
         data is dictionary
         n is the maxium number of recomendations to make """
         self.n=n
         self.movieid2={}
         self.avg={}
         self.datauser={}
         if type(data).__name__=='dict':
              self.data=data




    def  loaddata(self,path=''):
        """loads u.data and u.item,path should end with /,like /a/d/c"""

        self.data={}
        i=0

        #
        #First load movie ratings into self.data
        #
        f=open(path+"u.data",'r')
        for line in f:
            i +=1
            #separate line into fields
            fields=line.split('\t')
            #u.data split by blank
            user=fields[0].strip()
            #returns str that strip "" "" from the begining and end of string
            movie=fields[1].strip()
            rating=int(fields[2].strip())
            if movie in self.data:
                currentRatings=self.data[movie]
            else:
                currentRatings={}
            currentRatings[user]=rating
            self.data[movie]=currentRatings
        f.close()

        #prepare user:movie:rating form of data,for computing
        f=open(path+"u.data",'r')
        for line in f:
            i +=1
            #separate line into fields
            fields=line.split('\t')
            #u.data split by blank
            user=fields[0].strip()
            #returns str that strip "" "" from the begining and end of string
            movie=fields[1].strip()
            rating=int(fields[2].strip())
            if user in self.datauser:
                currentRatings=self.datauser[user]
            else:
                currentRatings={}
            currentRatings[movie]=rating
            self.datauser[user]=currentRatings
        f.close()
        for user in self.datauser:
            sum_x = 0
            count = 0
            for item in self.datauser[user]:
                sum_x +=self.datauser[user][item]
                count +=1
            mean=float(sum_x)/count
            self.avg[user]=mean

        f=open(path+"u.item",'r')
        for line in f:
            i +=1
            #separate line in to fields
            fields=line.split("|")
            movieId=fields[0].strip()
            moviename=fields[1].strip()
            self.movieid2[movieId]=moviename
        f.close()
        ###data loaded successful

    def movieid2name(self,movieid):
        if movieid in self.movieid2:
            return self.movieid2[movieid]
        else:
            return movieid



    def cosine(self,rating1,rating2):
        sum_xy=0
        sum_x2=0
        sum_y2=0
        for key1 in rating1:
            for key2 in rating2:
                if key1==key2:
                    #print(key1)
                    #print(rating1)
                    #print(rating1[key1])
                    #print(self.avg[key1])
                    sum_xy +=(rating1[key1]-self.avg[key1])*(rating2[key2]-self.avg[key2])
                    sum_x2 +=pow((rating1[key1]-self.avg[key1]),2)
                    sum_y2 +=pow(rating2[key2]-self.avg[key2],2)
        denominator=sqrt(sum_x2)*sqrt(sum_y2)
        if denominator==0:
            return 0
        else:
            return(float(sum_xy)/denominator)

    def score(self,user,ritem):
        #self.datauser[user] contains all moive user had rated
        #item is the movie that user had not rated
        #normliza rating first
        nrating={}
        similar={}
        umax=self.datauser[user][max(self.datauser[user])]
        umin=self.datauser[user][min(self.datauser[user])]
        for item in self.datauser[user]:
            nrating[item]=(2*(self.datauser[user][item]-umin)-(umax-umin))/2*(umax-umin)
        #calculating similarity between item user had rated and the item
            similar[item]=self.cosine(self.data[item],self.data[ritem])
        #calculating estimate score
        sum_xw=0
        sum_x=0
        for item in nrating:
            sum_xw +=nrating[item]*similar[item]
            sum_x +=abs(similar[item])
        if sum_x ==0:
            return 0
        else:
            score=float(0.5*((float(sum_xw)/sum_x+1)*(umax-umin))+umin)
            return score

    def acrecom(self,userid,n):
        #compute score for each of the item user did not rated
        recomlist={}
        list=[]
        k=0
        for item in self.data:
            if item not in self.datauser[userid]:
                recomlist[item]=self.score(userid,item)
                k+=1
                if k>4*n:
                    break
        list=[(self.movieid2name(k),v)for (k,v)in recomlist.iteritems()]
        list.sort(key=lambda a:a[1],reverse=True)
        list=list[:n]
        for i in range(0,n):
            print("%s:%.2f"%(list[i][0],list[i][1]))

    def test(self,n):
        i=0
        for item in self.datauser:
            i=i+1
            print self.datauser[item]
            if i>n:
                break











