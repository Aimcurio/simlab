import check_table_vs_records

table_status = check_table_vs_records.table_status
rc = [pid for pid, st in table_status.items() if st == "REPRODUCTION_CANDIDATE"]
pbu = [pid for pid, st in table_status.items() if st == "PROMISING_BUT_UNVERIFIED"]

print(f"REPRODUCTION_CANDIDATE count: {len(rc)}: {rc}")
print(f"PROMISING_BUT_UNVERIFIED count: {len(pbu)}: {pbu}")
