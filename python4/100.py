import copy
import random

boardsize=4
board=[[0,0,2,2],[2,2,0,0],[4,2048,0,4],[0,2,0,0]]

def display():
    largest=board[0][0]
    for row in board:
        for j in row:
            if j>largest:
                largest=j
    bosluk=len(str(largest))#en büyük rakamın uzunluğunu bul

    for row in board:
        ROW='|'
        for element in row:
            if element==0:
                ROW=ROW+" "*bosluk+ '|'
            else:
                ROW=ROW+(" "*(bosluk-len(str(element)))+str(element)+'|')#her bölme için en uzun sayının boyutundan girilen sayının boyutunu çıkarıp boşluk olarak ekle sonra sayıyı yaz(bölmeyi eşitlemek için kullanılacak)
        print(ROW)
    print()

def mergeleft(row):#tüm sayıları sola doğru taşıma fonksiyonu
    for j in range(boardsize-1):#4*4'lük matris için
        for i in range(boardsize-1,0,-1):#her bir satır için
            if row[i-1]==0:#her satır için sondan bir önceki değer 0 ise
                row[i-1]=row[i]#onun yerine ondan sonra gelen değeri ata
                row[i]=0#bir önceki değeri sıfırla

    for i in range(boardsize-1):
        if row[i]==row[i+1]:#soldan sağa her satırdaki ardışık iki değer eğer birbirine eşitse
            row[i]=row[i]*2#bir önceki sayıyı ikiye katla
            row[i+1]=0#bir sonraki sayıyı sıfırla

    for i in range(boardsize-1,0,-1):#sağdan sola
        if row[i-1]==0:#sağdan sola bir önceki değer 0 ise
            row[i-1]=row[i]#bir sonraki değeri bir önceki değerin yerine ata
            row[i]=0#bir sonraki değeri sıfırla
    return row#satırı döndür

def merge_left(currentBoard):#listeyi çağır
    for i in range(boardsize):#listenin içindeki listelerin uzunluğu kadar
        currentBoard[i]=mergeleft(currentBoard[i])#her bir liste için mergeleft fonksiyonundaki işle
    return currentBoard#listenin tamamını döndür

def reverse(row):
    new=[]
    for i in range(boardsize-1,-1,-1):#sağdan sola
        new.append(row[i])#her bir listeyi ters çevir
    return new#listenin tamamını döndür

def merge_right(currentBoard):#
    for i in range(boardsize):
        currentBoard[i]=reverse(currentBoard[i])#her bir satırı ters çevir
        currentBoard[i] = mergeleft(currentBoard[i])#satırların içindeki sayıların yerini değiştir
        currentBoard[i] = reverse(currentBoard[i])#tekrar ters çevir
    return currentBoard#listenin tamamını döndür

def transpose(currentBoard):#satır ve sütün konumlarının yerlerini değiştir yeni konumu ata.
    for j in range(boardsize):
        for i in range(j,boardsize):
            if not i==j:
                temp=currentBoard[j][i]#
                currentBoard[j][i]=currentBoard[i][j]
                currentBoard[i][j]=temp
    return currentBoard

def merge_up(currentBoard):
    currentBoard = transpose(currentBoard)
    currentBoard=merge_left(currentBoard)
    currentBoard=transpose(currentBoard)

    return currentBoard

def merge_down(currentBoard):#
    currentBoard=transpose(currentBoard)#transpozesini al
    currentBoard=merge_right(currentBoard)#sağa doğru topla
    currentBoard=transpose(currentBoard)#tekrar transpozesini al

    return currentBoard#aşağı doğru toplanmış tabloyu döndür

def picknewvalue():#
    if random.randint(1,8)==1:
        return 4
    else:
        return 2

def addnewvalue():#
    rownum=random.randint(0,boardsize-1)#rastgele satır
    colnum=random.randint(0,boardsize-1)#rastgele sütün

    while not board[rownum][colnum]==0:#0'a eşit değilse
        rownum=random.randint(0,boardsize-1)
        column=random.randint(0,boardsize-1)

    board[rownum][colnum]=picknewvalue()#değeri ata

board=[]#boş blok oluştur#
for i in range(boardsize):
    row=[]
    for j in range(boardsize):
        row.append(0)
    board.append(row)

numneeded=2
while numneeded>0:#rastgele 2 değer üret ve boşluğu doldur
    rownum=random.randint(0,boardsize-1)
    colmun=random.randint(0,boardsize-1)

    if board[rownum][colmun]==0:
        board[rownum][colmun]=picknewvalue()
        numneeded=numneeded-1

def won():#kazanma durumu
    for row in board:
        if 2048 in row:
            return True
    return False

def nomoves():#kullanıcının kaybedip kaybedemediği fonksiyon
    tempboard1=copy.deepcopy(board)#iki adet kopyasını oluştur
    tempboard2=copy.deepcopy(board)

    #hareket edecek hiçbir yeri kalmadığında true döndür
    tempboard1=merge_down(tempboard1)
    if tempboard1==tempboard2:
        tempboard1=merge_up(tempboard1)
        if tempboard1==tempboard2:
            tempboard1=merge_left(tempboard1)
            if tempboard1==tempboard2:
                tempboard1=merge_right(tempboard1)
                if tempboard1==tempboard2:
                    return True
    return False

display()#iki sayı atanmış tahtayı ekrana yazdır
gameover=False
while not gameover:#oyun bitmediği sürece harf girmesini iste
    move=input("hangi yönde toplamak istiyorsunuz:  ")
    valid_input=True
    tempboard = copy.deepcopy(board)  # her hamleden sonra kopya oluştur

    if move=="d":
        board=merge_right(board)
    elif move=="w":
        board=merge_up(board)
    elif move=="a":
        board=merge_left(board)
    elif move=="s":
        board=merge_down(board)
    else:
        valid_input=False

    if not valid_input:#eğer yanlış değer harf girilmişse
        print("Your input was not valid")
    else:#girilmemişse
        if board==tempboard:#eğer kopya bir sonraki hamle eşitse farklı bir değer girmesini iste
            print("Try a different direction")
        else:
            if won():#kazanırsa oyunu bitir
                display()#ekranda göster
                print("you won")
                gameover=True#döngüyü kır
            else:
                addnewvalue()#değilse yeni değer ekle
                display()#görüntüle

                if nomoves():#hareket edemiyorsa
                    print("sorry,you have no more")

display()#ekranı oluştur
