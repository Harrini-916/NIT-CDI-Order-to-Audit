
# NIT CDI Benchmark Test Data

## 1. Factory Details

Factory State: Tamil Nadu
Currency: INR
GST Rate: 5%

## 2. Opening Raw Material Stock

| Material | Opening Quantity | Unit | Rate |
|---|---:|---|---:|
| Flour | 100 | kg | ₹42 |
| Oil | 30 | L | ₹140 |
| Spice Mix | 5 | kg | ₹200 |
| 200g Pouches | 500 | pieces | ₹2.50 |
| Cartons | 30 | pieces | ₹15 |

## 3. Opening Finished Goods Stock

| Product | Opening Quantity |
|---|---:|
| Murukku 200g | 50 packets |

## 4. BOM – One Production Batch

Expected output: 200 packets

| Material | Planned Quantity |
|---|---:|
| Flour | 40 kg |
| Oil | 10 L |
| Spice Mix | 1.2 kg |
| 200g Pouches | 200 pieces |
| Cartons | 10 pieces |

## 5. Purchase Transaction

| Material | Purchased Quantity | Unit Rate |
|---|---:|---:|
| Flour | 60 kg | ₹45/kg |

## 6. Production Run

| Parameter | Value |
|---|---:|
| Planned output | 200 packets |
| Actual good output | 188 packets |
| Flour consumed | 40 kg |
| Oil consumed | 10.5 L |
| Spice mix consumed | 1.2 kg |
| Damaged pouches | 6 |
| Cartons used | 9 |

## 7. Sales Orders

### Retailer A – Tamil Nadu

- Ordered quantity: 150 packets
- Selling price: ₹50 per packet
- Taxable amount: ₹7,500
- CGST: ₹187.50
- SGST: ₹187.50
- Invoice total: ₹7,875

### Distributor B – Karnataka

- Ordered quantity: 120 packets
- Available finished goods after Retailer A dispatch: 88 packets
- Shortage: 32 packets
- GST: IGST

## 8. Payment

Retailer A payment received: ₹4,000

Outstanding amount: ₹3,875

## 9. Production Expenses

- Labour: ₹1,200
- Gas and power: ₹600
