Mongo DB 실행하기

```
mongo
```

모든 Database 보기

```show dbs
show dbs
```

모든 작업을 수행하려면 우선 Database 를 선택해야 함!!!!

```
use DB_name
```

-----------------------------------------------------------------------------------------------------------------------------------------------------------

특정 Database 삭제하기

```
db.dropDatabase()
```

특정 Database의 Collections(Table) 보기

```
show collections
```

특정 Collection 살펴보기

```
db.collection_name.find()
db.collection_name.find().pretty()
```

