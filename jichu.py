id = 2
while 1:
 id+=1

while not getValue('PRODUCT_EXIT'):
    be = time.time()
    sql = f"select id,aminer_id,zl_path,source_id from {self.table_name}  where id >%s  and is_ava=1 order by id asc limit 10"
    cursor.execute(sql, (ids,))
    # cursor.execute(sql)
    mes_list = list(cursor.fetchall())  # ((id,title,source_id),(id,title,source_id))

    if len(mes_list) > 0:
        ids = mes_list[-1][0]  # ()
        print(mes_list[0])
        print(f"消费者获取成功，目前最大值{ids}")
        # 目前最大值23  #目前最大值87
        for mes in mes_list:
            self.product_queue.put(mes)  # 添加入队列
        break
    else:
        setValue("PRODUCT_EXIT", True)
    self.conn.commit()
    print(time.time() - be)