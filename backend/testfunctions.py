from radar_data_calculator import normalize


print('OFFENSE:')
print(normalize(0.97,0.779,1.118))
print('DEFENSE:')
print(normalize(1/1.008,1/1.057,1/0.853))
print('OVERAll')
print(normalize(0.109,-0.255, 0.232))