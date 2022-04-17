# 基于Python3 版本的简单sqlite3数据库调用

论如何优雅的使用sqlite3数据库

---

## 需要依赖:

    sqlite3(应该是自带库)

## 使用方法:

### 示例:

```python3
import my_sqlite
db = my_sqlite.core("db.sqlite3")
# 数据库操作。。。
db.close()
```

### 主函数:

#### 初始化

```python3
db = my_sqlite.core()
```

参数:

    path(sqlite3的文件路径，参数类型为str)

#### 连接

```python3
db.connect()
```

无参数传递

无返回

**注意在初始化的时候会自动连接!**

##### 高级(给会用sqlite3库的人写的)

```python3
db.conn	= sqlite3.connect(self.path)
db.cur 	= self.conn.cursor()
```

#### 发送带返回值的命令

```python3
db.command()
```

参数:

    sql_command(sql命令，参数类型为str)

    sql_param(用于替换sql_command里面的"?"，可选，参数类型为list)

#### 发送不带返回值的命令

```python3
db.execute()
```

参数:

    sql_command(sql命令，参数类型为str)

    sql_param(用于替换sql_command里面的"?"，可选，参数类型为list)

无返回

#### 提交命令(用于修改过数据库之后的保存)

```python3
db.commit()
```

无参数传递

无返回

#### 关闭数据库连接

```python3
db.close()
```

无参数传递

无返回

### 功能函数

#### 列出所有表

```python3
db.list_table()
```

无参数传递

返回list类型

#### 列出所选表的头部信息

```python3
db.show_table_header()
```

参数:

    table_name(表名称，参数类型为str)

返回dict类型，key为第几列，value为列的详细数据

#### 列出所选表的主体信息

```python3
db.show_table_body()
```

参数:

    table_name(表名称，参数类型为str)

    column(列出哪些列，可选，默认全部列，参数类型为list)

返回list，使用dict类型包含行的信息

#### 创建表

```python3
db.crate_table()
```

参数:

    table_name(表名称，参数类型为str)

    header_list(头部列表，类型为list，使用my_sqlite.sqlite_table_header类型)

无返回

#### 删除表

```python3
db.delete_table()
```

参数:

    table_name(表名称，参数类型为str)

无返回

#### 添加一行数据

db.insert_data()

参数:

    table_name(表名称，参数类型为str)

    args(数据的键对，使用dict类型)

无返回

#### 修改数据

```python3
db.update_data()
```

参数:

    table_name(表名称，参数类型为str)

    update_key(要修改的数据列，参数类型为str)

    update_data(修改之后的数据，参数类型不要太离谱就行，已经完成str和int、float的常用转化，没有加转义检测)

    pk_select(主键的数值，用于检索行)

    pk_name(主键名称，可选，默认为"id")

无参数返回

#### 删除数据

```python3
db.delete_data()
```

参数:

    table_name(表名称，参数类型为str)

    pk_select(主键的数值，用于检索行)

    pk_name(主键名称，可选，默认为"id")

无参数返回
