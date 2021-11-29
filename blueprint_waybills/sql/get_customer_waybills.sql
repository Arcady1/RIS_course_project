SELECT waybill.idwaybill, waybill.waybill_date, waybill.full_price, users.user_name, users.user_group
FROM waybill LEFT JOIN users
ON waybill.user_id = users.idusers
WHERE waybill.customer_id = "$customer_id"