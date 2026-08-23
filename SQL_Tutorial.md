
# <span><b>Most Important SQL Queries: </b></span>

* <span style="color:#fa0f4e"><b>Select With `SELECT`:</b></span>
    
    - **Rule**: 
    ```postgres
        SELECT { column_name } FROM { table_name };
    ```
- **Example**
    ```postgres
        <!--* ex: select one column -->
        SELECT first_name FROM users;

        <!-- ====================|Multi-Selection|==================== -->
        <!--* ex: select multiple column's  -->
        SELECT name, age FROM users;

        <!-- ====================|*=All|==================== -->
        <!--* ex: select all  -->
        SELECT * FROM users;
        ```
---
* <span style="color:#fa0f4e"><b>Select With `WHERE`:</b></span>
    - **Rule**:
```postgres
        SELECT { column_name } FROM { table_name } WHERE { condition };
```
### <span style="color: #fcd45d"><b>======================|WHERE|======================</b></span>
```postgres
        <!--* ex: Select adult users (+18)-->
        SELECT name, age FROM users WHERE age >= 18;

        <!--* ex: Select Specific User  -->
        SELECT name FROM users WHERE name='Ahmed';

        <!-- ====================|WHERE & AND|==================== -->
        <!--* ex: Multiple Filtering using `AND`  -->
        SELECT name, age FROM users WHERE name='Ahmed' AND age >= 18;

       <!-- ====================|WHERE & OR|==================== -->
        <!--* ex: check user adultness (get aduly users only) -->
        SELECT name, isGraduated, age FROM users WHERE isGraduated=true OR age >= 18;
```
- **all operations supported**: 
    - **Equality**: **=** 
    - **UnEquality**:  **!=**
    - **Greater-Than** :  **>** , **>=**
    - **Less-Than**:  **<** , **<=**


---

### <span style="color: #fcd45d"><b>======================|WHERE & IN|======================</b></span>
- **Rule**:
```postgres
        SELECT { column_name } FROM { table_name } WHERE { column_name } IN (x1, x2, x3)
```
- **Example**
```postgres
        <!--* ex: Select ID's From List (selecting id=1 OR id=2 OR id=3) -->
        SELECT id FROM users WHERE id IN (1, 2, 3) 


        <!--* using `OR` (not recomendded) -->
        SELECT id FROM users WHERE id=1 OR id=2 OR id=3
```

### <span style="color: #fcd45d"><b>======================|WHERE & LIKE|======================</b></span>
- **Rule**:
```postgres
        SELECT { column_name } FROM { table_name } WHERE { column_name } LIKE {pattern}
        <!--! Where {pattern} means: a repeatetive number, string ... etc -->
        <!--! % : means any char/number -->
        
```
- **Example**
```postgres
        <!--? get only numbers `with` +123 -->
        <!--* to select only number that `Starts` with -->
        SELECT phone_numbers FROM users WHERE phone_number LIKE '123%'

        <!--* to select only number that `Ends` with -->
        SELECT phone_numbers FROM users WHERE phone_number LIKE '%123'

        <!--* to select only number that `Have` in anywhere -->
        SELECT phone_numbers FROM users WHERE phone_number LIKE '%123%'        

```
### <span style="color: #fcd45d"><b>======================|WHERE & NOT LIKE|======================</b></span>
- **Rule**:
```postgres
        SELECT { column_name } FROM { table_name } WHERE { column_name } LIKE {pattern}
        <!--! Where {pattern} means: a repeatetive number, string ... etc -->
        <!--! % : means any char/number -->
```
- **Example**:     
```postgres
        <!--? get only numbers `without` +123 -->

        <!--* execlude only numbers that `Starts` with 123 -->
        SELECT phone_numbers FROM users WHERE phone_number NOT LIKE '123%'

        <!--* execlude only numbers that `Ends` with 123 -->
        SELECT phone_numbers FROM users WHERE phone_number NOT LIKE '%123'

        <!--* execlude only numbers that `Have` in 123 anywhere -->
        SELECT phone_numbers FROM users WHERE phone_number NOT LIKE '%123%'
```
* <span style="color:#fa0f4e"><b>Select With `ORDER BY`:</b></span>
    - **Rule**:
### <span style="color: #fcd45d"><b>======================|ORDER BY|======================</b></span>
- **Rule**:
```postgres
        <!--! ASC = From `low` to `high` values -->
        SELECT { column_name } FROM { table_name } ORDER BY { column_name } ASC;
        <!--! DESC = From `high` to `low` values (reverse of ASC)-->
        SELECT { column_name } FROM { table_name } ORDER BY { column_name } DESC;
```
- **Example:** 

