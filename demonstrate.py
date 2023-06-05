import psycopg2

conn = psycopg2.connect(host='localhost',dbname='Hotel',user='postgres',password='1234',port='5432')
cur = conn.cursor()

print("개인정보 (id, password, name, age, phonenumber)를 입력하세요")

id, password, name, age, phonenumber = input().split()

#만약 입력한 id가 데이터베이스에 존재한다면 DB에 추가하지않고 아니라면 추가해
cur.execute('SELECT * FROM member m WHERE m.member_id LIKE (%s);' , [id])
res = cur.fetchall()

count = 0
for x in res:
   if id in x :
       count = count + 1 
       
print(count)

if count == 0:
    cur.execute("INSERT INTO member(member_id,member_pw,member_name,member_age,member_phonenumber) VALUES (%s, %s, %s, %s, %s);",(id,password, name, age, phonenumber))
    conn.commit()

fid = 1

while True:
    print("메뉴를 선택하세요.\n 1. 특정 호텔 정보 검색하기. \n 2. 지역별 호텔 검색하기.\n 3. 즐겨찾기 추가하기. \n 4. 즐겨찾기 검색하기. \n 5. 여행일지 기록하기. \n 6. 나가기. \n 번호 입력 ")
    num = int(input())
    if num == 1 :
        print("원하시는 숙박업소를 입력하세요 ") 
        hope = input()
        cur.execute('SELECT a.accomodation_id, a.accomodation_name, a.accomodation_lowprice, a.accomodation_rate FROM accomodation a WHERE a.accomodation_name LIKE \'%' + hope +'%\'')
        res = cur.fetchall()
        print(res )
        
    elif num == 2 :
        print("여행지를 입력하세요 ")
        location = input()
        cur.execute('SELECT a.accomodation_name, a.accomodation_lowprice, a.accomodation_rate FROM accomodation a WHERE a.accomodation_address LIKE \'%' + location +'%\'')
        res = cur.fetchall()
        print(res )
        
    elif num == 3:
        print("즐겨찾기 추가를 위한 호텔 ID 숫자를 입력하세요 ")
        favorite = int(input())
        cur.execute("INSERT INTO favorite(favorite_num,member_id,accomodation_id) VALUES (%s, %s, %s);",(fid, id , favorite)) #즐겨찾기 
        fid = fid + 1
    
    elif num == 4:
        print("사용자의 즐겨찾기 목록입니다")
        cur.execute('SELECT a.* FROM favorite f INNER JOIN accomodation a ON f.accomodation_id = a.accomodation_id WHERE f.member_id = \'' + id + '\';')
        res = cur.fetchall()
        print(res )
        
    elif num == 6:
        break
    