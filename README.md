# find_MAC_Organization
找出MAC地址所属机构

## 数据说明
* Traffic.csv : 字段Source、字段Destination都为MAC地址，主要用到这两列，其他可以不看。
* mean.csv : 记录着每个MAC地址的归属机构。字段Assignment为机构的前几个MAC地址编码，字段Organization Name为对应机构名称。
* oui.csv ： 同上

## 需求
统计表Traffic.csv中字段Source和字段Destination各自出现的MAC地址所对应的机构占比。

## 操作流程
MAC地址中由于数据格式不一，因此要挑出有价值的字节或统一其数据格式。
表Traffic.csv MAC地址会出现如下几种情况的数据格式：
 - 4b:9a:8a:b4:47:52 ： 完整的MAC地址，只需提取前三个编码的字符，并转换成统一的大写，与机构数据表找匹配即可。
 - Apple_c8:d1:e2 (8c:85:90:c8:d1:e2) (TA) ： 像这类前面带有机构字符，但后面括号中又记录了用户的完整MAC地址，因此只需提取括号里面MAC地址中前三个编码。
 - Apple_88:df:21 ：像这样虽然带有机构前缀的MAC，但'_'后面带但MAC编码对比第二种情况可以知道，只是完整MAC地址的后面三个编码，对查找出机构没有意义。因此只能提取前缀中对机构名字。在机构数据表中匹配。

而表mean.csv中的Assignment列（MAC地址）有7个字符，在匹配的时候只需匹配前六个字符即可。
且表mean.csv和oui.csv都是记录一个类型的数据，只是放在不同的表中，在匹配前可以先对这两表进行合并。



