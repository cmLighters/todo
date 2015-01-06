这是我的Todo项目

---
第一版MySQL存todo_entry

---
第二版使用Redis做数据库， entry_id记录当前项， entry:entry_id为hash类型，记录本id的todo_entry


早上11点开始，给todo加delete

下午两点到四点弄好todo界面和在服务器上nginx配置，按blog的配置配好后忘了nginx -s reload然后一只刷新出错！。遇到问题是服务器上mysql配置my.conf没有配置好字符编码为‘utf-8’。重启命令为sudo /etc/init.d/mysql restart. 界面的调整知道了margin、border、padding各自意义。在对不同设备做适配时，往往width使用90%这种而不是800px，然后用max-width: 800px来定义最大宽度防止过宽。因为可以根据不同设备自己去适配宽度的百分之九十。还有就是"<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0">"语句用来添加设备屏幕自适应。
因为后台没有验证空字符串或空格问题，所以需要添加这个功能。在这时可以考虑在前端用javascript实现，也可以后台实现。但是**永远不要相信前端验证**。因为如果只在前端验证的话，只需把脚本屏蔽后就可往后台写入数据，这是不能允许的。前端的验证往往是简单和快速验证，为了安全应该在后端实现验证功能。


---
第三版实现认证登陆功能，本版用todo_user来记录用户名和密码， 为hash类型，确保了用户名的唯一性（重复的用户名提示重设用户名）。

重构了整个数据表。使用"todo_`username`_entries"来记录`username`所包含的todo项，列表类型。
按插入顺序读取和列出，自然有序。无需设置entry_id来记录插入顺序。但是出现的一个问题是redis中并无
直接删除index项的命令，只有lrem来删除count个value值。最终先lset第index项为某一特殊值，再按这个
特殊值lrem删除即可。



