# Finance Rules

## Budget Categories
- Offering: 10% - Stays in BDO until withdrawn
- Savings: 17% - Goes to GoTyme
- Emergency fund: 7% - Goes to GoTyme (separate from savings)
- Food: 20% - Goes to GCash
- Bills: 9% - Goes to GCash
- Fun money: 12% - Goes to GCash (guilt-free spending)
- Buffer: 25% - Goes to GCash

## Key Rules
- Percentages must total 100%
- Always retain minimum PHP 500 in BDO
- Retained amount is separate from percentage allocations
- Savings and emergency funds are conceptually distinct
- All amounts in PHP (Philippine Peso)

## Calculation Logic
1. Calculate category amounts based on percentages of payout
2. Ensure minimum BDO retention is maintained
3. If retention would be less than minimum, adjust allocations accordingly
4. Use safe rounding to avoid floating point issues

## Account Routing
- BDO: Offering + Retained minimum
- GoTyme: Savings + Emergency (separate buckets)
- GCash: Food + Bills + Fun + Buffer

## Validation
- Payout amount > 0
- Retained BDO amount >= 0
- Percentages sum to 100
- All amounts are positive

## Rounding
- Use decimal arithmetic for precision
- Round to nearest centavo (0.01 PHP)
- Ensure total allocated equals payout amount