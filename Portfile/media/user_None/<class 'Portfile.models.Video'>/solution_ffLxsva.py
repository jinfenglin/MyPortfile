
def solution(A,D):
    #N is the river width
    #D is the jump range
    N= len(A)
    if D<=0:
        return -1
    dict={}
    for loc,time in enumerate(A):
        dict[time]=loc
    dp=[-1 for i in range(N)]
    current_stones=[]
    for time in dict:
        current_stones.append(dict[time])
        for i in range(N-1):
            for jump in range(1,D+1):
                if i-jump<0:
                    if i in current_stones:
                        dp[i]=1
                        #print i,time
                        if i+D>=N:
                            return time
                else:
                    if dp[i-jump]==1 and i in current_stones:
                        dp[i]=1
                        #print i,time
                        if i+D>=N:
                            return time
    return -1;

A=[1,-1,0,2,3,5]
print solution(A,3)


#
First of all, construct a dictionary with time as key and stone location as value
then I build up a dp array store the available location on the river and update it when time changes.
Then, I loop over the dictionary with the key 'time'. 
In each iteration 
1.I add new stones in my current_sotnes list
2.I test whether a location is accessible. If there is a location within the jump range and before current location index, and current index have a available stone, the current index is accessible.
  - 2.1 if current location is accessible, and the final destination is within the jump range, then I return the current time.

This solution has a O(N^2) time complexity and O(N) space complexity

