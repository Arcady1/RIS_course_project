UPDATE  detail
SET
    stock_count = "$new_count",
    stock_date_update = "$new_date"
WHERE iddetail = "$detail_id";