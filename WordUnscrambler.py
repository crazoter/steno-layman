import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
from collections import defaultdict

# https://github.com/tinmarr/Word-Unscrambler
NUMBER_OF_ALPHABETS = 26
MAX_SUPPORTED_DUPES = 16

# To further optimize, we can use np.matmul. Unfortunately the numbers can get pretty huge so we will need another encoding.
# To fit the data into an unsigned 64 bit, we will have to do a special encoding:
# Every alphabet takes up 2 bits by default, supporting up to 3 duplicates with 2 bits. That leaves us with 12 bits free.
# We can analyse the english lexicon to see which words are most likely to need the 3rd bit:
# https://colab.research.google.com/drive/1Ga0OXyN41zYxu-CjiPxXr8YD38YCxcA8#scrollTo=93F2FyizPkpN
THREE_BIT_CHARS = ['a', 'c', 'd', 'e', 'i', 'l', 'n', 'o', 'r', 's', 't', 'u']

def prepareMaps():
  vectMap = []
  bitmaskMap = []
  maxSupportedDupes = []
  char_code = ord('a')
  currentBitIdx = 0
  for i in range(NUMBER_OF_ALPHABETS):
    vectMap.append([])
    m = 2 ** (i * 3)
    for j in range(MAX_SUPPORTED_DUPES + 1):
      vectMap[-1].append(j * m)

    # 3 bits for every character
    bitmaskMap.append(m + (m<<1) + (m<<2))
  # print(vectMap)
  return (vectMap, bitmaskMap)

    # character = chr(char_code + i)

    # Optimize to fit final number into an int64
    # m = 2**(currentBitIdx)
    # vectMultMap.append(m)
    
    # make space for the next character
    # bits = 2
    # if character in THREE_BIT_CHARS:
    #   bits += 1
    # currentBitIdx += bits

    # keep track of the max number of duplicates supported
    # length = 2 ** bits
    # maxSupportedDupes.append(length - 1)
  # return (vectMultMap, maxSupportedDupes)

# VECT_MULT_MAP, MAX_SUPPORTED_DUPES = prepareVectMap()
VECT_MAP, BIT_MASKS = prepareMaps()

def RemoveFromList(thelist, val):
    return [value for value in thelist if value != val]

def GetDic():
    try:
        dicopen = open("DL.txt", "r")
        dicraw = dicopen.read()
        dicopen.close()
        diclist = dicraw.split("\n")
        diclist = RemoveFromList(diclist, '')
        return diclist
    except FileNotFoundError:
        print("No Dictionary!")
        return 
    
def Word2Vect(word):
    l = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    v = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    w = word.lower()
    wl = list(w)
    for i in range(0, len(wl)):
        if wl[i] in l:
            ind = l.index(wl[i])
            v[ind] += 1
    return v

def Vect2Int(vect):
    # return np.dot(np.minimum(vect, MAX_SUPPORTED_DUPES), VECT_MULT_MAP)
    f = 0
    for i in range(NUMBER_OF_ALPHABETS):
      f += VECT_MAP[i][min(vect[i], MAX_SUPPORTED_DUPES)]
    return f
   
def Ints2Dic(dic):
  d = {}
  for i in range(0, len(dic)):
    v = Word2Vect(dic[i])
    Int = Vect2Int(v)
    if Int in d:
        tat = d.get(Int)
        tat.append(dic[i])
        d[Int] = tat
    elif Int not in d:
        d[Int] = [dic[i]]
  return d

def bitmaskNum(num, id, doShift):
  if not doShift:
    return num & BIT_MASKS[id]
  return (num & BIT_MASKS[id]) >> (id * 3)
  

def ModifyInt(num, id, val):
  if (val > 0):
    return num + VECT_MAP[id][val]
  return num - VECT_MAP[id][-val]

def dic2Cluster(dic):
  global pca
  global kmeans
  global clusterMap
  X = np.array(list(map(Word2Vect, dic)))
  print("Evaluating PCA...")
  pca = PCA(n_components=21)
  fitted_X = pca.fit_transform(X)
  # print(pca.components_)
  # print(pca.explained_variance_)
  kmeans = MiniBatchKMeans(n_clusters=len(dic) // 30,
                          random_state=0)
  print("Performing kmeans clustering...")
  kmeans.fit(fitted_X)
  print("Building cluster map...")
  clusterMap = defaultdict(list)
  for k,v in zip(kmeans.labels_, dic):
    clusterMap[k].append(v)
  # print(clusterMap)
  # return (pca, kmeans, clusterMap)

def transformWordIntoCluster(word):
  global pca
  global kmeans
  global clusterMap
  v = Word2Vect(word)
  p = pca.transform([v])
  c = kmeans.predict(p)
  print(c.item())
  return clusterMap[c.item()]