```postgres
        <!--* ASC:  0->1->2...->10 -->
        SELECT age FROM users ORDER BY age ASC;

        <!--* DESC: 10->9->8->...0 -->
        SELECT age FROM users ORDER BY age DESC;
```


* <span style="color:#fa0f4e"><b>Select With `LIMIT` & `OFFSET`:</b></span>
### <span style="color: #fcd45d"><b>======================|LIMIT|======================</b></span>
- **Rule**:
```postgres
        <!--! get a static number of results-->
        SELECT { column_name } FROM { table_name } LIMIT { limit_number };
```
- **Example**:
```postgres
        <!--! show 5 users only -->
        SELECT name FROM users LIMIT 5;
```

### <span style="color: #fcd45d"><b>======================|LIMIT-OFFSET|======================</b></span>
<span style="color:#555"><b>OFFSET : ازاحة</b></span>

- **Rule**:
```postgres
        <!--! get a static number of results-->
        SELECT { column_name } FROM { table_name } LIMIT { limit_number } OFFSET { offset_number } ;
```
- **Example**:
```postgres
        <!--! show 5 product when move from page-1 to page-2 (execlude page-1 content)-->
        SELECT product FROM product LIMIT 10 OFFSET 5;
```




* <span style="color:#fa0f4e"><b>Addition using `INSERT`: </b></span>
### <span style="color: #fcd45d"><b>======================|INSERT|======================</b></span>
- **Rule**:
```postgres
        <!--* add new values in table  -->
        INSERT INTO { table_name } ( col-1, col-2,...,col-n ) VALUES ( val-1, val-2,...,val-n)
```
- **Example**:
```postgres
        INSERT INTO users( name, age, gender) VALUES ( 'Ahmed', 29, 'M')

        <!--* For Multiple Entries -->
        INSERT INTO users( name, age, gender) VALUES ('Ahmed', 29, 'M') , ('Walter', 8,'M'), ('Sophie', 40, 'F')
```

### <span style="color: #fcd45d"><b>======================|INSERT+RETURNING|======================</b></span>
- **Rule**:
```postgres

        <!--* add new values in table & return entries -->
        INSERT INTO { table_name } ( col-1, col-2,...,col-n ) VALUES ( val-1, val-2,...,val-n) RETURNING col-1, col-2, col-n
```
- **Example**:
```postgres
        INSERT INTO users( name, age, gender) VALUES ('Ahmed', 29, 'M') RETURNING name, age

        <!--* For Multiple Entries -->
        INSERT INTO users( name, age, gender) VALUES ('Ahmed', 29, 'M') , ('Walter', 8,'M'), ('Sophie', 40, 'F') RETURNING name, age
```

* <span style="color:#fa0f4e"><b>Deletion using `DELETE`: </b></span>
### <span style="color: #fcd45d"><b>======================|DELETE|======================</b></span>
- **Rule**:
```postgres

        <!--* delete data from table  -->
        DELETE FROM { table_name } WHERE { condition };

        <!--* delete data from table & return deleted   -->
        DELETE FROM { table_name } WHERE { condition } RETURNING *;
```
- **Example**:
```postgres
        <!--* we need to delete Womans  -->
        DELETE FROM users WHERE gender='F' ;

        <!--* delete & return deleted -->
        DELETE FROM users WHERE gender='F' RETURNING *;
```


* <span style="color:#fa0f4e"><b>Update using `UPDATE`: </b></span>
### <span style="color: #fcd45d"><b>======================|UPDATE|======================</b></span>

- **Rule**:
```postgres
        <!--* update data of item  -->
        UPDATE { table_name } SET col-1 = {new_value} WHERE { condition };

        <!--* Multiple updates -->
        UPDATE { table_name } SET col-1 = {new_value}, col-2 = {new_value} WHERE { condition };

        <!--* return updated item -->
        UPDATE { table_name } SET col-1 = {new_value} WHERE { condition } RETURNING *;
```
- **Example**:
```postgres
        <!--* change user name by passing id  -->
        UPDATE users SET name = 'Ali' WHERE id=203;

        <!--* update & return updated -->
        UPDATE users SET name = 'Ali' WHERE id=203 RETURNING *;

```


* <span style="background: -webkit-linear-gradient(180deg,  #a6fe84, #4efa0f); -webkit-background-clip: text; -webkit-text-fill-color: transparent;"><b>Good Practicies 💫: </b></span>:
    - **<span style="color: #bb0ffa">Write SQL Keywords in Upper-Case</span>**
    - **<span style="color: #bb0ffa">Always Put Strings inside 'single-quote'</span>**