from web3_util import get_contract,contract_functions,\
            see_contract_fuctions

alpha_address = '0x40C36799490042b31Efc4D3A7F8BDe5D3cB03526'
contract_as = get_contract('contracts/AlphaStrategy.json',alpha_address)
print(see_contract_fuctions(contract_as))
bt = contract_functions(contract_as,'baseThreshold')
lt = contract_functions(contract_as,'limitThreshold')
tick = contract_functions(contract_as,'getTick')
last_tick = contract_functions(contract_as,'lastTick')
twap = contract_functions(contract_as,'getTwap')
twap_duration = contract_functions(contract_as,'twapDuration')
max_twap_deviation = contract_functions(contract_as,'maxTwapDeviation')
deviation = abs(tick - twap)
should_rebalance = abs(tick - last_tick) > lt // 4
print('deviation_gap',deviation,max_twap_deviation,max_twap_deviation-deviation)
print('should_rebalance,last_tick_gap,lt//4', should_rebalance, abs(tick - last_tick), lt // 4)

av_address = '0x55535c4c56f6bf373e06c43e44c0356aafd0d21a'
contract_av = get_contract('contracts/AlphaVault.json',av_address)
print(see_contract_fuctions(contract_av))
TotalAmounts = contract_functions(contract_av,'getTotalAmounts')
print(TotalAmounts)
