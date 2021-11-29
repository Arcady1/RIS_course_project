SELECT detail.detail_type, detail.detail_material, detail.detail_weight, detail.detail_price, waybill_str.details_count
FROM waybill_str LEFT JOIN detail
ON  waybill_str.detail_id = detail.iddetail
WHERE waybill_str.waybill_id = "$waybill_id";