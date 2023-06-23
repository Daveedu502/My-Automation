import Library

devices = ["NJ-BIGIP-3","VA-BIGIP-3","NRT-BIGIP-2","LHR-BIGIP-1","FRA-BIGIP-1","HKG-BIGIP-1","SYD-BIGIP-2","NJ-BIGIP-DMZ-2","VA-BIGIP-DMZ-2"]
cert = ["otp.factset.com_2023"]

Library.get_vips_of_ssl_cert(devices,cert)
print("Finished.....!!!")