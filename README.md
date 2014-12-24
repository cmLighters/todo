这是我的Todo项目

---
第一版MySQL存todo_entry

---
第二版使用Redis做数据库， entry_id记录当前项， entry:entry_id为hash类型，记录本id的todo_entry

---
第三版实现认证登陆功能，本版用todo_user来记录用户名和密码， 为hash类型，确保了用户名的唯一性（重复的用户名提示重设用户名）。

重构了整个数据表。使用"todo_`username`_entries"来记录`username`所包含的todo项，列表类型。
按插入顺序读取和列出，自然有序。无需设置entry_id来记录插入顺序。但是出现的一个问题是redis中并无
直接删除index项的命令，只有lrem来删除count个value值。最终先lset第index项为某一特殊值，再按这个
特殊值lrem删除即可。



